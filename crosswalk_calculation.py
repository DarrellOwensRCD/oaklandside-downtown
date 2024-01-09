'''Program will calculate the differences in data from 2000 to 2010 at the block level.
The data accumulated can be summed up into tracts. The net data from the crosswalks will be saved
into a file so Part 2 of the program can use them and they also can be verified manually in case
of error.
'''
import json
import csv
import statistics
import os.path
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
# Census 2000 data Blocks
f00 = '/Users/darrell/Desktop/oaklandside-downtown/Census2000/nhgis0097_ds147_2000_block.csv'
# Census 2010 data Blocks
f10 = '/Users/darrell/Desktop/oaklandside-downtown/Census2010/nhgis0094_ds172_2010_block.csv'
# 2000 to 2010 Crosswalks
filecw1 = '/Users/darrell/Desktop/oaklandside-downtown/crosswalk/nhgis_blk2000_blk2010_gj_06/nhgis_blk2000_blk2010_gj_06.csv'
with open(filecw1, 'r') as a, open(f00, 'r') as c, open(f10, 'r') as d:
    cw1 = list(csv.reader(a, delimiter=',')) # Crosswalk 2000 - 2010
    d00 = list(csv.reader(c, delimiter=',')) # Census 2000
    d10 = list(csv.reader(d, delimiter=',')) # Census 2010
    a.close()
    c.close()
    d.close()
'''
# STEP 1 : iterate through crosswalk file blocks, find a 2000 block
# , copy and multiply the data of the 2000 blocks (We only care about cells 46 to 78) by the weight for that block
Basically we're reconstructing the Crosswalk List but inserting a vector of the 2000 data thats been weighted
So final product looks like: [Block 2010 , Block 2020, Data0 * Weight, Data1 * Weight . . . ]
'''
print("START")
wdata00 =[d00[0][46:80]]
wdata00[0].insert(0, "Block ID 2010")
wdata00[0].insert(0, "Block ID 2000")
for cross_row in cw1: 
    if cross_row[0][0:8] == 'G0600010': 
        for row in d00:
            if cross_row[0] == row[0]:
                weight = float(cross_row[2])
                line_list = [cross_row[0], cross_row[1]]
                for i in range(46, 80):
                    line_list.append(float(row[i]) * weight)
                wdata00.append(line_list)
                break
# GOAL: I want to Know for A SPECIFIC 2010 BLOCK what are the equvilanet pieces of 1 or more
# 2000 BLOCKS that make it equvilanet to the SPECIFIC 2010 BLOCK
# With 2000 Data Calculated, Create the equivilant 2000 target by Summing
# Up the 2000 weighted data for every instance of the selected 2010 block
'''The goal is to recreate the equivilant of a 2000 data fitted to a 2010 block.
So we shall iterate through the 2010 data (we only want the block label), find overlapping 2000 data from the above Crosswalk.
Sum the weighed data up. and then put the weighted summation in a dictionary with its 2010 equal.
Once we're done we can just subtract the weighted representation in the dictionary from the 2010 tracts
these weighted representations are called "targets"
'''
target00to10blks = {}
for row in d10:
    if row[7] == "Alameda County":
        # Regular Op
        first = True
        for wrow in wdata00:
            if row[0] == wrow[1]:
                # Append name of the 2010 block
                # then summate the fragments of the 2000 weighted data
                if first:
                    first = False
                    target00to10blks[row[0]] = wrow[2:36]
                else:
                    target00to10blks[row[0]] = [float(a) + float(b) for a, b in zip(target00to10blks[row[0]], wrow[2:36])]
print("Target Blocks Assembled")
final2010= {}
for row in d10:
    if row[0] in target00to10blks:
        target = target00to10blks[row[0]]
        content =[]
        content.append(float(row[58]) - target[0])#Total Pop0
        content.append(float(row[60]) - target[1] )#White1
        content.append(float(row[61]) - target[2])#Black2
        content.append(float(row[62]) - target[3])#Native3
        content.append(float(row[63]) - target[4])#Asian4
        content.append( float(row[64]) - target[5])#Haiwanna5
        content.append(float(row[65]) - target[6])#Other6
        content.append( float(row[66]) - target[7])#Multi7
        content.append(float(row[67]) - (target[8] + target[9] + target[10] + target[11] + target[12] + target[13] + target[14]))#Hispanic
        content.append( float(row[75]) - target[15]) #Homes9
        content.append( float(row[77]) - target[17])#Vacant10
        content.append( float(row[87]) - (target[25] + target[26] + target[27] + target[28] + target[29] + target[30] + target[31]))# Renters
        content.append( float(row[79]) - (target[18] + target[19] + target[20] + target[21] + target[22] + target[23] + target[24]))# Homeowners
        content.append( float(row[80]) - target[18]) #White Homeowners13
        content.append( float(row[81]) - target[19])#Black14
        content.append( float(row[82]) - target[20])#Native15
        content.append( float(row[83]) - target[21])#Asian16
        content.append( float(row[84]) - target[22])#Haiwanna17
        content.append( float(row[85]) - target[23])#Other18
        content.append( float(row[86]) - target[24])#Multi19
        content.append( float(row[98]) - target[32]) #Hispanic Honeowners20
        content.append( float(row[88]) - target[25])#White Renters21
        content.append( float(row[89]) - target[26])#Black22
        content.append( float(row[90]) - target[27])#Native23
        content.append( float(row[91]) - target[28])#Asian24
        content.append( float(row[92]) - target[29])#Haiwanna25
        content.append( float(row[93]) - target[30])#Other26
        content.append( float(row[94]) - target[31])#Multi27
        content.append( float(row[101]) - target[33])#Hispanic Renter28
        final2010[row[0]] = content
print("2000 to 2010 done; now  ")
'''
NOW THE ISSUE IS HOW TO TAKE THE NET CHANGES IN BLOCKS 2010 AND ADD ONTO THEM FOR 2020
TAKE THE STANDARD WEIGHED CHANGES BUT APPLY WEIGHTS TO THE STATIC AND CHANGE DATA
THEN WHEN SUBTRACT FROM TARGET BLOCKS, THE NET CHANGES SHOULD BE ADDED (OR SUBTRACTED?) AT THIS STAGE
# STEP 4 : iterate through crosswalk file blockgroups for 2020, find a 2010 block
# , copy and multiply the data of the 2010 blocks
# weight x data
Basically we're reconstructing the Crosswalk List but inserting the 2000 data thats been weighted
So final product looks like: [Block 2010 , Block 2020, Data0 * Weight, Data1 * Weight . . . ]
'''
net0010t = tract_maker(final2010) #Tract version. final2020 is the blocks
with open('/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change0010tract.csv', mode='w', newline='') as file1:
    csv_writer = csv.writer(file1)
    for key, value in net0010t.items():
        csv_writer.writerow([key, value])
    file1.close()
with open('/Users/darrell/Desktop/oaklandside-downtown-project/crosswalk/change0010.csv', mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    for key, value in final2010.items():
        csv_writer.writerow([key, value])
    file.close()

print("END")
