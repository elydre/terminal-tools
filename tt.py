'''
--|~|--|~|--|~|--|~|--|~|--|~|--

██  ████        ██████        ██
████    ██     ██           ████
██      ██   ████████     ██  ██
████████       ██       ██    ██
██             ██       █████████
██             ██             ██
██
 - codé en : UTF-8
 - langage : python 3
 - GitHub  : github.com/pf4-DEV
--|~|--|~|--|~|--|~|--|~|--|~|--
'''

tt_version = "v0.1.1b"

##### importation ####

from time import time as actual_time

import system.shell.com as c
from system.mod.ColorPrint import colorprint

##### erreurs #####

erreurs = {
"001": "commande inconnue",
"002": "dossier de destination invalide, ici -> {}",
"003": "url invalide, ici -> {}",
"004": "argument inconnu, ici -> {}",
"005": "registre {} non trouvé dans les roads",
"006": "La commande nécessite un/des argument(s) pour fonctionné",
"007": "pas de connection internet",
"008": "erreur d'excution,\nici -> {}",
"009": "le theme {} n'existe pas",
"010": "la commande ne necessite pas d'argument",
}

##### path #####

path = {
    "cd":           (c.cd,            "change le dossier de travail"),
    "cy":           (c.cy_run,        "lance des commandes cytron"),
    "clear":        (c.clear,         "efface la console"),
    "exec":         (c.py_exec,       "lance des commandes python"),
    "exit":         (c.quiter,        "quitte le programme/la session"),
    "help":         (c.help,          "affiche de l'aide"),
    "ls":           (c.ls,            "affiche le contenu dossier de travail ou du dossier spécifier"),
    "mkdir":        (c.mkdir,         "créé le dossier du nom spécifié"),
    "moonbreaker":  (c.moonbreaker,   "afficher le break du texte entré"),
    "theme":        (c.theme,         "affiche les couleurs ou les thèmes disponibles et le modifie"),
    "tt-update":    (c.tt_update,     "lance la misse à jour de terminal-tools"),
    "tt-version":   (c.version,       "affiche la version de terminal-tools et des modules"),
    "update":       (c.update,        "lance le systeme de mise a jour (update help)"),
    "wget":         (c.wget,          "télécharge un fichier depuis une url")
}

#### setup ####

c.setup(erreurs)
time = actual_time()

##### debut du terminal #####

def interpreteur(ipt):
    global time
    time = actual_time()
    for i in ipt.split("&&"):
        com = [c for c in str(i).split(" ") if c != ""]
        if len(ipt.split("&&")) > 1: colorprint("──} " + i.strip(),"dark")

        if com:
            if com[0] in path: path[com[0]][0](com, {"path": path,
                                                    "erreurs": erreurs,
                                                    "tt_version": tt_version,
                                                    "time": time})
            else: c.erreur("001")
    return time

while True:
    time = interpreteur(c.user_input(time, c.input_theme_name))