###############################################################################
# MAIN.PY: Module principal du programme qui charge ses sous-modules et       #
#          démarre leurs threads                                              #
###############################################################################

# IMPORTS:
# Python
import os, platform

###############################################################################

# PROGRAMME PRINCIPAL

# Pour les systèmes utilisant Windows, configuration du chemin d'accès vers les
# fichiers DLL de la bibliothèque SDL2 et ses extensions correspondant à
# l'architecture que Python utilise (32 ou 64-bit)
if platform.system() == "Windows":
	os.environ["PYSDL2_DLL_PATH"] = \
		os.getcwd() + "/sdl2-dll-" + platform.architecture()[0]

# Chargement et initialisation de la SDL2 et des extensions sdlimage et sdlttf
from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *
SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS)
IMG_Init(IMG_INIT_PNG)
TTF_Init()


# Import des modules principaux du programme
import game, controls, ui

# Initialisation des modules principaux et sauvegarde des threads qui sont
# associés à chacun
Threads = []
for module in [game, ui, controls]:
	Threads.append(module.Init())

# Démarrage des threads des modules principaux, le programme est maintenant
# divisé en 3+1 fils d'exécution fonctionnants en parallèle
for thread in Threads:
	thread.start()

# Mise en attente du fil d'exécution actuel (celui de Main) qui attend la fin
# de l'exécution du thread du module Game (c'est-à-dire la fin du programme)
game.GameThread.join()

# Libération des ressources qui étaient employées par les modules du programme
for submodule in [game, ui, controls]:
	submodule.Quit()

# Dé-initialise la SDL2 et ses extensions (dans l'ordre inverse de leur
# initialisation)
TTF_Quit()
IMG_Quit()
SDL_Quit()

###############################################################################
