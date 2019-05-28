
class Bornes:


	def __init__(self, evacuationInfo, graph):
		self.evacuationInfo = evacuationInfo
		self.graph = graph

	# Pour calculer une borne inférieure :
	#	- on calcule le temps d'évacuation de chaque sommet comme s'il était seul
	#	- on prend le max de tous ces temps d'évacuation 
	def borneInf(self, verbose = False):
		return max(self.calculTempsEvacuation(verbose))

	# Pour calculer une borne supérieure :
	#	- on calcule le temps d'évacuation de chaque sommet comme s'il était seul
	#	- on prend le total de tous ces temps d'évacuation (chaque sommet s'évacue un par un)
	def borneSup(self, verbose = False):
		return sum(self.calculTempsEvacuation(verbose))

	def calculTempsEvacuation(self, verbose = False):

		times = []
		# pour tous les noeuds à évacuer
		for nodeId in self.evacuationInfo:
			if verbose:
				print("\n\n\n\n")
				print("Je fais le noeud " + nodeId)
			# arcs[node] est l'arc qui mène à node
			arcs = {}
			# le nombre de personnes à évacuer
			nbAEvacuer = int(self.evacuationInfo[nodeId]["population"])
			nbSauves = 0
			# attentesSommet[node] est le nombre de personnes en attente sur le sommet node
			attentesSommet = {}
			attentesSommet[nodeId] = nbAEvacuer # au début tout le monde attend sur le premier sommet
			# predecesseurs[node] est le noeud qui précède node dans le path d'évacuation
			predecesseurs = {}
			predecesseurs[nodeId] = None


			lastNode = nodeId
			for node in self.evacuationInfo[nodeId]["path"]:
				# le prédécesseur du noeud courant est le noeud d'avant
				predecesseurs[node] = lastNode
				# l'arc menant jusqu'a node est initialisé
				arcs[node] = [0]*int(self.getArc(lastNode, node)["length"])
				# Personne n'attend sur les noeuds intermédiaires au début
				attentesSommet[node] = 0
				lastNode = node



			# on comptera les pas de temps
			time = 0
			if verbose:
				print(predecesseurs)
			# tant qu'on a pas sauvé tout le monde
			while nbSauves < nbAEvacuer: # and attentesSommet[nodeId] > 0:
				if verbose:
					print("Il reste " + str(attentesSommet[nodeId]) + " personnes à evacuer")
					print(str(nbSauves) + " sont déjà arrivées")
					print("Les arcs " + str(arcs))
					print("En attente aux sommets avant : " + str(attentesSommet))
				time += 1
				isFirst = True


				# pour chaque noeud du path
				for node in self.evacuationInfo[nodeId]["path"]:
					#si le dernier espace du "couloir" menant au noeud est occupé
					if arcs[node][int(self.getArc(predecesseurs[node], node)["length"])-1] > 0:
						# on met les personne en attente sur le sommet 
						attentesSommet[node] = arcs[node][int(self.getArc(predecesseurs[node], node)["length"])-1]
						# si on est sur le dernier noeud
						if node == lastNode:
							# les personnes sont sauvées
							nbSauves += arcs[node][int(self.getArc(predecesseurs[node], node)["length"])-1]



					#pour toutes les autres parties du couloir
					for i in range(int(self.getArc(predecesseurs[node], node)["length"])-1, 0, -1): 
						arcs[node][i] = arcs[node][i-1]



					# pour le premier espace du couloir menant au noeud
					nbQuiPart = 0
					# Si on est pas sur le dernier noeud (on en voit plus si on y est)
					if predecesseurs[node] != lastNode:
						#si on a du monde en attente au sommet d'avant
						if (int(attentesSommet[predecesseurs[node]]) > int(self.getArc(predecesseurs[node], node)["capacity"])):
							nbQuiPart = int(self.getArc(predecesseurs[node], node)["capacity"])
						else:
							nbQuiPart = int(attentesSommet[predecesseurs[node]])
						if verbose:
							print("On fait partir : " + str(nbQuiPart) + " de " + predecesseurs[node])
						# on envoit le nombre de personne dans le premier espace du couloir
						arcs[node][0] = nbQuiPart
						# les personnes que l'on vient d'envoyer n'attendent plus
						attentesSommet[predecesseurs[node]] -= nbQuiPart
				if verbose:
					print("En attente aux sommets après : " + str(attentesSommet))
					print("-----------")

			times.append(time)
		if verbose:
			print("Les temps : " + str(times))
		return times



	def getArc(self, nodeDepart, nodeDestination):
		return self.graph[nodeDepart][nodeDestination]
