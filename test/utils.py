# coding: utf-8

import os


def read_xml(file_name, template_path):
    '''
    read a xml file
    and return a xml string
    '''
    with open(os.sep.join([template_path, file_name])) as xml:
        xml_string = xml.read()
        xml_string = xml_string.replace("\n", '').replace("  ", "")
    return xml_string
