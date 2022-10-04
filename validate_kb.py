import requests, json, time
from requests.auth import HTTPBasicAuth
from lib.static_vars import get_all_variables
from lib.file import write_csv
import numpy as np
import traceback

#6 and 7 have very low counts. 5 is generally people from the middle east. Only 1-4 are particularly reliable, with decent count sizes
ethnicities = [1,2,3,4,5,6,7,8]
ethnicity_converter = {1: 'Mexican American',
                       2: 'Hispanic',
                       3: 'Non-Hispanic White',
                       4: 'Non-Hispanic Black',
                       5: "Non-Hispanic",
                       6: "Non-Hispanic Asian",
                       7: "Non-Hispanic Multiracial",
                       8: "NA"}
#all possible valid age ranges
ages = range(18,66,1)

genders = [1,2]
gender_converter = {1:"Male",
                    2:"Female"}

all_variables = get_all_variables()
del all_variables['ethnicity']
base_url = 'http://127.0.0.1:8085/normative_data/'

def validate_kb(variables = [], override_cache = 1, filepath = 'data/kb_validation.csv', filepath_times = 'data/kb_validation_response_times.json'):
    if len(variables) == 0:
        variables = all_variables.keys()
    #response = requests.get("http://api.open-notify.org/iss-now.json")
    auth = HTTPBasicAuth('INGH', 'isgreat')

    header = ['Variable', 'Ethnicity', 'Gender', 'Age', 'Target_Value', 'Interpretation', 'Percentile', 'Distribution_Size']
    write_csv(filepath, [header], append = False)
    response_times = {}
    response_time_first = {}
    response_time_after = {}
    for variable in variables:
        output = []
        response_time_first[variable] = []
        response_time_after[variable] = []
        for ethnicity in ethnicities:
            print('Testing ' + variable + ' for ethnicity ' + ethnicity_converter[ethnicity])
            for gender in genders:
                for age in ages:
                    try:
                        start_time = time.time()
                        if ethnicity < 8:
                            url = base_url+"targets={0}+0&variables=ethnicity+{1},age+{3},gender+{2}&params=override_cache+{4}".format(variable, ethnicity, gender, age, 1 if override_cache else 0)
                        else:
                            url = base_url+"targets={0}+0&variables=age+{2},gender+{1}&params=override_cache+{3}".format(variable, gender, age, 1 if override_cache else 0)
                        response = requests.get(url, auth = auth)
                        data = json.loads(response.content)
                        if len(data) > 0 and type(data) == type(list()):
                            data = data[0]

                        if 'distribution_stats' in data:
                            response_time_first[variable].append(time.time()-start_time)
                            mean = data['distribution_stats']['mean']
                            sd = data['distribution_stats']['standard deviation']

                            for target_value in [mean-2*sd, mean - sd, mean, mean + sd, mean + 2 * sd]:
                                start_time = time.time()
                                target_value = max([target_value, 0])
                                if ethnicity < 8:
                                  url = base_url+"targets={0}+{4}&variables=ethnicity+{1},age+{3},gender+{2}"
                                  response = requests.get(url.format(variable, ethnicity, gender, age, target_value), auth = auth)
                                else:
                                  url = base_url+"targets={0}+{3}&variables=age+{2},gender+{1}"
                                  response = requests.get(url.format(variable, gender, age, target_value), auth = auth)
                                data = json.loads(response.content)[0]
                                response_time_after[variable].append(time.time()-start_time)
                                output = [all_variables[variable]['display_name'],
                                               ethnicity_converter[ethnicity],
                                               gender_converter[gender],
                                               age,
                                               target_value,
                                               data['interpretation'],
                                               data['percentile'],
                                               len(data['distribution']) if 'distribution' in data else 'NA']
                                write_csv(filepath, [output], append = True)
                        elif 'cutpoints' in data:
                            target_values = set(map(lambda x: x['value_1'], data['cutpoints'])+map(lambda x: x['value_2'], data['cutpoints']))
                            if 'NA' in target_values:
                                target_values.remove('NA')
                            if len(target_values) > 0:
                                target_values = set(map(lambda x: float(x), target_values))
                                target_values.add(min(target_values)-.001)
                                target_values.add(max(target_values)+.001)
                                target_values = sorted(target_values)
                                for target_value in target_values:
                                    url = base_url + "targets={0}+{4}&variables=ethnicity+{1},age+{3},gender+{2}"
                                    response = requests.get(url.format(variable, ethnicity, gender, age, target_value), auth = auth)
                                    data = json.loads(response.content)[0]
                                    output = [all_variables[variable]['display_name'],
                                                   ethnicity_converter[ethnicity],
                                                   gender_converter[gender],
                                                   age,
                                                   target_value,
                                                   data['interpretation'] if 'interpretation' in data else 'Unknown',
                                                   data['percentile'] if 'percentile' in data else 'Unknown',
                                                   'NA']
                                    write_csv(filepath, [output], append = True)
                            else:
                                output = [all_variables[variable]['display_name'],
                                               ethnicity_converter[ethnicity],
                                               gender_converter[gender],
                                               age,
                                               'NA',
                                               'Unknown',
                                               'Unknown',
                                               'NA']
                                write_csv(filepath, [output], append = True)
                        else:
                            output = [all_variables[variable]['display_name'],
                                           ethnicity_converter[ethnicity],
                                           gender_converter[gender],
                                           age,
                                           'NA',
                                           'Unknown',
                                           'Unknown',
                                           'NA']
                            write_csv(filepath, [output], append = True)
                    except Exception as e:
                        traceback.print_exc()
                        print('{0} for ethnicity {1}, gender {2}, and age {3} did not work!'.format(variable, ethnicity, gender, age))
                        print('url was ' + url)
        #{'mean':np.mean(response_time_first[variable]), 'sd':np.std()}


        if len(response_time_first[variable]) > 0 and response_time_after[variable] > 0:
            response_times[variable] = {'first': {'mean':np.mean(response_time_first[variable]), 'sd':np.std(response_time_first[variable])},
                                        'second': {'mean':np.mean(response_time_after[variable]), 'sd':np.std(response_time_after[variable])}}


    json.dump(response_times, open(filepath_times, 'w'))

if __name__ == '__main__':
    validate_kb(variables = [], override_cache = 0, filepath = 'data/validation.csv', filepath_times = 'data/kb_validation_response_times.json')
