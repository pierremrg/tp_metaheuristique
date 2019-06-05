import json
import sys

from evacuation_parser import EvacuationParser
from solution_parser import SolutionParser
from checker import Checker
from simulator import Simulator
from bornes import Bornes
from local_search import LocalSearch


def printJSON(data):
	print(json.dumps(data, indent=2))



# Variable de debug
DEBUG = True if len(sys.argv) > 1 and sys.argv[1] == "-v" else False
DEBUG_SIMULATION = False

# Noms des fichiers à utiliser -- TODO Rajouter une option dans le terminal pour sélectionner le fichier
EVACUATION_FILEPATH = "exemple_cours.txt"
# SOLUTION_FILEPATH = "exemple_cours_solution.txt"
SOLUTION_FILEPATH = "generated_files/borneSup_solution.txt"

# Parsers
evacuation_parser = EvacuationParser(EVACUATION_FILEPATH)
[evacuation_info, graph] = evacuation_parser.parseData()

solution_parser = SolutionParser(SOLUTION_FILEPATH)
infos_solution = solution_parser.parseData()

# Checker de solution
checker = Checker(evacuation_info, graph, infos_solution)
solution_ok = checker.check(DEBUG)
print(solution_ok)

# Calcul des bornes
bornes = Bornes(evacuation_info, graph)
print("Borne inférieure : " + str(bornes.borneInf(DEBUG)))
print("Borne supérieure : " + str(bornes.borneSup(DEBUG)))




# Simulation d'une solution
start_dates =  {}
rates = {}
for node in infos_solution['evacuation_plan']:
	start_dates[node['id_node']] = node['start_date']
	rates[node['id_node']] = node['evacuation_rate']

simulator = Simulator(evacuation_info, graph, start_dates, rates)
duration = simulator.simulate(DEBUG_SIMULATION)
print("Simulation borne supérieure" + str(duration))


print(Simulator(evacuation_info, graph, {'1':8, '2':7, '3':7}, {'1':8, '2':5, '3':3}).simulate())
print(Simulator(evacuation_info, graph, {'1':7, '2':7, '3':8}, {'1':8, '2':5, '3':3}).simulate())






# print("Premier intensification : ")
# intensification = LocalSearch(evacuation_info, graph, start_dates, rates).intensification()
# print(str(intensification))

diversification = LocalSearch(evacuation_info, graph, start_dates, rates).diversification()
while 1:
	diversification = LocalSearch(evacuation_info, graph, diversification['start_dates'], diversification['rates']).diversification()
	print(diversification)
