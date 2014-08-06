#/usr/bin/env python
# -*- coding: utf-8 -*-

from PyPAM.parse import csv_extract, raw_extract, tryconvert
import numpy as np
from scipy.stats import nanmean, nanstd

def npq(plight, pdark):
    """"Try to compute NPQ (Non-photochemical quenching) from pulses
        values

        input: dict, dict

               plight = light-addapted pulse.
               pdark = dark-addpated pulse.

        output:
               float: NPQ
               np.array: light-addapted pulse
               np.array: dark-addapted pulse

    """
    ppl = np.array([plight['Fm1'],
                    plight['Fm2'],
                    plight['Fm3'],
                    plight['Fm4']])

    ppd = np.array([pdark['Fm1'],
                    pdark['Fm2'],
                    pdark['Fm3'],
                    pdark['Fm4']])

    Fm_ = nanmean(nanmean(ppl))
    Fm = nanmean(nanmean(ppd))
    npq = (Fm - Fm_) / Fm_

    return npq, ppl, ppd


def npq_pulses(pulses):
    """Try to compute NPQ (Non-photochemical quenching) from pulses
        values extracted after using any PyPAM.parse methods.


        input:  list of dicts
                each element of list contains a dictionary of pulses.

        example:
                from PyPAM.parse import raw_extract
                curves, pulses = raw_extract('file.rpt')
    """

    # TODO implement automatic way
    words = ['Claro', 'claro']
    tt = []
    for pulse in pulses:
        comments = pulse['comments']
        for word in comments:
            tt.append([word.find(key) for key in words])
        if tt != -1:
            pass
        else:
            print('It seems you don\'t have light addapted pulse.\n'
                  'Please run `npq_single` instead, informing as input\n'
                  'arguments, your light-addapted and dark-addapted pulses')

