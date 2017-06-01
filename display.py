###############################################################################
# DISPLAY.PY: Module qui gère l'affichage du jeu de façon primaire (fenêtre,  #
#             textures, fonctions de rendu, etc)                              #
#                                                                             #
# Note: les convertions de format de chaînes de caractères avec les fonctions #
#       str.encode() et bytes.decode() sont nécessaires car la SDL est à      #
#       l'origine une librairie programmée pour le langage C                  #
###############################################################################

# IMPORTS
# Python
import math, time
# PySDL2
from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *
# Locales
from constants import *

###############################################################################

# GLOBALES
# SDL_Window qui correspond à la fenêtre du jeu
Window = None
# SDL_Surface qui correspond à l'icône de la fenêtre
Icon = None
# SDL_Renderer qui correspond au contexte de rendu 2D de la fenêtre
Renderer = None
# Booléen indiquant si le contexte de rendu est prêt à être utilisé
RendererReady = False

# Tableau de SDL_Texture correspondant aux textures figées
FixedTextures = []
# Tableau de tableaux contenant les SDL_Texture des images de chaque animation
AnimatedTextures = []
# Tableau de SDL_Texture correspondant aux textures de texte
LabelTextures = []
# Tableau à dimension variable contenant de nombreuse informations sur toutes
# les textures utilisées par le jeu (textures fixes, animées, de texte) et
# notamment les informations permettant de les charger de nouveau si nécessaire
TexturesData = [[[]], [[], []], [[] , []]]

###############################################################################

# FONCTIONS DU MODULE

# > OpenWindow():
# Ouvre la fenêtre du jeu et crée son contexte de rendu 2D
def OpenWindow():
	global Window, Icon, Renderer, RendererReady

	# Crée la fenêtre du jeu
	Window = SDL_CreateWindow("Raptor Ball".encode(),
		SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
		WIN_WIDTH, WIN_HEIGHT, 0)

	# Charge et assigne un icone à la fenêtre
	Icon = LoadImage("icon.png")
	SDL_SetWindowIcon(Window, Icon)

	# Utilise le premier pilote d'affichage supportant la synchronisation de la
	# fréquence de raffraichissement de l'écran disponible pour créer le
	# contexte de rendu 2D
	Renderer = SDL_CreateRenderer(Window, -1, SDL_RENDERER_PRESENTVSYNC)

	# Indique que le contexte de rendu est prêt à être utilisé
	RendererReady = True



# > CloseWindow():
# Libère la mémoire utilisée par le module en fermant la fenêtre du jeu
def CloseWindow():
	global Window, Icon, Renderer, RendererReady
	global FixedTextures, AnimatedTextures, LabelTextures, TexturesData

	# Indique aux fonctions du modules de ne plus utiliser Renderer car il va
	# être effacé
	RendererReady = False
	time.sleep(WAIT_TIME)

	# Libère toutes les textures dans les différents tableaux les contenant
	for FixedTexture in FixedTextures:
		SDL_DestroyTexture(FixedTexture)
	for AnimatedTexture in AnimatedTextures:
		for FrameTexture in AnimatedTexture:
			SDL_DestroyTexture(FrameTexture)
	for LabelTexture in LabelTextures:
		SDL_DestroyTexture(LabelTexture)

	# Libère le contexte de rendu, la fenêtre et son icone
	SDL_DestroyRenderer(Renderer)
	SDL_DestroyWindow(Window)
	SDL_FreeSurface(Icon)

	# Réinitialise les globales à leur valeur d'origine
	Window, Icon, Renderer = None, None, None
	FixedTextures, AnimatedTextures, LabelTextures = [], [], []
	TexturesData = [[[]], [[], []], [[], []]]



# > DrawWindow():
# Rafraîchit le contenu de la fenêtre (les opérations de dessin dans la fenêtre
# ne sont pas affichés directement, elles sont d'abord stockées en mémoire)
# Cette opération est synchronisée par la SDL avec la fréquence de
# raffraîchissement de l'écran pour éviter des problèmes d'affichage
def DrawWindow():
	# Vérifie que le contexte de rendu est prêt à être utilisé avant d'indiquer
	# à la SDL de mettre à jour l'écran, sinon attend un peu pour permettre aux
	# contexte de rendu de finir de se préparer dans un autre thread
	if RendererReady:
		SDL_RenderPresent(Renderer)
	else:
		time.sleep(WAIT_TIME)



# > DrawFixedTexture(id, x, y, w, h, angle):
# Dessine une texture fixe sur l'écran à une position, taille et avec un angle
# donné. Cette fonction n'a pas un effet direct sur ce qui se trouve à l'écran,
# il faut valider les changements une fois ceux-ci terminés avec la fonction
# DrawWindow()
# Paramètres:
#   id: identifiant numérique de la texture fixe
#   x, y: coordonnées où on dessine la texture sur l'écran
#   w, h: taille horizontale et verticale désirée pour la texture
#   angle: angle de la rotation à appliquer sur la texture en radians
def DrawFixedTexture(id, x, y, w, h, angle):
	# Vérifie que le contexte de rendu est prêt à être utilisé
	if RendererReady:
		# Définit le rectangle où sera affiché la texture (position et taille)
		Rect = SDL_Rect(x, y, w, h)

		# Dessine la texture correspondante à l'id dans le rectangle avec
		# l'angle spécifié (avec traduction rad/direct vers °/indirect)
		SDL_RenderCopyEx(Renderer, FixedTextures[id], None, Rect,
			-math.degrees(angle), None, SDL_FLIP_NONE)



# > DrawAnimatedTexture(id, x, y, w, h, angle):
# Dessine une texture animée sur l'écran de la même manière que
# DrawFixedTexture() mais en sélectionnant l'image de l'animation à afficher
# grâce aux informations dans TexturesData
# Paramètres:
#   id: identifiant numérique de l'animation
#   x, y: coordonnées où on dessine la texture sur l'écran
#   w, h: taille horizontale et verticale désirée pour la texture
#   angle: angle de la rotation à appliquer sur la texture en radians
def DrawAnimatedTexture(id, x, y, w, h, angle):
	# Vérifie que le contexte de rendu est prêt à être utilisé
	if RendererReady:
		# Définit le rectangle où sera affiché la texture (position et taille)
		Rect = SDL_Rect(x, y, w, h)

		# Calcule le temps qui s'est écoulé depuis le dernier affichage de
		# cette animation
		dt = time.time() - \
			 TexturesData[TD_ANIMATED][TD_DATA][id][TD_ANIM_LASTTIME]

		# Calcule quelle image de l'animation il faut afficher maintenant
		# avec la formule:
		# image actuelle = (image précédente + durée écoulée/durée d'une image)
		#                   % nombre d'images dans l'animation
		frame = (TexturesData[TD_ANIMATED][TD_DATA][id][TD_ANIM_LASTFRAME] +
			dt / TexturesData[TD_ANIMATED][TD_INIT][id][TD_ANIM_FRAMELENGTH]) \
			   % TexturesData[TD_ANIMATED][TD_INIT][id][TD_ANIM_FRAMECOUNT]

		# Affiche l'image de l'animation (en arrondissant le numéro d'image qui
		# est décimal à l'entier inférieur)
		SDL_RenderCopyEx(Renderer, AnimatedTextures[id][math.floor(frame)],
			None, Rect, -math.degrees(angle), None, SDL_FLIP_NONE)

		# Sauvegarde les informations de cette affichage dans TexturesData
		TexturesData[TD_ANIMATED][TD_DATA][id] = [frame, time.time()]



# > DrawLabelTexture(id, x, y, angle):
# Affiche une texture de texte à une position et avec une rotation donnée
# Contrairement aux autres fonctions Draw...Texture(), la texture est dessinée
# avec son centre (et non son coin supérieur gauche) à la position donnée car
# la taille de la texture est variable puisque le texte qu'elle contient l'est
# Paramètres:
#   id: identifiant numérique de la texture
#   x, y: coordonnées sur laquelle la texture est centrée
#   angle: angle de la rotation à appliquer sur la texture en radians
def DrawLabelTexture(id, x, y, angle):
	# Vérifie que le contexte de rendu est prêt à être utilisé
	if RendererReady:
		# Définit le rectangle où sera affiché la texture sur l'écran. On
		# récupère la taille de la texture depuis les données sauvegardées dans
		# TexturesData
		Rect = SDL_Rect(
			int(x - (TexturesData[TD_LABEL][TD_DATA][id][TD_LABEL_WIDTH]/2)),
			int(y - (TexturesData[TD_LABEL][TD_DATA][id][TD_LABEL_HEIGHT]/2)),
			TexturesData[TD_LABEL][TD_DATA][id][TD_LABEL_WIDTH],
			TexturesData[TD_LABEL][TD_DATA][id][TD_LABEL_HEIGHT])

		# Affiche la texture correspondante sur l'écran
		SDL_RenderCopyEx(Renderer, LabelTextures[id], None, Rect,
			-math.degrees(angle), None, SDL_FLIP_NONE)



# > ToggleFullscreen():
# Active ou désactive le mode plein-écran du jeu
def ToggleFullscreen():
	global Renderer, RendererReady

	# Indique aux fonctions de ce module de ne plus utiliser Renderer car il ne
	# sera bientôt plus valide
	RendererReady = False
	time.sleep(WAIT_TIME)

	# Libère l'ancien contexte de rendu
	SDL_DestroyRenderer(Renderer)

	# Applique le mode plein-écran sur la fenêtre du jeu
	flags = SDL_GetWindowFlags(Window) ^ SDL_WINDOW_FULLSCREEN_DESKTOP
	SDL_SetWindowFullscreen(Window, flags)

	# Remplace l'ancien contexte de rendu par un nouveau adapté au mode
	# d'affichage actuel et recharge toutes les textures du jeu
	Renderer = SDL_CreateRenderer(Window, -1, SDL_RENDERER_PRESENTVSYNC)
	SDL_RenderSetLogicalSize(Renderer, WIN_WIDTH, WIN_HEIGHT)
	print("Rechargement des textures...")
	ReloadTextures()
	print("Terminé!")
	RendererReady = True



# > LoadImage(path):
# Charge le fichier d'une image et retourne la SDL_Surface qui la contient
# Paramètre:
#  path: chemin d'accès vers la texture depuis le sous-dossier "textures" dans
#        le dossier du jeu
def LoadImage(path):
	# Obtient les droits de lecture du fichier de l'image et la charge
	rwops = SDL_RWFromFile(("textures/" + path).encode(), "r".encode())
	return IMG_Load_RW(rwops, True)



# > ReloadTextures():
# Recharge tous les fichiers de textures fixes et animées et recrée les
# textures de texte à partir des données sauvegardées dans les parties TD_INIT
# de TexturesData
def ReloadTextures():
	global FixedTextures

	# Libère la mémoire utilisée par les textures associées à un contexte de
	# rendu précédent
	for FixedTexture in FixedTextures:
		SDL_DestroyTexture(FixedTexture)
	for AnimatedTexture in AnimatedTextures:
		for FrameTexture in AnimatedTexture:
			SDL_DestroyTexture(FrameTexture)
	for LabelTexture in LabelTextures:
		SDL_DestroyTexture(LabelTexture)

	# Recharge les textures à partir des valeurs initiales sauvegardées dans
	# TexturesData
	LoadFixedTextures(TexturesData[TD_FIXED][TD_INIT])
	LoadAnimatedTextures(TexturesData[TD_ANIMATED][TD_INIT])
	LoadLabelTextures(TexturesData[TD_LABEL][TD_INIT])



# > LoadFixedTextures(texturesPaths):
# Charge les fichiers de textures fixes dont le chemin d'accès se trouve dans
# le tableau en paramètre et les mets dans FixedTextures
# Paramètre:
#   texturesPaths: tableau de chaines de caractères correspondant aux chemins
#                  d'accès vers les fichiers de textures à charger
def LoadFixedTextures(texturesPaths):
	# Initialise le tableau avec le nombre de textures à stocker
	global FixedTextures
	FixedTextures = [None for n in range(len(texturesPaths))]

	# Pour chaque texture à charger
	for i in range(len(texturesPaths)):
		# Charge le fichier image contenant la texture
		Surface = LoadImage(texturesPaths[i])
		# Convertit l'image en texture utilisable par la SDL
		FixedTextures[i] = SDL_CreateTextureFromSurface(Renderer, Surface)
		# Libère la mémoire utilisée par l'image
		SDL_FreeSurface(Surface)

	# Sauvegarde le paramètre de cette fonction dans TexturesData
	TexturesData[TD_FIXED][TD_INIT] = texturesPaths



# > LoadAnimatedTextures(animationInfo):
# Charge les fichiers de textures des animations d'une manière semblable à
# LoadFixedTextures().
# Paramètre:
#   animationsInfo: tableau de tableaux contenant des informations associées
#                   aux animations dans le format [str:nom du sous-dossier de
#                   textures contenant les fichiers des images de l'animation,
#                   int:nombre d'images dans l'animation, float:durée
#                   d'affichage de chaque image de l'animation en secondes]
def LoadAnimatedTextures(animationsInfo):
	# Initialise le tableau avec le nombre de textures à stocker
	global AnimatedTextures
	AnimatedTextures = [None for n in range(len(animationsInfo))]

	# Pour chaque animation à charger
	for i in range(len(animationsInfo)):
		# Initialise le tableau avec le nombre d'images qu'elle contient
		AnimatedTextures[i] = [None for n in
			range(animationsInfo[i][TD_ANIM_FRAMECOUNT])]
		# Pour chaque image la composant
		for j in range(animationsInfo[i][TD_ANIM_FRAMECOUNT]):
			# Charge la texture (même technique que pour les textures fixes
			# mais en transformant le chemin d'accès)
			Surface = LoadImage(animationsInfo[i][TD_ANIM_FOLDERNAME] + "/" +
				str(j+1) + ".png")
			AnimatedTextures[i][j] = \
				SDL_CreateTextureFromSurface(Renderer, Surface)
			SDL_FreeSurface(Surface)

	# Sauvegarde le paramètre de cette fonction dans TexturesData
	TexturesData[TD_ANIMATED][TD_INIT] = animationsInfo
	# Initialise les informations d'animations
	TexturesData[TD_ANIMATED][TD_DATA] = \
		[[0.0, time.time()] for n in range(len(animationsInfo))]



# > LoadLabelTextures(labelsInfo):
# Crée des textures contenant du texte avec une police d'écriture, une taille
# et une couleur donnée en paramètre
# Paramètre:
#   labelsInfo: tableau de tableaux contenant des informations sur le texte à
#               afficher avec le format [str: texte à afficher, str: nom du
#               fichier contenant la police d'écriture à utiliser, int: taille
#               de la police en points, SDL_Color: couleur du texte]
def LoadLabelTextures(labelsInfo):
	# Initialise les tableaux avec le nombre de textures à stocker
	global LabelTextures
	LabelTextures = [None for n in range(len(labelsInfo))]
	TexturesData[TD_LABEL][TD_DATA] = [None for n in range(len(labelsInfo))]

	# Pour chaque texte à afficher
	for i in range(len(labelsInfo)):
		# Ouvre le fichier contenant la police d'écriture à une taille donnée
		rwops = SDL_RWFromFile(labelsInfo[i][TD_LABEL_FONT].encode(),
			"r".encode())
		Font = TTF_OpenFontRW(rwops, True, labelsInfo[i][TD_LABEL_SIZE])
		# Génère une image avec le texte et la couleur spécifiée
		Surface = TTF_RenderUTF8_Blended(Font,
			labelsInfo[i][TD_LABEL_TEXT].encode(),
			labelsInfo[i][TD_LABEL_COLOR])
		# Sauvegarde la taille de l'image
		TexturesData[TD_LABEL][TD_DATA][i] = \
			[Surface.contents.w, Surface.contents.h]
		# Convertit l'image en texture
		LabelTextures[i] = SDL_CreateTextureFromSurface(Renderer, Surface)
		# Libère la mémoire utilisée par l'image et la police d'écriture
		SDL_FreeSurface(Surface)
		TTF_CloseFont(Font)

	# Sauvegarde le paramètre de cette fonction dans TexturesData
	TexturesData[TD_LABEL][TD_INIT] = labelsInfo



# > UpdateLabelTexture(id, text):
# Met à jour le texte affiché dans une texture avec celui donné en paramètre
# Paramètres:
#   id: identifiant numérique de la texture à modifier
#   text: nouveau texte à afficher
def UpdateLabelTexture(id, text):
	# Vérifie que le texte a bien été modifié (évite l'utilisation inutile de
	# ressources si ce n'est pas le cas)
	if TexturesData[TD_LABEL][TD_INIT][id][TD_LABEL_TEXT] != text:
		# Met à jour le texte dans TexturesData
		TexturesData[TD_LABEL][TD_INIT][id][TD_LABEL_TEXT] = text

		# Libère la mémoire utilisée par l'ancienne texture
		SDL_DestroyTexture(LabelTextures[id])

		# Génère la nouvelle texture de la même façon que LoadLabelTextures()
		# mais en utilisant les variables sauvegardées dans TexturesData
		rwops = SDL_RWFromFile(
			TexturesData[TD_LABEL][TD_INIT][id][TD_LABEL_FONT].encode(),
			"r".encode())

		Font = TTF_OpenFontRW(rwops, True,
			TexturesData[TD_LABEL][TD_INIT][id][TD_LABEL_SIZE])

		Surface = TTF_RenderUTF8_Blended(Font,
			TexturesData[TD_LABEL][TD_INIT][id][TD_LABEL_TEXT].encode(),
			TexturesData[TD_LABEL][TD_INIT][id][TD_LABEL_COLOR])

		TexturesData[TD_LABEL][TD_DATA][id] = \
			[Surface.contents.w, Surface.contents.h]

		LabelTextures[id] = SDL_CreateTextureFromSurface(Renderer, Surface)
		SDL_FreeSurface(Surface)
		TTF_CloseFont(Font)

###############################################################################
