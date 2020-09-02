import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

x   = np.arange(start=0.0, stop=2*np.pi, step=0.1)


for case in range(1, 5):
    f_x = np.cos(np.pi + case*x*np.pi)/2.0

    fig, model = plt.subplots()
    plt.figure(figsize=(30,40))
    model.set(
        xlabel='x',
        ylabel=f'f(x) = cos({case}*x*PI)',
        title='Simple data'
    )

    model.plot(x, f_x)
    model.grid()
    fig.savefig(os.path.dirname(__file__) + f'/../static/plots/mplib_{case}.png')
    fig.show()
