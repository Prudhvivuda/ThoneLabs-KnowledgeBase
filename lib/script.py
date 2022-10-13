# run this file when new dataset comes to convert the .csv files into required JSONs and Dictionary.
# this script works assuming the given dataset is in sorted order and need to be run only once.

from copy import deepcopy
import csv, json
from collections import OrderedDict

def read_csv_universal_newline (filename, delimiter = ","):
    try:
        csvreader = csv.reader(open(filename, 'r'))
        data = []
        for row in csvreader:
            data.append(row)
        return data
    except Exception as e:
        log.error(e)
        return False
    
def tryFloat(var):
    try:
        return float(var)
    except:
        return var

def tryFloatBool(var):
    try:
        float(var)
        return True
    except:
        return False

def ordertest(A):
    for i in range(len(A) - 1):
        if isinstance(A[i], float) and isinstance(A[i+1], float) and A[i]<A[i+1]:
            return False
    return True

# give the path of the new dataset for which we need to configure or convert the data into existing file formats
source = '/Work/Quisitive/Weight.csv'

template = OrderedDict()
'''
    template can be created based on the number of age groups and the gender.
    here, there are 8 age groups in each gender, so there would be 16 keys and 
    values depends on the data for each age group.
'''
template["gender_2_age_0"] = []
template["gender_2_age_1"] = []
template["gender_2_age_2"] = []
template["gender_2_age_3"] = []
template["gender_2_age_4"] = []
template["gender_2_age_5"] = []
template["gender_2_age_6"] = []
template["gender_2_age_7"] = []
template["gender_1_age_0"] = []
template["gender_1_age_1"] = []
template["gender_1_age_2"] = []
template["gender_1_age_3"] = []
template["gender_1_age_4"] = []
template["gender_1_age_5"] = []
template["gender_1_age_6"] = []
template["gender_1_age_7"] = []

def static_distribution_list():
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
        value_table = list(map(lambda x: tryFloat(x['value']), var_data))
        percentile_table = list(map(lambda x: tryFloat(x['percentile']), var_data))
        
    '''
        code to get the variable(weight/height/waistcircumferece) values 
        for the keys in the above defined template in the form of a dictionary
    '''
    i = 0
    while i < len(value_table):
        for key in template:
            template[key].append(value_table[i])
            i += 1
    result = json.dumps(template)
    

    # code to get the percentiles for a variable in the form of a dictionary
    i = 0
    p = {}
    while i < len(percentile_table):
        p[i] = percentile_table[i]
        i += 1
    result = json.dumps(p)
    print(len(p))
    
    with open("demo.json", "w") as outfile:
        outfile.write(result)
