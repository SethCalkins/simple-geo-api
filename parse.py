import csv
import json

with open('cityzip.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
    	out_file_name = 'data/US_%s.json' % r['Postal']
    	r = { k.lower() : v for k,v in r.items() }
    	r['country'] = 'US'
    	with open(out_file_name, 'w') as fo:
    		json.dump(r, fo)

#    	print out_file_name
#    xml_str = f.read()

