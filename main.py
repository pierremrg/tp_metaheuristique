import json

import parser
import solution_parser


def printJSON(data):
	print(json.dumps(data, indent=2))



filename = "exemple_cours.txt"

[evacuationInfo, graph] = parser.parseData(filename)

printJSON(graph)



