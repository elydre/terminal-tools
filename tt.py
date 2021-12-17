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

tt_version = "v0.0.11c"

##### importation ####
import system.mod.cytron as cy
from system.mod.ColorPrint import colorprint, colorinput, setcolor
from system.mod.sunbreaker import sunbreaker as sb
from system.mod.login import StartLogin
from system.mod.updater import update as start_update, road
from urllib.request import urlopen
from os import system, name
from time import time as actual_time

##### erreur #####

erreurs = {
"001": "commande inconnue",
"002": "dossier de destination invalide, ici -> {}",
"003": "url invalide, ici -> {}",
"004": "argument inconnu, ici -> {}",
"005": "registre {} non trouvé dans les roads",
"006": "La commande nécessite un/des argument(s) pour fonctionné",
"007": "pas de connection internet",
"008": "erreur d'excution"
}

setcolor("litepurple", (228, 138, 255))
setcolor("darkpurple", (137,  83, 153))
setcolor("litered",    (228,  86,  73))
setcolor("darkred",    (178,  36,  23))

def erreur(e,*arg):
    colorprint("Erreur "+e,"litered", "k")
    colorprint(": " + erreurs[e].format(*arg),"darkred")

##### commandes #####

def user_input(time):
    colorprint("\n┌──(","darkpurple","k")
    colorprint(co_user,"litepurple","k")
    colorprint(" • ","darkpurple","k")
    colorprint(str(round(actual_time() - time,2)),"litepurple","k")
    colorprint(")-[","darkpurple","k")
    colorprint(action_rep,"cyan","k")
    colorprint("]","darkpurple")
    return(colorinput("└─} ","darkpurple"))

def clear():
    system('cls' if name == 'nt' else 'clear')

def bvn():
    colorprint("\nbienvenue ","darkpurple","k")
    colorprint(co_user,"litepurple","k")
    colorprint(" sur Terminal Tools","darkpurple")
    colorprint("Copyright (C) pf4. Tous droits réservés.\n","darkpurple")

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

def version():
    def printversion(nom,doc):
        colorprint(nom,"litepurple","k")
        colorprint(f": {doc}","darkpurple")
    printversion("terminal tools",tt_version)
    printversion("cytron",cy.version())

def update(ar,com):  # sourcery no-metrics
    def u_dl():
        try: start_update(ar+com[2],com[3])
        except: erreur("003",com[3])

    def u_help():
        def printhelp(nom,doc):
            colorprint(nom,"litepurple","k")
            colorprint(f": {doc}","darkpurple")
        printhelp("update dl <chemin> <url>","télécharger un registre directement depuis son url")
        printhelp("update rdl <chemin> <nom>", "télécharger un registre depuis les fichier de redirection")
        printhelp("update road list", "afficher la liste")
        printhelp("update road add <nom>", "ajouter une url de la liste")
        printhelp("update road del <nom>", "supprimer une url de la liste")
        printhelp("update road read", "lire les fichiers de redirection")

    def u_road():
        if com[2] in ["list", "l"]:
            colorprint(str(road),"darkpurple")
        elif com[2] in ["add", "a"]:
            road.append(com[3])
        elif com[2] in ["del", "d"]:
            try: road.remove(com[3])
            except: erreur("003",com[3])
        elif com[2] in ["read", "r"]:
            for r in road:
                colorprint(f"road: {r}","darkpurple")
                for l in urlopen(r).read().decode("utf-8").split("\n"):
                    colorprint(f"  {l}","darkpurple")
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

def sunbreaker(com):
    colorprint(str(sb("".join(x+" "for x in com[1:len(com)]).strip())), "darkpurple")

def tt_update():
    update("/",["update","rdl","/","tt"])

def cy_run(com):
    commande = com[1:]
    if len(commande) > 0:
        retour = str(cy.run(commande))
        colorprint(retour,"darkpurple")
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
            colorprint("le fichier a été téléchargé!","darkpurple")

    else: erreur("006")

def py_exec(com):
    if len(com) > 1:
        try: exec("".join([c + " " for c in com[1:]]))
        except: erreur("008")
    else: erreur("006")

def help():
    def printhelp(nom,doc):
        colorprint(nom,"litepurple","k")
        colorprint(f": {doc}","darkpurple")
    printhelp("bvn","affiche l'écran de bienvenue")
    printhelp("cd [chemin]","change le dossier de travail")
    printhelp("cy <*arg>","lance des commandes cytron")
    printhelp("clear","efface la console")
    printhelp("help","affiche cette aide")
    printhelp("ls [chemin]","affiche le contenu dossier de travail ou du dossier spécifier")
    printhelp("mkdir <nom>","créé le dossier du nom spécifié")
    printhelp("sunbreaker <str>","afficher le break du texte entré")
    printhelp("tt-update","lance la misse à jour de terminal-tools")
    printhelp("tt-verion","affiche la version de terminal-tools et des modules")
    printhelp("update <*arg>","lance le systeme de mise a jour (update help)")
    printhelp("wget <chemin> <url>","télécharge un fichier depuis une url")

##### setup #####

global action_rep
action_rep = "/"

global co_user
co_user = StartLogin()
time = actual_time()
bvn()

##### debut du terminal #####

def interpreteur(ipt):
    time = actual_time()
    for i in ipt.split("&&"):
        com = [c for c in str(i).split(" ") if c != ""]
        if len(ipt.split("&&")) > 1:
            colorprint("──} ","darkpurple")
            colorprint(i.strip(),"darkpurple", "k")

        if com:
            rc = com[0] #root commande
            if rc == "bvn": bvn()
            elif rc == "cd": cd(com)
            elif rc == "cy": cy_run(com)
            elif rc in ["clear", "cls"]: clear()
            elif rc == "exec": py_exec(com)
            elif rc == "help": help()
            elif rc == "ls": ls(com)
            elif rc == "mkdir": mkdir(com)
            elif rc in ["sunbreaker", "sb"]: sunbreaker(com)
            elif rc == "tt-version": version()
            elif rc == "tt-update": tt_update()
            elif rc == "update": update(action_rep,com)
            elif rc == "wget": wget(com)
            else: erreur("001")
    return time

while True:
    time = interpreteur(user_input(time))