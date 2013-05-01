#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
from os import chdir path 
import csv

from pypam.parse import extract
from pypam.visuals import etr_plot, yield_plot

def main(dirs):
    """
    Input the directory of .csv files to be parsed and analysed.

    """
    chdir(path.abspath(dirs))
    for name in glob.glob('*.csv'):
        arq_name = "".join(name.split('.')[0:-1])
        newdir = os.path.join('fig', arq_name)
        try:
            os.makedirs(newdir)
        except OSError:
            print ('Directory already exists: %s' % newdir)
        else:
            print ('%s directory created.' % newdir)
        
        curves, pulses = extract(name) # curves, pulses
        etr_plot(curves, newdir)
        fname = path.join(newdir,'data_' + arq_name) 
        f = open(fname, 'wb')
        w = csv.writer(f)
        w.writerows(curves.items())
        w.writerows(pulses.items())
        f.close()


if __name__ == '__main__':
    main(sys.argv[1])

