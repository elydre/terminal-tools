from os import name, system
from time import time as actual_time
from urllib.request import urlopen

import system.mod.cytron as cy
from system.mod.ColorPrint import colorinput, colorprint, setcolor
from system.mod.ColorPrint import version as cp_version
from system.mod.moonbreaker import moonbreaker as mb
from system.mod.moonbreaker import version as mb_version
from system.mod.updater import road
from system.mod.updater import update as start_update
from system.shell.login import StartLogin, login_setup
from system.shell.themes import color_themes, input_themes, theme_version

com_version = "0.0.1c"

def erreur(e, *arg):
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
        if mode == "demo":
            break

def bvn():
    colorprint("\nbienvenue ","dark","k")
    colorprint(co_user,"lite","k")
    colorprint(" sur Terminal Tools","dark")
    colorprint("Copyright (C) pf4. Tous droits réservés.\n","dark")

##### commandes #####

def clear(com, k):
    if len(com) == 1:
        system('cls' if name == 'nt' else 'clear')
    else: erreur("010", k["erreurs"])

def ls(com, k):
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

def cd(com, k):
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
            to_test = loc if loc.startswith("/") else action_rep + "/" + loc
            temp = [mors for mors in to_test.split("/") if mors != ""]
            to_test = ""
            for t in temp: to_test += "/" + t
            if to_test == "": to_test = "/"
            try:
                cy.cy_ls(to_test)
                action_rep = to_test
            except: erreur("002",to_test)
    else: action_rep = "/"

def version(com, k):
    if len(com) == 1:
        def printversion(nom,doc):
            colorprint(nom,"lite", "k")
            colorprint(f": {doc}", "dark")
        printversion("terminal tools", k["tt_version"])
        printversion("cytron", cy.version())
        printversion("colorprint", cp_version)
        printversion("moonbreaker", mb_version)
        printversion("themes", theme_version)
        printversion("commande", com_version)
    else: erreur("010")

def update(com, k):  # sourcery no-metrics
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

def moonbreaker(com, k):
    colorprint(str(mb("".join(x+" "for x in com[1:len(com)]).strip())), "dark")

def tt_update(com, k):
    if len(com) == 1:
        update(["update", "rdl", "/", "tt"], k)
    else: erreur("010")

def cy_run(com, k):
    commande = com[1:]
    if len(commande) > 0:
        retour = str(cy.run(commande))
        colorprint(retour,"dark")
    else:
        erreur("006")

def mkdir(com, k):
    if len(com) > 1:
        for e in com[1:]:
            cy.mkdir(action_rep, e)
    else: erreur("006")

def wget(com, k):
    if len(com) > 1:
        if cy.wget(action_rep, com[1], com[2]) == "DONE":
            colorprint("le fichier a été téléchargé!","dark")

    else: erreur("006")

def py_exec(com, k):
    if len(com) > 1:
        try: exec("".join([c + " " for c in com[1:]]))
        except Exception as e: erreur("008", str(e))
    else: erreur("006")

def theme(com, k):
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
                user_input(k["time"], theme_name, "demo")
                print("\n")
        elif com[2] in input_themes.keys():
            input_theme_name = com[2]
        else: erreur("009",com[2])
    else: erreur("004",com[1])
    
def quiter(com, k):
    if len(com) == 1:
        clear(["clear"], None)
        exit()
    elif com[1] == "logout":
        setup()
    else: erreur("004",com[1])

def help(com, k):
    def printhelp(nom,doc):
        colorprint(nom,"lite","k")
        colorprint(f": {doc}","dark")
    if len(com) == 1:
        for c in k["path"].keys():
            printhelp(c,k["path"][c][1])
    elif com[1] in k["path"].keys():
        printhelp(com[1],k["path"][com[1]][1])
    else: erreur("004",com[1])

##### setup #####

def setup(e):
    global action_rep, input_theme_name, erreurs
    erreurs = e
    action_rep = "/"
    input_theme_name = "kalike"
    makecolor("default")

    global co_user
    login_setup()
    co_user = StartLogin()
    bvn()