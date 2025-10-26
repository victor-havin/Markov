# Markov.py
# Simulation of a one-dimensional random walk in a time dilated field with linear gradient.
# Compares the resulting expectancy distribution to the brachistochrone curve and an inverse quadratic function.
#
# Author: Victor Havin
# Date: 2024-06-10

# Prereqvisites:
# - numpy
# - matplotlib

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from spectrum import *

#simulation parameters
<<<<<<< HEAD
LENGTH=80        #length of the 1D space
ITERATIONS=10000       #number of particles
GRADIENT=0.5           #gradient of the time dilation field
=======
LENGTH=20000            #length of the 1D space
#LENGTH=5000            #length of the 1D space
ITERATIONS=10000        #number of particles
GRADIENT=2              #gradient of the time dilation field
>>>>>>> d491e22ff75c5b51158d259c0661afe4a9d5fce8

# initialization
space=np.zeros(LENGTH)
time=np.linspace(0,GRADIENT,LENGTH)

scale_x = np.linspace(0, 1, LENGTH)
scale_y = np.zeros(LENGTH)

# step function to move the particle based on random walk and time dilation
# pos: current position of the particle
# time: time dilation field
# returns new position of the particle
def step(pos, time):
    random=np.random.rand()
    probability=random+time[pos]
    if probability > 0.5:
        pos=(pos+1)
    else:
        pos=(pos-1)
    return pos

# walk function to simulate the random walk of a particle
# start: starting position of the particle
# length: length of the 1D space
# updates the global space array with the number of visits to each position
def walk(start, length):
    position=start
    while position < length:
        position=step(position, time)
        if position >= 0 and position < length:
            space[position]+=1
            
# brachistochrone curve calculation
def brachistochrone():
    a = 0.5
    theta = np.linspace(0, np.pi, 100)
    x = a * (theta - np.sin(theta))
    y = -a * (1 - np.cos(theta))
    brach_x = (x - x.min()) / (x.max() - x.min())
    brach_y = np.interp(scale_x, brach_x, y)
 
    brach_y += 1
    return brach_y

# inverse quadratic function calculation
def inverse_quadratic():
    x = np.linspace(0.01, 1, LENGTH)
    y = 1 / (x ** 2)
    y /= np.max(y)
    return y    

# plotting function
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

# curve fitting function
def curve_fiting(scale, curve):
    scale[0] += 1e-6  # avoid division by zero
    initial_guess = [2, 1, 0.1]
    bounds = ([1, 0, 0], [3, np.inf, np.inf])
    def inverse_quadratic(x, a, b, c):
        return b / (x ** a) + c
    params, _ = curve_fit(
        inverse_quadratic, 
        scale+1e-6,  # avoid division by zero
        curve, 
        p0=initial_guess,
        bounds=bounds,
        maxfev=10000)
<<<<<<< HEAD
    print(f"Fitted parameters: a = {params[0]}, b = {params[1]}, c = {params[2]}")

    curve = curve - params[2]  # adjust for offset
    log_scale = np.log(scale)
    log_curve = np.log(curve)
    slope, intercept = np.polyfit(log_scale, log_curve, 1)
    print(f"Logarithmic slope: {slope}")
=======
    print(f"Fitted parameters: a = {params[0]}, b = {params[1]}")
>>>>>>> d491e22ff75c5b51158d259c0661afe4a9d5fce8
    
# Run the simulation
for i in range(ITERATIONS):
    walk(1, LENGTH)
scale_y = space / np.max(space)
#curve_fiting(scale_x, scale_y)
plot_results()
analyze_spectrum(space)
