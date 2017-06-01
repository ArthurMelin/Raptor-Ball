###############################################################################
# GAME.PY: Module-thread qui gère le jeu en lui-même (position des joueurs et #
#          de la balle, score, etc)                                           #
###############################################################################

# IMPORTATIONS
# Python
from threading import Thread
import math, random, time
# Locales
from constants import *
import controls, ui
import physics

###############################################################################

# GLOBALES
# Thread de ce module (utilisé par Main)
GameThread = None

# Booléen indiquant si le programme est en cours d'exécution ou arrêté
Running = False
# Etat du jeu (hors du jeu / en jeu / jeu en pause)
GameState = GS_NPLAYING
# Score des joueurs
Score = [0,0]
# Temps restant de la partie en secondes
GameTime = 0.0
# Tableau des positions et orientations des joueurs et de la balle
Positions = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
# Etat des joueurs et de la balle (figé / marche / attaque / etc.)
PlayersState = [PS_STOP, PS_STOP, PS_STOP]

###############################################################################

# FONCTIONS DU MODULE

# > Init():
# Initialise le module et le Thread lui correspondant en lui indiquant la
# fonction Run() qu'il doit exécuter et son nom
def Init():
	global GameThread
	GameThread = Thread(target=Run, name="GameThread")
	return GameThread


# > Quit():
# Libère les ressources employées par ce module et ses sous-modules
def Quit():
	pass
	

# > SetPS_Mode(player, mode):
# Change la valeur PlayersState d'un joueur (hors PS_HOLD)
# Paramètres:
#   player: joueur concernée (PLAYER1, PLAYER2 ou BALL)
#   mode: valeur d'état à attribuer au joueur (PS_STOP, PS_WALK, PS_DASH ou
#         PS_SPIT mais pas PS_HOLD)
def SetPS_Mode(player, mode):
	global PlayersState
	# Utilisation d'un ET binaire pour garder le 3eme bit de PlayersState 
	# correspondant à PS_HOLD et remettre à 0 les autres bits
	PlayersState[player] &= PS_HOLD
	# Utilisation d'un OU binaire pour ajouter à PlayersState la nouvelle
	# valeur d'état
	PlayersState[player] |= mode

	
# > SetPS_Hold(player, hold):
# Change la valeur PlayersState d'un joueur (uniquement PS_HOLD)
# Paramètres:
#   player: joueur concernée (PLAYER1, PLAYER2 ou BALL)
#   hold: nouvelle état de PS_HOLD à attribuer au joueur
def SetPS_Hold(player, hold):
	global PlayersState
	# Utilise un ET et un OU binaire pour remplacer la valeur de PS_HOLD tout
	# en gardant les autres bits de la variable dans le même état
	PlayersState[player] = hold | (PlayersState[player] & 3)


# > Run():
# Fonction exécutée par le thread de ce module lorsqu'il est démarré
def Run():
	global Running, GameState, Score, GameTime, Positions, PlayersState
	Running = True

	# Tant que le jeu est en cours d'exécution
	while Running:
		# Attente du démarrage d'une partie ou de la fermeture du jeu
		while Running and GameState == GS_NPLAYING:
			time.sleep(WAIT_TIME)

		# Initialisation des globales pour une nouvelle partie
		Score = [0,0] # Score nul
		GameTime = float(3 * 60) # 3 minutes de jeu
		Positions = [[-2/3,0.0,0.0], [2/3,0.0,math.pi], [0.0, 0.0, math.pi/2]]
		PlayersState = [PS_STOP, PS_STOP, PS_STOP]
		
		# Initialisation de variable locales
		# DashCooldowns: tableau contenant un décompte pour chaque joueur qui
		# permet de limiter leur usage de l'attaque
		DashCooldowns = [0.0, 0.0]
		# SpitCooldowns: tableau contenant une décompte pour chaque joueur qui
		# permet de les immobiliser temporairement après qu'ils aient été 
		# attaqués
		SpitCooldowns = [0.0, 0.0]
		# BallCooldowns: décompte permettant d'empêcher la balle d'être
		# attrapée directement après avoir été relachée
		BallCooldown = 0.0
		# Coordonnées sur le terrain vers lesquelles la balle se déplace quand
		# elle n'est pas tenue
		BallTarget = [0.0, 0.0]

		# Attends 3 secondes pour démarrer la partie si le jeu n'est pas fermé
		# (sauf si le jeu a été fermé)
		if Running:
			time.sleep(3)

		LastTick = time.time()
		# Tant que le jeu n'est pas fermé et qu'une partie est en cours
		# (ou en pause)
		while Running and GameState != GS_NPLAYING:
			# Si le jeu n'est pas en pause
			if GameState == GS_PLAYING:
				# Calcule la différence de temps qui s'est écoulée depuis la
				# dernière exécution de cette boucle
				DeltaTime = time.time() - LastTick

				# Décrémente les décomptes du jeu non associés à un joueur
				BallCooldown -= DeltaTime
				GameTime -= DeltaTime
				# Si le temps restant est 0 ou moins, termine la partie et
				# affiche l'écran de fin de partie
				if GameTime <= 0.0:
					GameState = GS_NPLAYING
					ui.CurrentUi = ui.UiGameOverScreen()

				# Pour chacun des joueurs (ordre du tableau aléatoire pour
				# éviter qu'un des joueurs est toujours la priorité sur ses
				# actions)
				players = [PLAYER1, PLAYER2]
				random.shuffle(players)
				for player in players:
					# Décrémente les décomptes du jeu associés à un joueur
					DashCooldowns[player] -= DeltaTime
					SpitCooldowns[player] -= DeltaTime

					# Copie la position, l'orientation et le vecteur vitesse du
					# joueur dans des variables plus faciles à utiliser
					x, y = Positions[player][POS_X], Positions[player][POS_Y]
					angle = Positions[player][POS_ANGLE]
					v_vec = controls.PlayersControls[player][PC_VELOCT]

					# Si le joueur a sa touche Action enfoncée, qu'il a un état
					# Marche, ne tient pas la balle et a son décompte pour
					# utiliser l'attaque à 0 ou moins, fait attaquer le joueur
					if controls.PlayersControls[player][PC_ACTION] \
					and PlayersState[player] == PS_WALK \
					and DashCooldowns[player] <= 0.0:
						# Réinitialisation de l'état de la touche action pour
						# empêcher le joueur d'attaquer automatiquement en
						# gardant la touche enfoncée
						controls.PlayersControls[player][PC_ACTION] = False
						# Réinitialise le décompte d'attaque du joueur
						DashCooldowns[player] = CDOWN_DASH

					# Si le joueur a été attaqué (décompte non terminé)
					if SpitCooldowns[player] > 0.0:
						# Si le joueur a été attaqué il y a plus de 0.5 s,
						# le joueur prend un état Immobile
						if SpitCooldowns[player] < CDOWN_SPIT - 0.5:
							SetPS_Mode(player, PS_STOP)
						# Sinon le joueur a un état de Perte de la balle
						# (permet d'afficher l'animation correspondante)
						else:
							SetPS_Mode(player, PS_SPIT)
					# Sinon si le joueur a un vecteur vitesse nul
					elif v_vec[VEC_NORM] == 0.0:
						# Le joueur a un état Immobile
						SetPS_Mode(player, PS_STOP)
					# Sinon
					else:
						# Définit le coefficient normal de la vitesse du joueur
						v_multiplier = 0.3
						# Le joueur a un état Marche
						SetPS_Mode(player, PS_WALK)

						# Si le joueur a attaqué il y a moins de 0.5s et qu'il
						# ne tient pas la balle
						if DashCooldowns[player] > CDOWN_DASH - 0.5 \
						and not PlayersState[player] & PS_HOLD:
							# Augmente le coeffiecient de vitesse du joueur
							# (accélération)
							v_multiplier = 0.5
							# L'état du joueur devient Attaque
							SetPS_Mode(player, PS_DASH)
						
						# Si le joueur tient la balle
						if PlayersState[player] & PS_HOLD:
							# Diminue le coefficient de vitesse du joueur
							# (Ralentissement)
							v_multiplier = 0.25

						# Calcule de la vitesse du joueur
						v = v_vec[VEC_NORM] * v_multiplier
						# Copie de l'angle du déplacement du joueur
						angle = v_vec[VEC_ANGLE]
						# Calcul des coordonnées du vecteur vitesse du joueur
						vx, vy = v * math.cos(angle), v * math.sin(angle)
						# Calcul de la nouvelle position du joueur
						x, y = physics.ComputeMovements(x,y, vx,vy, DeltaTime)
						# Sauvegarde de la position et de l'orientation du
						# joueur dans Positions
						Positions[player] = [x, y, angle]

						# Tableau associant à chaque joueur son adversaire
						opponent = [PLAYER2, PLAYER1]
						# Copie de la position et de l'orientation du joueur
						# adverse
						o_x = Positions[opponent[player]][POS_X]
						o_y = Positions[opponent[player]][POS_Y]
						o_angle = Positions[opponent[player]][POS_ANGLE]
						# Si le joueur est en état Attaque, que son adversaire
						# tient la balle et qu'ils sont assez proches
						if PlayersState[player] & 3 == PS_DASH \
						and PlayersState[opponent[player]] & PS_HOLD \
						and physics.ComputeDistance(x,y, o_x,o_y) <= 0.2:
							# L'adversaire perd la balle
							SetPS_Hold(opponent[player], 0)
							SetPS_Mode(opponent[player], PS_SPIT)
							# Réinitialise le décompte d'immobilisation de
							# l'adversaire
							SpitCooldowns[opponent[player]] = CDOWN_SPIT
							# Calcul une position pour la balle en la plaçant
							# devant l'adversaire
							b_x = o_x + 0.25*math.cos(o_angle)
							b_y = o_y + 0.25*WIN_RATIO*math.sin(o_angle)
							# Sauvegarde la nouvelle position de la balle dans
							# Positions
							Positions[BALL] = [b_x, b_y, o_angle]
							# La balle n'est plus tenue
							SetPS_Hold(BALL, 0)
							# Réinitialisation du décompte de la balle
							BallCooldown = CDOWN_BALL

						# Si la balle n'est pas tenue
						if not PlayersState[BALL] & PS_HOLD:
							# Copie de la position de la balle
							b_x = Positions[BALL][POS_X]
							b_y = Positions[BALL][POS_Y]
							# Si la balle est proche du joueur et que son
							# décompte est à 0 ou moins
							if physics.ComputeDistance(x,y, b_x,b_y) < 0.2 \
							and BallCooldown <= 0.0:
								# Le joueur prend un état Marche
								SetPS_Mode(player, PS_WALK)
								# et tient la balle
								SetPS_Hold(player, PS_HOLD)
								# Et la balle est tenue
								SetPS_Hold(BALL, PS_HOLD)
						# Sinon si le joueur tient la balle
						elif PlayersState[player] & PS_HOLD:
							# Tableau qui contient les limites horizontales des
							# buts adverses de chaque joueur
							Goal = [[0.9, 1.0], [-1.0, -0.9]]
							# Si le joueur se trouve dans les limites des buts
							# du joueur adverse
							if Goal[player][0] <= x <= Goal[player][1]:
								# Le joueur gagne un point
								Score[player] += 1
								# Attente d'1 seconde pour indiquer la prise en
								# compte du but aux joueurs
								time.sleep(1)
								
								# Réinitialise les positions des joueurs, leur
								# état, les décomptes et la cible de la balle
								Positions = [[-2/3,0.0,0.0], [2/3,0.0,math.pi],
									[0.0, 0.0, math.pi/2]]
								PlayersState = [PS_STOP, PS_STOP, PS_STOP]
								DashCooldowns = [0.0, 0.0]
								SpitCooldowns = [0.0, 0.0]
								BallCooldown = 0.0
								BallTarget = [0.0, 0.0]

								# Si le joueur a 3 points, termine la partie et
								# affiche l'écran de fin de partie
								if Score[player] == 3:
									GameState = GS_NPLAYING
									ui.CurrentUi = ui.UiGameOverScreen()
								# Sinon, attente d'1 seconde avant la reprise
								# du jeu
								else:
									time.sleep(1)
				
				# Si la balle n'est pas tenue
				if not PlayersState[BALL] & PS_HOLD:
					# Copie de la position de la balle
					x, y = Positions[BALL][POS_X], Positions[BALL][POS_Y]
					# Tant que la balle est proche de sa cible
					while physics.ComputeDistance(x,y,
						BallTarget[0],BallTarget[1]) <= 0.1:
						# Génération aléatoire d'une nouvelle cible au milieu
						# du terrain pour la balle
						BallTarget[0] = 0.4*random.random() - 0.2
						BallTarget[1] = 2.0*random.random() - 1.0
					
					# Calcul de la distance entre la balle et sa cible
					h = physics.ComputeDistance(x,y,
						BallTarget[0], BallTarget[1])
					# Calcul de l'orientation que la balle doit avoir pour se
					# diriger vers sa cible
					angle = math.acos((BallTarget[0]-x)/h)
					# Correction de la mesure de l'angle si la cible est en
					# dessous de la balle
					if y > BallTarget[1]:
						angle = -angle

					# Calcul des coordonnées du vecteur vitesse de la balle
					vx, vy = 0.2 * math.cos(angle), 0.2 * math.sin(angle)
					# Calcul de la nouvelle position de la balle
					x, y = physics.ComputeMovements(x,y, vx,vy, DeltaTime)
					# Sauvegarde de la nouvelle position et orientation dans
					# Positions
					Positions[BALL] = [x, y, angle]
					# L'état de la balle est Marche
					SetPS_Mode(BALL, PS_WALK)

			# Enregistrement de la date de la dernière exécution de la boucle
			LastTick = time.time()
			# Attente permettant de réduire l'utilisation du processeur
			time.sleep(WAIT_TIME)

###############################################################################
