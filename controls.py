###############################################################################
# CONTROLS.PY: Module-thread qui gère les contrôles (clavier, souris) et les  #
#              associent à des fonctions ou à des variables                   #
###############################################################################

# IMPORTS
# Python
from threading import Thread
import math, time
# PySDL2
from sdl2 import *
# Locales
from constants import *
import game, ui

###############################################################################

# GLOBALE
# Tableau constitué de deux tableaux contenant des variables correspondant aux
# contrôles des joueurs (vecteur vitesse + état de la touche action)
PlayersControls = [[(0.0, 0.0), False], [(0.0, 0.0), False]]

###############################################################################

# FONCTIONS DU MODULE

# > Init():
# Initialise le module et le Thread lui correspondant en lui indiquant la
# fonction Run() qu'il doit exécuter et son nom
def Init():
	return Thread(target=Run, name="ControlsThread")

# > Quit():
# Libère les ressources employées par ce module et ses sous-modules
# Ce module ne consommant aucune ressource pouvant être libérée, cette fonction
# ne fait rien (elle doit cependant être présente)
def Quit():
	pass

# > Run():
# Fonction exécutée par le thread de ce module lorsqu'il est démarré
def Run():
	# Initialisation du sous-système vidéo de la SDL via le module UI
	ui.InitSDLVideoSubSystem()

	# SDL_Event représentant un évenement
	Event = SDL_Event()

	while game.Running:
		# Tant qu'il y'a un évènement dans la file d'attente, on le traite
		while SDL_PollEvent(Event) != 0:
			# L'évènenement est un évènement de type clavier (changement de
			# l'état d'une touche du clavier)
			if (Event.type == SDL_KEYDOWN or Event.type == SDL_KEYUP) \
			and Event.key.repeat == 0:

				# Variable indiquant l'état de la touche qui vient de changer
				# d'état
				# (KS_RELEASED=False : relâchée, True=KS_PRESSED : enfoncée)
				keystate = bool(Event.key.state)

				# Touche Echap: entrée ou sortie du mode pause du jeu
				if Event.key.keysym.sym == SDLK_ESCAPE \
				and keystate == KS_RELEASED:
					# Selon l'état actuel du jeu on met en pause ou reprend le
					# jeu
					if game.GameState == GS_PLAYING:
						game.GameState = GS_PAUSED
					elif game.GameState == GS_PAUSED:
						game.GameState = GS_PLAYING

				# Touche F11: activation/désactivation du mode plein-écran
				if Event.key.keysym.sym == SDLK_F11 \
				and keystate == KS_RELEASED:
					ui.ToggleFullscreen()

				# Quelquesoit la touche qui a changé d'état, on récupère l'état
				# de tout le clavier
				kbstate = SDL_GetKeyboardState(None)

				# Tableau qui contiendra l'état des 4 touches directionnelles
				# d'un joueur)
				Keys = [False, False, False, False]

				# JOUEUR 1: WASD (ZQSD sur un clavier AZERTY) + Espace
				# Récupération de l'état de chaque touche directionnelle
				Keys[KEY_UP] = bool(kbstate[SDL_SCANCODE_W])
				Keys[KEY_LEFT] = bool(kbstate[SDL_SCANCODE_A])
				Keys[KEY_DOWN] = bool(kbstate[SDL_SCANCODE_S])
				Keys[KEY_RIGHT] = bool(kbstate[SDL_SCANCODE_D])
				# Traduction de l'état des touches directionnelles en vecteur
				# vitesse sauvegardé dans PlayersControls
				PlayersControls[PLAYER1][PC_VELOCT] = TranslateKbInput(Keys)
				# Sauvegarde de l'état de la touche action (Espace) dans
				# PlayersControls
				if Event.key.keysym.sym == SDLK_SPACE:
					PlayersControls[PLAYER1][PC_ACTION] = keystate

				# JOUEUR 2 : Touches fléchées + 0 (Pavé numérique)
				# Idem que pour le joueur 1 mais avec des touches différentes
				Keys[KEY_UP] = bool(kbstate[SDL_SCANCODE_UP])
				Keys[KEY_LEFT] = bool(kbstate[SDL_SCANCODE_LEFT])
				Keys[KEY_DOWN] = bool(kbstate[SDL_SCANCODE_DOWN])
				Keys[KEY_RIGHT] = bool(kbstate[SDL_SCANCODE_RIGHT])
				PlayersControls[PLAYER2][PC_VELOCT] = TranslateKbInput(Keys)
				if Event.key.keysym.sym == SDLK_KP_0:
					PlayersControls[PLAYER2][PC_ACTION] = keystate

			# L'évènement est un clic gauche de souris
			if Event.type == SDL_MOUSEBUTTONUP \
			and Event.button.button == SDL_BUTTON_LEFT:
				# Transfert des informations sur la position de la souris lors
				# du clic à l'interface utilisateur actuellement affichée
				ui.CurrentUi.OnClick(Event.button.x, Event.button.y)

			# Gestion des évènements liés à la fenêtre du jeu
			if Event.type == SDL_WINDOWEVENT:
				# Bouton de fermeture de fenêtre: arrêt du jeu
				if Event.window.event == SDL_WINDOWEVENT_CLOSE:
					game.Running = False

		# On laisse les ressources processeur utilisée par ce thread à d'autres
		# threads du programme puisque la file d'attente est vide
		time.sleep(WAIT_TIME)

# > TranslateKbInput(keys):
# Traduit un tableau de 4 booléens correspondants aux touches de déplacement
# d'un joueur en un vecteur vitesse
# Paramètre:
#   keys: tableau de 4 booléens correspondant à l'état des touches
#         directionnelles d'un joueur dans l'ordre Haut, Bas, Gauche, Droite
def TranslateKbInput(keys):
	# Si aucune touche n'est pressée ou que les directions pressées s'annulent,
	# retourne un vecteur vitesse nul
	if keys[KEY_UP] == keys[KEY_DOWN] and keys[KEY_LEFT] == keys[KEY_RIGHT]:
		return (0.0, 0.0)

	# Traduit l'état de chaque touche appuyées ou non en coordonnées d'un point
	# (x,y) dans un repère
	x, y = 0, 0
	if keys[KEY_UP]:
		y += 1
	if keys[KEY_DOWN]:
		y -= 1
	if keys[KEY_LEFT]:
		x -= 1
	if keys[KEY_RIGHT]:
		x += 1

	# Calcul l'angle formé entre l'axe horizontal et la demi-droite dont
	# l'extrémité est l'origine# (0;0) du repère et qui passe par le point
	# (x,y)
	h = math.sqrt(x**2 + y**2)
	angle = math.acos(x/h)

	# Corrige la valeur calculée de l'angle s'il se trouve sous l'axe
	# horizontal en le rendant négatif
	if y < 0:
		angle = -angle

	# Retourne un vecteur vitesse avec l'angle calculé et une norme fixée à 1
	return (angle, 1.0)

###############################################################################
