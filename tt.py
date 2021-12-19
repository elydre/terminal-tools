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

tt_version = "v0.0.17c"

##### importation ####
import system.mod.cytron as cy
from system.mod.ColorPrint import colorprint, colorinput, setcolor, version as cp_version
from system.mod.moonbreaker import moonbreaker as mb, version as mb_version
from system.mod.login import StartLogin, login_setup
from system.mod.updater import update as start_update, road
from system.mod.themes import themes, theme_version
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
}

def erreur(e,*arg):
    colorprint("Erreur "+e,"litered", "k")
    colorprint(": " + erreurs[e].format(*arg),"darkred")

##### commandes #####

def makecolor(theme_name):
    for k in themes[theme_name].keys():
        setcolor(k,themes[theme_name][k])

def user_input(time):
    colorprint("\n┌──(","dark","k")
    colorprint(co_user,"lite","k")
    colorprint(" • ","dark","k")
    colorprint(str(round(actual_time() - time,2)),"lite","k")
    colorprint(")-[","dark","k")
    colorprint(action_rep,"cyan","k")
    colorprint("]","dark")
    return(colorinput("└─} ","dark"))

def clear():
    system('cls' if name == 'nt' else 'clear')

def bvn():
    colorprint("\nbienvenue ","dark","k")
    colorprint(co_user,"lite","k")
    colorprint(" sur Terminal Tools","dark")
    colorprint("Copyright (C) pf4. Tous droits réservés.\n","dark")

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
        colorprint(nom,"lite", "k")
        colorprint(f": {doc}", "dark")
    printversion("terminal tools", tt_version)
    printversion("cytron", cy.version())
    printversion("colorprint", cp_version)
    printversion("moonbreaker", mb_version)
    printversion("themes", theme_version)

def update(ar,com):  # sourcery no-metrics
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

def tt_update():
    update("/",["update","rdl","/","tt"])

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
        for theme_name in themes.keys():
            print()
            colorprint(f" -{theme_name.upper()}-", "dark")
            for k in themes[theme_name].keys():
                setcolor("temp", themes[theme_name][k])
                colorprint(f"• {k}", "temp")
    elif com[1] in themes.keys():
        makecolor(com[1])
    else: erreur("009",com[1])

def help():
    def printhelp(nom,doc):
        colorprint(nom,"lite","k")
        colorprint(f": {doc}","dark")
    printhelp("bvn","affiche l'écran de bienvenue")
    printhelp("cd [chemin]","change le dossier de travail")
    printhelp("cy <*arg>","lance des commandes cytron")
    printhelp("clear","efface la console")
    printhelp("exec <*arg>","lance des commandes python")
    printhelp("help","affiche cette aide")
    printhelp("ls [chemin]","affiche le contenu dossier de travail ou du dossier spécifier")
    printhelp("mkdir <nom>","créé le dossier du nom spécifié")
    printhelp("sunbreaker <str>","afficher le break du texte entré")
    printhelp("theme","affiche les themes disponibles")
    printhelp("theme <theme>","change le theme actuel")
    printhelp("tt-update","lance la misse à jour de terminal-tools")
    printhelp("tt-verion","affiche la version de terminal-tools et des modules")
    printhelp("update <*arg>","lance le systeme de mise a jour (update help)")
    printhelp("wget <chemin> <url>","télécharge un fichier depuis une url")

##### setup #####

def setup():
    global action_rep, time
    action_rep = "/"
    makecolor("default")

    global co_user
    login_setup()
    co_user = StartLogin()
    bvn()
    time = actual_time()

setup()

##### debut du terminal #####

def interpreteur(ipt):
    time = actual_time()
    for i in ipt.split("&&"):
        com = [c for c in str(i).split(" ") if c != ""]
        if len(ipt.split("&&")) > 1:
            colorprint("──} ","dark", "k")
            colorprint(i.strip(),"dark")

        if com:
            rc = com[0]             #prefixe de la commande
            if rc == "bvn": bvn()
            elif rc == "cd": cd(com)
            elif rc == "cy": cy_run(com)
            elif rc in ["clear", "cls"]: clear()
            elif rc == "exec": py_exec(com)
            elif rc == "exit": setup()
            elif rc == "help": help()
            elif rc == "ls": ls(com)
            elif rc == "mkdir": mkdir(com)
            elif rc in ["moonbreaker", "mb"]: moonbreaker(com)
            elif rc == "theme": theme(com)
            elif rc == "tt-version": version()
            elif rc == "tt-update": tt_update()
            elif rc == "update": update(action_rep, com)
            elif rc == "wget": wget(com)
            else: erreur("001")
    return time

while True:
    time = interpreteur(user_input(time))