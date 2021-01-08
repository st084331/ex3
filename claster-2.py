import csv
import statistics
import math
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
additional_Statenames = []
additional_Population = []
LandAreas = []

with open('State Populations.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        additional_Statenames.append(row['State'])
        additional_Population.append(row['2018 Population'])
States = list(set(State))
state_to_num = {States[i]: i for i in range(len(States))}
Covid_deaths = [0]*len(States)
Deaths = [0]*len(States)
for i in range(len(State)):
    j = state_to_num[State[i]]  # index of seen State in actual states
    Covid_deaths[j] += Covid_death[i]
    Deaths[j] += Death[i]


Deaths = [k for _, k in sorted(zip(States, Deaths), key=lambda pair: pair[0])]
Covid_deaths = [k for _, k in sorted(zip(States, Covid_deaths), key=lambda pair: pair[0])]
additional_Population = [k for _, k in sorted(zip(additional_Statenames, additional_Population), key=lambda pair: pair[0])]
States.sort()
total = []
for i in range(len(Deaths)):
    population = float(additional_Population[i])
    print(States[i], 10000 * Covid_deaths[i] / population, 10000*Deaths[i] / population)
    total.append([10000*Deaths[i]/population, 10000*Covid_deaths[i]/population])


k = 1
first = []
second = []
third = []
while k != 0:
    first = []
    second = []
    third = []
    k = 0
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
        p = 0
        for dist in dists:
            if dist == min_dist:
                p += 1
                if p > 1:
                    print(point, '- точка касания')
                    k = 1
        if dists[0] == min_dist:
            first.append(point)
        elif dists[1] == min_dist:
            second.append(point)
        else:
            third.append(point)

classes = [first, second, third]
i = 0
color = ['blue', 'red', 'green']
for Class in classes:
    for point in Class:
        scater = plt.scatter(point[0], point[1], c=color[i])
    i += 1
plt.title('COVID danger rating of USA states')
plt.xlabel('Death by ten thousands citizens')
plt.ylabel('COVID Death by ten thousands citizens')
plt.show()
