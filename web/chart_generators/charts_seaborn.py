import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


x = np.arange(start=0.0, stop=2*np.pi, step=0.1)
sb.set(style="darkgrid")


for case in range(1, 5):
    f_x = np.cos(np.pi + case*x*np.pi)/2.0
    
    axises = sb.lineplot(x=x, y=f_x)
    plt.savefig(f'../static/plots/sborn_{case}.png')
    plt.clf()
