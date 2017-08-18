
# coding: utf-8

# In[ ]:

#Define a list of all the numbers
list_of_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


#Define a helper function that takes an input string, then converts all numbers to 'X'
# Allows me to  audit phone numbers by looking at all the phone numbers in a format i.e. (XXX) XXX-XXXX

def X_formatter(number, list_of_digits):
    
    #Replace every number in the phone number with X
    for num in list_of_digits:
        number = number.replace(num, 'X')
        
    return number










# Create dictionary of phone formats
phone_number_formats = {}

#Use a for loop to iterate over the dataset, putting standardized formats into a dictionary
for event, element in ET.iterparse(filename, events = ('start',)):
    if (element.tag == 'node'):
    
        #Loop through the node tags. If it finds a phone number, call the X_formatter and area_coder functions  
        for tag in element.iter('tag'):
            try:
                #If the key value is a tag, put its value into the X_formatter function
                if (tag.attrib['k'] == 'phone'):
                    phone_num = X_formatter(tag.attrib['v'])
                    
                    # If phone number format is already in the dictionary. Otherwise, 
                    # add it to the dictionary keys with a value of 1
                    if phone_num in phone_number_formats:
                        phone_number_formats[phone_num] += 1
                    else:
                        phone_number_formats[phone_num] = 1
                        
            
            # If the try block returns an error
            except:
                pass
                    
    # Clear the element to save memory
    element.clear()
    

# Print out the dictionary of phone numbers
print phone_number_formats




