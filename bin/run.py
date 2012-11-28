#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
from os import chdir

from PyPAM.pam import extract
from PyPAM.visuals import etr_plot, yield_plot

chdir(sys.argv[1])

for name in glob.glob('*.csv'):
    arq_name = "".join(name.split('.')[0:-1])
    newdir = os.path.join('fig', arq_name)
    try:
        os.makedirs(newdir)
    except OSError:
        print ('diretorio já existe: %s' % newdir)
    else:
        print ('criado diretorio %s' % newdir)
    
    curves, pulses = extract(name) # curves, pulses
    etr_plot(curves, newdir)
