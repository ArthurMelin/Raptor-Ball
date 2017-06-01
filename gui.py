###############################################################################
# GUI.PY: Module qui gère l'interface graphique du jeu de façon abstraite     #
#         (menus du jeu, différentes interfaces, etc)                         #
###############################################################################

# IMPORTATIONS
from sdl2 import SDL_Color
# Locales
from constants import *
import display

###############################################################################

# FONCTIONS DU MODULE

# > Init():
# Initialise ce module en chargeant toutes les textures du jeu
def Init():
	print("Chargement des textures... ")

	# Chargement des textures fixes
	display.LoadFixedTextures([
		"field.png",
		"title_screen.png",
		"background_small.png",
		"background_medium.png",
		"background_large.png",
		"chicken/1.png",
		"raptor_blue/1.png",
		"raptor_blue_chicken/1.png",
		"raptor_red/1.png",
		"raptor_red_chicken/1.png"])

	# Chargement des animations avec leur paramètres d'affichage (nombre
	# d'images, temps entre chaque images)
	display.LoadAnimatedTextures([
		["chicken", 8, 0.1],
		["raptor_blue", 6, 0.15],
		["raptor_blue_chicken", 6, 0.175],
		["raptor_blue_dash", 5, 0.1],
		["raptor_blue_spit", 6, 0.1],
		["raptor_red", 6, 0.15],
		["raptor_red_chicken", 6, 0.175],
		["raptor_red_dash", 5, 0.1],
		["raptor_red_spit", 6, 0.1]])

	# Création des textures de texte avec leur paramètres de rendu (police,
	# taille de police, couleur)
	display.LoadLabelTextures([
		["Jouer", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["Règles", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["A propos", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["Quitter", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["Menu principal","MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["Reprendre","MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["Rejouer", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,20)],
		["Pause","MiddleSchoolCrushNBP.ttf", 96, SDL_Color(50,50,50)],
		["Partie terminée", "MiddleSchoolCrushNBP.ttf", 96, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(20,20,200)],
		[" ", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(200,20,20)],
		[" ", "MiddleSchoolCrushNBP.ttf", 64, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 48, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)],
		[" ", "MiddleSchoolCrushNBP.ttf", 32, SDL_Color(50,50,50)]])

	print("Terminé")



# > DrawGame(score, gameTime, paused, positions, playersState):
# Affiche la partie en cours avec les textures du terrain, des joueurs et de la
# balle, ainsi que le menu pause si le jeu est en pause
# Paramètres:
#   score: liste de deux entiers correspondant au score de chaque joueur
#   gameTime: temps en secondes restant dans la partie
#   paused: booléen indiquant si le jeu est en pause
#   positions: tableau contenant les coordonnées et orientation des joueurs
#   playersState: tableau contenant l'état de chaque joueur
def DrawGame(score, gameTime, paused, positions, playersState):
	# Affiche le fond (terrain de jeu)
	display.DrawFixedTexture(TFX_FIELD, 0, 0, WIN_WIDTH, WIN_HEIGHT, 0.0)

	# Plusieurs tableaux associant des valeurs données en indices à des
	# constantes correspondants à ces valeurs :
	# tfx_map: id du joueur -> texture fixe correspondante
	# ani_map: id du joueur -> animation correspondante
	# sz_map: id du joueur -> taille de la texture en pixels correspondante
	# var_map: état de joueur -> variation de texture correspondante
	tfx_map = [TFX_RAPTRB, TFX_RAPTRR, TFX_CHICKN]
	ani_map = [ANI_RAPTRB, ANI_RAPTRR, ANI_CHICKN]
	sz_map = [256, 256, 128]
	var_map = [0, 0, V_ANI_DASH, V_ANI_SPIT, V_ANI_CHIC, V_ANI_CHIC, -1, -1]

	# Affiche chaque joueur (on considère la balle comme un joueur)
	for player in [BALL, PLAYER1, PLAYER2]:
		# Si le joueur est la balle et qu'elle est tenu, ne l'affiche pas
		if player == BALL and playersState[player] & 4 == PS_HOLD:
			continue

		# Si le joueur est immobile, affiche la texture figée correspondant à
		# son id (player) et son état (playersState). On traduit par ailleurs
		# sa position dans le repère du jeu en position réelle sur l'écran en
		# pixels
		if playersState[player] & 3 == PS_STOP:
			display.DrawFixedTexture(tfx_map[player] + \
			var_map[playersState[player]],
			int(((1.0+positions[player][POS_X])*WIN_WIDTH-sz_map[player])/2),
			int(((1.0-positions[player][POS_Y])*WIN_HEIGHT-sz_map[player])/2),
			sz_map[player], sz_map[player], positions[player][POS_ANGLE])
		# Si le joueur marche, affiche l'animation correspondante de la même
		# manière que pour le cas précédent
		else:
			display.DrawAnimatedTexture(ani_map[player] + \
			var_map[playersState[player]],
			int(((1.0+positions[player][POS_X])*WIN_WIDTH-sz_map[player])/2),
			int(((1.0-positions[player][POS_Y])*WIN_HEIGHT-sz_map[player])/2),
			sz_map[player], sz_map[player], positions[player][POS_ANGLE])

	# Met à jour les textures de texte de score et de temps avec les valeurs
	# actuelles
	display.UpdateLabelTexture(LBL_SCOREP1, str(score[PLAYER1]))
	display.UpdateLabelTexture(LBL_TIMER, "{0}:{1:0>2}".format(
		int(gameTime/60), int(gameTime%60)))
	display.UpdateLabelTexture(LBL_SCOREP2, str(score[PLAYER2]))

	# Affiche le score et le temps restant
	display.DrawFixedTexture(TFX_BCKGDS,
		int((WIN_WIDTH-512)/2), -16, 512, 96, 0.0)
	display.DrawLabelTexture(LBL_SCOREP1, int(WIN_WIDTH/2)-200, 40, 0.0)
	display.DrawLabelTexture(LBL_TIMER, int(WIN_WIDTH/2), 40, 0.0)
	display.DrawLabelTexture(LBL_SCOREP2, int(WIN_WIDTH/2)+200, 40, 0.0)

	# Si le jeu est en pause, affiche le menu de pause
	if paused:
		# Fond du menu et des boutons
		display.DrawFixedTexture(TFX_BCKGDM,
			int((WIN_WIDTH-640)/2), int((WIN_HEIGHT-384)/2), 640, 384, 0.0)
		display.DrawFixedTexture(TFX_BCKGDS,
			int((WIN_WIDTH-512)/2), int(WIN_HEIGHT/2-48), 512, 96, 0.0)
		display.DrawFixedTexture(TFX_BCKGDS,
			int((WIN_WIDTH-512)/2), int(WIN_HEIGHT/2+72), 512, 96, 0.0)

		# Titre du menu et textes des boutons
		display.DrawLabelTexture(LBL_PAUSE, int(WIN_WIDTH/2),
			int(WIN_HEIGHT/2-120), 0.0)
		display.DrawLabelTexture(LBL_RESUME, int(WIN_WIDTH/2),
			int(WIN_HEIGHT/2), 0.0)
		display.DrawLabelTexture(LBL_TITLESCR, int(WIN_WIDTH/2),
			int(WIN_HEIGHT/2+120), 0.0)

	display.DrawWindow()


# > DrawGameOverScreen(score, gameTime):
# Affiche l'écran de fin de partie avec le score de chaque joueur, un message
# indiquant le vainqueur de la partie, et 2 boutons
# Paramètres:
#   score: tableau contenant le score de chaque joueur
#   gameTime: décompte du temps restant de la partie avant qu'elle ne soit
# terminée
def DrawGameOverScreen(score, gameTime):
	# Affiche le fond de terrain
	display.DrawFixedTexture(TFX_FIELD, 0, 0, WIN_WIDTH, WIN_HEIGHT, 0.0)

	# Composition du message à afficher selon la partie
	gameover_msg = ""
	# Si le temps restant est à 0 ou moins, la partie a atteint la limite de
	# temps
	if gameTime <= 0.0:
		gameover_msg += "Temps ecoulé! "
	# Le joueur ayant le plus de points gagne
	if score[PLAYER1] > score[PLAYER2]:
		gameover_msg += "Le joueur 1 a gagné!"
	elif score[PLAYER1] < score[PLAYER2]:
		gameover_msg += " Le joueur 2 a gagné!"
	# Si les 2 joueurs ont le même score, le match est nul
	else:
		gameover_msg += "Match nul!"

	# Mise à jour de la texture avec le message de fin de partie
	display.UpdateLabelTexture(LBL_GOVERMSG, gameover_msg)

	# Fond du menu et des boutons
	display.DrawFixedTexture(TFX_BCKGDL, int((WIN_WIDTH-1024)/2),
		int((WIN_HEIGHT-512)/2), 1024, 512, 0.0)
	display.DrawFixedTexture(TFX_BCKGDS, int((WIN_WIDTH-512)/2),
		int((WIN_HEIGHT-512)/2)+272, 512, 96, 0.0)
	display.DrawFixedTexture(TFX_BCKGDS, int((WIN_WIDTH-512)/2),
		int((WIN_HEIGHT-512)/2)+384, 512, 96, 0.0)

	# Titre du menu, scores des joueurs, message de fin de partie et texte
	# des boutons
	display.DrawLabelTexture(LBL_GAMEOVER, int(WIN_WIDTH/2),
		int((WIN_HEIGHT-512)/2)+64, 0.0)
	display.DrawLabelTexture(LBL_SCOREP1, int(WIN_WIDTH/2)-48,
		int((WIN_HEIGHT-512)/2)+160, 0.0)
	display.DrawLabelTexture(LBL_SCOREP2, int(WIN_WIDTH/2)+48,
		int((WIN_HEIGHT-512)/2)+160, 0.0)
	display.DrawLabelTexture(LBL_GOVERMSG, int(WIN_WIDTH/2),
		int((WIN_HEIGHT-512)/2)+224, 0.0)
	display.DrawLabelTexture(LBL_NEWGAME, int(WIN_WIDTH/2),
		int((WIN_HEIGHT-512)/2)+320, 0.0)
	display.DrawLabelTexture(LBL_TITLESCR, int(WIN_WIDTH/2),
		int((WIN_HEIGHT-512)/2)+432, 0.0)

	display.DrawWindow()



# > DrawTitleScreen(button_x_pos, button_y_pos):
# Affiche l'écran titre du jeu avec un fond et 4 boutons et le texte des menus
# correspondant
# Paramètres:
#   button_x_pos: position horizontale des boutons du menu
#   button_y_pos: tableau des positions verticales des 4 boutons
def DrawTitleScreen(button_x_pos, button_y_pos):
	# Fond de l'écran titre
	display.DrawFixedTexture(TFX_TTLSCR, 0, 0, WIN_WIDTH, WIN_HEIGHT, 0.0)

	# Tableau mettant les textures des textes de boutons du menu dans l'ordre
	# pour être affiché dans la boucle for
	lbl_map = [LBL_PLAY, LBL_RULES, LBL_ABOUT, LBL_QUIT]

	# Pour chaque bouton, affiche son fond et son texte
	for i in range(4):
		display.DrawFixedTexture(TFX_BCKGDS, button_x_pos, button_y_pos[i],
			512, 96, 0.0)
		display.DrawLabelTexture(lbl_map[i],
			button_x_pos + 256, button_y_pos[i] + 48, 0.0)

	display.DrawWindow()



# > DrawTextScreen():
# Affiche un menu de texte (règles ou à propos). Il faut d'abord générer les
# textures de texte avec UpdateTextScreenLabel().
def DrawTextScreen():
	# Affiche le fond du menu principal
	display.DrawFixedTexture(TFX_TTLSCR, 0, 0, WIN_WIDTH, WIN_HEIGHT, 0.0)

	# Position verticale du fond dans la fenêtre
	y_pos = int(WIN_HEIGHT*456/720-256)

	# Affiche un fond pour le texte
	display.DrawFixedTexture(TFX_BCKGDL, int((WIN_WIDTH-1024)/2),
		y_pos, 1024, 512, 0.0)
	# Affiche le fond du bouton de retour au menu principal
	display.DrawFixedTexture(TFX_BCKGDS, int((WIN_WIDTH-512)/2),
		y_pos+400, 512, 96, 0.0)

	# Affiche chaque ligne du texte
	for i in range(12):
		display.DrawLabelTexture(LBL_TEXTSCR + i, int(WIN_WIDTH/2),
			y_pos+32*(i+1), 0.0)

	# Affiche le texte du bouton de retour au menu principal
	display.DrawLabelTexture(LBL_TITLESCR, int(WIN_WIDTH/2), y_pos+448,
		0.0)

	display.DrawWindow()



# > UpdateTextScreenLabel(text):
# Génère les textures de texte des menus textes (règles ou à propos)
# Paramètre:
#   text: texte du menu à afficher
def UpdateTextScreenLabels(text):
	# Sépare les lignes du texte (les textures de textes ne peuvent faire
	# qu'une ligne chacune)
	lines = text.splitlines()
	# Complète la liste lines avec des lignes vides pour qu'il y en ait 12
	for i in range(12 - len(lines)):
		lines.append(" ")
	# Génère les textures de textes en remplaçant
	for i in range(12):
		display.UpdateLabelTexture(LBL_TEXTSCR + i, lines[i])

###############################################################################

# FONCTIONS INTERFACES INTER-MODULES

# > OpenWindow():
# Demande à display d'ouvrir la fenêtre du jeu
def OpenWindow():
	display.OpenWindow()

# > CloseWindow():
# Demande à display de fermer la fenêtre du jeu et de libérer la mémoire
# utilisée par les textures du jeu
def CloseWindow():
	display.CloseWindow()

# > WindowIsOpen():
# Détermine si la fenêtre du jeu est ouverte ou non en comparant la globale
# Window avec None (valeur initiale)
def WindowIsOpen():
	return display.Window != None and display.RendererReady

# > ToggleFullscreen():
# Active ou désactive le mode plein-écran du jeu
def ToggleFullscreen():
	display.ToggleFullscreen()

###############################################################################
