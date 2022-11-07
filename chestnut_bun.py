# -*- coding: utf-8 -*-
"""Chestnut_Bun.ipynb

Automatically generated by Colaboratory.
#005Chestnut Bun Problem
"""

def solar_system(object_size):

    solar_system_size = 50000

    time = 0

    while True:
        if object_size >= solar_system_size:
            break
        else:
            object_size *= 2
            time += 5
    return print("It will take the Chestnut bun {}minutes to cover the solar system.".format(time))
solar_system(500) #Let's Assume that the volume of a chestnut bun is 500 m3.

"""#Graphical Representation"""

def Tokyo_Dome(object_size):
    size_tokyo_dome = 500000 #Size of the Tokyo Dome is in Cubic Meters
    time = 0
    minutes = []
    size = []
    while True:
        if object_size >= size_tokyo_dome:
            break
        else:
            object_size *=2
            time +=5
            minutes.append(time)
            size.append(object_size)
    
    import matplotlib.pyplot as plt

    plt.plot(minutes, size, 'b-o', linewidth=2, markersize=12, markeredgewidth=3, markeredgecolor='orange', color="2")
    plt.xlabel('Time in Minutes')
    plt.ylabel('Size of the object')
    plt.title("Relating to Tokyo Dome Situation")
    plt.legend(loc='upper center')
    print("It takes {} Minutes".format(time))
Tokyo_Dome(10000)
