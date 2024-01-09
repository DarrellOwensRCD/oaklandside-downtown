'''Program will calculate the differences in data from 2010 to 2020 at the block level,
will open net change data 00 - 10 from the Part 1 program and multiplying values by the 10 - 20 weights,
(in addition to calculating the 10 - 20 net data as Part 1 calculated the 00 - 10),
and add those weighted net changes and demographics up to the tract level of 2020.
'''
import ast
import json
import csv
import statistics
import os.path
import copy
from os import path

def tract_maker(final2020):
    tract2020 = {}
    seen = []         
    for k in final2020.keys():
        tract = k[0:14]
        if tract not in seen:
            values = []
            for key, value in final2020.items():
                if key[0:14] == tract:
                    if not values:
                        values = value
                    else:
                        values = [float(a) + float(b) for a, b in zip(values, value)]
            if values:
                tract2020[tract] = values
                seen.append(tract)
    return tract2020
def zerodiv(a, b):
    if b > 0:
        return round(a / b, 1)
    return 0
print("Opening Data files")
#Census tracts of 2020 map
# Census 2000 data Blocks
# Census 2010 data Blocks
f10 = '/Users/darrell/Desktop/oaklandside-downtown-project/Census2010/nhgis0094_ds172_2010_block.csv'
# Census 2020 data Blocks
f20 = '/Users/darrell/Desktop/oaklandside-downtown-project/Census2020/nhgis0095_ds258_2020_block.csv'
# Weighted Data from 2000 to 2010
filecw1 = '/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change0010.csv'
# 2010 to 2020 Crosswalks
filecw2 = '/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/nhgis_blk2010_blk2020_gj_06(1)/nhgis_blk2010_blk2020_gj_06.csv'
with open(filecw1) as a, open(filecw2) as b, open(f10) as d, open(f20) as e:
    f2010 = list(csv.reader(a, delimiter=',')) # Crosswalk 2000 - 2010
    cw2 = list(csv.reader(b, delimiter=',')) # Crosswalk 2010 - 2020
    d10 = list(csv.reader(d, delimiter=',')) # Census 2010
    d20 = list(csv.reader(e, delimiter=',')) # Census 2020
final2010 = {}
# Digitizing the net changes calculated in PART 1 from a string list to a real list, accompanied with each 2010 block which is final2010
for row in f2010:
    final2010[row[0]] = ast.literal_eval(row[1])
print("Weighting Data")
''' Weighting the 2010 data from the 2020 crosswalks
    Iterate through the crosswalk file. Find a 2010 block in the crosswalk row (cross_row)
    then find its data from d10 database which is row. Take the weight and multiply each
    value by the weight. This shows the share of data represented for the 2020 block, placed
    into the "weighted" or wdata10 database
'''
wnet10 = [["Block ID 2010", "Block ID 2020", "List of Net Changes"]]
wdata10 =[d10[0][58:102]]
wdata10[0].insert(0, "Block ID 2020")
wdata10[0].insert(0, "Block ID 2010")

for cross_row in cw2:
    if cross_row[0][0:8] == 'G0600010': 
        for row in d10:
            if cross_row[0] == row[0]:
                weight = float(cross_row[2])
                line_list = [cross_row[0], cross_row[1]]
                for i in range(58, 102):
                    line_list.append(float(row[i]) * weight)
                # Now apply weights to the net changes. If block 2010 exists in the 2010 net changes sheet
                if row[0] in final2010:
                    netdata10 = copy.deepcopy(final2010[row[0]])
                    for n, d in enumerate(netdata10):
                        netdata10[n] = d * weight
                    line_list.append(netdata10) # Last element in weighted data should be a sublist of the net changes
                    wdata10.append(line_list)
                break
'''The goal is to recreate the equivilant of a 2010 data fitted to a 2020 block.
So we shall iterate through the 2020 data, find overlapping 2010 data from the above Crosswalk.
Sum the weighed data up. and then put the weighted summation in a dictionary with its 2010 equal.
Once we're done we can just subtract the weighted representation in the dictionary from the 2010 tracts
these weighted representations are called "targets"

We do the same thing with these net changes. Iterate through the 2020s block labels, find all crosswalk 2010 weighted lines
featuring that 2020 block label. Sum up the net changes for each instance of that line and then put the final product in a dictionary for that
assigned 2020 block
'''
print("Generating 2010 targets for 2020 data")
targetnet0010 = {}
target10to20blks = {}
for row in d20:
    if row[9] == "Alameda County":
        first = True
        for wrow in wdata10:
            if wrow[1] == row[0]:
                # Append name of the 2020 block
                # then summate the fragments of the 2010 weighted data
                # and the 2010 net weighted data (APPLY THIS)
                if first:
                    first = False
                    target10to20blks[row[0]] = wrow[2:46] # 2 - 45 are weighted 2010s data and 46 is a sub list of net changes
                    targetnet0010[row[0]] = wrow[46]
                else:
                    target10to20blks[row[0]] = [float(a) + float(b) for a, b in zip(target10to20blks[row[0]], wrow[2:46])]
                    targetnet0010[row[0]] = [float(a) + float(b) for a, b in zip(targetnet0010[row[0]], wrow[46])]
print("2010 Target Blocks Assembled. Calculating net changes")
'''
At this point, we need to calculate the net differences between 2010 to 2020 between the 2020 blocks and the target 2010 recreations.
For every calculation, we can then add that to the 2020's target 2010 net change blocks to calculate the changes from 2020 to 2000, a span of 20 years
'''
final2020= {}
finalnet2020 = {}
for row in d20:
    if row[0] in target10to20blks and row[0] in targetnet0010:
        target = target10to20blks[row[0]]
        content =[]
        content.append(float(row[59]) - target[0])#Total Pop
        content.append(float(row[61]) - target[2])#White
        content.append(float(row[62]) - target[3])#Black
        content.append(float(row[63]) - target[4])#Native
        content.append(float(row[64]) - target[5])#Asian
        content.append( float(row[65]) - target[6])#Haiwanna
        content.append(float(row[66]) - target[7])#Other
        content.append( float(row[67]) - target[8])#Multi
        content.append(float(row[68]) - target[9])#Hispanic
        content.append( float(row[76]) - target[17]) #Homes
        content.append( float(row[78]) - target[19])#Vacant
        content.append( float(row[92]) - target[29])# Renters
        content.append( float(row[84]) - target[21])# Homeowners
        content.append( float(row[85]) - target[22]) #White Homeowners
        content.append( float(row[86]) - target[23])#Black
        content.append( float(row[87]) - target[24])#Native
        content.append( float(row[88]) - target[25])#Asian
        content.append( float(row[89]) - target[26])#Haiwanna
        content.append( float(row[90]) - target[27])#Other
        content.append( float(row[91]) - target[28])#Multi
        content.append( float(row[80]) - target[40]) #Hispanic Honeowners
        content.append( float(row[93]) - target[30])#White Renters
        content.append( float(row[94]) - target[31])#Black
        content.append( float(row[95]) - target[32])#Native
        content.append( float(row[96]) - target[33])#Asian
        content.append( float(row[97]) - target[34])#Haiwanna
        content.append( float(row[98]) - target[35])#Other
        content.append( float(row[99]) - target[36])#Multi
        content.append( float(row[82]) - target[43])#Hispanic Renter
        final2020[row[0]] = content
        # Summating the net changes now, same as above
        ntarget =  targetnet0010[row[0]]
        if row[17] == "983200":
            print(row[0],float(row[59]) - target[0], " Target", ntarget[0])
        #Note that its in the same alignment as the above content but of the 00 - 10 version so ZIP() will do
        finalnet2020[row[0]] = [float(a) + float(b) for a, b in zip(content, ntarget)]
print("Calculations finished. Making tracts")
''' At this point sum up all census block values like vectors for each census tract '''
tract0020 = tract_maker(finalnet2020) # this should be the final product 
tract1020 = tract_maker(final2020) #this tests if 2010 to 2020 calc were right

print("Writing Back")
# Final Tract data
with open('/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change1020tract.csv', mode='w', newline='') as file0:
    csv_writer = csv.writer(file0)
    for key, value in tract1020.items():
        csv_writer.writerow([key, value])
    file0.close()
with open('/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change0020tract.csv', mode='w', newline='') as file1:
    csv_writer = csv.writer(file1)
    for key, value in tract0020.items():
        csv_writer.writerow([key, value])
    file1.close()
# Final Block data
with open('/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change0020.csv', mode='w', newline='') as file2:
    csv_writer = csv.writer(file2)
    for key, value in finalnet2020.items():
        csv_writer.writerow([key, value])
    file2.close()
with open('/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change1020.csv', mode='w', newline='') as file3:
    csv_writer = csv.writer(file3)
    for key, value in final2020.items():
        csv_writer.writerow([key, value])
    file3.close()

'''
With the net values from 2010 to 2020 calculated via a target 2010 value onto a current 2020 block
, add these differences to the net changes. Probably should do it immediately after the net changes'''
