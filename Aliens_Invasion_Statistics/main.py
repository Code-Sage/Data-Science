import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import html
import numpy as np


def index(toSearch, toFind):
    i = -1
    try:
        i = toSearch.index(toFind)
    except:
        i = i
    return i


def invert_map(map):
    #  [1]
    inv_map = {v: k for k, v in map.items()}
    return inv_map


reader = csv.reader(open('ufo_sighting_data.csv'))
listData = []
for row in reader:
    if '-' in row[8]:
        splitRes = row[8].strip().split('-')
        year = splitRes[2].strip()
        yearInt = int(year)
        if yearInt > 17:
            yearInt = yearInt + 1900
        else:
            yearInt = yearInt + 2000
        year = str(yearInt)
        row[8] = splitRes[0].strip() + '/' + splitRes[1].strip() + '/' + year
    listData.append([html.unescape(row[1].strip()), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(), row[8].strip(), row[9].strip(), row[10].strip()])
    #   [city, state, country, UFO_Shape, length_of_encounter_seconds,
writer = csv.writer(open('v0_deleted_extraneous_columns_and_date_format_fixed.csv', "w"), lineterminator='\n')
troubledRows = []
for row in listData:
    try:
        writer.writerow(row)
    except:
        troubledRows.append(row)
for row in troubledRows:
    listData.remove(row)

state_country_links = {}
for row in listData[1:]:
    try:
        if(row[1] != '' and row[2] != '' and row[2] not in state_country_links[row[1]]):
            state_country_links[row[1]].append(row[2])
    except:
        state_country_links[row[1]] = [row[2]]


for row in listData[1:]:
    if(row[2] == '' and row[1] != '' and len(state_country_links[row[1]]) == 1):
        row[2] = state_country_links[row[1]][0]
writer = csv.writer(open('v1_inserted_countries_using_state-links.csv', "w"), lineterminator='\n')
writer.writerows(listData)

countries = []
for row in listData[1:]:
    if(row[2] == 'gb'):
        row[2] = 'uk'
    if(row[2] != '' and row[2] not in countries):
        countries.append(row[2])
writer = csv.writer(open('v2_replaced_gb_with_uk.csv', "w"), lineterminator='\n')
writer.writerows(listData)

for row in listData[1:]:
    for country in countries:
        i = index(row[0], '(' + country + '/')
        if(i != -1):
            j = i + 1
            try:
                while(row[0][j] != ')'):
                    j = j + 1
            except:
                j = j
            country_state = (str(row[0])[i:j]).strip()
            country_state = country_state.split('/')
            country = country_state[0].strip()
            state = country_state[1].strip()
            if(row[1].strip() == ''):
                row[1] = state.strip()
            if(row[2].strip() == ''):
                row[2] = (country.split('(')[1]).strip()
            row[0] = (str(row[0])[0:i]).strip()
            break
writer = csv.writer(open('v3_inserted_country_state_from_city_column.csv', "w"), lineterminator='\n')
writer.writerows(listData)


for row in listData[1:]:
    state = row[1].strip()
    if('wales' in state):
        if(state == 's.wales'):
            row[1] = 'south wales'
        elif (state == 'wales, north country'):
            row[1] = 'north wales'
        else:
            row[1] = 'wales'
    elif(state == 'n. ireland'):
        row[1] = 'northern ireland'
    elif (state.startswith('england') or state == 'englnd' or state == 'endland' or state == 'london' or state == 'birmingham'):
        row[1] = 'england'
writer = csv.writer(open('v4_states_from_city_column_corrected.csv', "w"), lineterminator='\n')
writer.writerows(listData)


country_code_file = open('countrycode.org.csv')
reader = csv.reader(country_code_file)
country_codes = {}
for row in reader:
    country_codes[row[0].strip()] = row[1].strip().lower()
for row in listData[1:]:
    if row[2] == '' and row[0][-1] == ')':
        i = j = len(row[0]) - 1
        while i >= 0 and row[0][i] != '(':
            i = i - 1
        probable_country = row[0][i+1:j]
        for country in country_codes.keys():
            if country.lower() == probable_country:
                row[0] = row[0][0:i].strip()
                row[2] = country_codes[country].lower()
writer = csv.writer(open('v5_inserted_more_countries_from_city_column.csv', "w"), lineterminator='\n')
writer.writerows(listData)


for row in listData[1:]:
    if row[2] == '' and row[0][-1] == ')':
        i = j = len(row[0]) - 1
        while i >= 0 and row[0][i] != '(':
            i = i - 1
        splitRes = row[0][i+1:j].split()
        found = False
        for country in country_codes.keys():
            for res in splitRes:
                if country.lower().strip() == res.lower().strip():
                    found = True
                    row[2] = country_codes[country].lower().strip()
                    toAppend = ''
                    if len(splitRes) > 1:
                        for temp in splitRes:
                            if temp != res:
                                toAppend = toAppend + ' ' + temp
                    row[0] = row[0][0:i]
                    if toAppend != '':
                        if i < 0:
                            row[0] = row[0] + toAppend + ')'
                        else:
                            row[0] = row[0] + '(' + toAppend + ')'
                    break
            if found:
                break
writer = csv.writer(open('v6_inserted_countries_from_city_column_using_whitespace_split.csv', "w"), lineterminator='\n')
writer.writerows(listData)


toRemove = []
for row in listData[1:]:
    if row[2] == '':
        toRemove.append(row)
for row in toRemove:
    listData.remove(row)
writer = csv.writer(open('v7_removed_rows_with_missing_countries.csv', "w"), lineterminator='\n')
writer.writerows(listData)


for row in listData[1:]:
    if row[2] == 'uk':
        row[2] = 'gb'
writer = csv.writer(open('v8_set_uk_country_code_according_to_standards.csv', "w"), lineterminator='\n')
writer.writerows(listData)


for row in listData[1:]:
    if 'wales' in row[1]:
        row[1] = 'wales'
    if 'ireland' in row[1]:
        row[1] = ''
writer = csv.writer(open('v9_state_column_fixed_for_uk.csv', "w"), lineterminator='\n')
writer.writerows(listData)


state_codes = {}
state_codes_file = open('loc172csv/2017-2 SubdivisionCodes.csv')
reader = csv.reader(state_codes_file)
for row in reader:
    try:
        if row[1].lower() not in state_codes[row[0].lower()].keys():
            state_codes[row[0].lower()][row[1].lower()] = row[2]
    except:
        state_codes[row[0].lower()] = {row[1].lower():row[2]}
country_codes = invert_map(country_codes)
for row in listData[1:]:
    if row[1] != '':
        try:
            country_states = state_codes[row[2]]
            state = country_states[row[1]]
            row[1] = state
        except:
            row[1] = row[1]
    row[2] = country_codes[row[2]]
writer = csv.writer(open('v10_country_and_state_codes_replaced_with_names.csv', "w"), lineterminator='\n')
writer.writerows(listData)


# reader = csv.reader(open('v10_country_and_state_codes_replaced_with_names.csv'))
# listData = []
# for row in reader:
#     listData.append(row)

listData[0].append('abs_latitude')
for row in listData[1:]:
    row.append(abs(float(row[6])))


reader = csv.reader(open('visualization_params.csv'))
vis_cities = []
vis_states = []
vis_countries = []
vis_shapes = []
for row in reader:
    if row[0] != '' and row[0] not in vis_cities:
        vis_cities.append(row[0])
    if row[1] != '' and row[1] not in vis_states:
        vis_states.append(row[1])
    if row[2] != '' and row[2] not in vis_countries:
        vis_countries.append(row[2])
    if row[3] != '' and row[3] not in vis_shapes:
        vis_shapes.append(row[3])





# unique_cities = []
# unique_states = []
# unique_countries = []
# unique_shapes = []
# for row in listData[1:]:
#     if(row[0].strip() not in unique_cities):
#         unique_cities.append(row[0])
#     if(type(row[1]) == str and row[1].strip() not in unique_states):
#         unique_states.append(row[1])
#     if(type(row[2]) == str and row[2].strip() not in unique_countries):
#         unique_countries.append(row[2])
#     if(type(row[3]) == str and row[3].strip() not in unique_shapes):
#         unique_shapes.append(row[3].strip())
# writer = csv.writer(open('uniques.csv', "w"), lineterminator='\n')
# writer.writerow(['city', 'state/province', 'country', 'UFO_shape'])
# for i in range(0, len(unique_cities)):
#     toAdd = [unique_cities[i]]
#     try:
#         toAdd.append(unique_states[i])
#     except:
#         toAdd = toAdd
#     try:
#         toAdd.append(unique_countries[i])
#     except:
#         toAdd = toAdd
#     try:
#         toAdd.append(unique_shapes[i])
#     except:
#         toAdd = toAdd
#     writer.writerow(toAdd)
a = 0

listData_DataFrame = listData.copy()
for row in listData_DataFrame[1:]:
    for i in range(0, len(listData_DataFrame[0])):
        if row[i] == '':
            row[i] = np.nan
        if i == 4 or i == 6 or i == 7:
            row[i] = float(row[i])
dict_for_DataFrame = {}
columnNames = listData_DataFrame[0]
for columnName in columnNames:
    dict_for_DataFrame[columnName] = []
for row in listData_DataFrame[1:]:
    i = 0
    for rowItem in row:
        dict_for_DataFrame[columnNames[i]].append(rowItem)
        i = i + 1
Data = pd.DataFrame(dict_for_DataFrame)
Data.plot(x='abs_latitude', y='length_of_encounter_seconds', style='o')
Data.plot(x='longitude', y='length_of_encounter_seconds', style='o')


listData_DataFrame = listData.copy()
toRemove = []
for row in listData_DataFrame[1:]:
    if row[3] not in vis_shapes:
        toRemove.append(row)
for row in toRemove:
    listData_DataFrame.remove(row)
for row in listData_DataFrame[1:]:
    for i in range(0, len(listData_DataFrame[0])):
        if row[i] == '':
            row[i] = np.nan
        if i == 4 or i == 6 or i == 7:
            row[i] = float(row[i])
dict_for_DataFrame = {}
columnNames = listData_DataFrame[0]
for columnName in columnNames:
    dict_for_DataFrame[columnName] = []
for row in listData_DataFrame[1:]:
    i = 0
    for rowItem in row:
        dict_for_DataFrame[columnNames[i]].append(rowItem)
        i = i + 1
Data = pd.DataFrame(dict_for_DataFrame)
bp = Data.boxplot(by='UFO_shape', column=['length_of_encounter_seconds'], grid = False, showfliers = False)
bp = Data.boxplot(by='UFO_shape', column=['abs_latitude'], grid = False, showfliers = False)
bp = Data.boxplot(by='UFO_shape', column=['longitude'], grid = False, showfliers = False)


listData_DataFrame = listData.copy()
toRemove = []
for row in listData_DataFrame[1:]:
    if row[2] not in vis_countries:
        toRemove.append(row)
for row in toRemove:
    listData_DataFrame.remove(row)
for row in listData_DataFrame[1:]:
    for i in range(0, len(listData_DataFrame[0])):
        if row[i] == '':
            row[i] = np.nan
        if i == 4 or i == 6 or i == 7:
            row[i] = float(row[i])
dict_for_DataFrame = {}
columnNames = listData_DataFrame[0]
for columnName in columnNames:
    dict_for_DataFrame[columnName] = []
for row in listData_DataFrame[1:]:
    i = 0
    for rowItem in row:
        dict_for_DataFrame[columnNames[i]].append(rowItem)
        i = i + 1
Data = pd.DataFrame(dict_for_DataFrame)
bp = Data.boxplot(by='country', column=['length_of_encounter_seconds'], grid = False, showfliers = False)


listData_DataFrame = listData.copy()
toRemove = []
for row in listData_DataFrame[1:]:
    if row[1] not in vis_states:
        toRemove.append(row)
for row in toRemove:
    listData_DataFrame.remove(row)
for row in listData_DataFrame[1:]:
    for i in range(0, len(listData_DataFrame[0])):
        if row[i] == '':
            row[i] = np.nan
        if i == 4 or i == 6 or i == 7:
            row[i] = float(row[i])
dict_for_DataFrame = {}
columnNames = listData_DataFrame[0]
for columnName in columnNames:
    dict_for_DataFrame[columnName] = []
for row in listData_DataFrame[1:]:
    i = 0
    for rowItem in row:
        dict_for_DataFrame[columnNames[i]].append(rowItem)
        i = i + 1
Data = pd.DataFrame(dict_for_DataFrame)
bp = Data.boxplot(by='state/province', column=['length_of_encounter_seconds'], grid = False, showfliers = False)


listData_DataFrame = listData.copy()
toRemove = []
for row in listData_DataFrame[1:]:
    if row[0] not in vis_cities:
        toRemove.append(row)
for row in toRemove:
    listData_DataFrame.remove(row)
for row in listData_DataFrame[1:]:
    for i in range(0, len(listData_DataFrame[0])):
        if row[i] == '':
            row[i] = np.nan
        if i == 4 or i == 6 or i == 7:
            row[i] = float(row[i])
dict_for_DataFrame = {}
columnNames = listData_DataFrame[0]
for columnName in columnNames:
    dict_for_DataFrame[columnName] = []
for row in listData_DataFrame[1:]:
    i = 0
    for rowItem in row:
        dict_for_DataFrame[columnNames[i]].append(rowItem)
        i = i + 1
Data = pd.DataFrame(dict_for_DataFrame)
bp = Data.boxplot(by='city', column=['length_of_encounter_seconds'], grid = False, showfliers = False)

plt.show()
a = 0


#  [1]  https://stackoverflow.com/questions/483666/python-reverse-invert-a-mapping?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa