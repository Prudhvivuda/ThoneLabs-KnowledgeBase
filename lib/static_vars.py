import os
from lib.file import read_JSON, read_csv_universal_newline
from lib.NHANES_nutrition import dsq_vars_list
from lib.PHQ9 import phq9_vars_list
from lib.anthropometrics import absi_vars_list
from lib.vitals import chol_hdl_vars_list
from lib.helper import takeClosest
from copy import deepcopy

vars_list = {'dsq':dsq_vars_list,
             'phq9':phq9_vars_list,
             'absi':absi_vars_list,
             'cholesterol_hdl':chol_hdl_vars_list
             }

#looads data in variable_reference.csv to get all variables used in lab100 (including some that are no longer used)
def get_all_variables(var_filepath = 'data/variable_reference.csv'):
    variable_reference_data = read_csv_universal_newline(var_filepath)
    variables = {}
    for row in variable_reference_data[1:]:
        variables[row[0]] = {'dbid':[],
                             'data_type':row[5],
                             'units':row[4],
                             'display_name':row[1]}
        if len(row[3]) > 0:
            variables[row[0]]['dbid'] = row[3].split(';')


    return variables

#loads cutpoints.csv file. Creates functions for each cutpoint that will evaluate whether the cutpoint applies to a patient
def get_cutoffs(cutoffs_filepath = 'data/cutpoints.csv'):
    cutoffs = read_csv_universal_newline(cutoffs_filepath)
    cutoff_keys = cutoffs[0]
    cutoff_dict = {}
    for row in cutoffs:
        try:
            r = dict(filter(lambda x: not x[0] == '', map(lambda x: (cutoff_keys[x], row[x] ), range(len(cutoff_keys)))))
        except Exception as e:
            for col in row:
                try:
                    col.decode('utf-8')
                except:
                    pass
        if not r['Variable'] in cutoff_dict:
            cutoff_dict[r['Variable']] = [r]
        else:
            cutoff_dict[r['Variable']].append(r)
        for key in ['Age_sign1', 'Age_sign2', 'Sign_1', 'Sign_2']:
            if r[key] == '=':
                r[key] = '=='
        r.update({'Age_Function': lambda x, r: r['Age_value1'] == 'NA' or r['Age_sign1'] == 'NA'
                                               or (eval(str(x)+r['Age_sign1']+r['Age_value1'])
                                                   and (r['Age_sign2'] == 'NA'
                                                        or eval(str(x)+r['Age_sign2']+r['Age_value2'])
                                                        )
                                                   ),
                  'Cutoff_Function': lambda x, r: r['Sign_1'] == 'NA' or
                                                  (eval(str(x)+r['Sign_1']+r['Cut_off_value_1'])
                                                   and (r['Sign_2'] == 'NA'
                                                        or eval(str(x)+r['Sign_2']+r['Cut_off_value_2'])
                                                        )
                                                   )})
    return cutoff_dict

#load list of all NHANES variables
def get_all_normalization_variables(filepath = 'NHANES_Downloader/data/'):
    csv_path = filepath + 'csv_data'
    raw_path = filepath + 'raw_data'
    years = [x for x in os.listdir(csv_path) if os.path.isdir(csv_path+'/'+x)]
    data = {}
    for year in years:
        categories = [x for x in os.listdir(csv_path+'/'+year) if os.path.isdir(csv_path+'/'+year+'/'+x)]
        for category in categories:
            json_files = [x for x in os.listdir(raw_path+'/'+year+'/'+category) if '.JSON' in x]
            for json_file in json_files:
                #print(year, category, json_file)
                labels = read_JSON(raw_path+'/'+year+'/'+category+'/'+json_file)
                data.update(labels)
    return data

#loads a list of the possible calculated variables
def calculated_variable_list():
    calculated_vars = dict(filter(lambda x: 'outputs' in x[1], vars_list.items()))
    calculated_vars_keys = list(calculated_vars.keys())
    for key1 in calculated_vars_keys:
        for key2 in calculated_vars[key1]['outputs']:
            calculated_vars[key2] = key1
    #return calculated_vars
    return {}

#list of population distributions based off of pop stats (ie mean, sd) rather than pop data. Also generates a function that will determine whether a distribution matches a patients demographics
def static_distribution_list(source = 'data/static_distributions.csv'):
    raw_data = read_csv_universal_newline(source)
    keys = raw_data[0]
    keys = dict(map(lambda x: (keys[x], x), range(len(keys))))
    proc_data = {}
    for row in raw_data[1:]:
        var_name = row[keys['variable']]
        if not var_name in proc_data:
            proc_data[var_name] = []
        proc_data[var_name].append({})
        for key, index in keys.items():
            proc_data[var_name][-1][key] = row[index]

    results = {}
    for key in proc_data.keys():
        var_data = deepcopy(proc_data[key])
        age_table = sorted(list(set(map(lambda x: tryFloat(x['age_min']), var_data))))
        gender_table = sorted(list(set(map(lambda x: tryFloat(x['gender']), var_data))))
        results[key] = static_distribution_func(age_table, gender_table, var_data).result_func
    return results

class static_distribution_func():
    def __init__(self, age_table, gender_table, var_data):
        self.lookup = {'keygen':lambda gender, age: ('gender_' + str(gender) + '_' if gender is not None \
                                                            and tryFloat(gender) in gender_table else 'gender_NA_')\
                                                    + ('age_' + str(takeClosest(age_table, tryFloat(age), round = 'down')) + '_' \
                                                            if len(age_table) > 1 and age is not None and tryFloatBool(age) and \
                                                            float(age) < 200 and float(age) > 0 else 'age_NA_')\
                                                    + 'key',
                       }
        lookup_values = list(map(lambda x: (self.lookup['keygen'](var_data[x]['gender'], var_data[x]['age_min']),
                                       var_data[x]),
                            range(len(var_data))))
        if len(set(map(lambda x: x[0], lookup_values))) < len(list(lookup_values)):
            print('Error in static distribution keys:', sorted(map(lambda x: x[0], lookup_values)), \
                'vs', sorted(list(set(map(lambda x: x[0], lookup_values)))))
            print(lookup_values)
        self.lookup['values'] = dict(lookup_values)

    def result_func(self, gender, age):
        key = self.lookup['keygen'](gender, age)
        print(key, gender, age, self.lookup)
        return self.lookup['values'][key]

def tryFloatBool(var):
    try:
        float(var)
        return True
    except:
        return False

def tryFloat(var):
    try:
        return float(var)
    except:
        return var

static_distribution_vars = static_distribution_list()
# normalization_variables_all = get_all_normalization_variables()
