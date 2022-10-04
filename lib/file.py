# set of utilities to interact with files
import pickle

import csv, json
from lib.log import slogger

# log = slogger ('IPVisit-file')

def read_obj (filename):
	try:
		data = pickle.load (open(filename, 'rb'))
		return data
	except Exception as e:
		log.error(e)
		return None


# write an object (list, set, dictionary) to a serialized file
def write_obj (filename, data):
	try:
		pickle.dump(data, open(filename, 'wb'))
		return True
	except Exception as e:
		log.error(e)
		return False

# read an dictionary from a json file
def read_JSON (filename, encoding = 'utf-8'):
	try:
		data = json.load(open(filename, 'r'), encoding = encoding)
		return data
	except Exception as e:
		log.error(e)
		return None


# write a dictionary to a json file
def write_JSON (filename, data, encoding = 'utf-8', pretty = True):
	try:
		if pretty:
			json.dump(data, open(filename, 'w'), sort_keys = True, indent = 4, encoding = encoding)
		else:
			json.dump(data, open(filename, 'w'), encoding = encoding)
		return True
	except Exception as e:
		log.error(e)
		return False

#check if something is an allowed file
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# read data from a csv file    
def read_csv (filename, delimiter = "auto", escapechar = '\\'):
	try:
		if delimiter == 'auto':
			with open(filename, 'rb') as csvfile:
				delimiter = csv.Sniffer().sniff(csvfile.read(1024)).delimiter
		reader = csv.reader (open(filename, "r"), escapechar=escapechar, delimiter = delimiter)
		data = []
		for r in reader:
			data.append(r)
		return data
	except Exception as e:
		log.error(e)
		return False

# read data from a csv file    
def read_csv_universal_newline (filename, delimiter = ","):
	try:
		reader = csv.reader (open(filename, "rU"), escapechar='\\', delimiter = delimiter)
		data = []
		for r in reader:
			data.append(r)
		return data
	except Exception as e:
		log.error(e)
		return False

# read a text file
def read_file (filename):
	try:
		fid = open(filename, 'rU')
		data = []
		for line in fid:			
			if len(line) > 0:
				data.append (line.strip())		
		fid.close()
		return data
	except Exception as e:
		log.error(e)
		return False


# write data to a csv file
def write_csv (filename, data, quotechar='"', append = False, delimiter = ',' ):
	if quotechar is None: quoting=csv.QUOTE_NONE
	else: quoting=csv.QUOTE_ALL
	if append: writetype = 'a'
	else: writetype = 'wb'
	try:
		doc = csv.writer (open(filename, writetype), delimiter=delimiter, quotechar=quotechar, quoting=quoting, escapechar = '\\')
		for d in data:
			doc.writerow (d)
		return True			
	except Exception as e:
		log.error(e)
		return False
	
# read a csv and output a list of dictionaries
def csvToDictionaryList(filename, delimiter = 'auto'):
	try:
		if delimiter == 'auto':
			with open(filename, 'rb') as csvfile:
				delimiter = csv.Sniffer().sniff(csvfile.read(1024)).delimiter
		reader = csv.DictReader (open(filename, "rU"),delimiter = delimiter, escapechar='\\')
		data = []  
		for r in reader:
			data.append(r)
		return data
	except Exception as e:
		log.error(e)
		return False

# read a csv and output a dictionary with the keys as the specified column, and a list of dictionary rows for their result
def csvToDictionary(filename, key, delimiter = 'auto', unique = True):
	try:
		if delimiter == 'auto':
			with open(filename, 'rb') as csvfile:
				delimiter = csv.Sniffer().sniff(csvfile.read(1024))
		reader = csv.DictReader (open(filename, "rU"))
		data = {}
		for r in reader:
			keyvalue = r[key]
			if unique:
				del r[key]
				data[keyvalue] = r
			elif keyvalue in data:
				del r[key]
				data[keyvalue].append(r)
			else:
				del r[key]
				data[keyvalue] =[r]
		return data
	except Exception as e:
		log.error(e)
		return False

def dictionaryToCSV(filename, data, fieldnames, indexName, encode = None, delimiter = ','):
#	try:
		doc = csv.DictWriter (open(filename, 'wb'), fieldnames=[indexName]+fieldnames, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL, extrasaction = 'ignore')
		doc.writeheader()
		for key, dl in data.items():
			if isinstance(dl, dict): dl = [dl]
			for d in dl:
				if encode:
					for key, value in d.items():
						try:
							d[key] = value.encode(encode)
						except AttributeError:
							try:
								d[key] = ';'.join(value).encode(encode)
							except Exception:
								d[key] = '' 
				d[indexName] = key
				doc.writerow (d)
		return True	

def dictionaryListToCSV(filename, data, fieldnames, encode = None, delimiter = ','):
	try:
		doc = csv.DictWriter (open(filename, 'wb'), fieldnames=fieldnames, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL, extrasaction = 'ignore')
		doc.writeheader()
		for d in data:
			if encode:
				for key, value in d.items():
					try:
						d[key] = value.encode(encode)
					except AttributeError:
						try:
							d[key] = ';'.join(value).encode(encode)
						except Exception:
							d[key] = '' 
			doc.writerow (d)
		return True			
	except Exception as e:
		log.error(e)
		return False

def readSet(filename, delimiter = 'auto', escapechar = '\\'):
	try:
		if delimiter == 'auto':
			with open(filename, 'rb') as csvfile:
				delimiter = csv.Sniffer().sniff(csvfile.read(1024)).delimiter
		reader = csv.reader (open(filename, "rU"), escapechar=escapechar, delimiter = delimiter)
		data = set()
		for r in reader:
			for c in r:
				data.add(c)
		return data
	except Exception as e:
		log.error(e)
		return False

def prettyPrint(localobject, prefix = ''):
	if len(prefix) > 40:
		print(prefix+json.dumps(localobject, sort_keys=True,
	                  	 indent=4, separators=(',', ': ')))
	else:
		print(prefix)
		print(json.dumps(localobject, sort_keys=True,
	                  	 indent=4, separators=(',', ': ')))