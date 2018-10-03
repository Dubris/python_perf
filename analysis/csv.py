import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class SetOfParliamentMembers:
	"""Classe Ensemble de députés"""
	def __init__(self, name):
		"""Initialisation de la classe"""
		self.name = name
		self.dataframe = pd.DataFrame()
		
	def data_from_csv(self, path_csv):
		"""Ajouter des députés à partir d'un fichier csv"""
		self.dataframe = pd.read_csv(path_csv, sep=";")
		
	def data_from_dataframe(self, dataframe_source):
		"""Ajouter des députés à partir d'un dataframe"""
		self.dataframe = dataframe_source
		
	def display_chart(self):
		"""Affichage d'un camembert avec la part homme / femme"""
		data = self.dataframe
		nbr_members_male = data[data.sexe == "H"].shape[0]
		nbr_members_female = data[data.sexe == "F"].shape[0]
		counts = np.array([nbr_members_male, nbr_members_female])
		percents = counts / counts.sum()
		
		fig, ax = plt.subplots()
		ax.axis("equal")
		labels = ["Male ({})".format(counts[0]), "Female ({})".format(counts[1])]
		print(counts)
		ax.pie(percents, labels = labels, autopct = "%1.1f percents")
		plt.title("{} ({} members)".format(self.name, counts.sum()))
		plt.show()
		
	def split_by_political_party(self):
		"""Séparer le groupe des députés selon leur parti politique"""
		result = {}
		data = self.dataframe
		political_parties = data["parti_ratt_financier"].dropna().unique()
		
		for pp in political_parties:
			data_subset = data[data.parti_ratt_financier == pp]
			subset = SetOfParliamentMembers('Members from party "{}"'.format(pp))
			subset.data_from_dataframe(data_subset)
			result[pp] = subset
		
		return result


def launch_analysis(name_parliament, data_file, by_party = False):
	directory = os.path.dirname(os.path.dirname(__file__)) # we get the right path.
	path_to_file = os.path.join(directory, "data", data_file) # with this path, we go inside the folder `data` and get the file.

	try:
		parliament_members = SetOfParliamentMembers(name_parliament)
		parliament_members.data_from_csv(path_to_file)
		parliament_members.display_chart()
	
		if by_party == True:
			political_party = parliament_members.split_by_political_party()
			for party, subset in political_party.items():
				subset.display_chart()
				
	except FileNotFoundError as e:
		print("Ow :( The file was not found. Here is the original message of the exception :", e)

	
