import json


filename = "exemple_cours.txt"
f = open(filename, "r")

lines = f.read().splitlines()

i = 0

nodeIds = {}
graph = {}

readingEvac = False
readingGraph = False

# Pass comments
while lines[i].startswith('c'):
	i += 1

evacNodesNumber = int(lines[i].split()[0])
safeNodeId = int(lines[i].split()[1])

i += 1

j = i + evacNodesNumber
while i<j:
	lineSplited = lines[i].split();

	vks = []
	for bouclage in range(0, int(lineSplited[3])):
		vks.append(lineSplited[bouclage+4])

	nodeIds[lineSplited[0]] = {
		'population': lineSplited[1],
		'max_rate': lineSplited[2],
		'path': vks
	}

	i += 1

# Pass comments
while lines[i].startswith('c'):
	i += 1


nodesNumber = int(lines[i].split()[0])
edgesNumber = int(lines[i].split()[1])

i += 1

j = i + edgesNumber
while i<j:
	lineSplited = lines[i].split();

	if not lineSplited[0] in graph:
		graph[lineSplited[0]] = []
	
	if not lineSplited[1] in graph:
		graph[lineSplited[1]] = []

	graph[lineSplited[0]].append({
		'dest': lineSplited[1],
		'due_date': lineSplited[2],
		'length': lineSplited[3],
		'capacity': lineSplited[4]
	})

	graph[lineSplited[1]].append({
		'dest': lineSplited[0],
		'due_date': lineSplited[2],
		'length': lineSplited[3],
		'capacity': lineSplited[4]
	})


	i += 1

print(json.dumps(graph, indent=2))
