import json

import parser
import solution_parser


def printJSON(data):
	print(json.dumps(data, indent=2))



filename = "exemple_cours.txt"
filename_solution = "exemple_cours_solution.txt"

[evacuationInfo, graph] = parser.parseData(filename)
evac_plan = solution_parser.parseData(filename_solution)

printJSON(evac_plan)



