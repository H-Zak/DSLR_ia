import numpy as np


# il faut creer des matrices:
# 	- une  qui detient les entrees(les notes des colonnes choisis)
# 	- une qui correspond au poids(il  faut nb_cours + 1 pour la constante) il en faut une par maison
#	- une matrice avec les sorties avec de calculer les couts d'erreur

#Matrice:
	# - Theta
	# - X : feature (note des cours)
	# - h : les resultats de sigmoids
	# - y : les resultats que l'on doit obtenir
# def loss_cost():
# 	print("cout de la perte")

alpha = 0.01
num_iter = 1000

def descent_gradient(X, y, theta, num_iter):
	for i in range(num_iter):
		theta -= alpha * gradient(X, y , theta)
	print("start gradient")

def gradient(X, y , theta):
	print("start here")
	m =len(y)
	h = sigmoid(X * theta)
	return (1/m) *  X.T @ (h - y)
def sigmoid(z):
	print("strat calcul sigmoid")
	return (1/ (1+ np.exp(-z)))

# def zscore():#possiblement necessaire pour mieux calculer la probabilite avec sigmoid
# 	print("zscore")

# def calcul_lineaire():
# 	print("start lineaire")



