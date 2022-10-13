from lib.sample_post import sample_post
from copy import deepcopy
from lib.file import read_csv_universal_newline
import json, math
age_ranges = [None]

#lookup dict for various cereals and what sort of nutrition they provide
def get_cereal_dict(cereal_filepath = 'data/calib_DSQ_cereal_ntile.csv'):
    cereal_dict = {}
    cereal_data = read_csv_universal_newline(cereal_filepath)
    cereals_header = cereal_data[0]
    for row in cereal_data[1:]:
        cereal_dict[row[0].lower()] = {}
        cereal_dict[row[6].lower()] = {}
        for index, col in enumerate(cereals_header):
            cereal_dict[row[0].lower()][cereals_header[index]] = row[index]
            cereal_dict[row[6].lower()][cereals_header[index]] = row[index]
    return cereal_dict

#adjust portion size by age and gender - 20 year old male eats more than 60 year old woman or 12 year old child
def get_portions(age_group, sex, psize_filepath = 'data/calib_portion_size.csv'):
    psize_file = read_csv_universal_newline(psize_filepath)
    psize_dict = {}
    psize_keys = psize_file[0]
    for row in psize_file[1:]:
        if int(row[1]) == int(age_group) and int(row[0]) == int(sex):
            for index, col in enumerate(row[2:]):
                psize_dict[psize_keys[index+2]] = float(col)
            break
    return psize_dict

#get a bunch of multipliers for various variables
def get_coeff(gender, coeff_filepath = 'data/calib_equation_coeff.csv'):
    coeff_file = read_csv_universal_newline(coeff_filepath)
    coeff_keys = coeff_file[0]
    coeff_dict = {}
    for row in coeff_file[1:]:
        if int(gender) == int(row[0]):
            for index, col in enumerate(row[1:]):
                coeff_dict[coeff_keys[index+1]] = float(col)
            break
    return coeff_dict

#input survey results here
def dsq_survey_processor(input, #input is survey results - see dsq portion of sample_post
                         max_values = "data/max_values_DSQ.csv"):

    max_freq = {}
    for row in open(max_values, 'rU'):
        key, value = row.strip().split(',')
        max_freq[key] = float(value)
    for key, data in input.items():
        #get name, translate name
        #get freq in times per day

        #cap values according to data
        if key in max_freq:
            if 'freq' in data:
                data['freq'] = float(data['freq'])
                if data['freq'] > max_freq[key]:
                    input[key]['freq'] = max_freq[key]
                else:
                    input[key]['freq'] = float(data['freq'])
            elif 'cereals' in data:
                for cereal in input[key]['cereals']:
                    cereal['freq'] = float(cereal['freq'])
                    if cereal['freq'] > max_freq[key]:
                        cereal['freq'] = max_freq[key]

    return input

#generates scores from input
def dsq_scorer(cereal_filepath = 'data/calib_DSQ_cereal_ntile.csv',
        psize_filepath = 'data/calib_portion_size.csv',
        coeff_filepath = 'data/calib_equation_coeff.csv',
        age_group_filepath = 'data/age_groups.csv',
        coeff_to_var_filepath = 'data/DSQ_coefficient_to_var.csv',
        calc_vars_filepath = 'data/DSQ_calculated_vars.csv',
        calc_vars_description_filepath = 'data/DSQ_calculated_vars_descriptions.csv',
        survey_results = deepcopy(sample_post['dsq'])
        ):

    age_groups = read_csv_universal_newline(age_group_filepath)
    for row in age_groups[1:]:
        if float(survey_results['age']) <= float(row[1]):
            age_group = row[2]
            age_group_type = row[3]
            break

    kidgrp = 0
    teengrp = 0
    if age_group_type == 'child':
        kidgrp = 1
    elif age_group_type == 'teenager':
        teengrp = 1

    portion_size = get_portions(age_group, survey_results['sex'], psize_filepath = psize_filepath)

    survey_results['cereal']['num_cereals'] = len(survey_results['cereal']['cereals'])
    cereal_dict = get_cereal_dict(cereal_filepath)

    cereal_stats = {"sug":[0,0,0],
                    "whg":[0,0,0],
                    "calc":[0,0,0],
                    "fib":[0,0,0]}
    if survey_results['cereal']['num_cereals'] > 0:
        for cereal in survey_results['cereal']['cereals']:
            for category in ['sug', 'whg', 'calc', 'fib']:
                try:
                    cereal_stats[category][int(cereal_dict[cereal['name'].lower()][category+'nt'])-1] += cereal['freq']
                except KeyError:
                    cereal_stats[category][int(cereal_dict['cereal, nfs'][category+'nt'])-1] += cereal['freq']


    for category in ['sug', 'whg', 'calc', 'fib']:
        for index, value in enumerate(cereal_stats[category]):
            survey_results[category+str(index+1)] = {'freq':float(value)}

    coefficients = get_coeff(survey_results['sex'])
    print('coffieictne ', coefficients)
    coeff_to_var = read_csv_universal_newline(coeff_to_var_filepath)
    temp_vars = {}
    for row in coeff_to_var[1:]:
        temp_vars[row[0]] = (coefficients[row[1]] if row[1] in coefficients else portion_size[row[1]]) \
                             * survey_results[row[2]]['freq']
        #this executes the formulas in the coeff_to_var file. This could potentially be a huge vulnarability if the file were open to the public
        exec(row[0] + ' = ' + str(temp_vars[row[0]]))
    d = coefficients.copy()
    # d.update(temp_vars)
    for key, value in d.items():
        #this sets a number of keys to the above values so that they can be evaluated later
        exec(key + ' = ' + str(value))


    results = {}
    for row in open(calc_vars_description_filepath, 'rU'):
        var, description = row.split(',')
        results[var] = {'description':description.strip()}
    for row in open(calc_vars_filepath, 'rU'):
        var, formula = row.split(',')
        formula = formula.strip()
        #a formula from calc_vars_description is run to generate result
        value = eval(formula)
        if 'probability' in results[var]['description']:
            if value < -100:
                value = math.exp(-100)/(1+math.exp(-100))
            elif value > 100:
                value = math.exp(100)/(1+math.exp(100))
            else:
                value = math.exp(value)/(1+math.exp(value))
        results[var]['val'] = value
        exec(var +'='+str(value))
    return results


#nhanes survey has weird metric where 1 = day, 2 = week, 3 = month
def units_to_days(x):
    try:
        x = float(x)
    except ValueError:
        x = 999999999999999999
    if x == 1.0:
        return 1.0
    elif x == 2.0:
        return 7.0
    elif x == 3.0:
        return 30.0
    return x

#prepares NHANES DSQ results for use in data.
def process_NHANES_DSQ(patient_data):
    patient_data = deepcopy(patient_data)
    for key, value in patient_data.items():
        if key in DSQ_NHANES_vars_list:
            try:
                patient_data[key] = float(value)
            except:
                if 'DTD' in key:
                    patient_data[key] = 0
                elif 'DTQ' in key:
                    patient_data[key] = 99999999999
    return \
        {"age": patient_data['RIDAGEYR'],
         "sex": patient_data['RIAGENDR'],
         "cereal":
            {"cereals":
                [{"freq":int(patient_data['DTD010Q']) / units_to_days(patient_data['DTQ010U']) * (.75 if patient_data['DTDCER'] == '2' else 1),
                  "name":patient_data['DTQ020a'] if 'DTQ020a' in patient_data else 'NA'},
                 {"freq":int(patient_data['DTD010Q']) / units_to_days(patient_data['DTQ010U']) * (.25 if patient_data['DTD010Q'] == '2' else 0),
                  "name":patient_data['DTQ020b'] if 'DTQ020b' in patient_data else 'NA'}]
                    },
         "milk":
            {"freq":patient_data['DTD030Q']/units_to_days(patient_data['DTQ030U']),
             "type":'NA'},
         "soda":{"freq":patient_data['DTD040Q']/units_to_days(patient_data['DTQ040U'])},
         "fruit_juice":{"freq":patient_data['DTD050Q']/units_to_days(patient_data['DTQ050U'])},
         "coffee":{"freq":patient_data['DTD060Q']/units_to_days(patient_data['DTQ060U'])},
         "sweet_drinks":{"freq":patient_data['DTD070Q']/units_to_days(patient_data['DTQ070U'])},
         "fruit":{"freq":patient_data['DTD080Q']/units_to_days(patient_data['DTQ080U'])},
         "salad":{"freq":patient_data['DTD090Q']/units_to_days(patient_data['DTQ090U'])},
         "potatoes_fried":{"freq":patient_data['DTD100Q']/units_to_days(patient_data['DTQ100U'])},
         "dry_beans":{"freq":patient_data['DTD120Q']/units_to_days(patient_data['DTQ120U'])},
         "potatoes_other":{"freq":patient_data['DTD110Q']/units_to_days(patient_data['DTQ110U'])},
         "grains":{"freq":patient_data['DTD210Q']/units_to_days(patient_data['DTQ210U'])},
         "vegetables":{"freq":patient_data['DTD130Q']/units_to_days(patient_data['DTQ130U'])},
         "salsa":{"freq":patient_data['DTD150Q']/units_to_days(patient_data['DTQ150U'])},
         "pizza":{"freq":patient_data['DTD140Q']/units_to_days(patient_data['DTQ140U'])},
         "tomato_sauce":{"freq":patient_data['DTD160Q']/units_to_days(patient_data['DTQ160U'])},
         "cheese":{"freq":patient_data['DTD190Q']/units_to_days(patient_data['DTQ190U'])},
         "red_meat":{"freq":patient_data['DTD170Q']/units_to_days(patient_data['DTQ170U'])},
         "proc_meat":{"freq":patient_data['DTD180Q']/units_to_days(patient_data['DTQ180U'])},
         "bread":{"freq":patient_data['DTD200Q']/units_to_days(patient_data['DTQ200U'])},
         "candy":{"freq":patient_data['DTD220Q']/units_to_days(patient_data['DTQ220U'])},
         "doughnuts":{"freq":patient_data['DTD230Q']/units_to_days(patient_data['DTQ230U'])},
         "cookies":{"freq":patient_data['DTD240Q']/units_to_days(patient_data['DTQ240U'])},
         "desserts":{"freq":patient_data['DTD250Q']/units_to_days(patient_data['DTQ250U'])},
         "popcorn":{"freq":patient_data['DTD260Q']/units_to_days(patient_data['DTQ260U'])},
         }

#returns DSQ scores for NHANES patients
def DSQ_to_Score(patient_data):
    processed_data = process_NHANES_DSQ(patient_data)
    processed_data = dsq_survey_processor(deepcopy(processed_data))
    results = dsq_scorer(survey_results = deepcopy(processed_data))
    return dict(map(lambda x: (x[0], x[1]['val']) ,results.items()))

#loads some variables into memory
DSQ_NHANES_vars_list, DSQ_output_vars = read_csv_universal_newline('data/DSQ_NHANES_var_names.csv')
DSQ_NHANES_vars_list = DSQ_NHANES_vars_list + ['RIDAGEYR', 'RIAGENDR']

dsq_vars_list = {'dbids':DSQ_NHANES_vars_list,
                 'outputs':DSQ_output_vars,
                 'calc':DSQ_to_Score}

if __name__ == '__main__':
    survey = dsq_survey_processor(sample_post['dsq'])
    print(json.dumps(dsq_scorer(survey_results = survey), indent = 4))
