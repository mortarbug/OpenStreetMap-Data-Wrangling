
# coding: utf-8

# In[10]:

#Import cElementTree
import xml.etree.cElementTree as ET



#Create a list of numbers and a dict of letters to map:
letter_mapping = {'a':'2','b':'2','c':'2','d':'3','e':'3','f':'3','g':'4',                  'h':'4','i':'4','j':'5','k':'5','l':'5','m':'6','n':'6',                  'o':'6','p':'7','q':'7','r':'7','s':'7','t':'8','u':'8',                  'v':'8','w':'9','x':'9','y':'9','z':'9'}
list_of_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


#Create a dictionary with incorrect phone numbers to be used for mapping
exceptional_pn_mapping = { '+1 310 0001': '6043100001', '+1 425 9888': '425-391-9888',                         '+1-360-428-6615-9402':'3604289402', '206-903-022':'2069030224',                         '+1-425-569-090': '4255569090', '852-9595': '2538529595'}
    




# Define the main cleaning function
def phone_format_cleaner(phone_number, letter_mapping = letter_mapping, list_of_digits = list_of_digits,
                        exceptional_pn_mapping = exceptional_pn_mapping):
    """ Takes in a phone number and returns a cleaned phone number containing only digits"""
    
     #If it's a website, return website
    if  'http' in phone_number:
        return 'Change to Website'
    
    # If the phone number is null, return null
    elif 'NULL' in phone_number:
        return 'NULL'
    
    
    #Define a has_extension bool, to insert an extension into the phone number later
    has_extension = ('x' in phone_number) or ('ext' in phone_number)
    
    #If the phone number has an extension, or if the phone number is one of a few exceptional numbers
    if (has_extension ==1) or ('ECHO' in phone_number) or     (';' in phone_number):   
        #Call the singular exceptions function to handle the phone number
        phone_number = single_exceptions (phone_number)
        
    #If the phone number is in the manual cleaning dictionary   
    elif (phone_number in exceptional_pn_mapping):
        phone_number = exceptional_pn_mapping[phone_number]
        return phone_number
    
    
    
    # Run through the phone number and pull out all the numbers. Use the letter_mapping dictionary to convert
    #   letters to numbers when they show up.
    numeric_string = ''
        
    #Go through the phone number character-by-character. If the character is a number, append it to the numeric_string. 
    for character in phone_number:
        if character in list_of_digits:
            numeric_string = numeric_string + character
        #If it's a letter, convert it first and then append it to numeric_string
        elif character.lower() in letter_mapping:
            numeric_string = numeric_string + letter_mapping[character.lower()]
        #If the character is neither letter or number, ignore it
        else: 
            continue
        
    # While the first number is a zero or 1, remove it
    while numeric_string[0] in ['0', '1']:
        numeric_string = numeric_string [1:]
        
    #If the number has an extension, insert an 'x' after the first 10 digits
    if (has_extension == True):
        numeric_string = numeric_string[:10] + 'x' + numeric_string[10:]
        
    #return the numeric string that was just built up   
    return numeric_string




            

#Create a function to handle extensions and unique numbers
def single_exceptions(phone_number):
    
    # If the number contains an extension, remove the extension, then find and replace the extension
    if ('ext' in phone_number):
        phone_number = phone_number.replace('ext', '')
    elif ('x' in phone_number):
        phone_number = phone_number.replace('x', '')
        
    #If the phone number contains 'ECHO'
    elif ('ECHO' in phone_number):
        phone_number = phone_number.replace('ECHO', '')
        
    #If the phone number contains a semicolon
    elif (';' in phone_number): 
        phone_number = phone_number.split(";")[0] 
    
    return phone_number
    


# In[ ]:



