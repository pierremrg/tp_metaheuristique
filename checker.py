"""
"instant" entre 0 et temps_max (37)
Vérifier que la capacité de chaque arc est respectée à chaque instant
Vérifier que le duedate est respecté
"""

"""
############# PSEUDO-CODE DE L'ALGORITHME DU CHECKER #############

vecteur remaining_number
= nombre de personnes restant à envoyer depuis chaque noeud
	ne prend pas en compte les noeuds intermédiaires !

vecteur stock_tmp
= ce que chaque noeud a reçu de ses prev et qu'il doit propager

vecteur arc
= autant de cases que d'instants de temps
	chaque case contient le nombre de personnes à cet instant

Propagate :

Pour chaque noeud current --> prendre le terminal
	stock_tmp[current] = 0

	Récupérer précédents
	Si précédents:
		pour chaque précédent:
			cap_ok = cap_ok && propagate(prev)

	# ici : préc déjà propagés
	# on commence la propagation de ce noeud
	arc = arc_sortant
	dest = dest de arc
	stock_tmp[dest] += arc[LAST]
	avancer toutes les valeurs à l'instant suivant sur arc
	arc[FIRST] = combien on doit envoyer (remaining_number[current] + 
		stock_tmp[current] + prendre en compte date de début d'envoi)
	vérifier que cap pas dépassée sur chaque instant de l'arc
	retourner le résultat du test
"""

import parser
import solution_parser
import json


"""
Functions
"""

def printJSON(data):
	print(json.dumps(data, indent=2))
	print()

def printArray(data):
	print('\n'.join('{}: {}'.format(*k) for k in enumerate(data)))
	print()

"""
End functions
"""

class Checker:

	# Initialise tout ce qui est nécessaire pour le checker
	def __init__(self, evacuation_info, graph, infos_solution):
		self.evacuation_info = evacuation_info
		self.graph = graph
		self.infos_solution = infos_solution

		self.maxTime = self.infos_solution['objectif'];
		self.evac_solution = self.infos_solution['evacuation_plan']


		# times : dict
		# De la forme [A][B] = [<instants> instants possibles]
		# Pour un arc de A vers B, ayant <instants> instants de traversée
		# Chaque case contient le nombre de personne présentes à cet endroit
		#	dans le couloir
		self.times = {}

		# stock_tmp : dict
		# Permet de connaître le nombre de personnes envoyées vers un noeud
		# 	par les noeuds précédents
		# Utilisé uniquement pour l'algorithme : il n'a pas de signification en réalité !
		self.stock_tmp = {}

		# remaining_people : dict
		# Contient pour chaque sommet à évacuer le nombre de personnes restantes
		self.remaining_people = {}


		for node in self.graph:

			# Gestion de times
			dests = {}

			for dest in self.graph[node]:
				if self.getNextNode(node) == dest:
					dests[dest] = [0 for i in range(int(self.graph[node][dest]['length']))]

			self.times[node] = dests


			# Gestion de stock_tmp : initialement, tous sont vides
			self.stock_tmp[node] = 0


		for node in self.evacuation_info:
			# Gestion des personnes à évacuer
			self.remaining_people[node] = int(self.evacuation_info[node]['population'])


	############## TRAITEMENT PREALABLE SUR TOUS LES NOEUDS DU GRAPH ###############

	# Retourne la liste des noeuds précédents d'un noeud
	def getPreviousNodes(self, current_node_id):
		prevs = {}

		for node_id in self.evacuation_info:
			path = [node_id] + self.evacuation_info[node_id]['path']
			
			for i in range(1, len(path)):
				if path[i] in prevs:
					if not path[i-1] in prevs[path[i]]:
						prevs[path[i]].append(path[i-1])
				else:
					prevs[path[i]] = [path[i-1]]

		if current_node_id in prevs:
			return prevs[current_node_id]
		else:
			return []


	# Retourne le prochain noeud à visiter
	# à partir des chemins présents
	def getNextNode(self, current_node_id):
		prevs = {}

		for node_id in self.evacuation_info:
			path = [node_id] + self.evacuation_info[node_id]['path']
			
			for i in range(0, len(path)-1):
				if path[i] == current_node_id:
					return path[i+1]

		return None


	# Retourne True si la solution est valide
	# False sinon
	# Si verbose = True, affichage du debug
	def check(self, verbose = False):
		capacities_ok = True

		for t in range(self.maxTime):

			# Reset des stocks temporaires
			for node in self.graph:
				self.stock_tmp[node] = 0

			last_node = self.evacuation_info[list(self.evacuation_info.keys())[0]]['path'][-1]
			self.propagate(last_node, t)

			if not self.check_quantities():
				capacities_ok = False

			if verbose:
				print('Time: ' + str(t+1) + ' - Capacities OK: ' + str(capacities_ok))
				printJSON(times)

		return (capacities_ok and self.check_room_is_empty())


	# propage vers l'arc sortant
	# retourne la quantité sortie de l'arc (arrivée au noeud suivant)
	def propagate(self, current_node_id, t):
		# On propage tous les noeuds précédents	
		prevs = self.getPreviousNodes(current_node_id)

		if len(prevs) > 0:
			for prev in prevs:
				# print(prev)
				self.propagate(prev, t)


		# Ici : les noeuds précédents ont été traités,
		# on peut propager au suivant
		next_node_id = self.getNextNode(current_node_id)

		if next_node_id != None:

			# On transfère au noeud suivant (temporairement) ce qui doit
			# sortir de l'arc
			self.stock_tmp[next_node_id] += self.times[current_node_id][next_node_id][-1]

			# On avance sur l'instant suivant
			for i in range(len(self.times[current_node_id][next_node_id])-1,0,-1):
				self.times[current_node_id][next_node_id][i] = self.times[current_node_id][next_node_id][i-1]

			self.times[current_node_id][next_node_id][0] = self.getNumberToAdd(current_node_id, t)


	# Retourne le nombre de personnes à ajouter
	# sur le prochain arc
	def getNumberToAdd(self, node_id, t):
		number = 0

		if node_id in self.remaining_people:

			if t >= int(self.evac_solution[int(node_id)-1]['start_date']):
				tmp1 = self.remaining_people[node_id]
				tmp2 = int(self.evac_solution[int(node_id)-1]['evacuation_rate'])
				qty = min(tmp1, tmp2)

				number += qty
				self.remaining_people[node_id] -= qty

		number += self.stock_tmp[node_id]

		return number


	# Retourne True s'il y a un arc entre node_id1 et node_id2,
	# 	False sinon
	def edgeExist(self, node_id1, node_id2):
		for current_node_id in self.graph:
			if current_node_id != node_id1:
				continue

			for edge in self.graph[current_node_id]:

				# Si il y a un arc de current_node_id vers node_id
				if edge['dest'] == node_id2:
					return True

		return False


	# Retourne True si toutes les quantités sont respectées
	# sur tous les chemins à l'instant actuel, False sinon
	def check_quantities(self):
		for node in self.times:
			for dest in self.times[node]:
				quantities = self.times[node][dest]

				for q in quantities:
					if q > int(self.graph[node][dest]['capacity']):
						return False;

		return True;


	# Retourne True si tous les chemins sont vides
	# à l'instant actuel, False sinon
	def check_room_is_empty(self):
		for node in self.times:
			for dest in self.times[node]:
				quantities = self.times[node][dest]

				for q in quantities:
					if q > 0:
						return False;

		return True;