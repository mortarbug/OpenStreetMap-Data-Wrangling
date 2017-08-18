
# coding: utf-8

# In[1]:

# MODIFIED CODE, BASED UPON ORIGINAL CODE FROM UDACITY
# ORIGINAL CODE FOUND IN DATA WRANGLING--LESSON 13--CASE STUDY: OPENSTREETMAP DATA--QUIZ 11
# 

# Import modules from original Udacity Code
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import Schema

#Import modules from cleaning
import phoneNumberCleaning
import streetAuditClean
import zipCodeCleaning

#Declare the name of the osm file
OSM_PATH = "seattle_washington.osm"

#Declare the names of the files to be written out to
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

#Regular expressions used to process values
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#Schema for validation
SCHEMA = Schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# Shape elements function prepares the elements to be written to CSV
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    #Declare dictionaries and lists to hold the elements
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # For a node element, attempt to list every item. Certain nodes will return a keyError, so use try/except block
    #     as described in Data Wrangling Forums
    if element.tag == 'node':
        for item in NODE_FIELDS:
            try:
                node_attribs[item] = element.attrib[item]
            except:
                pass
    
    #For way elements, fill in the attributes of the way element.
    if element.tag == 'way':
        for item in WAY_FIELDS:
            way_attribs[item] = element.attrib[item]
        i = 0
        #Iterate through the child elements of the way, filling in information for the nodes of the way element
        for nd in element.iter('nd'):
            way_nodes_dict = {}
            way_nodes_dict['id'] = element.attrib['id']
            way_nodes_dict['node_id'] = nd.attrib['ref']
            way_nodes_dict['position'] = i
            i+=1
            way_nodes.append(way_nodes_dict)
    
    #For every tag, ignore key values with problem characters. If a colon is present, split on that colon, and use the
    #    first part as the "type" value
    for tag in element.iter("tag"):
        tagK = tag.attrib['k']
        if re.search(PROBLEMCHARS, tagK):
            continue
        elif re.search(LOWER_COLON, tagK):
            k_split = tagK.split(":",1)
            key_val = k_split[1]
            type_val = k_split[0]
        #For tags without problematic characters in the key value, assign the key value to the tag's "k" attribute and the 
        #     value_val to the tag's "v" attribute
        else:
            key_val = tagK
            type_val = default_tag_type
        id_val = element.attrib['id']
        value_val = tag.attrib['v']
        
        # If the tag is an address, call the street cleaning function.
        if key_val == 'addr:street':
            value_val = streetAuditClean.update_name(value_val)
        # If the tag is a phone number, call the phone cleaning function.
        elif key_val == 'phone':
            possib_web = value_val
            value_val = phoneNumberCleaning.phone_format_cleaner(value_val)
            if value_val == 'Change to Website':
                key_val = 'website'
                value_val = possib_web
        #If the tag value is a zip code, call the zip cleaning function (takes 2 values)
        elif key_val == 'postcode':
            value_val = zipCodeCleaning.zip_code_cleaner(value_val, id_val)
        
        
        #For the element, append the id, key, value, and type of every child tag into a dictionary
        dict_tags = {'id': id_val, 'key': key_val, 'value': value_val, 'type': type_val}
        tags.append(dict_tags)
    
    
    
    #For node elements, return a tuple of the node's attributes and tags
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    #For way elements, return attributes, nodes, and tags
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}



# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)


# In[ ]:



