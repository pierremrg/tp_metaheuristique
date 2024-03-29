class EvacuationParser:
	def __init__(self, evacuation_filepath):
		self.filename = evacuation_filepath

	def parseData(self):

		f = open(self.filename, "r")

		lines = f.read().splitlines()

		i = 0

		evacuationInfo = {}
		graph = {}

		# Skip comments
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

			evacuationInfo[lineSplited[0]] = {
				'population': lineSplited[1],
				'max_rate': lineSplited[2],
				'path': vks
			}

			i += 1

		# Skip comments
		while lines[i].startswith('c'):
			i += 1


		nodesNumber = int(lines[i].split()[0])
		edgesNumber = int(lines[i].split()[1])

		i += 1

		j = i + edgesNumber
		while i<j:
			lineSplited = lines[i].split();

			if not lineSplited[0] in graph:
				graph[lineSplited[0]] = {}
			
			if not lineSplited[1] in graph:
				graph[lineSplited[1]] = {}

			graph[lineSplited[0]][lineSplited[1]] = {
				'due_date': lineSplited[2],
				'length': lineSplited[3],
				'capacity': lineSplited[4]
			}

			graph[lineSplited[1]][lineSplited[0]] = {
				'due_date': lineSplited[2],
				'length': lineSplited[3],
				'capacity': lineSplited[4]
			}


			i += 1

		return [evacuationInfo, graph]