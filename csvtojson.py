'''Inserts finished data into a geojson file and csv file'''
import csv
import json
import ast
csv_file_name = '/Users/darrell/Desktop/oaklandside-downtown/oakdata.csv'
fn = '/Users/darrell/Desktop/oaklandside-downtown/crosswalk/change0020tract.csv'
gj = '/Users/darrell/Desktop/oaklandside-downtown/dwtnoak20_00.geojson'
oakland = ["G0600010402801","G0600010402802","G0600010402900","G0600010403100", "G0600010403000", "G0600010403402","G0600010403301","G0600010403302","G0600010983200"]
with open(fn, 'r') as a:
    info = list(csv.reader(a, delimiter=','))
with open(gj, 'r') as b:
    tracts = json.load(b)
csv_file = [["GISJOIN", "POP", "WHITE", "BLACK", "NATIVE AMERICAN", "ASIAN", "PACIFIC ISLANDER",
             "SOME OTHER RACE", "MULTI-RACIAL", "LATINO", "HOMES", "VACANT", "RENTERS",
             "HOMEOWNERS", "WHITE HOMEOWNERS", "BLACK HOMEOWNERS", "NATIVE AMERICAN HOMEOWNERS",
             "ASIAN HOMEOWNERS", "PACIFIC ISLANDER HOMEOWNERS", "OTHER RACE HOMEOWNERS", "MULTI-RACIAL HOMEOWNERS",
             "LATINO HOMEOWNERS","WHITE LEASEHOLDERS", "BLACK LEASEHOLDERS", "NATIVE AMERICAN LEASEHOLDERS",
             "ASIAN LEASEHOLDERS", "PACIFIC ISLANDER LEASEHOLDERS", "OTHER RACE LEASEHOLDERS", "MULTI-RACIAL LEASEHOLDERS",
             "LATINO LEASEHOLDERS"]]
print("START")
areas = ["UPTOWN WEST","SAN PABLO GATEWAY","UPTOWN EAST","CHINATOWN","CITY CENTER","MADISON SQ. PARK","LANEY/ JLS EAST","LAKESIDE","JACK LONDON SQ."]
for row in info:
    if row[0] in oakland:
        # CSV
        r = ast.literal_eval(row[1])
        rounded_list = [round(num) for num in r]
        rounded_list.insert(0,row[0])
        csv_file.append(rounded_list)
        # JSON
        for tract in tracts['features']:
            if row[0] == tract['properties']['GISJOIN']:
                # insert data
                data = ast.literal_eval(row[1])
                for i, d in enumerate(data):
                    tract['properties'][str(i)] = round(d)
                break
with open(csv_file_name, 'w', newline='') as cf:
    csv_writer = csv.writer(cf)
    # Writing each element as a row
    for row in csv_file:
        csv_writer.writerow(row)
    cf.close()
print("END")
with open(gj, 'w') as d: #Writing the new data into the empty GJ file
    json.dump(tracts, d)
    d.close()
                    
    
