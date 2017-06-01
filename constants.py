###############################################################################
# CONSTANTS.PY: Fichier regroupant l'ensemble des constantes utilisées dans   #
#               le code source du programme pour améliorer sa lisibilité      #
###############################################################################


# Indices généraux pour accéder aux valeurs spécifiques d'un joueur:
PLAYER1 = 0 # Joueur 1 (raptor bleu)
PLAYER2 = 1 # Joueur 2 (raptor rouge)
BALL    = 2 # Balle (poulet)


# Globale controls.PlayersControls[][]:
# 1er indice du tableau: joueur concerné
# Constantes générales PLAYER1 ou PLAYER2
# 2eme indice du tableau: vecteur vélocité ou état touche d'action
PC_VELOCT = 0 # Tableau représentant le vecteur vitesse recherché par le joueur
PC_ACTION = 1 # Etat de la touche Action


# Globale game.Positions[][]:
# 1er indice du tableau: joueurs concerné
# Constantes générales PLAYER1, PLAYER2, et BALL
# 2ème indice du tableau: coordonnées et orientation
POS_X     = 0 # Coordonnées horizontales sur le terrain [-1.0;1.0]
POS_Y     = 1 # Coordonnées verticales sur le terrain [-1.0;1.0]
POS_ANGLE = 2 # Orientation en radians par rapport à l'horizontale(sens direct)


# Globale display.TexturesData[][][][]:
# 1er indice du tableau: type de texture
TD_FIXED    = 0 # Textures fixes
TD_ANIMATED = 1 # Textures animées
TD_LABEL    = 2 # Textures de texte
# 2eme indice du tableau: données recherchées
TD_INIT = 0 # Paramètre initialement passé à Load...Textures() et permettant
			# à ces textures d'être rechargées (le format du contenu de ce
			# tableau est identique à celui décrit dans les commentaires
			# introduisant chaque fonction Load...Textures())
TD_DATA = 1 # Données supplémentaires (TD_ANIMATED et TD_LABEL)
# 3eme indice du tableau: identifiant numérique de la texture concernée
# 4eme indice du tableau (pour TD_ANIMATED > TD_INIT):
TD_ANIM_FOLDERNAME  = 0 # Nom du sous-dossier contenant chaque image de
                        # l'animation
TD_ANIM_FRAMECOUNT  = 1 # Nombre d'images dans l'animation
TD_ANIM_FRAMELENGTH = 2 # Durée d'affichage de chaque image en secondes
# 4eme indice du tableau (pour TD_ANIMATED > TD_DATA):
TD_ANIM_LASTFRAME = 0 # Valeur décimale indiquant quelle a été la dernière
					  # image de l'animation a être affichée
TD_ANIM_LASTTIME  = 1 # Date du dernier affichage de l'animation
# 4eme indice du tableau (pour TD_LABEL > TD_INIT):
TD_LABEL_TEXT  = 0 # Texte affiché
TD_LABEL_FONT  = 1 # Police d'écriture du texte
TD_LABEL_SIZE  = 2 # Taille de la police en points
TD_LABEL_COLOR = 3 # Couleur du texte
# 4eme indice du tableau (pour TD_LABEL > TD_DATA):
TD_LABEL_WIDTH  = 0 # Largeur de la texture de texte en pixels
TD_LABEL_HEIGHT = 1 # Hauteur de la texture de texte en pixels


# Indices pour accéder à des variables correspondant à des vecteurs:
VEC_ANGLE = 0 # Angle en radians dans le sens direct du vecteur avec l'axe xx'
VEC_NORM = 1  # Norme du vecteur


# Indices pour accéder aux booléens dans le tableau Keys dans display.Run() et
# display.TranslateKbInput():
KEY_UP    = 0 # Touche Haut
KEY_LEFT  = 1 # Touche Gauche
KEY_DOWN  = 2 # Touche Bas
KEY_RIGHT = 3 # Touche Droite


# Valeurs prises par keystate dans display.Run() décrivant l'état d'une touche
# de clavier:
KS_RELEASED = False  # Une touche a été relachée
KS_PRESSED  = True   # Une touche a été enfoncée


# Valeurs prises par game.GameState décrivant l'état du jeu:
GS_NPLAYING = 0 # Pas de partie en cours
GS_PLAYING  = 1 # Une partie est en cours
GS_PAUSED   = 2 # Une partie est en cours mais en pause


# Valeurs prises par chaque élément dans game.PlayerState décrivant l'état d'un
# joueur ou de la balle
PS_STOP = 0 # Immobile
PS_WALK = 1 # Marche
PS_DASH = 2 # Attaque (uniquement pour les joueurs)
PS_SPIT = 3 # Crache la balle (uniquement pour les joueurs)
PS_HOLD = 4 # Tient la balle (pour les joueurs) ou balle tenue (pour la balle)


# Identifiants numériques des textures, animations et textes utilisés par le
# jeu :
#  -- Textures figées --
TFX_FIELD  = 0 # Texture du terrain (field.png)
TFX_TTLSCR = 1 # Texture de l'écran titre (title_screen.png)
TFX_BCKGDS = 2 # Texture petite d'arrière-plan (background_small.png)
TFX_BCKGDM = 3 # Texture moyenne d'arrière-plan (background_medium.png)
TFX_BCKGDL = 4 # Texture grande d'arrière-plan (background_large.png)
TFX_CHICKN = 5 # Texture du poulet immobile (chicken/1.png)
TFX_RAPTRB = 6 # Texture du raptor bleu (joueur 1) immobile (raptor_blue/1.png)
TFX_RAPTRR = 8 # Texture du raptor rouge (joueur 2) immobile (reptor_red/1.png)
#  -- Animations --
ANI_CHICKN = 0 # Animation du poulet (chicken)
ANI_RAPTRB = 1 # Animation du raptor bleu (raptor_blue)
ANI_RAPTRR = 5 # Animation du raptor rouge (raptor_red)
# -- Variations des textures et animations des raptors--
V_TFX_CHIC = 1 # Variation de texture d'un raptor tenant le poulet (_chicken)
V_ANI_CHIC = 1 # Variation d'animation d'un raptor tenant le poulet (_chicken)
V_ANI_DASH = 2 # Variation d'animation d'un raptor faisant une charge (_dash)
V_ANI_SPIT = 3 # Variation d'animation d'un raptor lâchant le poulet (_spit)
#  -- Textes --
LBL_PLAY     =  0 # Texte du bouton 'Jouer' du menu principal
LBL_RULES    =  1 # Texte du bouton 'Règles' du menu principal
LBL_ABOUT    =  2 # Texte du bouton 'A propos' du menu principal
LBL_QUIT     =  3 # Texte du bouton 'Quitter' du menu principal
LBL_TITLESCR =  4 # Texte du bouton 'Menu principal' utilisé plusieurs fois
LBL_RESUME   =  5 # Texte du bouton 'Reprendre' du menu pause
LBL_NEWGAME  =  6 # Texte du bouton 'Rejouer' du menu partie terminée
LBL_PAUSE    =  7 # Titre du menu pause
LBL_GAMEOVER =  8 # Titre du menu partie terminée
LBL_SCOREP1  =  9 # Score du joueur 1
LBL_SCOREP2  = 10 # Score du joueur 2
LBL_TIMER    = 11 # Temps restant de la partie
LBL_GOVERMSG = 12 # Message affiché lorsque la partie est terminée
LBL_TEXTSCR  = 13 # N°13 à 25: lignes des textes des menus A propos et Règles


# Résolution de la fenêtre du jeu:
WIN_WIDTH  = 1280 # Largeur (valeur conseillée: 1280)
WIN_HEIGHT = 720  # Hauteur (valeur conseillée: 720)
WIN_RATIO  = WIN_WIDTH / WIN_HEIGHT # Rapport Largeur/Hauteur de la fenêtre


# Durée d'attente en secondes pour les fonctions time.sleep():
# Si trop élevée : le jeu est peu réactif et saccadé
# Si trop court : utilisation excessive du processeur
WAIT_TIME = 0.01

# Décomptes du jeu en secondes
CDOWN_DASH = 2.0 # Décompte limitant l'attaque d'un joueur
CDOWN_SPIT = 1.0 # Décompte immbobilisant un joueur attaqué
CDOWN_BALL = 1.0 # Décompte empêchant la balle d'être attrapée juste après
                 #avoir été relâchée

###############################################################################
