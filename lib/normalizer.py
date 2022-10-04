import os, json, traceback, itertools, numpy, traceback, json, time
from copy import deepcopy
from lib.file import read_JSON, read_csv
from scipy.stats import ks_2samp, percentileofscore
from lib.static_vars import get_cutoffs, get_all_variables, calculated_variable_list
from lib.gen_density_plot import generate_density_plot
from lib.helper import takeClosest
from lib.static_vars import static_distribution_vars
from scipy.stats import norm
import numpy as np
from lib.body_scan.weight import weight
from lib.body_scan.height import height
from lib.body_scan.waist_circumference import waist_circumference
#all the variables used in lab100
all_variables = get_all_variables()
#all the variables calculated in lab100
calculated_variables = calculated_variable_list()
#a list of default parameters for calculating normalization that can be passed to API
default_params = {'min_sample_size' : 200, #minimum sample size to be consider statistically relevant
                  'min_subset_size' : 50, #min subset size to be considered statistically relevant
                  'num_subsets' : 50, #number of subsets to divide the range by
                  'threshold_to_reject' : .1, #pvalue to reject the null hypothesis that two subsets are statistically identical
                  'size_of_distribution':200,
                  'bandwidth':'auto', #bandwidth for generating density plot - affects how "smooth" it is
                  'upper_bound':97.725, #highest percentile displayed in density plot
                  'lower_bound':2.225, #lowest percentile displayed in density plot
                  'override_cache':0} #whether to ignore an existing cache and replace it

#main class - instantiate this to generate normalized data
class Normalizer():
    data = {}
    params = {}

    def __init__(self,
                 filepath,
                 cache_dir = '',
                 target_variables = {},
                 normalization_variables = {},
                 **kwargs):
        self.NHANES_filepath = filepath
        self.target_variables = {}
        self.normalization_variables = deepcopy(normalization_variables)
        self.cutoffs = get_cutoffs()
        self.calculated_variables = {}
        #initialize the variables you want to return data for
        for key, var in target_variables.items():
            if key in all_variables:
                self.target_variables[key] = all_variables[key]
                self.target_variables[key].update({'value':var})
                if len(all_variables[key]['dbid']) > 0 and all_variables[key]['dbid'][0] in calculated_variables:
                    try:
                        calc_key = calculated_variables[all_variables[key]['dbid'][0]]
                        self.calculated_variables[calc_key] = calculated_variables[calc_key]
                    except:
                        traceback.print_exc()
            else:
                print(key,"not in all_variables")
                raise UnsupportedTargetException('Target Variable is not found among possible values!')

        #initialize the variables you want to control for
        for key, var in normalization_variables.items():
            if key in all_variables:
                self.normalization_variables[key] = all_variables[key]
                self.normalization_variables[key].update({'value':var})
            else:
                print(var,"not in all_variables")
        #make a dict with all of the subjects data
        self.subject_data = deepcopy(self.target_variables)
        self.subject_data.update(deepcopy(self.normalization_variables))
        #initialize the parameters for the normalization
        self.params = deepcopy(default_params)
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in default_params:
                    try:
                        self.params[key] = float(value)
                    except:
                        self.params[key] = value
                else:
                    raise ValueError('Invalid parameter entered!')
        #convert override_cache to a boolean
        try:
          print("override cache val", self.params['override_cache'])
          self.params['override_cache'] = bool(int(self.params['override_cache']))
        except ValueError:
          self.params['override_cache'] = False

        self.cache_dir = cache_dir
        start_time = time.time()
        self.load_data()
        print("Took " + str(time.time()-start_time) + " seconds to load data.")

    #load data
    def load_data(self):
        desired_variables = list(itertools.chain(*map(lambda x: x['dbid'], self.subject_data.values())))
        calc_vars = set.union(*map(lambda x: set(x['dbids']), calculated_variables.values())) if len(self.calculated_variables.values()) > 0 else set()
        cache_path = self.NHANES_filepath + 'cache/'
        if not os.path.isdir(cache_path):
            os.mkdir(cache_path)
        cache_name = '_'.join(sorted(set.union(calc_vars, set(desired_variables))))+'.json'
       
        if os.path.isfile(cache_path+cache_name) and not self.params['override_cache']:
            f = open(cache_path+cache_name, 'r')
            start_time = time.time()
            self.data = json.load(f)
            print("Took " + str(time.time() - start_time) + " seconds to load cached json data")
        else:
          start_time = time.time()
          self.data = _load_data(self.NHANES_filepath,
                                 desired_variables = desired_variables,
                                 calculated_variables = self.calculated_variables)

          _filter_data(self.data, required_variables = self.normalization_variables)
          f = open(cache_path+cache_name, 'w')
          json.dump(self.data, f)
          print("Took " + str(time.time() - start_time) + " seconds to generate data from csvs")

    #returns target distributions for each target variable
    def get_target_distributions(self):
        ls = []
        for item in self.target_variables.items():
            res = self.get_target_distribution(item)
            ls.append(res)
        return ls

    #returns the target distribution. First gets the distibution with _get_distribution, then generates:
    # a) an interpretation based on the cutpoints file, as well as which cutpoints are applicable absed on demographics
    # b) distribution stats, including mean, median, sd, min, max
    # c) percentile rank
    # d) a density plot using get_density_plot
    def get_target_distribution(self, target_variable):
        required_variables = deepcopy(self.normalization_variables)
        required_variables[target_variable[0]] = target_variable[1]
        if len(target_variable[1]['dbid']) > 0:
            start_time = time.time()
            hash_code = hash(json.dumps([[x for x in self.params.items() if not x[0] == 'override_cache'], target_variable[0], self.normalization_variables], sort_keys=True))
            cache_path = self.cache_dir + str(hash_code) + '.json'
            if os.path.isfile(cache_path) and not self.params['override_cache']:
              out = json.load(open(cache_path, 'r'))
            else:
              out =  _get_distribution(self.data,
                                       self.params,
                                       subject_values = self.subject_data,
                                       target_variable = target_variable,
                                       normalization_variables = self.normalization_variables,
                                       required_variables = required_variables)
              json.dump(out, open(cache_path, 'w'))
              
            print("Got normalized distribution in " + str(time.time() - start_time) + " seconds.")
        else:
            out = {}
        out['target_variable'] = target_variable[0]
        if 'distribution' in out and len(out['distribution']) > 0:
            if out['target_variable'] == 'percent_body_fat':
                out['distribution'] = map(lambda x: max(x - 4.62,0), out['distribution'])
                #we use bioelectrical impedence, NHANES is dexa scan, difference is about 4.62 points on avg
            out['percentile'] = percentileofscore(out['distribution'], float(target_variable[1]['value']))
            out['distribution_stats'] = {'mean':numpy.mean(out['distribution']),
                                         'median':numpy.median(out['distribution']),
                                         'standard deviation':numpy.std(out['distribution']),
                                         'min':numpy.min(out['distribution']),
                                         'max':numpy.max(out['distribution'])}
        elif out['target_variable'] in static_distribution_vars:
            distribution_stats = static_distribution_vars[out['target_variable']](self.subject_data['gender']['value'] if 'gender' in self.subject_data else None,
                                                                                  self.subject_data['age']['value'] if 'age' in self.subject_data else None)
            out['density_plot'] = generate_density_plot(stats = distribution_stats,
                                                        min = self.params['lower_bound'],
                                                        max = self.params['upper_bound'],
                                                        number_of_points = self.params['size_of_distribution'],
                                                        filedir = self.cache_dir,
                                                        override_cache = self.params['override_cache'])
            out['distribution_stats'] = {'mean':float(distribution_stats['mean']),
                                         'standard deviation':float(distribution_stats['sd'])
                                         }
            if out['target_variable'] in ['body_weight', 'height', 'waist_circumference']:
                if out['target_variable'] == 'height':
                    out["percentile"] = height.get_percentile(self.subject_data['age']['value'],
                                        self.subject_data['gender']['value'], target_variable[1]['value'])
                if out['target_variable'] == 'body_weight':
                    out["percentile"] = weight.get_percentile(self.subject_data['age']['value'],
                                        self.subject_data['gender']['value'], target_variable[1]['value'])
                if out['target_variable'] == 'waist_circumference':
                    out["percentile"] = waist_circumference.get_percentile(self.subject_data['age']['value'],
                                        self.subject_data['gender']['value'], target_variable[1]['value'])
            else:
                out['percentile'] = norm.cdf(float(target_variable[1]['value']),
                                         loc = float(distribution_stats['mean']),
                                         scale = float(distribution_stats['sd'])) * 100.0
        try:
            if target_variable[1]['display_name'] in self.cutoffs:
                out['cutpoints'] = []
                out['interpretation'] = []
                for cutoff in self.cutoffs[target_variable[1]['display_name']]:
                    if check_cutoff_validity(target_variable[1]['value'], cutoff,
                                             Age = float(self.subject_data['age']['value']) if 'age' in self.subject_data else None,
                                             Education = self.subject_data['education']['value'] if 'education' in self.subject_data else None,
                                             Ethnicity = self.subject_data['ethnicity']['value'] if 'ethnicity' in self.subject_data else None,
                                             Gender = self.subject_data['gender']['value'] if 'gender' in self.subject_data else None,
                                             Socioeconomic_status = self.subject_data['socioeconomic_status']['value'] if 'socioeconomic_status' in self.subject_data else None):
                        out['interpretation'].append(cutoff['Interpretation 1'])
                    if check_cutoff_possibility(cutoff,
                                                Age = float(self.subject_data['age']['value']) if 'age' in self.subject_data else None,
                                                Education = self.subject_data['education']['value'] if 'education' in self.subject_data else None,
                                                Ethnicity = self.subject_data['ethnicity']['value'] if 'ethnicity' in self.subject_data else None,
                                                Gender = self.subject_data['gender']['value'] if 'gender' in self.subject_data else None,
                                                Socioeconomic_status = self.subject_data['socioeconomic_status']['value'] if 'socioeconomic_status' in self.subject_data else None):
                        out['cutpoints'].append({'interpretation':cutoff['Interpretation 1'],
                                                 'value_1': cutoff['Cut_off_value_1'],
                                                 'sign_1':cutoff['Sign_1'],
                                                 'value_2':cutoff['Cut_off_value_2'],
                                                 'sign_2':cutoff['Sign_2'],
                                                 'units':cutoff['Unit']})

                if len(out['interpretation']) == 0:
                    out['interpretation'] = 'NA'
                elif len(out['interpretation']) == 1:
                    out['interpretation'] = out['interpretation'][0]
                else:
                    print("Multiple interpretations: taking first interpretation.")
                    out['interpretation'] = out['interpretation'][0]
            elif out['target_variable'] in static_distribution_vars:
                out['interpretation'] = percentile_to_interpretation(out['percentile'])
                out['cutpoints'] = distribution_to_cutpoints(np.random.normal(float(distribution_stats['mean']),
                                                                              float(distribution_stats['sd']),
                                                                              100000))
            elif 'distribution' in out and len(out['distribution']) > 0:
                out['interpretation'] = percentile_to_interpretation(out['percentile'])
                out['cutpoints'] = distribution_to_cutpoints(out['distribution'])

            if 'distribution' in out and len(out['distribution']) > 0:
                out['density_plot'] = generate_density_plot(distribution = out['distribution'],
                                                            filedir = self.cache_dir,
                                                            min = self.params['lower_bound'],
                                                            max = self.params['upper_bound'],
                                                            number_of_points = self.params['size_of_distribution'],
                                                            bandwidth = self.params['bandwidth'])

        except ValueError as e:
            print(e)
        return out

class UnsupportedTargetException(Exception): pass

#helper function to turn "X-Y" into [X,Y]. Not to be confused with _get_range, which has an unfortunately similar name
def _range(range):
    if len(range.split('-')) > 1:
        range = range.split('-')

#use distribution to cutpoints for interpretations if a distribution is available but no cutpoints
percentile_to_interpretation_index = [0,0.135,2.275,15.865,84.135,97.725,99.685]
percentile_to_interpretation_label = ['Extremely Below Average', 'Significantly Below Average', 'Below Average',
                                      'Average','Above Average', 'Significantly Above Average', 'Extremely Above Average']

def percentile_to_interpretation(percentile):
    return percentile_to_interpretation_label[takeClosest(percentile_to_interpretation_index,
                                                          percentile,
                                                          round = 'down')
                                              ]

def distribution_to_cutpoints(distribution):
    cutpoint_template = {"interpretation": "NA",
                        "sign_1": "NA",
                        "sign_2": "NA",
                        "value_1": "NA",
                        "value_2": "NA"
                        }
    cutpoints = []
    cutpoints.append(deepcopy(cutpoint_template))
    cutpoints[-1].update({'interpretation':percentile_to_interpretation_label[0],
                          'value_1':numpy.percentile(distribution,percentile_to_interpretation_index[1]),
                          'sign_1':'<='})
    for index in range(5):
        cutpoints.append(deepcopy(cutpoint_template))
        cutpoints[-1].update({'interpretation':percentile_to_interpretation_label[index+1],
                              'value_1':numpy.percentile(distribution,percentile_to_interpretation_index[index+1]),
                              'sign_1':'>=',
                              'value_2':numpy.percentile(distribution,percentile_to_interpretation_index[index+2]),
                              'sign_2':'<='})
    cutpoints.append(deepcopy(cutpoint_template))
    cutpoints[-1].update({'interpretation':percentile_to_interpretation_label[6],
                          'value_1':numpy.percentile(distribution,percentile_to_interpretation_index[6]),
                          'sign_1':'>='})
    return cutpoints

#loads data from csvs. Note that it only loads a csv file if that file has one of the target or demographic variables in it.
def _load_data(filepath, desired_variables = [], calculated_variables = {}, id_name = 'SEQN'):

    calc_vars = set.union(*map(lambda x: set(x['dbids']), calculated_variables.values())) if len(calculated_variables.values()) > 0 else set()

    csv_path = filepath + 'csv_data'
    raw_path = filepath + 'raw_data'
    years = [x for x in os.listdir(csv_path) if os.path.isdir(csv_path+'/'+x)]
    data = {}
    variable_descriptions = {}

    for year in years:
        categories = [x for x in os.listdir(csv_path+'/'+year) if os.path.isdir(csv_path+'/'+year+'/'+x)]
        for category in categories:
            json_files = [x for x in os.listdir(raw_path+'/'+year+'/'+category) if '.JSON' in x]
            for json_file in json_files:
                labels = read_JSON(raw_path+'/'+year+'/'+category+'/'+json_file)
                labels = dict(map(lambda x: (x[0].strip(), x[1].strip()), labels.items()))
                desired_labels = [x for x in labels.keys() if x in desired_variables or x in calc_vars]
                for label in desired_labels:
                    variable_descriptions[label] = labels[label]

                if len(desired_labels) > 0:
                    data_csv = read_csv(csv_path+'/'+year+'/'+category+'/'+json_file.replace('JSON', 'csv'), delimiter = ',')
                    header = data_csv[0]
                    try:
                        id_index = header.index(id_name)
                        for row in data_csv[1:]:
                            if not row[id_index] in data: #add new id to file, if id is not yet in the file
                                data[row[id_index]] = {}
                            for index, col in enumerate(row):
                                if header[index] in desired_labels:
                                    try:
                                        data[row[0]][header[index]] = float(col)
                                    except ValueError:
                                        data[row[0]][header[index]] = col
                        print(year+'/'+category+'/'+json_file.replace('.JSON', ''), 'loaded.')
                    except ValueError as e:
                        #traceback.print_exc()
                        print(year+'/'+category+'/'+json_file.replace('.JSON', ''), 'was not included - this is OK!')
                        #print 'Header was: ', header
    for key in calculated_variables.keys():
        print('calculating', key)
        local_calc_vars = set(calculated_variables[key]['dbids'])
        count = 0
        for index in data.keys():
            if not False in [x in data[index].keys() for x in local_calc_vars]:
                data[index].update(calculated_variables[key]['calc'](data[index]))
                count = count + 1
                if count % 100 == 0:
                    print(count, key, 'calcs completed')
        print('calculated', count)

    return data

#this filters out any rows in the data which do not have the target variable or one of the required demographic variables. You may also pass it variables you want to count as exclusionary, such as if the subject was pregnant.
def _filter_data(data,
                exclusion_variables = {},
                required_variables = {}):
    data = deepcopy(data)
    special_criterion_failures = set()
    print('Filtering!')
    for subject_id, subject_data in data.items():
        #Check that required variables are present
        for var in required_variables.values():
            toDelete = True
            for dbid in var['dbid']:
                if dbid in subject_data and not subject_data[dbid] == '':
                    toDelete = False
            if toDelete and subject_id in data:
                del data[subject_id]

        #check that exclusionary variables are not present
        if subject_id in data:
            for var in exclusion_variables.values():
                #print(subject_data, var)
                toDelete = False
                for dbid in var['dbid']:
                    if var in subject_data and not subject_data[var] == '':
                        toDelete = True
                if toDelete and subject_id in data:
                    del data[subject_id]
    return data

#given the data from NHANES, generate a demographically similar set. First, it filters out anyone who deos share identical categorical normalization variables (like gender or ethnicity). Then, in _get_range, it subsets the data into equally sized ranges (according to "num_subsets" in params) and evaluates whether their distribution of the target value are stiatistically similar. All statistically similar sets (using a pvalue determined by "threshold_to_reject") which form an unbroken range with the patients range are included in the demographically similar set. If a set contains too few samples, it is joined with a set with an adjacent range, until it is large enough (defined by "min_subset_size").
def _get_distribution(NHANES_data,
                      params,
                      subject_values = {},
                      target_variable = {},
                      normalization_variables = {},
                      required_variables = {}):
    data = deepcopy(NHANES_data)
    for key in required_variables.keys():
        target_var = required_variables[key]['dbid'][0]
        print('Num samples with', target_var, 'is:', len(list(filter(lambda x: target_var in x and not x[target_var] == '', data.values()))))
    print('Getting distribution. Number of potential subjects is: ', len(data.keys()))
    for NH_subject_id, NH_subject_data in data.items():
        if False in [len(set(required_variables[x]['dbid']).intersection(set(NH_subject_data)))>0 for x in required_variables]:
            del data[NH_subject_id]
        else:
            for var in [x for x in normalization_variables.keys()
                        if normalization_variables[x]['data_type'] == 'C']:
                dbids = normalization_variables[var]['dbid']
                dbid = filter(lambda x: x in NH_subject_data, dbids)[0]
                if not float(subject_values[var]['value']) == float(NH_subject_data[dbid]):
                    del data[NH_subject_id]
                    break
            if NH_subject_id in data:
                for var in [x for x in normalization_variables.keys()
                            if normalization_variables[x]['data_type'] == 'Q']:
                    dbids = normalization_variables[x]['dbid']
                    dbid = filter(lambda x: x in NH_subject_data, dbids)[0]
                    if not dbid in NH_subject_data or NH_subject_data[dbid] == '':
                        del data[NH_subject_id]
                        break
    print ('After filtering for categorical variables, the number of demographically similar subjects is:', len(data.keys()))
    ranges = {}
    for var in [x for x in normalization_variables.keys()
                if normalization_variables[x]['data_type'] == 'Q']:
        dbids = normalization_variables[var]['dbid']
        targets = target_variable[1]['dbid']

        distribution = list(map(lambda x: [float(x[dbids[0]]),float(x[targets[0]])],
                           filter(lambda x: not(x[dbids[0]] == '' or x[targets[0]] == ''),
                                  data.values())))
        if len(distribution) == 0 and len(data.values()) > 0:
            return {'distribution':[], 'error':['No data available for given parameters']}
        elif len(distribution) == 0:
            return {}
        ranges[var] = _get_range(distribution, subject_values[var]['value'], params)

    for NH_subject_id, NH_subject_data in data.items():
        for var, (lower_bound, upper_bound) in ranges.items():
            if float(NH_subject_data[normalization_variables[var]['dbid'][0]]) < lower_bound or \
                    float(NH_subject_data[normalization_variables[var]['dbid'][0]]) > upper_bound:
                del data[NH_subject_id]
                break
    for var in [x for x in normalization_variables.keys()
                if all_variables[x]['data_type'] == 'C']:
        ranges[var] = subject_values[var]
    print('After filtering for quantitative variables, the number of demographically similar subjects is:', len(data.values()))
    return {'distribution':filter(lambda x: isinstance(x, float), map(lambda x: tryfloat(x[target_variable[1]['dbid'][0]]), data.values())), 'ranges':ranges}

def tryfloat(value):
    try:
        return float(value)
    except:
        return value

def _get_range(distribution, subject_value, params):
    var_distribution = map(lambda x: x[0], distribution)
    total_count = len(var_distribution)
    min_var = min(var_distribution)
    max_var = max(var_distribution)
    increment = (max_var - min_var)/params['num_subsets']
    subsets = []

    for index in range(params['num_subsets']):
        min_val = min_var + index * increment
        max_val = min_var + (index+1) * increment
        subsets.append([[min_val, max_val], #range of normalization variable
                        map(lambda x: float(x[1]), #target value
                            filter(lambda x: x[0] >= min_val and (x[0] < max_val or (index + 1) == params['num_subsets']),
                                   distribution))]
                       )
    indices_to_remove = set()
    for index, subset in enumerate(subsets):
        if not len(subset[1]) > params['min_subset_size']:
            if (index + 1) < params['num_subsets']:
                subsets[index+1][0][0] = subsets[index][0][0]
                subsets[index+1][1] = subsets[index+1][1] + subsets[index][1]
            else:
                subsets[index-1][0][1] = subsets[index][0][1]
                subsets[index-1][1] = subsets[index-1][1] + subsets[index][1]
            indices_to_remove.add(index)
    for index in sorted(indices_to_remove, reverse = True):
        del subsets[index]
    range_tests = map(lambda x: (x[0][0] <= float(subject_value),
                        x[0][1] > float(subject_value)),
                        subsets)
    try:
        target_index = range_tests.index((True, True))
    except ValueError:
        if range_tests[-1][1] == False:
            target_index = len(range_tests)-1
        else:
            target_index = 0
    lower_bound = min_var
    upper_bound = subsets[target_index][0][1]
    scores = range(len(subsets))
    for index, subset in enumerate(subsets):
        pvalue = ks_2samp(subset[1],subsets[target_index][1])[1]
        scores[index] = pvalue
        if pvalue < params['threshold_to_reject'] and index < target_index:
            lower_bound = subsets[index + 1][0][0]
        elif index > target_index:
            if pvalue > params['threshold_to_reject']:
                upper_bound = subset[0][1]
            else:
                break
    return (lower_bound, upper_bound)

#converts ethnicity names to NHANES classification
ethnicity_converter = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,
                       "Mexican American":1,
                       "Hispanic":2,
                       "Other Hispanic":2,
                       "White":3,
                       "Non-Hispanic White":3,
                       "Black":4,
                       'Non-Hispanic Black':4,
                       "African American":4,
                       "Non-Hispanic":5,
                       "Non-Hispanic Asian":6,
                       'Asian':6,
                       "Multiracial":7,
                       "Non-Hispanic Multiracial":7,
                       'Sub-Saharan African':4,
                       'All':'NA',
                       'Japanese ':6,
                       'Chinese':6,
                       'NA':'NA',
                       'Ethnic South and Central American':2,
                       'Ethnicity':'NA',
                       'Chinese American':6,
                       'African origin':4,
                       'Eastern Mediterranean and Middle East (Arab) populations':5,
                       'Latino':2,
                       'South Asian':6,
                       'Europid':3,
                       '':'NA',
                       None:'NA'}
gender_converter = {'1':"Male",'2':"Female",None:'NA'}

#using the organization of the cutoffs, returns true if a cutoff matches the patients demographics and target_value
def check_cutoff_validity(value, cutoff_dict, Age = None, Education = None, Ethnicity = None, Gender = None,
                          Socioeconomic_status = None):
    return cutoff_dict['Cutoff_Function'](value, cutoff_dict) and \
           cutoff_dict['Age_Function'](Age, cutoff_dict) and \
           (cutoff_dict['Education'] == 'NA' or cutoff_dict['Education'] == Education) and \
           (ethnicity_converter[cutoff_dict['Ethnicity']] == 'NA' or
            ethnicity_converter[cutoff_dict['Ethnicity']] == ethnicity_converter[Ethnicity]) and \
           (cutoff_dict['Sex'] == 'NA' or cutoff_dict['Sex'] == gender_converter[Gender]) and \
           (cutoff_dict['Socioeconomic status'] == 'NA' or cutoff_dict['Socioeconomic_status'] == Socioeconomic_status)

#using the organization of the cutoffs, returns true if a cutoff matches just the demographic values of patient
def check_cutoff_possibility(cutoff_dict, Age = None, Education = None, Ethnicity = None, Gender = None,
                             Socioeconomic_status = None):
    try:
        return cutoff_dict['Age_Function'](Age, cutoff_dict) and \
               (cutoff_dict['Education'] == 'NA' or cutoff_dict['Education'] == Education) and \
               (ethnicity_converter[cutoff_dict['Ethnicity']] == 'NA' or
                ethnicity_converter[cutoff_dict['Ethnicity']] == ethnicity_converter[Ethnicity]) and \
               (cutoff_dict['Sex'] == 'NA' or cutoff_dict['Sex'] == gender_converter[Gender]) and \
               (cutoff_dict['Socioeconomic status'] == 'NA' or cutoff_dict['Socioeconomic_status'] == Socioeconomic_status)
    except:
        return False
        print("Cutoff Failed - Age", Age, 'Education', Education, 'Ethnicity', Ethnicity, \
            'Gender', Gender, 'Socieeconomic_status', Socioeconomic_status)

