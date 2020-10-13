#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import pickle
import json
import os
import re
# import csv

Data = pickle.load(open('intern_msvs.pkl', 'rb'))
count = 0
def matchValue(input, parsedValues):
    temp = {}
    value = re.sub("[^0-9a-zA-Z]+", "", input)
    if 'yearofbirth' in value:
            split_values = input.split('yearofbirth')
            if len(split_values) > 1 and split_values[1] is not None \
                    and split_values[1] != '':
                    val = split_values[1].replace('o', '0')
                    # print(val)
                    while not val[0].isdigit():
                        val = val[1:]
                    temp['Date of Birth'] = '00-00-' + re.sub("[^0-9]+", "", val)
    elif 'dob' in value:
        # Checking if DOB is present
        # Note: if DOB is written as Date Of Birth, Birth Date etc. we have to analyze input and change conditions accordingly here

        split_values = input.split('dob')
        if len(split_values) > 1 and split_values[1] is not None \
                and split_values[1] != '':
            val = split_values[1].replace('o', '0')
            temp['Date of Birth'] = re.sub('[^0-9]', '-', val)
            while len(temp['Date of Birth'])>0 and not temp['Date of Birth'][0].isdigit():
                temp['Date of Birth'] = temp['Date of Birth'][1:]
    else:
        # Checking for state / pincode
        for state in STATES:
            state_text = state.replace(' ', '').lower()

            # Checking if any state declared is present in text

            if state_text in value:
                # State is present, to get pin code. making regex groups
                v = value.replace('o', '0')
                regex = r"([a-zA-Z ,\.-]+)([0-9]{6})"
                if 'State Name' in parsedValues:
                    regex = r"([0-9]{6})"
                x = re.match(regex, v, re.I)
                # we need not to parse state from text since we exactly know which state it matched to

                temp['State Name'] = state
                # Checking if state and pin are present. To avoid cases where name/address or other component itself contains state
                if x:
                    # identifying groups, first will contain city/state etc. another will be pin code number

                    items = x.groups()
                    if len(items) > 1:
                        temp['Postal Code'] = items[1]
                    else:
                        temp['Postal Code'] = items[0]
    return temp

# state and union territories of india

def merge_results(val1, val2, val3):
    temp = {}
    if 'State Name' in val1:
        temp['State Name']= val1['State Name']
    elif 'State Name' in val2:
        temp['State Name']= val2['State Name']
    elif 'State Name' in val3:
        temp['State Name']= val3['State Name']

    if 'Postal Code' in val1:
        temp['Postal Code']= val1['Postal Code']
    elif 'Postal Code' in val2:
        temp['Postal Code']= val2['Postal Code']
    elif 'Postal Code' in val3:
        temp['Postal Code']= val3['Postal Code']


    if 'Date of Birth' in val1:
        temp['Date of Birth']= val1['Date of Birth']
    elif 'Date of Birth' in val2:
        temp['Date of Birth']= val2['Date of Birth']
    elif 'Date of Birth' in val3:
        temp['Date of Birth']= val3['Date of Birth']
    return temp

STATES = [
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chhattisgarh',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jammu and Kashmir',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal',
    'Andaman and Nicobar Islands',
    'Chandigarh',
    'Dadra and Nagar Haveli',
    'Daman and Diu',
    'National Capital Territory of Delhi',
    'Lakshadweep',
    'Pondicherry',
    'Delhi',
    'New Delhi',
]

# variable to hold all final results
# Note: Currently Aadhar number is not added in the response as per requirement, so we might get confused in which dob, pin and state is for whom.

FINAL_VALUES = []

# Traversing loaded data row by row

for row in Data:
    # Traversing each parsed value of person
    temp = {}
    for row_val in row:
        value = row_val.replace(' ', '').lower()
        result_set1 = matchValue(value, temp)
        value = value.replace('0', 'o')
        result_set2 = matchValue(value, temp)
        temp = merge_results(result_set1, result_set2, temp)

    # added empty values to add in csv correctly
    # if 'Date of Birth' not in temp:
    #     temp['Date of Birth'] = ''
    
    # if 'State Name' not in temp:
    #     temp['State Name'] = ''

    # if 'Postal Code' not in temp:
    #     temp['Postal Code'] = ''
    
    FINAL_VALUES.append(temp)

# data = open('test.csv', 'w', newline='')
# csvwriter = csv.writer(data)

# count = 0

# for val in FINAL_VALUES:
#       if count == 0:
#              header = val.keys()
#              csvwriter.writerow(header)
#              count += 1
#       csvwriter.writerow(val.values())
# data.close()

# pretty print final response
print(json.dumps(FINAL_VALUES, indent=4, sort_keys=True))

