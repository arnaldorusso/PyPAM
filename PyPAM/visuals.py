#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from rpy import r


colors = ['blue','green','red','brown']
compr = ['470nm', '520nm', '645nm', '665nm']



def etr_plot(curves, indir='.', subplot=False):
    '''
    Relative Electron Transference Rate plots.

    INPUT
    -----
    curves : list of curves
    indir : directory to save plots. Default current directory
    subplot : Default False.

    OUTPUT
    ------
    Return =     
    Figure saved (png)
    '''
    light = []
    etr = []
    opts = []
    x = []
    y = []

    if type(curves) != list:
        raise TypeError('variable "curves", must be a list')

    for ii,cur in enumerate(curves):
        light.append(np.float64(cur['PAR']))
        etr.append(np.float64(cur['ETR1'])/1000.)
        etr.append(np.float64(cur['ETR2'])/1000.)
        etr.append(np.float64(cur['ETR3'])/1000.)
        etr.append(np.float64(cur['ETR4'])/1000.)
        for value in etr:
            r.assign("x",light[0])
            r.assign("y",value)
            min_platt = r("""
            platt<- function(params){
                alpha<-params[1]
                Beta<- params[2]
                Ps<- params[3]
                return( sum( (y-Ps*(1-exp(-alpha*x/Ps))*exp(-Beta*x/Ps))^2))
            } """)
            min_adp = r("""
            min_ad<-function(params){ 
                alpha<-params[1]
                Beta<-params[2]
                Ps<-params[3]
                return( ( (Ps*(1-exp(-alpha*x/Ps)) *exp(-Beta*x/Ps)) ))
            }""")
            r('etr_sim<-optim(par=c(0.4, 1.5 , 80),fn=platt)')
            opts.append(r('min_ad(par = etr_sim$par)'))

        if subplot==True:
            #plt.subplot(6,5,cur+1)
            for i in xrange(len(opts)):
                #plt.figure(figsize=(8, 6), dpi=80)
                plt.subplot(6,5,ii+1)
                plt.subplots_adjust(wspace=0.2, hspace=0.7) #adjust spaces between subplots
                plt.plot(light[0],etr[i], 'o', color=str(colors[i]))
                plt.ylim(0, 100)
                plt.xlabel('Light (PAR)')
                plt.ylabel(u'(rETR)')
                plt.plot(np.sort(light[0]), np.sort(opts[i]), color=str(colors[i]), label=str(compr[i]))
                plt.legend(loc='upper left', prop={'size':7})  #markerscale=0.1, borderpad=0.1, labelspacing=0.1, mpl.font_manager.FontManager(size=10))#,ncol=4,prop=font_manager.FontProperties(size=10))
                plt.title(str(cur['Date'][0]+' '+cur['Time'][0]))
            light = []
            etr = []
            e_sim = []
            opts = []
            x = []
            y = []
    if subplot==True:
        plt.savefig(os.path.join(indir + str(cur['Date'][0]+'_'+ cur['Time'][0] + '.png')))
        
    plt.show()
        
    return opts


def yield_plot(pulses, indir):
    '''
    BarPlot of Photosynthetic Efficiency

    Input
    ----
    pulses : List of Saturating Pulses
    indir : String of directory, to save figures

    Output
    ------
    Figure saved (png)

    '''

    Date = []
    Time = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    ybl = []
    ygr = []
    ybr = []
    for pul in pulses:
            Date.append(pul['Date'][0])
            Time.append(pul['Time'][0])
            y1.append(pul['Yield1'][0])
            y2.append(pul['Yield2'][0])
            y3.append(pul['Yield3'][0])
            y4.append(pul['Yield4'][0])
            ybl.append(pul['Y(Bl)'][0])
            ygr.append(pul['Y(Gr)'][0])
            ybr.append(pul['Y(Br)'][0])


    y1a = np.int32([l for i,l in enumerate(y1) if i%2 == 0])
    y1b = np.int32([l for i,l in enumerate(y1) if i%2 != 0])
    tah = [l.strip()[:-3] for i,l in enumerate(Time) if i%2 == 0]
    tbh = [l.strip()[:-3] for i,l in enumerate(Time) if i%2 != 0]
    real_par = [83.76,1091,154.2,0,0,0,341.3,950,148.5,0,0,0,272.5]


    ind = np.arange(len(Date)/2)  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rec1 = ax.bar(ind, y1a, width, color='k')
    rec2 = ax.bar(ind+width, y1b, width, color='grey')
    
    ## add some
    ax.set_ylabel('Fv/Fm')
    ax.set_xlabel('Time- hours')
    ax.set_title(u'Photosynthetic Efficiency')
    ax.set_ylim(50,700)

    ax2 = ax.twinx()
    ax2.plot(ind, real_par, '-', color='orange')
    ax2.set_ylim(0,1300)
    ax2.set_ylabel('PAR (in situ)')
    ax.set_xticks(ind+width)
    ax.set_xlim(-0.25,13.25)
    ax.set_xticklabels(tah, rotation=30)

    ax.legend((rec1[0], rec2[0]), ('A', 'B'), loc='upper left')
    
    plt.savefig(indir + 'yield' + '.png')
