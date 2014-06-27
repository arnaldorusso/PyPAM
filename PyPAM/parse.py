#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
import sys

def tryconvert(x):
    '''
    Convert if possible an string to float.
    Parameter
    ---------
    x : value
    '''
    try:
        y = np.float64(x)
        return y
    except:
        if x == '----':
            return np.nan
        else:
            return x


def csv_extract(arq):
    '''
    Parse a csv processed file by PhytoWIN.
    PhytoWIN is a software from WALZ ind., to proccess PhytoPAM data.
    http://www.walz.com/products/chl_p700/phyto-pam/phytowin.html
    
    Parameters
    ----------
    arq: str
        opened csv file
    
    Returns
    -------
    curves : arr
        Store the "Rapid Light Curves"
    pulses : arr
        Saturated light pulses
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
        elif re.match(pre_dados,line):
            if line.split(',')[2] == str(1):
                #print line
                if new_dict:
                    dicts.append(new_dict)
                new_dict = {}
                for k in keys:
                    new_dict[k] = []
            line = re.sub('""', str(np.nan),line)
            data = line.split(',')
            data = [tryconvert(i) for i in data]
            values = zip(keys, data)
            for k, v in values:
                new_dict[k].append(v)
    dicts.append(new_dict)

    # FIXME Insert some functionalities to exclude
    #       duplicate measures
    curves = [l for l in dicts if len(l['No.']) >= 16]


    pulses = []
    for k in dicts:
        if k['No.']:
            if len(k['No.']) < 16:
                if len(k['No.']) <= 7:
                    pulses.append(k)

    return curves, pulses

#extract(sys.argv[1])


def raw_extract(arq):
    '''
    Parse raw data obtained with Phyto-Pam.
    This raw data is an .rpt file containing
    values of curves records, and other useful
    informations.    
    
    Parameters
    ----------
    arq: str
        opened csv file
    
    Returns
    -------
    curves : arr
        Store the "Rapid Light Curves".
    pulses : arr
        Saturated light pulses.
    '''

    f = open(arq,'r')
    t = f.readlines()
    f.close()

    infos = re.compile("[0-9]{2}[A-Z]{3}[0-9]{4}")
    gain = re.compile("[A-Z]{4}", flags=re.I) #flag for case Insensitive
    comments = re.compile("^%")
    comments2 = re.compile(";")
    header = re.compile("No   Time")
    dados = re.compile("[0-9]{1,2}\s*[0-9]{2}")
    first = re.compile("[1]{1}\s")
    dicts = []
    new_dict = {'comments':[], 'gain':[], 'info':[]}
    keys = []
    for line in t:

        line = line[:-1].strip()

        if not line:
            pass

        if re.match(comments,line):
            new_dict['comments'].append(line)

        if re.match(comments2,line):
            new_dict['comments'].append(line)

        if re.match(gain,line):
            new_dict['gain'].append(line)

        if re.match(header,line):
            keys = line.split() 

        if re.match(infos,line):
            new_dict['info'].append(line)

        elif re.match(dados,line):
            if re.match(first,line):
                old_dict = new_dict                
                new_dict = {'comments':[], 'gain':[], 'info':[]}
                for k in keys:
                    new_dict[k] = []
                dicts.append(old_dict)
            
            line = re.sub('""', str(np.nan),line)
            data = line.split()
            data = [tryconvert(i) for i in data]
            values = zip(keys, data)
            for k,v in values:
                new_dict[k].append(v)

    dicts.append(new_dict)
    
    # inserting comments for relative empty keys    
    comment = ''
    for d in dicts:
        if d['comments']:
            comment = d['comments']
        else:
            d['comments'] = comment
        
    ## FIXME Insert some functionalities to exclude
    ##       duplicate measures
    curves = [l for l in dicts[1:] if len(l['No']) >= 16]

    pulses = []
    for k in dicts[1:]:
        if k['No']:
            if len(k['No']) < 16:
                if len(k['No']) <= 7:
                    pulses.append(k)
    
    return curves, pulses

