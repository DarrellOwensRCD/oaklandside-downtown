'''Inserts finished data into a geojson file'''
import csv
import json
import ast
fn = '/Users/darrell/Desktop/oaklandside-downtown/crosswalk/change0020tract.csv'
gj = '/Users/darrell/Desktop/oaklandside-downtown/dwtnoak20_00.geojson'
oakland = ["G0600010402801","G0600010402802","G0600010402900","G0600010403100", "G0600010403000", "G0600010403402","G0600010403301","G0600010403302","G0600010983200"]
with open(fn, 'r') as a:
    info = list(csv.reader(a, delimiter=','))
with open(gj, 'r') as b:
    tracts = json.load(b)
for row in info:
    if row[0] in oakland:
        for tract in tracts['features']:
            if row[0] == tract['properties']['GISJOIN']:
                # insert data
                data = ast.literal_eval(row[1])
                for i, d in enumerate(data):
                    tract['properties'][str(i)] = round(d)
                break
with open(gj, 'w') as d: #Writing the new data into the empty GJ file
    json.dump(tracts, d)
    d.close()
                    
    
