# Quick Calculations of Homeowners and 2020 data
import json
def div(a,b):
    if b == 0:
        return "This Group Was 0 in 2000"
    else:
        return round((a / b) * 100, 1)
fn2 = '/Users/darrell/Desktop/oaklandside-downtown/dwtnoak20_00.geojson'
oak_tracts = json.load(open(fn2))
print("START")
for ot in oak_tracts['features']:
    ot['properties']["0_netper"] = div(ot['properties']["0"] , (ot['properties']["Population"] - ot['properties']["0"]))#Total Pop
    ot['properties']["1_netper"] = div(ot['properties']["1"] , (ot['properties']["White"] - ot['properties']["1"]))#White
    ot['properties']["2_netper"] = div(ot['properties']["2"] , (ot['properties']["Black"] - ot['properties']["2"]))#Black
    ot['properties']["3_netper"] = div(ot['properties']["3"] , (ot['properties']["Native American"] - ot['properties']["3"]))#Native
    ot['properties']["4_netper"] = div(ot['properties']["4"] , (ot['properties']["Asian"] - ot['properties']["4"]))#Asian
    ot['properties']["5_netper"] = div(ot['properties']["5"] , (ot['properties']["Pacific Islander"] - ot['properties']["5"]))#Haiwanna
    ot['properties']["6_netper"] = div(ot['properties']["6"] , (ot['properties']["Other"] - ot['properties']["6"]))#Other
    ot['properties']["7_netper"] = div(ot['properties']["7"] , (ot['properties']["Multi-Race"] - ot['properties']["7"]))#Multi

    ot['properties']["8_netper"] = div(ot['properties']["8"] , (ot['properties']["Latino"] - ot['properties']["8"]))#Hispanic
    ot['properties']["9_netper"] = div(ot['properties']["9"] , (ot['properties']["Homes"] - ot['properties']["9"]))#Homes
    ot['properties']["10_netper"] = div(ot['properties']["10"] , (ot['properties']["Vacant"]- ot['properties']["10"]))#Vacant
    ot['properties']["11_netper"] = div(ot['properties']["11"] , (ot['properties']["Renters"]- ot['properties']["11"]))# Renters
    ot['properties']["12_netper"] = div(ot['properties']["12"] , (ot['properties']["Homeowners"]- ot['properties']["12"]))# Homeowners
    ot['properties']["13_netper"] = div(ot['properties']["13"] , (ot['properties']["WhiteHomeowners"] - ot['properties']["13"]))#White Homeowners
    ot['properties']["14_netper"] = div(ot['properties']["14"] , (ot['properties']["BlackHomeowners"]- ot['properties']["14"]))#Black
    ot['properties']["15_netper"] = div(ot['properties']["15"] , (ot['properties']["Native AmericanHomeowners"]- ot['properties']["15"]))#Native
    ot['properties']["16_netper"] = div(ot['properties']["16"] , (ot['properties']["AsianHomeowners"]- ot['properties']["16"]))#Asian
    ot['properties']["17_netper"] = div(ot['properties']["17"] , (ot['properties']["Pacific IslanderHomeowners"]- ot['properties']["17"]))#Haiwanna
    ot['properties']["18_netper"] = div(ot['properties']["18"] , (ot['properties']["OtherHomeowners"]- ot['properties']["18"]))#Other
    ot['properties']["19_netper"] = div(ot['properties']["19"] , (ot['properties']["Multi-RaceHomeowners"]- ot['properties']["19"]))#Multi
    ot['properties']["20_netper"] = div(ot['properties']["20"] , (ot['properties']["LatinoHomeowners"] - ot['properties']["20"]))#Hispanic Honeowners
    ot['properties']["21_netper"] = div(ot['properties']["21"] , (ot['properties']["WhiteRenters"]- ot['properties']["21"]))#White Renters
    ot['properties']["22_netper"] = div(ot['properties']["22"] , (ot['properties']["BlackRenters"]- ot['properties']["22"]))#Black
    ot['properties']["23_netper"] = div(ot['properties']["23"] , (ot['properties']["Native AmericanRenters"]- ot['properties']["23"]))#Native
    ot['properties']["24_netper"] = div(ot['properties']["24"] , (ot['properties']["AsianRenters"]- ot['properties']["24"]))#Asian
    ot['properties']["25_netper"] = div(ot['properties']["25"] , (ot['properties']["Pacific IslanderRenters"]- ot['properties']["25"]))#Haiwanna
    ot['properties']["26_netper"] = div(ot['properties']["26"] , (ot['properties']["OtherRenters"]- ot['properties']["26"]))#Other
    ot['properties']["27_netper"] = div(ot['properties']["27"] , (ot['properties']["Multi-RaceRenters"]- ot['properties']["27"]))#Multi
    ot['properties']["28_netper"] = div(ot['properties']["28"] , (ot['properties']["LatinoRenters"]- ot['properties']["28"]))#Hispanic Renter
with open(fn2, 'w') as a:
    json.dump(oak_tracts, a)
    a.close()
print("DONE")
