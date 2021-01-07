import csv
import statistics
import math
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

Covid_death = []
Death = []
State = []

with open('AH_County-level_Provisional_COVID-19_Deaths_Counts.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Death.append(int(row['Total Deaths']))
        Covid_death.append(int(row['COVID-19 Deaths']))
        State.append(row['State'])

States = set(State)
Covid_deaths = [0]*len(States)
Deaths = [0]*len(States)
i = 0

for states in States:
    for state in State:
        if(state == states):
            Covid_deaths[i] += Covid_death[i]
            Deaths[i] += Death[i]
    i += 1

total = []
for i in range(len(Deaths)):
    total.append([Deaths[i], Covid_deaths[i]])

k=1
first = []
second = []
third = []
while k != 0:
    first = []
    second = []
    third = []
    k=0
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(total)
    labels = kmeans.predict(total)
    centroids = kmeans.cluster_centers_
    for point in total:
        min_dist = float('inf')
        dists = []
        for centroid in centroids:
            dist = math.sqrt(((point[0] - centroid[0])**2) + ((point[1] - centroid[1])**2))
            dists.append(dist)
            if dist < min_dist:
                min_dist = dist
        p=0
        for dist in dists:
            if dist == min_dist:
                p += 1
                if p>1:
                    print(point, '- точка касания')
                    k = 1
        if dists[0] == min_dist:
            first.append(point)
        elif dists[1] == min_dist:
            second.append(point)
        else:
            third.append(point)

classes = [first, second, third]
i=0
color = ['blue', 'red', 'green']
for Class in classes:
    for point in Class:
        scater = plt.scatter(point[0], point[1], c = color[i])
    i+=1
plt.show()

"""
k = []
for i in range(len(Deaths)):
    k.append(Covid_deaths[i]/Deaths[i])

k1 = sum(k)/(3*len(k))
k2 = (sum(k)*2)/(3*len(k))

q = statistics.median(Deaths)

Groups = []
for k3 in k:
    if(k3 <= k1):
        Groups.append('олдов')
    elif(k3 >= k2):
        Groups.append('зумеров')
    else:
        Groups.append('бумеров')
j=0

for state in States:
    print(state, 'штат', Groups[j])
    if(Groups[j] == 'зумеров'):
        if (Deaths[j] > q):
            print('В штате', state, 'средний уровень угрозы Covid')
        else:
            print('В штате', state, 'низкий уровень угрозы Covid')
    elif(Groups[j] == 'бумеров'):
        if (Deaths[j] > q):
            print('В штате', state, 'высокий уровень угрозы Covid')
        else:
            print('В штате', state, 'средний уровень угрозы Covid')
    else:
            print('В штате', state, 'высокий уровень угрозы Covid')
    j += 1
"""