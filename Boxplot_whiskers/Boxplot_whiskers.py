from pandas import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

state = read_csv('state.csv')
fs = 20 # fontsize
yfs = 19 # fontsize
labels = ['CT', 'MA', 'ME', 'NH', 'NY', 'RI', 'VT']
df = DataFrame(state, columns=labels)

color = dict(boxes='#f1a340', whiskers='#998ec3', medians='#542788', caps='#542788')

df.plot(kind='box', color=color, notch=True,showmeans=True, meanline=True,fontsize=yfs)

plt.ylabel('Continuous Duration (Years)', fontsize=yfs)

plt.title('Duration of 1,381 Climate Stations\nfrom New England and Adjacent States', fontsize=fs)

plt.show()