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

tt_version = "v0.0.22"

##### importation ####
import system.mod.cytron as cy
from system.mod.ColorPrint import colorprint, colorinput, setcolor, version as cp_version
from system.mod.moonbreaker import moonbreaker as mb, version as mb_version
from system.mod.login import StartLogin, login_setup
from system.mod.updater import update as start_update, road
from system.mod.themes import color_themes, theme_version, input_themes
from urllib.request import urlopen
from os import system, name
from time import time as actual_time

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

def erreur(e,*arg):
    colorprint("Erreur "+e,"litered", "k")
    colorprint(": " + erreurs[e].format(*arg),"darkred")

def makecolor(theme_name):
    for k in color_themes[theme_name].keys():
        setcolor(k,color_themes[theme_name][k])

def user_input(time, input_theme_name, mode = "input"):

    str2var = {
    "co_user": co_user,
    "time": str(round(actual_time() - time,2)),
    "action_rep": action_rep
    }

    theme = input_themes[input_theme_name]
    while True:
        for k in theme:
            if k["type"] == "print" or mode == "demo":
                if "texte" in k.keys():
                    colorprint(k["texte"], k["color"], k["code"])
                else:
                    colorprint(str2var[k["var"]], k["color"], k["code"])
            elif k["type"] == "input":
                
                    try:
                        if "texte" in k.keys():
                            return colorinput(k["texte"], k["color"], k["code"])
                        else:
                            return colorinput(str2var[k["var"]], k["color"], k["code"])
                    except KeyboardInterrupt:
                        print("")

def bvn():
    colorprint("\nbienvenue ","dark","k")
    colorprint(co_user,"lite","k")
    colorprint(" sur Terminal Tools","dark")
    colorprint("Copyright (C) pf4. Tous droits réservés.\n","dark")

##### commandes #####

def clear(com):
    if len(com) == 1:
        system('cls' if name == 'nt' else 'clear')
    else: erreur("010")

def ls(com):
    try: rep = com[1]
    except: rep = "/"
    colorprint(cy.cy_path()+action_rep,"green")
    colorprint("│","white")
    liste_cont = cy.cy_ls(action_rep + "/" + rep)
    for x in range(len(liste_cont)):
        element = liste_cont[x]
        if x == len(liste_cont)-1: colorprint("└─","white","k")
        else: colorprint("├─","white","k")
        if len(element.split(".")) > 1: colorprint(element,"yellow")
        else: colorprint(element,"blue")

def cd(com):
    if len(com) > 1:
        global action_rep
        loc = ""
        try:
            for x in range(len(com)-2): loc += com[x + 1] + " "
        except: pass
        loc += com[len(com)-1]
        loc = loc.replace("\\","/")
        if loc.startswith("..") or loc.startswith("/.."):
            temp3 = action_rep.split("/")
            temp4 = "".join("/" + temp3[x] for x in range(len(temp3)-1))
            action_rep = temp4
        else:
            to_test = action_rep + "/" + loc
            temp = [mors for mors in to_test.split("/") if mors != ""]
            to_test = ""
            for temp2 in temp: to_test += "/" + temp2
            try:
                cy.cy_ls(to_test)
                action_rep = to_test
            except: erreur("002",to_test)
    else: action_rep = "/"

def version(com):
    if len(com) == 1:
        def printversion(nom,doc):
            colorprint(nom,"lite", "k")
            colorprint(f": {doc}", "dark")
        printversion("terminal tools", tt_version)
        printversion("cytron", cy.version())
        printversion("colorprint", cp_version)
        printversion("moonbreaker", mb_version)
        printversion("themes", theme_version)
    else: erreur("010")

def update(com):  # sourcery no-metrics
    ar = action_rep
    def u_dl():
        try: start_update(ar+com[2],com[3])
        except: erreur("003",com[3])

    def u_help():
        def printhelp(nom,doc):
            colorprint(nom,"lite", "k")
            colorprint(f": {doc}", "dark")
        printhelp("update dl <chemin> <url>","télécharger un registre directement depuis son url")
        printhelp("update rdl <chemin> <nom>", "télécharger un registre depuis les fichier de redirection")
        printhelp("update road list", "afficher la liste")
        printhelp("update road add <nom>", "ajouter une url de la liste")
        printhelp("update road del <nom>", "supprimer une url de la liste")
        printhelp("update road read", "lire les fichiers de redirection")

    def u_road():
        if com[2] in ["list", "l"]:
            colorprint(str(road),"dark")
        elif com[2] in ["add", "a"]:
            road.append(com[3])
        elif com[2] in ["del", "d"]:
            try: road.remove(com[3])
            except: erreur("003",com[3])
        elif com[2] in ["read", "r"]:
            for r in road:
                colorprint(f"road: {r}","dark")
                for l in urlopen(r).read().decode("utf-8").split("\n"):
                    colorprint(f"  {l}", "dark")
        else: erreur("004",com[2])

    def u_rdl():
        done = False
        for r in road:
            for l in urlopen(r).read().decode("utf-8").split("\n"):
                l = str(l).split(",")
                if l[0] == com[3]:
                    start_update(ar+com[2],l[1].strip())
                    done = True
                    break
        if not done: erreur("005",com[3])
    if cy.check_internet():
        for _ in range(10 - len(com)): com.append("")
        commande = com[1]
        if commande == "dl":
            u_dl()
        elif commande in ["help", "h", ""]:
            u_help()
        elif commande in ["road", "r"]:
            u_road()
        elif commande == "rdl":
            u_rdl()
        else: erreur("004",commande)
    else: erreur("007")

def moonbreaker(com):
    colorprint(str(mb("".join(x+" "for x in com[1:len(com)]).strip())), "dark")

def tt_update(com):
    if len(com) == 1:
        interpreteur(f"cd && update rdl / tt && cd {action_rep}")
    else: erreur("010")

def cy_run(com):
    commande = com[1:]
    if len(commande) > 0:
        retour = str(cy.run(commande))
        colorprint(retour,"dark")
    else:
        erreur("006")

def mkdir(com):
    if len(com) > 1:
        for e in com[1:]:
            cy.mkdir(action_rep, e)
    else: erreur("006")

def wget(com):
    if len(com) > 1:
        if cy.wget(action_rep, com[1], com[2]) == "DONE":
            colorprint("le fichier a été téléchargé!","dark")

    else: erreur("006")

def py_exec(com):
    if len(com) > 1:
        try: exec("".join([c + " " for c in com[1:]]))
        except Exception as e: erreur("008", str(e))
    else: erreur("006")

def theme(com):
    if len(com) == 1:
        erreur("006")
    elif com[1] == "color":
        if len(com) == 2:
            for theme_name in color_themes.keys():
                print()
                colorprint(f" -{theme_name.upper()}-", "dark")
                for k in color_themes[theme_name].keys():
                    setcolor("temp", color_themes[theme_name][k])
                    colorprint(f"• {k}", "temp")
        elif com[2] in color_themes.keys():
            makecolor(com[2])
        else: erreur("009",com[2])
    elif com[1] == "input":
        global input_theme_name
        if len(com) == 2:
            for theme_name in input_themes.keys():
                colorprint(f" -{theme_name.upper()}-", "dark", "k")
                user_input(time, theme_name, "demo")
                print("\n")
        elif com[2] in input_themes.keys():
            input_theme_name = com[2]
        else: erreur("009",com[2])
    else: erreur("004",com[1])
    
def quiter(com):
    if len(com) == 1:
        clear(["clear"])
        exit()
    elif com[1] == "logout":
        setup()
    else: erreur("004",com[1])

def help(com):
    def printhelp(nom,doc):
        colorprint(nom,"lite","k")
        colorprint(f": {doc}","dark")
    if len(com) == 1:
        for c in path.keys():
            printhelp(c,path[c][1])
    elif com[1] in path.keys():
        printhelp(com[1],path[com[1]][1])
    else: erreur("004",com[1])

##### setup #####

def setup():
    global action_rep, time, input_theme_name
    action_rep = "/"
    input_theme_name = "kalike"
    makecolor("default")

    global co_user
    login_setup()
    co_user = StartLogin()
    bvn()
    time = actual_time()
setup()

##### path #####

path = {
    "cd":           (cd,            "change le dossier de travail"),
    "cy":           (cy_run,        "lance des commandes cytron"),
    "clear":        (clear,         "efface la console"),
    "exec":         (py_exec,       "lance des commandes python"),
    "exit":         (quiter,        "quitte le programme/la session"),
    "help":         (help,          "affiche de l'aide"),
    "ls":           (ls,            "affiche le contenu dossier de travail ou du dossier spécifier"),
    "mkdir":        (mkdir,         "créé le dossier du nom spécifié"),
    "moonbreaker":  (moonbreaker,   "afficher le break du texte entré"),
    "theme":        (theme,         "affiche les couleurs ou les thèmes disponibles et le modifie"),
    "tt-update":    (tt_update,     "lance la misse à jour de terminal-tools"),
    "tt-version":   (version,       "affiche la version de terminal-tools et des modules"),
    "update":       (update,        "lance le systeme de mise a jour (update help)"),
    "wget":         (wget,          "télécharge un fichier depuis une url")
}

##### debut du terminal #####

def interpreteur(ipt):
    global time
    time = actual_time()
    for i in ipt.split("&&"):
        com = [c for c in str(i).split(" ") if c != ""]
        if len(ipt.split("&&")) > 1:
            colorprint("──} " + i.strip(),"dark")

        if com:
            if com[0] in path: path[com[0]][0](com)
            else: erreur("001")

    return time

while True:
    time = interpreteur(user_input(time, input_theme_name))