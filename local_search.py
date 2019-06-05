import itertools

from simulator import Simulator
from checker import Checker


class LocalSearch:

	def __init__(self, evacuation_info, graph, start_dates, rates):
		self.evacuation_info = evacuation_info
		self.graph = graph
		self.start_dates = start_dates
		self.rates = rates

	# Pour intensifier à partir d'une solution :
	#	On fait varier le "start_date" de chaque noeud de -6 à +6, par pas de 2
	#	On fait varier le "rate" de chaque noeud de rate_min à rate_max, propre à chaque noeud, par pas de 1
	def intensification(self):
		current_best_solution = {}
		current_best_solution["start_dates"] = self.start_dates
		current_best_solution["rates"] = self.rates
		current_best_solution["value"] = Simulator(self.evacuation_info, self.graph, self.start_dates, self.rates).simulate()

		new_start_dates = self.start_dates
		new_rates = self.rates
		
		# Pour toutes les start_dates
		for current_sd in self.start_dates:
			# On fera des pas de 2 entre -6 et +6
			for i in range(-5, 5, 2):
				# Si la nouvelle start_date est > 0
				if int(self.start_dates[current_sd])+i > 0:
					new_start_dates[current_sd] = int(self.start_dates[current_sd])+i
					# Pour tous les noeds à evacuer
					for r in self.rates:
						# Récupération de la max rate du noeud concerné
						max_rate = int(self.evacuation_info[r]["max_rate"])
						# Pour tous les rates possibles
						for current_rate in (1, max_rate):
							new_rates[r] = current_rate
							# calcul de la nouvelle solution
							new_value = Simulator(self.evacuation_info, self.graph, new_start_dates, new_rates).simulate()
							# verification de la validité de la solution
							infos_solution = {}
							infos_solution["objectif"] = new_value
							infos_solution["evacuation_plan"] = []
							for sd in new_start_dates:
								infos_solution["evacuation_plan"].append({
									'id_node':sd,
									'evacuation_rate':new_rates[sd],
									'start_date':new_start_dates[sd]
									})


							if Checker(self.evacuation_info, self.graph, infos_solution).check():
								if new_value < current_best_solution["value"]:
									current_best_solution["start_dates"] = new_start_dates.copy()
									current_best_solution["rates"] = new_rates.copy()
									current_best_solution["value"] = new_value
		return current_best_solution
		


	# Pour diversifier à partir d'une solution :
	#	On calcule tous les arrangements possible dans l'ensemble des dates de départ
	#	On intensifie à partir de ces dates des départ
	def diversification(self):
		current_best_solution = {}
		current_best_solution["start_dates"] = self.start_dates.copy()
		current_best_solution["rates"] = self.rates.copy()
		current_best_solution["value"] = Simulator(self.evacuation_info, self.graph, self.start_dates, self.rates).simulate()
		

		for arr in itertools.permutations(self.start_dates.values()):
			i = 0
			temp_start_dates = self.start_dates

			for sd in self.start_dates:
				temp_start_dates[sd] = arr[i]
				i += 1

			new_value = LocalSearch(self.evacuation_info, self.graph, temp_start_dates, self.rates).intensification()

			# verification de la validité de la solution
			infos_solution = {}
			infos_solution["objectif"] = new_value["value"]
			infos_solution["evacuation_plan"] = []
			for sd in new_value["start_dates"]:
				infos_solution["evacuation_plan"].append({
					'id_node':sd,
					'evacuation_rate':new_value["rates"][sd],
					'start_date':new_value["start_dates"][sd]
					})

			if Checker(self.evacuation_info, self.graph, infos_solution).check():
				if new_value["value"] < current_best_solution["value"]:

					current_best_solution["start_dates"] = new_value["start_dates"].copy()
					current_best_solution["rates"] = new_value["rates"].copy()
					current_best_solution["value"] = new_value["value"]
			
		return current_best_solution