###############################################################################
# UI.PY: Module-thread qui gère l'interface utilisateur (fenêtre, graphismes) #
###############################################################################

# IMPORTATIONS
# Python
from threading import Thread
import time
# Locales
from constants import *
import game, controls
import gui

###############################################################################

# GLOBALES
# Instance d'une classe hérité de la classe de base Ui associé à un type
# d'interface utilisateur
CurrentUi = None

###############################################################################

# FONCTIONS DU MODULE

# > Init():
# Initialise le module et le Thread lui correspondant en lui indiquant la
# fonction Run() qu'il doit exécuter et son nom
def Init():
	return Thread(target=Run, name="UiThread")

# > Quit():
# Libère les ressources employées par ce module et ses sous-modules
def Quit():
	gui.CloseWindow()

# > Run():
# Fonction exécutée par le thread de ce module lorsqu'il est démarré
def Run():
	global CurrentUi

	# Attend que ControlsThread crée la fenêtre avec InitSDLVideoSubSystem()
	while not gui.WindowIsOpen():
		time.sleep(WAIT_TIME)

	# Initialise le module gui du jeu
	gui.Init()

	# Définit la première interface utilisateur à être affichée à l'écran comme
	# étant le menu principal (écran titre)
	CurrentUi = UiTitleScreen()

	# Dessine indéfiniment l'interface utilisateur décrite par la classe dont
	# l'instance est définie dans CurrentUi, tant que le jeu est executé.
	while game.Running:
		CurrentUi.Draw()



# > CheckMousePosition(x, y, x1, y1, x2, y2):
# Renvoie True si la souris en coordonnées x,y se trouve dans un rectangle dont
# le coin supérieur gauche a pour coordonnées x1,y1 et le coin inférieur droit
# a pour coordonnées x2, y2
# Paramètres:
#   x,y: coordonnées de la souris dans la fenêtre
#   x1,y1: coordonnées du coin supérieur gauche du rectangle
#   x2,y2: coordonnées du coin inférieur droit du rectangle
def CheckMousePosition(x, y, x1, y1, x2, y2):
	return x1 <= x <= x2 and y1 <= y <= y2

###############################################################################

# CLASSES INTERFACES UTILISATEURS

# Classe Ui: base de toutes les autres classes décrivant des interfaces
# utilisateurs
class Ui:
	# Fonction qui déclenche l'affichage d'une interface utilisateur
	# correspondante à la classe
	def Draw(self):
		pass
	# Fonction appelée par controls quand l'utilisateur clique sur la fenêtre,
	# traîte le clic sur l'interfacce selon la classe
	def OnClick(self, x, y):
		pass


# Classe UiGame: interface affichée lors d'une partie
class UiGame(Ui):
	# Utilise gui.DrawGame pour afficher dans la fenêtre le terrain, les
	# joueurs, la balle, le score et le temps restant ainsi que le menu pause
	# lorsque le jeu est en pause.
	def Draw(self):
		gui.DrawGame(game.Score, game.GameTime, game.GameState == GS_PAUSED,
			game.Positions, game.PlayersState)
	
	# Lorsque le jeu est en pause, réagit aux clics sur le menu pause
	def OnClick(self, x, y):
		global CurrentUi
		
		if game.GameState == GS_PAUSED:
			if CheckMousePosition(x,y, (WIN_WIDTH-512)/2, WIN_HEIGHT/2-48,
			(WIN_WIDTH-512)/2+512, WIN_HEIGHT/2+48):
				# Bouton 'Reprendre' -> la variable d'état du jeu reprend la
				# valeur indiquant que le jeu est en cours
				game.GameState = GS_PLAYING
			elif CheckMousePosition(x,y, (WIN_WIDTH-512)/2, WIN_HEIGHT/2+72,
			(WIN_WIDTH-512)/2+512, WIN_HEIGHT/2+168):
				# Bouton 'Menu principal' -> l'interface affichée à l'écran
				# devient l'écran titre et la variable d'état de jeu prend la
				# valeur indiquant qu'aucune partie n'est en cours
				CurrentUi = UiTitleScreen()
				game.GameState = GS_NPLAYING


# Classe UiGameOverScreen: interface de fin de partie
class UiGameOverScreen(Ui):
	# Utilise gui.DrawGameOverScreen pour afficher le menu de fin de partie en
	# lui passant le score et le temps restant de la partie
	def Draw(self):
		gui.DrawGameOverScreen(game.Score, game.GameTime)

	# Réagit à un clic sur l'un des boutons du menu
	def OnClick(self, x, y):
		global CurrentUi
		
		# Bouton 'Nouvelle partie' -> l'interface affichée devient celle du
		# jeu, la variable d'état de jeu prend une valeur indiquant
		# qu'une partie est en cours
		if CheckMousePosition(x,y, (WIN_WIDTH-512)/2, (WIN_HEIGHT-512)/2+272,
				(WIN_WIDTH-512)/2+512, (WIN_HEIGHT-512)/2+368):
			CurrentUi = UiGame()
			game.GameState = GS_PLAYING
		# Bouton 'Menu principal' -> l'interface affichée redevient l'écran
		# titre
		elif CheckMousePosition(x,y, (WIN_WIDTH-512)/2, (WIN_HEIGHT-512)/2+384,
				(WIN_WIDTH-512)/2+512, (WIN_HEIGHT-512)/2+480):
			CurrentUi = UiTitleScreen()


# Classe UiTitleScreen: interface de l'écran titre
class UiTitleScreen(Ui):
	button_x_pos = 0
	button_y_pos = [0, 0, 0, 0]

	# Lors de l'initialisation de la classe, calcule les positions des boutons
	# sur l'écran pour qu'il soit bien espacé et ne cache pas le nom du jeu
	def __init__(self):
		self.button_x_pos = int((WIN_WIDTH - 512) / 2)
		header_sz = WIN_HEIGHT * (192 / 720)
		space_sz = (WIN_HEIGHT - header_sz - 4 * 96) / 4
		for i in range(4):
			self.button_y_pos[i] = int(header_sz + i * (96 + space_sz))

	# Utilise gui.DrawTitleScreen pour afficher le menu principal,
	def Draw(self):
		gui.DrawTitleScreen(self.button_x_pos, self.button_y_pos)

	# Réagit à un clic sur l'un des boutons du menu principal de la façon
	# appropriée
	def OnClick(self, x, y):
		global CurrentUi
		
		for i in range(4):
			if CheckMousePosition(x,y, self.button_x_pos, self.button_y_pos[i],
				self.button_x_pos+512, self.button_y_pos[i]+96):

				if i == 0:
					# Bouton 'Jouer' -> l'interface affichée devient celle du
					# jeu, la variable d'état de jeu prend une valeur indiquant
					# qu'une partie est en cours
					CurrentUi = UiGame()
					game.GameState = GS_PLAYING
				elif i == 1:
					# Bouton 'Règles' -> l'interface affichée devient celle qui
					# affiche les règles du jeu à l'écran
					CurrentUi = UiRulesScreen()
				elif i == 2:
					# Bouton 'A propos' -> l'interface affichée devient l'écran
					# qui affiche des informations sur le jeu
					CurrentUi = UiAboutScreen()
				else:
					# Bouton 'Quitter' -> modifie la variable qui contrôle la
					# plupart des boucles du jeu pour que celles-ci s'arrêtent
					# et que le programme s'arrête
					game.Running = False


# Classe UiTextScreen: classe modèle qui permet d'afficher un écran informatif
# contenant du texte et un bouton pour revenir au menu principal
class UiTextScreen(Ui):
	# Initialise les textures de textes dans gui avec le texte donné en
	# paramètre
	def __init__(self,text):
		gui.UpdateTextScreenLabels(text)

	# Affiche l'écran informatif
	def Draw(self):
		gui.DrawTextScreen()

	# Réagir aux clics sur le bouton qui permet de revenir au menu principal
	def OnClick(self, x, y):
		global CurrentUi

		if CheckMousePosition(x,y, (WIN_WIDTH-512)/2, WIN_HEIGHT*456/720+144,
			(WIN_WIDTH-512)/2+512, WIN_HEIGHT*456/720+240):
			# Bouton 'Menu principal' -> l'interface affichée redevient l'écran
			# titre
			CurrentUi = UiTitleScreen()


# Classe UiRulesScreen: interface qui utilise le modèle UiTextScreen pour
# afficher les règles du jeu
class UiRulesScreen(UiTextScreen):
	text = """Controles (déplacements et charge):
Joueur 1: ZQSD + Espace
Joueur 2: Touches flechées + 0 (Pavé numérique)
 
Règles du jeu:
- Votre objectif consiste a attraper le poulet avec votre raptor et
a l'amener dans le but de votre adversaire sans vous faire charger.
- Vous pouvez utiliser la charge en vous dirigeant vers votre
adversaire pour lui faire perdre le poulet et le récuperer.
- Le premier a marquer 3 points ou celui qui a le plus de points
quand le temps sera ecoulé gagne la partie!
"""
	# Initialise UiTextScreen pour qu'il utilise le texte ci-dessus
	def __init__(self):
		UiTextScreen.__init__(self, self.text)


# Classe UiAboutScreen: interface qui utilise le modèle UiTextScreen pour
# afficher des informations sur le jeu (nos noms, la mention copyright, la
# licence sous laquelle le jeu est placé ainsi que les informations concernant
# les ressources extérieures utilisées pour créer le jeu)
class UiAboutScreen(UiTextScreen):
	text = """Raptor Ball a été crée par Gabriel Tartarin et Arthur Melin
Copyright (c) 2016 Arthur Melin et Gabriel Tartarin
Raptor Ball est un logiciel libre publié sous licence zlib (LICENCE.txt)
 
Ce logiciel utilise la librairie PySDL2 de Marcus von Appen
[https://pysdl.readthedocs.org] (domaine public), portage pour Python
de la librairie Standard DirectMedia Layer 2.0 et de ses extensions
SDL_image et SDL_ttf creees par Sam Latinga et les contributeurs du
projet [https://www.libsdl.org] (licence libre zlib).
 
Ce logiciel utilise la police d'écriture Middle School Crush NBP créée par
Nate Hailey [http://totalfontgeek.blogspot.com] (licence CC 3.0 BY-SA).
"""
	# Initialise UiTextScreen pour qu'il utilise le texte ci-dessus
	def __init__(self):
		UiTextScreen.__init__(self, self.text)

###############################################################################

# FONCTIONS INTERFACES INTER-MODULES

# > InitSDLVideoSubSystem():
# Initialise le sous-système vidéo de la SDL requis pour le fonctionnement de
# Controls en ouvrant la fenêtre du jeu
def InitSDLVideoSubSystem():
	gui.OpenWindow()

# > ToggleFullscreen():
# Active ou désactive le mode plein-écran du jeu
def ToggleFullscreen():
	gui.ToggleFullscreen()

###############################################################################
