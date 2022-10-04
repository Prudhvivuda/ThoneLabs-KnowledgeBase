from lib.normalizer import _load_data as normalizer_load_data
from lib.static_vars import calculated_variable_list, vars_list
from lib.file import write_csv, write_JSON, read_JSON, read_csv
from json import dumps
import itertools, os, traceback, time
import getpass, MySQLdb, MySQLdb.cursors

def chunker (l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def insert_into_db(cur, table_name, keylist, input, chunksize = 1000, replace = False):
    start = time.time()
    chunks = chunker(input, chunksize)
    numChunks = len(chunks)
    print(keylist, input[0].keys())
    for num, chunk in enumerate(chunks):
        print("Inserting chunk: " + str(num) + '/' + str(numChunks), 'took',time.time()-start,'seconds.')
        start = time.time()
        query = "INSERT IGNORE INTO "+table_name+" ("+', '.join(keylist)+") VALUES " + \
                ", ".join('('+', '.join(map(lambda x: '"'+str(x).replace('"','')+'"' if isinstance(x, basestring)
                                                      else "NULL" if x == None 
                                                      else str(x), 
                                            map(lambda x: y[x], keylist)))+')'
                           for y in chunk)
        try:
            cur.execute(query)
        except Exception as e:
            print(query)
            print(e)
            break
        


def upload_NHANES_to_mysql(basepath, drop_table = False):
    pswd = getpass.getpass('Password:')
    conn = MySQLdb.connect(host="la-forge.mssm.edu", # your host, usually localhost
                           user="tomlim02", # your username
                           passwd=pswd, # your password
                           db="nhanes", # name of the data base
                           cursorclass=MySQLdb.cursors.DictCursor)
    
    cur = conn.cursor()
    csv_path = basepath + 'csv_data'
    raw_path = basepath + 'raw_data'
    years = [x for x in os.listdir(csv_path) if os.path.isdir(csv_path+'/'+x)]
    variable_descriptions = {}
    calc_vars = set.union(*map(lambda x: set(x['dbids']), vars_list.values()))
    id_name = 'SEQN'
    print('calc_vars', calc_vars)
    
    if drop_table:
        cur.execute('''Drop table if exists nhanes;''')
        cur.execute('''create table nhanes
                   (subject_id varchar(20) not null,
                    variable varchar(20) not null,
                    value varchar(600) not null,
                    year varchar(15),
                    primary key (subject_id, variable));
                   ''')
        cur.execute('''alter table nhanes add index value (value);''')
        cur.execute('''alter table nhanes add index year (year);''')
    
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
#         for key in vars_list.keys():
#             print('calculating', key)
#             local_calc_vars = set(vars_list[key]['dbids'])
#             count = 0
#             for index in data.keys():
#                 if not False in [x in data[index].keys() for x in local_calc_vars]:
#                     data[index].update(vars_list[key]['calc'](data[index]))
#                     count = count + 1
#                     if count % 100 == 0:
#                         print(count, key, 'calcs completed')
#             print('calculated', count)
        #subject = [0] * len(data)
        try:
            this_year = year.split('-')[0]
        except:
            this_year = year
        print('Inserting year:', this_year)
        cur = conn.cursor()
        subject_data = map(lambda y: map(lambda x: {'subject_id':y[0], 
                                                    'variable':x[0], 
                                                    'value':x[1], 
                                                    'year':this_year}, 
                                         y[1].items()), 
                           data.items())
        subject_data = list(itertools.chain.from_iterable(subject_data))
        insert_into_db(cur, 
                       'nhanes', 
                       ['subject_id', 'variable', 'value', 'year'], 
                       subject_data, 
                       chunksize = 100000)
    
        cur.close()
        conn.commit()
        cur = conn.cursor()
    cur.close()
    conn.close()


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
    upload_NHANES_to_mysql('NHANES_Downloader/data/', drop_table = True)
#     client = establish_client('mongodb://localhost:27017/')
#     print(client)
#     db = client.lab100kb
#     upload_NHANES_to_MONGO('NHANES_Downloader/data/', db.subjects)
    #write_calculated_data_to_csv()