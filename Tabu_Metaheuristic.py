# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 00:58:40 2020
@authors: Stef / Brau
"""
# -*- coding: utf-8 -*-
"""
Generating random numbers
"""
## Importing the package to generate random numbers
from random import choices
import random
import pandas as pd
import math
import time
import re
from itertools import combinations, chain
import numpy as np

## Probability Distribution to generate the random numbers
population = [0, 400, 800, 1100, 1500, 2000, 2250, 2731, 3200, 3900, 4100, 5420]
weights = [0.005, 0.01, 0.01, 0.025, 0.05, 0.15, 0.25, 0.25, 0.15, 0.05, 0.04, 0.01]


## Function to generate the random mmr based on the number of players, and prob to play
## in a party (2,3, 4 0r 5 people).
## Logic behind this function: we will create two list, one with the id and the other one
## with the mmr. We need the id to identify when the players are individual or in a party.
## Example: if two of them have the same number that means they are in a party of two.
## So first we generate the id (based on the number of iteration) and then we generate the
## mmr. These data is being pull in a dataframe.

def random_mmr(n, prob2, prob3, prob4, prob5):
    mmr_id = []
    mmr_mmr = []
    m = n

    while m != 0:
        prob = random.random()

        if (prob < prob2 and m >= 2):
            for i in range(2):
                mmr_id.append(m)
                mmr_mmr.append(choices(population, weights))
            m = m - 2
        if (prob < prob3 and m >= 3):
            for i in range(3):
                mmr_id.append(m)
                mmr_mmr.append(choices(population, weights))
            m = m - 3
        if (prob < prob4 and m >= 4):
            for i in range(4):
                mmr_id.append(m)
                mmr_mmr.append(choices(population, weights))
            m = m - 4

        if (prob < prob5 and m >= 5):
            for i in range(5):
                mmr_id.append(m)
                mmr_mmr.append(choices(population, weights))
            m = m - 5

        else:
            mmr_id.append(m)
            mmr_mmr.append(choices(population, weights))
            m = m - 1
        flat_list = [mmr for sublist in mmr_mmr for mmr in sublist]
        d = {'id': mmr_id, 'MMR': flat_list}
        df = pd.DataFrame(d)
    return df


## Running an example
df = random_mmr(30, 0.1, 0.2, 0.3, 0.4)

# ## Saving the output in a txt file
# with open(r'C:\Users\stefq\iCloudDrive\CompComp\GitHub\Comp_Gh\proyecto2\pool.txt', 'a') as f:
#     f.write(
#         df.to_string(header=True, index=False)
#     )

"""
Match Making first solution
"""
df['index'] = df.index
df['combination'] = df['index'].astype(str) + " - " + df['MMR'].astype(str) + " - " + df['id'].astype(str) # Creates a variable with identifier + MRR
dataframe_size = len(df)
import statistics
print(df)
# The purpose of this heuristic is to create teams composed by opposite players, so that the best players compensate the worst ones.
# In this way, teams are heterogenous on the inside -although is it expected to have 2 good and 2 bad players in each team- but they're
# homogenous between them. For this purpose, the median of the MMR distribution is calculated, then the distance from the players' MMR
# and the distribution's median is calculated, then players are sorted by this difference and afterwards the extreme players are extracted, this means:
# first one with the last one, second one with the penultimate one, third one with the antepenultimate one and so on.

# La idea detrás de esta heurística crear equipos conformados por extremos de manera que los mejores jugadores compensen a los peores jugadores
# De esta manera, los equipos son heterogéneos a lo interno, aunque se espera hayan 2 jugadores buenos y 2 malos.
# Pero son homogéneos entre sí. Para eso se calcula la mediana de la distribución de los MMR, luego la distancia del MMR de cada jugador con
# la mediana, luego se acomodan los jugadores por esta diferencia y seguidamente se extraen los extremos: primero con último,
# segundo con penúltimo, tercero con antepenúltimo.

# STEP 1: Compute median
MMR_median = statistics.median(df['MMR'])

# STEP 2: Compute MMR & Median differences
df['median_diff'] = abs(df['MMR']-MMR_median)

# STEP 3: Sort
df = df.sort_values(by=['median_diff'])

# STEP 4: Take the first and last entry and place them in a bin
i = len(df)
t = 2

df2 = df.iloc[[0, -1]] #New dataframe with 2 first extractions

while(t < i):
    df = df.drop(df.index[[0, -1]]) #Removes first and last row (which were extracted)
    temp = df.iloc[[0,-1]] # Extracts first and last row
    df2 = df2.append(pd.DataFrame(data=temp), ignore_index=True) # Combines with the previously extracted rows
    t = t + 2


if(dataframe_size % 2 != 0): # Si la cantidad de jugadores es impar, el barrido del DF duplica la fila que queda sola
    df2 = df2.iloc[:-1] # Si n es impar, elimina ese duplicado.

modulo_10 = len(df2) % 10

# Si n no es multiplo de 10, algunos jugadores quedan fuera. Aquí se eliminan las últimas entradas del DataFrame
# Esto no afecta la homogeneidad de los equipos porque las últimas entradas del DF son los jugadores con menor distancia
# de la mediana, es decir, los más homogéneos.

if(modulo_10 != 0): #Si n no es múltiplo de 10, algunos jugadores quedan fuera
    df2 = df2[0:(len(df2)-(modulo_10))]

# Output on special format
lol = df2['MMR'].values.tolist()

def divide_chunks(l,n):
    for i in range(0,len(l),n):
        yield l[i:i + n]
#Divide an initial solution by teams
n = 5
x = list(divide_chunks(lol,n))
print('Prueba: ')
print(x)

#Make all possible team combinations by changing the first team
while_list = []
temporary_list = []
contador = 2
x_copy = x.copy()
while(contador <= len(x)-1):
    equipo_intercambiar = x[0]
    temporal1 = x_copy[contador]

    x_copy[0] = temporal1
    x_copy[contador] = equipo_intercambiar
    temporary_list = x_copy
    contador = contador + 1
    while_list.append(temporary_list[:])

print(while_list)

#Evaluate every possible match
MMR_comparative_list = []
for i in range(0, (len(while_list))):
    list_to_use = while_list[i]
    first = 0
    second = 1
    MMR_comparison = 0
    while(second < len(list_to_use)):
        first_team = list_to_use[first]
        second_team = list_to_use[second]
        first_team_average = statistics.mean(first_team)
        second_team_average = statistics.mean(second_team)
        average_diff = round(abs(first_team_average-second_team_average),0)
        MMR_comparison = MMR_comparison + average_diff
        #Update values
        first = first + 2
        second = second + 2
    MMR_comparative_list.insert(i, MMR_comparison)

print(MMR_comparative_list)

#Find index of the minimum MMR comparison

print(MMR_comparative_list.index(min(MMR_comparative_list)))

#for s in x:
#    print(*s)

