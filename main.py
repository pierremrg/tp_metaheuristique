import json

from evacuation_parser import EvacuationParser
from solution_parser import SolutionParser
from checker import Checker
from bornes import Bornes


def printJSON(data):
	print(json.dumps(data, indent=2))

# Variable de debug
DEBUG = False

# Noms des fichiers à utiliser
EVACUATION_FILEPATH = "exemple_cours.txt"
SOLUTION_FILEPATH = "exemple_cours_solution.txt"

# Parsers
evacuation_parser = EvacuationParser(EVACUATION_FILEPATH)
[evacuation_info, graph] = evacuation_parser.parseData()

solution_parser = SolutionParser(SOLUTION_FILEPATH)
infos_solution = solution_parser.parseData()

# Checker de solution
checker = Checker(evacuation_info, graph, infos_solution)
solution_ok = checker.check(DEBUG)

# Calcul des bornes
bornes = Bornes(evacuation_info, graph)
print(bornes.borneInf())


print(solution_ok)

# printJSON(graph)
