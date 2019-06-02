"""
Class Simulator
Permet de simuler l'évacuation des personnes
"""

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

"""
Pour chaque noeud :
- dates de départ
- débits


"""

class Simulator:

	# Initialise tout ce qui est nécessaire pour le simulateur
	def __init__(self, evacuation_info, graph, start_dates, rates):
		self.evacuation_info = evacuation_info
		self.graph = graph
		self.start_dates = start_dates
		self.rates = rates

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


		############## TRAITEMENT PREALABLE SUR TOUS LES NOEUDS DU GRAPH ###############

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


	# Simule l'évacuation des personnes
	# Retourne la durée totale nécessaire pour l'évacuation de toutes les personnes
	# Si verbose = True, affichage du debug
	def simulate(self, verbose = False):

		t = 0

		while self.check_still_remaining_people() or not self.check_room_is_empty():

			# Reset des stocks temporaires
			for node in self.graph:
				self.stock_tmp[node] = 0

			last_node = self.evacuation_info[list(self.evacuation_info.keys())[0]]['path'][-1]
			self.propagate(last_node, t)

			if verbose:
				is_empty = self.check_room_is_empty()

				print('Time: ' + str(t+1) + ' (Room empty: ' + str(is_empty) + ')')
				printJSON(self.times)

			t += 1

		return t

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

			if t >= int(self.start_dates[node_id]):
				tmp1 = self.remaining_people[node_id]
				tmp2 = int(self.rates[node_id])
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

	# Retourne True si tous les chemins sont vides
	# à l'instant actuel, False sinon
	def check_room_is_empty(self):
		for node in self.times:
			for dest in self.times[node]:
				quantities = self.times[node][dest]

				for q in quantities:
					if q > 0:
						return False;

		return True

	def check_still_remaining_people(self):
		for node in self.evacuation_info:
			if self.remaining_people[node] > 0:
				return True

		return False