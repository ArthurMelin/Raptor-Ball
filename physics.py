###############################################################################
# PHYSICS.PY: Module qui définie des fonctions qui permettent de gérer la     #
#             physique du jeu                                                 #
###############################################################################

# IMPORTATIONS
# Python
import math
# Locales
from constants import *

###############################################################################

# FONCTIONS DU MODULE

# > ComputeMovements(x, y, vx, vy, dt):
# Calcule la nouvelle position d'une entité à partir de son ancienne position,
# de son vecteur vitesse et de la durée écoulée
# Paramètres:
#   x, y: coordonnées précédente de l'entité
#   vx, vy: coordonnées du vecteur vitesse en demi-terrain (unité du repère)
#           par seconde
#   dt: temps écoulé depuis la dernière execution en secondes
def ComputeMovements(x, y, vx, vy, dt):
	# Calcul la nouvelle position de l'entité (en corrigeant les déformations
	# dues au format de la fenêtre
	x += vx * dt
	y += vy * WIN_RATIO * dt

	# Remet l'entité au bord du terrain si elle en a dépassé les limites
	if x < -1.0:
		x = -1.0
	if x > 1.0:
		x = 1.0

	if y < -1.0:
		y = -1.0
	if y > 1.0:
		y = 1.0

	return x, y

# > ComputeDistance(x1, y1, x2, y2):
# Calcule la distance corrigée entre deux points dans le repère du jeu (les
# distances horizontales et verticales ne sont pas forcément uniformes en
# fonction de la forme de la fenêtre du jeu)
# Paramètres:
#   x1, y1: coordonnées du premier point
#   x2, y2: coordonnées du second point
def ComputeDistance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + WIN_RATIO*(y1-y2)**2)

###############################################################################
