import csv

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

k = []
for i in range(len(Deaths)):
    k.append(Covid_deaths[i]/Deaths[i])

k1 = sum(k)/(3*len(k))
k2 = (sum(k)*2)/(3*len(k))

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
        print('В штате', state, 'низкий уровень угрозы Covid')
    elif(Groups[j] == 'бумеров'):
        print('В штате', state, 'средний уровень угрозы Covid')
    else:
        print('В штате', state, 'высокий уровень угрозы Covid')
    j += 1