##### importation ####
from mod.ColorPrint import Background, Colors, colorprint, colorinput
from mod.sunbreaker import sunbreaker
from mod.login import StartLogin
import mod.cytron as cy
from os import system, name

##### erreur #####
def erreur(num,text="commande inconnue"):
    colorprint("Erreur "+num,Colors.rouge,Background.none,False,True,False)
    colorprint(": "+text,Colors.rouge,Background.none,False,False,True)

##### commandes #####
def clear():
    system('cls' if name == 'nt' else 'clear')

def bvn():
    colorprint("\nbienvenue ",Colors.magenta,Background.none,False,False,False)
    colorprint(co_user,Colors.magenta,Background.none,False,True,False)
    colorprint(" sur Terminal Tools",Colors.magenta,Background.none,False,False,True)
    colorprint("Copyright (C) pf4. Tous droits réservés.\n",Colors.magenta,Background.none,False,False,True)

def ls():
    try:
        rep = com[1]
    except:
        rep = "/"
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
        except:
            pass
        loc += com[len(com)-1]
        loc = loc.replace("\\","/")
        if loc.startswith("..") or loc.startswith("/.."):
            temp4 = ""
            temp3 = action_rep.split("/")
            for x in range(len(temp3)-1): temp4 += "/" + temp3[x]
            action_rep = temp4
        else:
            to_test = action_rep + "/" + loc
            temp = []
            for mors in to_test.split("/"): 
                if mors != "": temp.append(mors)
            to_test = ""
            for temp2 in temp: to_test += "/" + temp2
            try:
                cy.cy_ls(to_test)
                action_rep = to_test
            except:
                erreur("002","dossier de destination invalide, ici -> "+to_test)
    else:
        action_rep = "/"

def user_input():
    colorprint("\n┌──(",Colors.magenta,Background.none,False,False,False)
    colorprint(co_user,Colors.magenta,Background.none,False,True,False)
    colorprint(")-[",Colors.magenta,Background.none,False,False,False)
    colorprint(action_rep,Colors.cyan,Background.none,False,True,False)
    colorprint("]",Colors.magenta,Background.none,False,False,True)
    return(colorinput("└─} ",Colors.magenta,Background.none,False,False))

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
    if rc == "clear" or rc == "cls": clear()
    elif rc == "bvn": bvn()
    elif rc == "ls": ls()
    elif rc == "cd": cd()
    elif rc == "": pass
    else: erreur("001")

while True:
    interpreteur(user_input())