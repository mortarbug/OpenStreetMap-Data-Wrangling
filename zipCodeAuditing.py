
# coding: utf-8

# In[4]:

import xml.etree.cElementTree as ET
filename = 'seattle_washington.osm'






# AUDIT PHASE 1: FIND UNIQUE ZIP CODES IN THE AREA

# Declare an empty dictionary of zips
zips = {}

# Loop over the file, 
for event, element in ET.iterparse(filename, events = ('start',)):
    try:
        for tag in element.iter('tag'):
            
            #If the tag attribute is a postcode
            if tag.attrib['k'] == 'addr:postcode':
                
                # If the postcode is in the dictionary keys, increment the counter. Otherwise, initialize with a value of 1
                if tag.attrib['v'] in zips:
                    zips[tag.attrib['v']] += 1
                else:
                    zips[tag.attrib['v']] = 1
    #If the try returns an error, skip
    except: 
        pass
        
        
    #Clear the element to save memory        
    element.clear()

print zips







# AUDIT PHASE 2: PRINT OUT ODD ZIP CODES THAT DO NOT CONFORM TO A SEATTLE AREA CODE(AT LEAST 5 NUMBERS, STARTS WITH '98')
#    OR A VICTORIA, BC AREA CODE (6 CHARACTERS, STARTS WITH 'V')

# Declare a list of digits
list_of_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



#Define a helper function that returns an X-format
def X_formatter(number, list_of_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
    
    #Replace every number in the phone number with X
    for num in list_of_digits:
        number = number.replace(num, 'X')
        
    return number



# Iterate over the keys of the dictionary
for postcode in zips.iterkeys():
    
    # Save the original postcode. If any irregularities are detected, print them out. 
    original_post = postcode
    
    #If the postcode starts with V, take out the space, then print if length does not equal 6
    if (postcode[0].upper() == 'V'):
        postcode = postcode.replace(' ', '')
        if len(postcode) != 6:
            print original_post
    else:
        try:
            # Use a while loop to remove characters that aren't numbers
            while postcode[0] not in list_of_digits:
                postcode = postcode[1:]
                
            # If zipcode doesn't start with '98' or the zipcode has a length of less than 5, then print it out
            if (postcode[0] != '9') or (postcode[1] != '8') or (len(postcode.split('-')[0]) < 5) or             ('XXXXX' not in X_formatter (postcode)):
                print original_post
        except: 
            print original_post



# In[ ]:



