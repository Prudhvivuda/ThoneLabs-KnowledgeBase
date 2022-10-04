from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from lib.normalizer import _load_data as normalizer_load_data
from lib.static_vars import calculated_variable_list, vars_list
from lib.file import write_csv, write_JSON, read_JSON, read_csv
from json import dumps
import itertools, os, traceback

def establish_client(location):
    client = MongoClient(location)
    return client

def upload_NHANES_to_MONGO(basepath, subjects):
    csv_path = basepath + 'csv_data'
    raw_path = basepath + 'raw_data'
    years = [x for x in os.listdir(csv_path) if os.path.isdir(csv_path+'/'+x)]
    data = {}
    variable_descriptions = {}
    calc_vars = set.union(*map(lambda x: set(x['dbids']), vars_list.values()))
    id_name = 'SEQN'
    print('calc_vars', calc_vars)
    
    for year in years:
        data = {}
        categories = [x for x in os.listdir(csv_path+'/'+year) if os.path.isdir(csv_path+'/'+year+'/'+x)]
        for category in categories:
            json_files = [x for x in os.listdir(raw_path+'/'+year+'/'+category) if '.JSON' in x]
            for json_file in json_files:
                labels = read_JSON(raw_path+'/'+year+'/'+category+'/'+json_file)
                labels = dict(map(lambda x: (x[0].strip(), x[1].strip()), labels.items()))
                for label in labels.keys():
                    variable_descriptions[label] = labels[label]
                data_csv = read_csv(csv_path+'/'+year+'/'+category+'/'+json_file.replace('JSON', 'csv'), delimiter = ',')
                header = data_csv[0]
                try:
                    id_index = header.index(id_name)
                    for row in data_csv[1:]:
                        if not row[id_index] in data: #add new id to file, if id is not yet in the file
                            data[row[id_index]] = {}
                        for index, col in enumerate(row):
                            if not col == '':
                                try:
                                    data[row[0]][header[index]] = float(col)
                                except ValueError:
                                    data[row[0]][header[index]] = col
                    print(year+'/'+category+'/'+json_file.replace('.JSON', ''), 'loaded.')
                except ValueError as e:
                    traceback.print_exc()
                    print(year+'/'+category+'/'+json_file.replace('.JSON', ''), 'was not included.')
                    #print('Header was: ', header)
        for key in vars_list.keys():
            print('calculating', key)
            local_calc_vars = set(vars_list[key]['dbids'])
            count = 0
            for index in data.keys():
                if not False in [x in data[index].keys() for x in local_calc_vars]:
                    data[index].update(vars_list[key]['calc'](data[index]))
                    count = count + 1
                    if count % 100 == 0:
                        print(count, key, 'calcs completed')
            print('calculated', count)
        #subject = [0] * len(data)
        for index, (key, value) in enumerate(data.items()):
            subject = value
            subject['_id'] = int(float(key))
            subjects.update_one({'_id': subject['_id']}, {"$set":subject}, upsert = True)


def load_calculated_data(base_dir):
    outputs = list(itertools.chain.from_iterable(map(lambda x: x['outputs'], vars_list.values())))
    #input = vars_list['dsq']['outputs']
    input = list(itertools.chain.from_iterable(map(lambda x: x['outputs'], vars_list.values())))
    data = normalizer_load_data(base_dir)
    data = dict(map(lambda x: (x[0], dict(filter(lambda y: y[0] in outputs, x[1].items()))), data.items()))
    print(dumps(data.items()[0:10]))
    return data
    
def update_calculated_data(base_dir):
    data = load_calculated_data(base_dir)
    out_data = []
    all_keys = set(list(itertools.chain.from_iterable(map(lambda x: list(x.keys()), data.values()))))
    print(all_keys)
    header = ['SEQN']+sorted(list(all_keys))
    for key, value in data.items():
        if len(value.keys()) > 0:
            out_data.append([key]+map(lambda x: value[x] if x in value else '', header[1:]))
    write_csv(base_dir+'calculated/calculated/CALCULATED.csv', [header]+out_data)
    write_JSON(base_dir+'calculated/calculated/CALCULATED.JSON',dict(map(lambda x: (x,'NA'), all_keys)))


if __name__ == '__main__':
    client = establish_client('mongodb://localhost:27017/')
    print(client)
    db = client.lab100kb
    upload_NHANES_to_MONGO('NHANES_Downloader/data/', db.subjects)
    #write_calculated_data_to_csv()