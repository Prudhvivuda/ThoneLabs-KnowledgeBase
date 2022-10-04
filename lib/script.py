# run this file when new dataset comes to convert the .csv files into required JSONs and Dictionary.

from copy import deepcopy
import csv
import json

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

    

# source = 'D:\data\static_distributions.csv'
# source= 'D:\data\WaistCircumference.csv'
source = '/content/drive/MyDrive/Work/Quisitive/Weight.csv'
# source = '/content/drive/MyDrive/Work/Quisitive/static_distributions.csv'
from collections import OrderedDict
template = OrderedDict()
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
        print(age_table)
        gender_table = sorted(list(set(map(lambda x: tryFloat(x['gender']), var_data))))
        print(gender_table)
        value_table = list(map(lambda x: tryFloat(x['value']), var_data))
        percentile_table = list(map(lambda x: tryFloat(x['percentile']), var_data))
        
    # code for values
    i = 0
    j = 0
  
    while i < len(value_table):
        for key in template:
            template[key].append(value_table[i])
            i += 1
    result = json.dumps(template)
    

    # code for percdntiles dictionary
    i = 0
    p = {}
    while i < len(percentile_table):
        p[i] = percentile_table[i]
        i += 1
    result = json.dumps(p)
    print(len(p))
    
    with open("demo.json", "w") as outfile:
        outfile.write(result)
