#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
import sys


def extract(arq):
    '''
    Parse a csv processed file by PhytoWIN.
    PhytoWIN is a software by WALZ, to proccess PhytoPAM data.
    
    Parameters
    ----------
    arq: opened csv file
    
    Returns
    -------
    curves : Store the "Rapid Light Curves"
    pulses : Saturated light pulses
    '''
    #f = open(sys.argv[1],'r')
    f = open(arq,'r')
    t = f.readlines()
    f.close()

    pre_dados = re.compile("[0-9]{2}[A-Z]{3}[0-9]{4}")
    header = t[0].split(',')
    dicts = []
    new_dict = {}
    keys = []
    for line in t:
        line = line[:-1].strip()
        if not line:
            pass
        if "Date,Time,No.," in line:
            keys = line.split(',')
            for k in keys:
                new_dict[k] = []
        elif re.match(pre_dados,line): #
            if line.split(',')[2] == str(1):
                #print line
                if new_dict:
                    dicts.append(new_dict)
                new_dict = {}
                for k in keys:
                    new_dict[k] = []
            data = line.split(',')
            values = zip(keys, data)
            for k, v in values:
                new_dict[k].append(v)
    dicts.append(new_dict)

    # FIXME Insert some functionalities to exclude
    #       duplicate measures
    curves = [l for l in dicts if len(l['No.']) >= 19]
    del curves[16] #retira a medida duplicada do arquivo

    pulses = []
    for k in dicts:
        if k['No.']:
            if len(k['No.']) < 19:
                if len(k['No.']) <= 3:
                    pulses.append(k)
    del pulses[16] # retira medida duplicada do arquivo.

    return curves, pulses

#extract(sys.argv[1])
