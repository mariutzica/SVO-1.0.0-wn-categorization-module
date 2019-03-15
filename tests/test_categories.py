#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:36:04 2019

@author: mariutzica
"""
import pandas as pd
import sys
sys.path.append("..")
import ontology_category as oc

#Test categories:

svo = oc.init_svo()
#process
num_correct = 0
num_incorrect = 0
not_found = 0
processes = pd.read_csv('process.csv')
process_labels = processes['process_label'].tolist()
for p in process_labels:
    if not '~' in p and not '_' in p:
        proc = svo.is_cat(p,'process')
        if len(proc)==0:
            not_found += 1
        elif any(proc['process']=='yes'):
            num_correct += 1
        else:
            num_incorrect += 1
        

#phenomenon
num_correct = 0
num_incorrect = 0
not_found = 0
phenomena = pd.read_csv('phenomenon.csv')
phen_labels = phenomena['phenomenon_label'].tolist()
for p in phen_labels:
    if not '~' in p and not '_' in p and not '-' in p:
        proc = svo.is_cat(p,'phenomenon')
        if len(proc)==0:
            not_found += 1
        elif any(proc['phenomenon']=='yes'):
            num_correct += 1
        else:
            num_incorrect += 1    
        
#body
num_correct = 0
num_incorrect = 0
not_found = 0
phenomena = pd.read_csv('inanimate_natural_body.csv')
phen_labels = phenomena['body_label'].tolist()
for p in phen_labels:
    if not '~' in p and not '_' in p and not '-' in p:
        proc = svo.is_cat(p,'phenomenon')
        if len(proc)==0:
            not_found += 1
        elif any(proc['phenomenon']=='yes'):
            num_correct += 1
        else:
            num_incorrect += 1    
            
#property
num_correct = 0
num_incorrect = 0
not_found = 0
properties = pd.read_csv('qualitative_property.csv')
prop_labels = properties['property_label'].tolist()
for p in prop_labels:
    if not '~' in p and not '_' in p and not '-' in p:
        prop = svo.is_cat(p,'property')
        quant = svo.is_cat(p,'quantity')
        if len(prop)==0 and len(quant)==0:
            not_found += 1
        elif any(prop['property']=='yes') or any(quant['quantity']=='yes'):
            num_correct += 1
        else:
            num_incorrect += 1    