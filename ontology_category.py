#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Maria Stoica
Date Modified: 15 November 2018
Description: This module contains the classes and function definitions for
            creating an "Ontology Categorizer." This "categorizer" takes any
            term, determines its possible senses, and the categorizes senses into
            the different ontological categories. Terms may have multiple categories,
            in which case they may need to be broken down into component
            concepts, as necessary.
"""

import pandas as pd
#import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet


# An ontology category is the building block of the ontology categorizer.
# It consists of
#       - a name: the label of the category
#       - synsets: a list of wordnet synsets that are root nodes to the subtrees that
#                   are considered to be part of the category
#       - verb: a Boolean value, set to true for categorization by pos == Verb
class OntologyCategory:
    """ A class that supports tree root synsets for ontological categories. """
    
    # Constructor
    def __init__(self, name = None, synset_list = None):
        error = 0
        if name is None:
            self.name = 'Anonymous'
        else:
            self.name = name
        self.synsets = set()
        self.verb = False
        self.adj = False
        if self.name == 'process':
            self.verb = True
        if self.name == 'attribute':
            self.adj = True
        if not synset_list is None:
            if isinstance(synset_list, list):
                ssit = synset_list
            elif isinstance(synset_list, dict):
                ssit = synset_list.items()
            else:
                print('Invalid synset: must be list or dict.')
                error = 1
            if error == 0:
                try:
                    for term, index in ssit:
                        for i in index:
                            self.add_synset(term, i)
                except:
                    print('Invalid synset contents.')
    
    # add a synset to the category by term name and WordNet index
    def add_synset(self, term, index):
        self.synsets.add((term, index, wordnet.synsets(term)[index]))
    
    # remove a synset category by term name and WordNet index
    def remove_synset(self, term, index):
        rem = [r for r in self.synsets if (r[0]==term) and (r[1]==index)]
        self.synsets.discard(rem[0])
    
    # print definitions of all synset nodes in the ontology category
    def print_defs(self):
        for name, index, ss in self.synsets:
            print(name, '\t' if len(name)>6 else '\t\t', \
                  ss.definition())
    
    # determine if a given term has hypernymy in this category (is subclass of)
    def is_hypernym_of(self,hypernym_tree):
        def is_verb(term):
            return term.pos()=='v'
        def is_adj(term):
            return (term.pos()=='a') or (term.pos()=='s')
        hyp = []
        for ss in hypernym_tree:
            for name, index, sss in self.synsets:
                if ss == sss:
                    hyp.append(name+'.'+str(index))
            if self.verb:
                if is_verb(ss):
                    hyp.append('verb')
            if self.adj:
                if is_adj(ss):
                    hyp.append('adjective')
        if hyp != []:
            hyp.append(self.name)
        return hyp

class OntologyCategorizer():
    """ A class that supports categorization of terms by OntologyCategory() """
    
    # Constructor
    def __init__(self, name = None, categories = None):
        if name is None:
            self.name = 'Anonymous'
        else:
            self.name = name
        self.categories = []
        if not categories is None and isinstance(categories,list):
            for cat in categories:
                self.add_category(cat)
                
    # add a category 
    def add_category(self, cat):
        self.categories.append(OntologyCategory(cat[0],cat[1]))
        
    # return a category 
    def get_category(self, cat):
        return [c for c in self.categories if c.name==cat][0]
    
    # remove a scategory by name
    def remove_category(self, name):
        rem = [r for r in self.categories if r.name==name]
        self.categories.discard(rem[0])
    
    # categorize a term    
    def categorize_term(self, term, cat = None):
        def det_hypernym(tree):
            elements = []
            for h in tree:
                if isinstance(h, list):
                    elements.extend(det_hypernym(h))
                else:
                    elements.append(h)
            return elements

        hyp = []
        hyp_tree = det_hypernym(term.tree(lambda s:s.hypernyms()))
        if cat is None:
            for cat in self.categories:
                hyp.extend(cat.is_hypernym_of(hyp_tree))
        else:
            hyp.extend(cat.is_hypernym_of(hyp_tree))
        return hyp
    
    def iscat_ss(self, term, category):
        cat = self.get_category(category)
        return self.categorize_term(term, cat)!=[]
    
    # Determine what categories a given terms' word senses belong to in the ontology
    #   oc. Returns a pandas DataFrame object consisting of word senses along with
    #   categories and source synset(s) for each category.       
    def what_is(self, term):
    
        term_cat = pd.DataFrame()
        term_ss = wordnet.synsets(term)
        loc = 0
        for ss in term_ss:
            index = len(term_cat)
            term_cat.loc[index,'term']=term
            term_cat.loc[index,'wordnet_ss_index']=loc
            term_cat.loc[index,'definition']=ss.definition()
            term_cat.loc[index,'pos']=ss.pos()
            hyp = self.categorize_term(ss)            
            for h in hyp:
                term_cat.loc[index,h]='yes'
            loc += 1
        return term_cat.fillna('no')

    # Determine whether the word senses of a term belong to a given category
    def is_cat(self, term, cat, out = 'long'):
    
        term_cat = pd.DataFrame()
        term_ss = wordnet.synsets(term)
        loc = 0
        for ss in term_ss:
            index = len(term_cat)
            term_cat.loc[index,'term']=term
            term_cat.loc[index,'wordnet_ss_index']=loc
            term_cat.loc[index,'definition']=ss.definition()
            term_cat.loc[index,'pos']=ss.pos()
            term_cat.loc[index,cat]= 'yes' if self.iscat_ss(ss,cat) else 'no' 
            loc += 1
        if out == 'long':
            return term_cat
        elif term_cat.empty:
            return False
        else:
            return (term_cat[cat]=='yes').any()
    
# Initialize the Scientific Variabes Ontology categorizer
#       return: object of class OntologyCategorizer
def init_svo():
    process_synsets  = ['process', {'process':[1,5], 'act':[1,5,6], \
                                'action':[0,1,3,4], 'event':[0] } ]
    property_synsets = ['property', {'property':[1,3], 'attribute':[0,1] } ]
    quantity_synsets = ['quantity', {'quantity':[0,2], 'amount':[0,2], \
                                 'ratio':[0], 'quantitative_relation':[0], \
                                 'distance':[0] } ]
    object_synsets   = ['object', {'object':[0,2,3,4], 'system':[1,4,5], \
                               'phenomenon':[0], 'body':[0,3,8], 'matter':[2], \
                               'form':[2,3,5,6], 'biological_group':[0], \
                               'body_of_water':[0], 'part':[2] } ]
    state_synsets = [ 'state', {'condition':[0,1,2], 'state':[1,4]}  ]
    attr_synsets = [ 'attribute', {}  ]

    return OntologyCategorizer('svo',[process_synsets, property_synsets, quantity_synsets,\
                                object_synsets, state_synsets, attr_synsets ])

if __name__ == "__main__":
    import sys
    svo = init_svo()
    if len(sys.argv) == 2:
        whatis = svo.what_is(sys.argv[1])
        print(sys.argv[1]+' has the following categories:')
        found = False
        cols = whatis.columns.values
        for _,row in whatis.iterrows():
            cats = []
            if 'object' in cols and (row['object']=='yes'):
                cats.append('object')
            if 'process' in cols and (row['process']=='yes'):
                cats.append('process')
            if 'property' in cols and (row['property']=='yes'):
                cats.append('property') 
            if 'state' in cols and (row['state']=='yes'):
                cats.append('state')
            if cats != []:
                found = True
                print(row['pos']+'. '+row['definition'])
                print('\t'+', '.join(cats))
        if not found:
            print('\tnone')
    elif len(sys.argv) == 3:
        iscat = svo.is_cat(sys.argv[1],sys.argv[2])
        print('The following definitions of '+sys.argv[1]+' are '+sys.argv[2]+':')
        found = False
        for _, row in iscat.iterrows():
            if row[sys.argv[2]]=='yes':
                print(row['pos']+'. '+row['definition'])
                found = True
        if not found:
            print('\tnone')