from flask import Flask
# from . import flask_index

app = Flask(__name__)

# from app import app
from flask import jsonify, render_template, url_for, request, abort
from flask.json import dumps as flaskDumps
from lib.normalizer import Normalizer, UnsupportedTargetException
from lib.static_vars import get_all_variables, get_cutoffs
# from lib.static_vars import normalization_variables_all
from lib.NHANES_nutrition import dsq_survey_processor, dsq_scorer
import itertools, tempfile, os, time
import numpy as np
import traceback, json
from lib.file import read_csv
from lib.sample_post import sample_post
from lib.ASCVD import ASCVD
from lib.NIH_motor import NIH_motor, balance
from lib.IPAQ import IPAQ
from lib.PSQI import PSQI
from lib.PHQ9 import PHQ9
from lib.blood_draw import blood_draw
from lib.cognition import cognition
from lib.body_composition import body_composition
from lib.anthropometrics import absi, sbsi, waist_to_hip_ratio, trunk_to_leg_ratio, symmetry
from functools import wraps
from flask import request, Response
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory

try:
    import seaborn as sns
except (RuntimeError, ImportError) as e:
    matplotlibImported = False
    #print e
    print('Try using "frameworkpython yourProgram.py" instead - this is only necessary if you want to generate graphs')


#Authentication stuff
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'INGH' and password == 'isgreat'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#list of all variables
variable_reference = get_all_variables()
#cutoffs from cutpoints.csv
cutoffs = get_cutoffs()
#for returning a prettier json version of above two files
printable_variable_reference = dict(map(lambda x: (x[0], x[1]), variable_reference.items()))
printable_cutoffs = dict(map(lambda x: (x[0],
                                        map(lambda y: dict(filter(lambda z: not 'Function' in z[0],
                                                                  y.items())),
                                            x[1])),
                             cutoffs.items()))

#takes the query and sends it to get_json to process request, then returns the json
@app.route('/normative_data/<query>')
@requires_auth
def return_target_json(query = None):
    data = get_json(query = query)
    for query in data:
        if 'error' in query:
            return jsonify(data), 404
    return data

#graphs the normative data, requires seaborn to be loaded
@app.route('/graph/<query>')
@requires_auth
def return_graph(query = None):
    data = get_json(query = query)
    if len(data) == 1:
        filepath = get_graph(data[0])
        return render_template('simple_graph.html', filepath = url_for('static', filename = filepath))
    else:
        pass #package graphs

#NHANES DSQ
def dsq(dsq_data):
    dsq_data = dsq_survey_processor(dsq_data)
    return dsq_scorer(survey_results = dsq_data)

#ACVSD
def acvsd_calc(acvsd_data):
    risk, comments = ASCVD(**acvsd_data)
    results = {'10-Year ASCVD Risk':risk}
    if len(comments) > 0:
        results['comments'] = comments
    return results

#list of all the functions that calculate variables. most of these are imported
#UPDATE THIS WHEN ADDING NEW DERIVED STATISTICS
possible_stats = {
        'dsq':dsq,
        'acvsd':acvsd_calc,
        'nih_motor':NIH_motor,
        'ipaq':IPAQ,
        'psqi':PSQI,
        'phq9':PHQ9,
        'cognition':cognition,
        'absi':absi,
        'sbsi':sbsi,
        'waist_to_hip_ratio':waist_to_hip_ratio,
        'trunk_to_leg_ratio':trunk_to_leg_ratio,
        'balance':balance,
        'symmetry':symmetry,
        "body_composition": body_composition, 
        "blood_draw": blood_draw               
    }

#for generating calculated variables
@app.route('/derived_stats', methods = {'POST'})
@requires_auth
def generated_statistics():
    data = request.get_json()
    print(data)
    results = {}
    for key in data.keys():
        if key in possible_stats:
            try:
                results[key] = possible_stats[key](data[key])
            except Exception as e:
                results[key] = {'error':e.message}
                print(traceback.print_exc())
    return jsonify(results)

#sample stats - lets you look at the results of a sample json
@app.route('/sample_derived_stats.html')
@requires_auth
def sample_derived_stats():
    return render_template('sample_derived_stats.html', sample_post = sample_post)

#sample json for above
@app.route('/sample_stats_for_derived')
@requires_auth
def sample_stats_for_derived():
    return jsonify(sample_post)

#list of all NHANES variables
# @app.route('/NHANES_vars')
# @requires_auth
# def list_NHANES_vars():
#     return jsonify(normalization_variables_all)

#kill the 404 errors
@app.route('/favicon.ico')
def favicon():
    return 'dummy', 200

#list of all cutpoints in the cutpoints file
@app.route('/cutoffs')
@app.route('/cutoffs/<variable>')
@requires_auth
def list_cutoffs(variable = None):
    if variable:
        return jsonify(dict(filter(lambda x: x[0] == variable, printable_cutoffs.items())))
    else:
        return jsonify(printable_cutoffs)

#cutpoints as a table instead of a json
formatted_cutpoints = []
cutpoint_header = ['Variable','Task','Ethnicity','Age_sign1','Age_value1','Age_sign2','Age_value2','Unit','Sex','Sign_1','Cut_off_value_1','Sign_2','Cut_off_value_2','Unit','Interpretation 1']
cutpoints_sets = []
@app.route('/cutpoints')
def cutpoints_table():
    global formatted_cutpoints
    global cutpoint_sets
    if len(formatted_cutpoints) == 0:
        formatted_cutpoints = sorted(list(itertools.chain.from_iterable(printable_cutoffs.values())), key = lambda x: (x["Task"], x["Variable"], x["Ethnicity"], x["Sex"], x["Age_value1"], x["Cut_off_value_1"]))
        formatted_cutpoints = [x for x in formatted_cutpoints if not x['Variable'] == 'Variable']
        cutpoint_dict = dict(map(lambda col_name: (col_name, dict(map(lambda y: (y[1],y[0]), enumerate(sorted(set(map(lambda row: row[col_name], formatted_cutpoints))))))), cutpoint_header))
        cutpoint_sets = map(lambda col_name: [col_name.replace(' ','_'),
                            map(lambda y: dict([('id',y[0]),('name',y[1])]),
                                enumerate(sorted(set(map(lambda row: row[col_name],
                                                       formatted_cutpoints)))))],
                            cutpoint_header)
        cutpoint_sets = sorted(cutpoint_sets, key = lambda x: x[0])
        for row in formatted_cutpoints:
            for col in cutpoint_header[0:1]:
                row[col] = cutpoint_dict[col][row[col]]
    return render_template('data_table.html', header = cutpoint_header, data = formatted_cutpoints, data_sets = cutpoint_sets)

#validation results, querying validation.csv
validation_header = ['Variable', 'Ethnicity', 'Gender', 'Age', 'Target_Value', 'Interpretation', 'Percentile', 'Distribution_Size']
@app.route('/validation')
def validation_table():
    filepath = os.getcwd()+'/data/validation.csv'
    if os.path.isfile(filepath):
        data = read_csv(filepath)
        validation_data = map(lambda row: dict(map(lambda col: (col[1].replace(' ','_'),row[col[0]]), enumerate(validation_header))), filter(lambda x: len(x) > 0, data[1:]))
        validation_sets = sorted(map(lambda col: (col.replace(' ','_'), map(lambda y: dict([('id',y[0]),('name',y[1])]),
                                                    enumerate(sorted(set(map(lambda row: row[col],
                                                       validation_data)))))),
            validation_header), key = lambda x: x[0])
        validation_dict = dict(map(lambda col_name: (col_name, dict(map(lambda y: (y[1],y[0]), enumerate(sorted(set(map(lambda row: row[col_name], validation_data))))))), validation_header))
        for row in validation_data:
            for col in validation_header[0:1]:
                row[col] = validation_dict[col][row[col]]
        return render_template('data_table.html', header = validation_header, data = validation_data, data_sets = validation_sets)

#list of all variables
@app.route('/vars')
@requires_auth
def list_all_vars():
    return jsonify(printable_variable_reference)

#list of cutoffs (names only)
@app.route('/cutoffs_names')
@requires_auth
def list_cutoffs_names(variable = None):
    return jsonify(map(lambda x: x[0], printable_cutoffs.items()))

#list of variables not in the cutoffs file
@app.route('/vars_without_cutoffs')
@requires_auth
def list_vars_without_cutoffs():
    return jsonify(map(lambda x: x[0], filter(lambda x: not x[0] in printable_cutoffs, printable_variable_reference.items())))

#list of variables without sample population data
@app.route('/vars_without_normative_data')
@requires_auth
def list_vars_without_normative_data():
    return jsonify(map(lambda x: x[0], filter(lambda x: len(x[1]['dbid']) == 0, printable_variable_reference.items())))

#list of variables *with* sample population data
@app.route('/vars_with_normative_data')
@requires_auth
def list_vars_with_normative_data():
    return jsonify(map(lambda x: x[0], filter(lambda x: len(x[1]['dbid']) > 0 and x[1]['data_type'] == 'Q', printable_variable_reference.items())))

#processes query using "process_query_string", then returns distribution + stats using "Normalizer"
def get_json(query = None):
    warnings = []
    query = process_query_string(query)
    if query == None:
        return {'error':'Malformed Query - please check your syntax'}
    if not 'targets' in query or len(query['targets']) == 0:
        return {'error':'unsupported target value'}
    if not 'variables' in query:
        query['variables'] = {}
    if not 'params' in query:
        query['params'] = {}
    try:
        normer = Normalizer('NHANES_Downloader/data/',
                             cache_dir = 'data/cached_jsons/',
                             target_variables = query['targets'],
                             normalization_variables = query['variables'],
                             **query['params']
                            )
    except UnsupportedTargetException:
        return {'error':'unsupported target value'}
    start_time = time.time()
    output = normer.get_target_distributions()
    print("Took " + str(time.time()-start_time) + " seconds to get target distributions.")
    
    return output

#generates a visual graph. Requires seaborn to be working
def get_graph(data):
    filepath = tempfile.NamedTemporaryFile(prefix = os.getcwd()+'/app/static/', suffix = '.png').name
    sns.set_style('whitegrid')
    sns_plot = sns.kdeplot(np.array(data['distribution']), cut = 1, )
    sns_plot.get_figure().savefig(filepath)
    sns_plot.get_figure().clf()
    return filepath.replace(os.getcwd()+'/app/static/', '')

#parses the normalization API query
def process_query_string(query):
    try:
        print([query])
        query_stages = [query]
        query_stages.append(query.split('&'))
        ls = []
        for query in query_stages[1]:
            ls.append(query.split('='))
        output = dict()
        for i in ls:
            temp = dict()
            for j in i[1].split(','):
                variable, value = j.split('+')
                temp[variable]= value
            output[i[0]] = temp
    except Exception as e:
        output = None
        traceback.print_exc()
    print(output)
    return output

def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'data': message
    })
    response.status_code = status_code
    return response


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "LAB KB 100 - API Documentation"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
@app.route("/static/swagger.json")
def send_static():
    return send_from_directory(os.getcwd(), "static/swagger.json")

### end swagger specific ###

@app.route('/')
@requires_auth
def default():
    return jsonify({'message' : 'KB server is up and running !'})