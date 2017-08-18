
# coding: utf-8

# In[2]:

#Set filename and import library
filename = 'sample_seattle.osm'
import xml.etree.cElementTree as ET







# Create a dictionary to map the exceptional zip codes
zip_codes_mapping = {'W Lake Sammamish Pkwy NE': '98052', '9322':'98296', '16518': '98271',                    '89370': '98346', '96221': '98221', '186631629:186700775:186700777':'98056',                    '90501': '98501', '99004': '98004', '90874':'98704',                     'Port Angeles': '98362', '97277': '98277', '272': '98321', '981-2': '98122'}

# Create a dictionary of the two IDs where the postcode was listed as 'WA'
WA_element_IDs = {'223469578': '98661', '284564183': '98053'}






# Define the zip code cleaning function
def zip_code_cleaner(zip_code, element_id, zip_codes_mapping = zip_codes_mapping, WA_element_IDs = WA_element_IDs):
    """Takes in a zip code and returns a cleaned zip code"""
    
    # If the zip starts with a V, then uppercase all the letters and remove any spaces (for consistency)
    if zip_code[0].upper() == 'V':
        zip_code = zip_code.upper().replace(' ', '')
        
        #Add a space between the first 3 and last 3 characters
        zip_code = zip_code[:3] + ' ' + zip_code[3:]
    
    # If the zip code does not start with a V
    else:
            
        #If the zip code is in zip_codes_mapping
        if zip_code in zip_codes_mapping:
            zip_code = zip_codes_mapping[zip_code]
            return zip_code
            
        #else if the element_ID is in the element_IDs
        elif element_id in WA_element_IDs:              
            zip_code = WA_element_IDs[element_id]
            return zip_code
                    
        # Remove any leading letters in the zip code
        try:
            while zip_code[0] not in list_of_digits:
                zip_code = zip_code[1:]
        except:
            pass
            
        index = zip_code.find('9')
        zip_code = zip_code[index:index+5]
            
    
    return zip_code


# In[ ]:



