"""
"instant" entre 0 et temps_max (37)
Vérifier que la capacité de chaque arc est respectée à chaque instant
Vérifier que le duedate est respecté
"""

import parser
import json

def printJSON(data):
	print(json.dumps(data, indent=2))

def printArray(data):
	print('\n'.join('{}: {}'.format(*k) for k in enumerate(data)))


filename = "exemple_cours.txt"
[evacuationInfo, graph] = parser.parseData(filename)

# TODO : Récupérer infos depuis le parser
maxTime = 37


capacities = []


for i in range(0, len(graph)):
	sub_capacities = []
	for j in range(0, len(graph)):
		sub_capacities.append(0)

	capacities.append(sub_capacities)


for node in graph:
	for arc in graph[node]:
		capacities[int(node)][int(arc['dest'])] = float(arc['capacity'])

printArray(capacities)


for t in range(0,maxTime):
	pass