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

tt_version = "v0.0.5"

##### importation ####
import system.mod.cytron as cy
from system.mod.ColorPrint import Background, Colors, colorprint, colorinput
from system.mod.sunbreaker import sunbreaker
from system.mod.login import StartLogin
from system.mod.updater import update as start_update, road
from urllib.request import urlopen
from os import system, name

##### erreur #####

erreurs = {
"001": "commande inconnue",
"002": "dossier de destination invalide, ici -> {}",
"003": "url invalide, ici -> {}",
"004": "argument inconnu, ici -> {}",
"005": "registre {} non trouvé dans les roads"
}

def erreur(e,*arg):
    colorprint("Erreur "+e,Colors.rouge,Background.none,False,True,False)
    colorprint(": " + erreurs[e].format(*arg),Colors.rouge,Background.none,False,False,True)

##### commandes #####

def user_input():
    colorprint("\n┌──(",Colors.magenta,Background.none,False,False,False)
    colorprint(co_user,Colors.magenta,Background.none,False,True,False)
    colorprint(")-[",Colors.magenta,Background.none,False,False,False)
    colorprint(action_rep,Colors.cyan,Background.none,False,True,False)
    colorprint("]",Colors.magenta,Background.none,False,False,True)
    return(colorinput("└─} ",Colors.magenta,Background.none,False,False))

def clear():
    system('cls' if name == 'nt' else 'clear')

def bvn():
    colorprint("\nbienvenue ",Colors.magenta,Background.none,False,False,False)
    colorprint(co_user,Colors.magenta,Background.none,False,True,False)
    colorprint(" sur Terminal Tools",Colors.magenta,Background.none,False,False,True)
    colorprint("Copyright (C) pf4. Tous droits réservés.\n",Colors.magenta,Background.none,False,False,True)

def ls():
    try: rep = com[1]
    except: rep = "/"
    colorprint(cy.cy_path()+action_rep,Colors.vert)
    colorprint("│",Colors.blanc)
    liste_cont = cy.cy_ls(action_rep + "/" + rep)
    for x in range(len(liste_cont)):
        element = liste_cont[x]
        if x == len(liste_cont)-1: colorprint("└─",Colors.blanc,Background.none,False,False,False)
        else: colorprint("├─",Colors.blanc,Background.none,False,False,False)
        if len(element.split(".")) > 1: colorprint(element,Colors.jaune)
        else: colorprint(element,Colors.bleu,Background.none)

def cd():
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

def version():
    def printversion(nom,doc):
        colorprint(nom,Colors.magenta,Background.none,False,True,False)
        colorprint(f": {doc}",Colors.magenta,Background.none,False,False,True)
    printversion("terminal tools",tt_version)
    printversion("cytron",cy.version())

def update():  # sourcery no-metrics
    def u_dl():
        try: start_update(action_rep+com[2],com[3])
        except: erreur("003",com[3])

    def u_help():
        def printhelp(nom,doc):
            colorprint(nom,Colors.magenta,Background.none,False,True,False)
            colorprint(f": {doc}",Colors.magenta,Background.none,False,False,True)
        printhelp("update dl <chemin> <url>","télécharger un registre directement depuis son url")
        printhelp("update rdl <chemin> <nom>", "télécharger un registre depuis les fichier de redirection")
        printhelp("update road list", "afficher la liste")
        printhelp("update road add <nom>", "ajouter une url de la liste")
        printhelp("update road del <nom>", "supprimer une url de la liste")
        printhelp("update road read", "lire les fichiers de redirection")

    def u_road():
        if com[2] in ["list", "l"]:
            colorprint(str(road),Colors.magenta)
        elif com[2] in ["add", "a"]:
            road.append(com[3])
        elif com[2] in ["del", "d"]:
            try: road.remove(com[3])
            except: erreur("003",com[3])
        elif com[2] in ["read", "r"]:
            for r in road:
                colorprint(f"road: {r}",Colors.magenta, ligne = True)
                for l in urlopen(r).read().decode("utf-8").split("\n"):
                    colorprint(f"  {l}",Colors.magenta)
        else: erreur("004",com[2])

    def u_rdl():
        done = False
        for r in road:
            for l in urlopen(r).read().decode("utf-8").split("\n"):
                l = str(l).split(",")
                if l[0] == com[3]:
                    start_update(action_rep+com[2],l[1].strip())
                    done = True
                    break
        if not done: erreur("005",com[3])

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

def help():
    def printhelp(nom,doc):
        colorprint(nom,Colors.magenta,Background.none,False,True,False)
        colorprint(f": {doc}",Colors.magenta,Background.none,False,False,True)
    printhelp("bvn","affiche l'écran de bienvenue")
    printhelp("cd <chemin>","change le dossier de travail")
    printhelp("clear","efface la console")
    printhelp("help","affiche cette aide")
    printhelp("ls [chemin]","affiche le contenu dossier de travail ou du dossier spécifier")
    printhelp("update <*arg>","lance le systeme de mise a jour (update help)")
    printhelp("verion","affiche la version de terminal tools et des modules")

##### setup #####

global action_rep
action_rep = "/"

global co_user
co_user = StartLogin()
bvn()

##### debut du terminal #####

def interpreteur(ipt):
    global com
    com = str(ipt).split(" ")
    rc = com[0] #root commande
    if rc == "bvn": bvn()
    elif rc == "cd": cd()
    elif rc == "help": help()
    elif rc in ["clear", "cls"]: clear()
    elif rc == "ls": ls()
    elif rc == "update": update()
    elif rc == "version": version()
    elif rc != "": erreur("001")


while True:
    interpreteur(user_input())