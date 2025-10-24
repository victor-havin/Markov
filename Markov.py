import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

LENGTH=20000
#LENGTH=5000
ITERATIONS=10000
GRADIENT=2

space=np.zeros(LENGTH)
#time=np.linspace(0,1,LENGTH)
time=np.linspace(0,GRADIENT,LENGTH)
grid=np.arange(LENGTH)

scale_x = np.linspace(0, 1, LENGTH)
scale_y = np.zeros(LENGTH)

def step(pos, time):
    random=np.random.rand()
    probability=random+time[pos]
    if probability > 0.5:
        pos=(pos+1)
    else:
        pos=(pos-1)
    return pos

def walk(start, length):
    position=start
    while position < length:
        position=step(position, time)
        if position >= 0 and position < length:
            space[position]+=1
            
def brachistochrone():
    a = 0.5
    theta = np.linspace(0, np.pi, 100)
    x = a * (theta - np.sin(theta))
    y = -a * (1 - np.cos(theta))
    brach_x = (x - x.min()) / (x.max() - x.min())
    brach_y = np.interp(scale_x, brach_x, y)
 
    brach_y += 1
    return brach_y

def inverse_quadratic():
    x = np.linspace(0.01, 1, LENGTH)
    y = 1 / (x ** 2)
    y /= np.max(y)
    return y    

def plot_results():
    # Post-simulation analysis and plotting
    #print(space)
    plt.figure(figsize=(12, 6))
    plt.plot(scale_x, scale_y, label='Expectancy', color='blue')
    plt.plot(scale_x, brachistochrone(), label='Brachistochrone', color='red')
    plt.plot(scale_x, inverse_quadratic(), label='1/x**2', color='green')
    plt.xlabel('Space')
    plt.ylabel('Expectancy')
    plt.title(f"Random Walk Simulation. Particles: {ITERATIONS}, Length: {LENGTH}, Gradient: {GRADIENT}")
    plt.legend()
    plt.grid()
    plt.show()

def curve_fiting(scale, curve):
    initial_guess = [2, 1]
    bounds = ([0, 0], [np.inf, np.inf])
    def inverse_quadratic(x, a, b):
        return b / (x ** a) 
    params, _ = curve_fit(
        inverse_quadratic, 
        scale,
        curve, 
        p0=initial_guess,
        bounds=bounds,
        maxfev=10000)
    print(f"Fitted parameters: a = {params[0]}, b = {params[1]}")
    

for i in range(ITERATIONS):
    walk(1, LENGTH)
scale_y = space / np.max(space)
#curve_fiting(scale_x+1e-6, scale_y)
plot_results()
