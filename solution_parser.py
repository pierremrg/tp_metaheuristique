def parseData(filename):
	filename = "exemple_cours_solution.txt"
	f = open(filename, "r")


	lines = f.read().splitlines()

	nb_edges = int(lines[1])

	list_edges = []
	i = 2
	while i < nb_edges+2:
		line_splited = lines[i].split();
		list_edges.append({
			'id_node':line_splited[0],
			'evacuation_rate':line_splited[1],
			'start_date':line_splited[2]
			})
		i += 1

	return {
		'instance_name':lines[0],
		'evacuation_plan':list_edges,
		'nature(valid invalid)':lines[i],
		'objectif':int(lines[i+1]),
		'temps calcul':lines[i+2],
		'method':lines[i+3],
		'champ libre':lines[i+4],
	}