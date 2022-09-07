
import json
import pickle
import pandas as pd
import numpy as np 
import logging

outputDictionary = {}

def read_choices():
    """
     Output : Return all the specialties code
    """
    with open('orientationSystem\data_preparatio_object\mytargets.json', 'r') as f:
        my_json_obj = json.load(f)

    return my_json_obj


def read_label_choices():
    """
     Output : return a dectionary with
      key : code spéciality
      name : the name of the spéciality
    """
    with open("orientationSystem\data_preparatio_object\code_label4.json", "r") as f:
        dictionnary  =  json.load(f)

    return dictionnary









