import numpy as np
from lib.helper import takeClosest
from lib.file import read_csv_universal_newline
from collections import defaultdict
from scipy.stats import norm

#loads tables used to look up scaled scores by demographic
def load_lookup_table(filepath):
    table = read_csv_universal_newline(filepath)
    header = map(lambda x: table[1][x].strip().replace(' ','_').replace('-','_').lower() + ('_' if len(table[2][x]) > 0 else '') \
                 + table[2][x].strip().replace(' ','_').replace('-','_').lower(), range(len(table[1])-1))
    header[0] = 'scaled_score'
    header = filter(lambda x: len(x) > 0, header)
    results = {}
    for key in header:
        results[key] = []
    for row in table[3:]:
        for index, col in enumerate(row[0:len(header)]):
            val = col.split('-')[-1]
            try:
                val = float(val)
                results[header[index]].append(val)
            except:
                results[header[index]].append('NA')
    return lambda category, value: results['scaled_score'][takeClosest(results[category], value, round = 'up')]

#loads formulas used to generate normalized scores from scaled scores by demographic
def load_scoring_formulas(ethnicity, age_category, filepath = 'data/NIH/NIH_Formulas.csv'):
    formulas = read_csv_universal_newline(filepath)
    type = ('A' if ethnicity == 'African' else 'H' if ethnicity == 'Hispanic' else 'W') + \
            ('A' if age_category == 'Adult' else 'C')
    results = {}
    print(type)
    for row in formulas:
        if len(row) > 0 and row[0] == type:
            results[row[1].lower()] = row[2].lower()
    return results

#filenames of lookup tables
source_lookup = {'Adult':defaultdict(lambda: 'AC_Adults.csv',
                                   {'African':'FC_African_Adults.csv',
                                    'White':'FC_White_Adults.csv',
                                    'Hispanic':'FC_Hispanic_Adults.csv'}),
                 'Child':defaultdict(lambda: 'AC_Children.csv',
                                   {'African':'FC_African_Children.csv',
                                    'White':'FC_White_Children.csv',
                                    'Hispanic':'FC_Hispanic_Children.csv',
                                    'Multi':'FC_Multi_Children.csv'})
                }
#translate ethnicity numbers to demographics used by NIH
ethnicity_translator ={1:'Hispanic',
                       2:'Hispanic',
                       3:'White',
                       4:"African",
                       5:'Multi',
                       6:'None',
                       7:'None'}

#convers NHANES data to format used by program
def convert_data(patient_data):
    out_data = \
            {'ethnicity':ethnicity_translator[patient_data['ethnicity']], #None, African, White, Hispanic, or Multi (if child)
            'age': int(patient_data['age']),
            'male': int(patient_data['gender']),
            'education':int(education_converter[int(patient_data['education'])]) if 'education' in patient_data and tryfloat(patient_data['education']) else 'NA',
            'endurance':float(patient_data['endurance']) if 'endurance' in patient_data else 'NA',
            'lo4mt_usual_pace': float(patient_data['lo4mt_usual_pace']) if 'lo4mt_usual_pace' in patient_data else 'NA',
            'lo4mt_fast_pace':float(patient_data['lo4mt_fast_pace']) if 'lo4mt_fast_pace' in patient_data else 'NA',
            'bam_theta': float(patient_data['bam_theta']) if 'bam_theta' in patient_data else 'NA'
            }
    if out_data['male'] > 1:
        out_data['male'] = 0
    if 'handedness' in patient_data:
        if 'dexterity_right' in patient_data and 'dexterity_left' in patient_data:
            if patient_data['handedness'] == 'right':
                out_data['dx9h_dominant'] = float(patient_data['dexterity_right'])
                out_data['dx9h_non_dominant'] = float(patient_data['dexterity_left'])
            else:
                out_data['dx9h_dominant'] = float(patient_data['dexterity_left'])
                out_data['dx9h_non_dominant'] = float(patient_data['dexterity_right'])
        if 'grip_strength_right' in patient_data and 'grip_strength_left' in patient_data:
            if patient_data['handedness'] == 'right':
                out_data['msgs_dominant'] = float(patient_data['grip_strength_right'])
                out_data['msgs_non_dominant'] = float(patient_data['grip_strength_left'])
            else:
                out_data['msgs_dominant'] = float(patient_data['grip_strength_left'])
                out_data['msgs_non_dominant'] = float(patient_data['grip_strength_right'])
    return out_data

#takes in data and returns score.
def NIH_motor(nih_data):
    patient_data = convert_data(nih_data)
    age_category = 'Adult' if float(patient_data['age']) > 17 else "Child"
    source = 'data/NIH/LookupTables/'+source_lookup[age_category][patient_data['ethnicity']]
    lookup_table = load_lookup_table(source)
    scoring_formulas = load_scoring_formulas(patient_data['ethnicity'], age_category)
    age = float(patient_data['age'])
    edu = float(patient_data['education'])
    male = float(patient_data['male'])
    # male = abs(float(patient_data['male'])-2)
    if (male > 1):
        male = 0.0
    for key, value in scoring_formulas.items():
        if key in patient_data and not patient_data[key] == 'NA':
            try:
                scaled_score = lookup_table(key.lower(), patient_data[key.lower()])
                #sets scaled_score variable to be used in eval function in next for loops
                exec(key.lower() +'_scaled_score = '+ str(scaled_score))
            except KeyError as e:
                print(e)
    results = {}
    for key, value in scoring_formulas.items():
        if key in patient_data and not patient_data[key] == 'NA':
            try:
                #evaluates formula from scoring formulas using variables initialized earlier
                formula_result = eval(value.lower())
                if key in name_converter:
                    key = name_converter[key]
                results[key] = {}
                results[key]['percentile'] = norm.cdf(formula_result, loc = 50.0, scale = 10.0)
                results[key]['value'] = formula_result
            except NameError as e:
                print(e)
    return results

#balance calc
def balance(nih_data):
    percentile = norm.cdf(nih_data['balance_score'], loc = 50.0, scale = 10.0)*100
    return {
        'percentile': percentile,
        'balance_score': nih_data['balance_score']
    }

def tryfloat(input):
    try:
        float(input)
        return True
    except:
        return False

#Lab100 education vals are a different scale than NIH motor
education_converter = {
    999: 12,
    1:0,
    2:0,
    3:0,
    4:1,
    5:2,
    6:3,
    7:4,
    8:5,
    9:6,
    10:7,
    11:8,
    12:9,
    13:10,
    14:11,
    15:12,
    16:12,
    17:12,
    18:13,
    19:13,
    20:14,
    21:15,
    22:14,
    23:16,
    24:18,
    25:20,
    26:20}

#converts var names to more human readable format
name_converter = {"dx9h_dominant": "dominant_hand_dexterity",
                  "dx9h_non_dominant": "non_dominant_hand_dexterity",
                  "msgs_dominant": "dominant_hand_grip_strength",
                  "msgs_non_dominant": "non_dominant_hand_grip_strength" }

if __name__ == '__main__':
    lookup_table = load_lookup_table('data/NIH/LookupTables/FC_Hispanic_Children.csv')
    print(lookup_table('msgs_dominant', 10.0))
    print(lookup_table('dx9h_dominant', 15.0))

