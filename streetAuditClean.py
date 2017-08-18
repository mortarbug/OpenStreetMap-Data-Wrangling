
# coding: utf-8

# In[30]:

# MODIFIED CODE:
# ADAPTED FROM ORIGINAL CODE FOUND AT UDACITY'S "DATA ANALYST NANODEGREE"
#    FOUND IN "DATA WRANGLING, LESSON 9: PREPARATION FOR THE DATA WRANGLING PROJECT


# Import libraries
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#Set the filename
filename = 'seattle_washington.osm'

# Regex statement that searches at the end of a string
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# List of streets/locations that are fine and expected
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "North", "South", "East", "West", "Northeast", "Northwest",
           "Southeast", "Southwest", "Highway","Way","Point","Suite","Circle","Terrace","Crescent",
            "Close","Row","Glen","Heights","Green","Woods","Rise","Ridge","Alley","Gate","Run",
            "Center","Gardens","Division","Loop","Meridian","Broadway","Mall","Grove","Bend","Chase",
            "Hills","Estates","Vista","Plaza","View","Esplanade", "Reach","Station","Dell","Cove",
            "Spur","Wood","Meadows","Speedway","Landing","Walk","Plateau", "Acres"]

# Dictionary that corrects words to their mapping.
mapping = { "St": "Street", "ST": "Street", "St.": "Street", "st": "Street", "Steet": "Street",
            "Ave": "Avenue", "Ave.": "Avenue", "Av.": "Avenue",
            "Rd.": "Road",  
            "Blvd": "Boulevard", "Blvd.": "Boulevard", 
            "Dr": "Drive", "Dr.": "Drive",
            "Ct": "Court", "Ct.": "Court", "CT": "Court",
           "Pl": "Place", "Pl." : "Place", "PL": "Place",
            "Sq": "Square", "Sq.": "Square",
            "Ln.": "Lane", "Ln" : "Lane",
            "Rd.": "Road", "Rd": "Road", "RD": "Road",
            "Pkwy.": "Parkway", "Pkwy": "Parkway",
           "N": "North", "N.": "North", "E": "East",
           "W": "West", "W.": "West",
           "S": "South", "S.": "South",
           "NE": "Northeast", "N.E.":"Northeast", 
           "NW": "Northwest",
           "SW": "Southwest", "SW,": "Southwest",
           "SE": "Southeast", "S.e.": "Southeast",
           "Hwy": "Highway",
           "Wy": "Way", "WY":"Way", "Wy.": "Way"
           
            }


# In[27]:


#Define a helper function to find out if a string is a number
def is_number(possible_number):
    try:
        #If number, return True
        float(possible_number)
        return True
    #Otherwise, in the event of an error, return false.
    except:
        return False
    
#Define a function to capitalize the first word of the street_type.  There were many cases
#      where the street_type would have been in "expected" if capitalization had been enforced.
def propcase(street_type):
    try:
        if len(street_type) ==2:
            return street_type.upper()
        else:
            return street_type[0].upper() + street_type[1:].lower()
    except:
        return street_type
    

# If the street type is not a recognized street type, print it out to update the mapping table. 
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        
        # Try to convert the street_type into a propcase (so that 'street' looks like "Street"). Save in a new variable
        street_type_prop = propcase(street_type)
        
        # If street type and its propcase are not in the expected list and street type is not a number, 
        #      print out the street name and add into a dictionary
        if (street_type_prop not in expected) and (street_type not in mapping.keys()) and        (not is_number (street_type)) and (street_type_prop not in mapping.keys()) and        (len(street_type) != 1):
            
            #Add to the dictionary and print it out
            street_types[street_type].add(street_name)
            print street_name, "     Street_type:", street_type

#Checks to see if the element is a street
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#Main function
def audit(osmfile):
    
    #Open the osm file and sets a defaultdict
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    #for the elements in the file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        #Check if the element is a node or a way. If it is, iterate through and check if each tag is a street.
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                
                #If the tag is a street, call the audit street types function. 
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        elem.clear()
    osm_file.close()
    return street_types

# When called, update name attempts to put the street name correctly. 
def update_name(name, mapping):
    """Takes in a street address and mapping, returns a cleaned street address"""
    name_elements = name.split(" ")
    street_type = name_elements[len(name_elements) - 1]
    street_type_prop = propcase(street_type)
    
    if (street_type in mapping):
        name = name.replace(street_type, mapping[street_type])
    elif(street_type_prop in mapping):
        name = name.replace(street_type, mapping[street_type_prop])
    
        
    
    
    print name
    return name



# In[ ]:



