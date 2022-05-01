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

import sys, os
from urllib.request import urlopen
from urllib.error import HTTPError
# relative path

global PATH
PATH = os.path.dirname(sys.argv[0])

# list of road

road = ["https://raw.githubusercontent.com/pf4-DEV/online-update/main/road/main.txt"]

# languages

fr = {
"mkdir done":"dossier {} créé avec succès",
"mkdir err":"le dossier {} est déjà existant",
"wget done": "{} téléchargemé avec succès",
"cmd err": "commande inconnue ici -> {}",
"url err" : "url invalide ici -> {}",
"arg err": "argument inconnu ici -> {}",
"name err":"registre {} non trouvé dans les road",
"help":
"""
~ ~ ~ ~ AIDE ~ ~ ~ ~
- LANG
    lang permet de saisir la langue de l'updater, en/fr

    lang <langue>
    - lang en -

- DL
    dl permet de téléchargé un registre directement depuis son url

    dl <chemin> <url>
    - dl /main https://raw.githubusercontent.com/pf4-DEV/glade/main/update.txt -

- ROAD
    road permet de géré la liste des fichier de redirection:

    - road list - affiche la liste
    - road add - ajoute une url a la liste
    - road del - supprime une url a la liste
    - road read - lie les fichier de redirection

- RDL
    rdl téléchargé un registre depuis les fichier de redirection:

    dl <chemin> + <nom>
    - dl /main glade -"""}

en = {
"mkdir done":"folder {} successfully created",
"mkdir err":"the folder {} is already existing",
"wget done": "{} successfully downloaded",
"cmd err": "unknown command here -> {}",
"url err" : "invalid url here -> {}",
"arg err": "unknown argument here -> {}",
"name err":"register {} not found in the road",
"help":
"""~ ~ ~ ~ HELP ~ ~ ~ ~
- LANG
    lang allows you to enter the updater's language, en/fr

    lang <language>
    - lang en -

- DL
    dl allows you to download a register directly from its url

    dl <path> <url>
    - dl / main https://raw.githubusercontent.com/pf4-DEV/glade/main/update.txt -

- ROAD
    road allows you to manage the list of redirection files:

    - road list - display the list
    - road add - add an url to the list
    - road del - remove an url from the list
    - road read - link redirection files

- RDL
    rdl downloaded a registry from the redirect files: \

    dl <path> + <name>
    - dl / main glade -"""}

lang = en

# system function

def mkdir(chem, name):
    try:
        os.makedirs(PATH+chem+name)
        print(lang["mkdir done"].format(name))
    except FileExistsError: print(lang["mkdir err"].format(name))

def wget(chem, name, url):
    try:
        open(PATH + chem + name, 'wb').write(urlopen(url).read())
        print(lang["wget done"].format(name))
    except HTTPError: print(lang["url err"].format(url))

def mkchem(chem):
    dos = chem.split("/")
    while "" in dos: dos.remove("")
    for x in range(len(dos)):
        mkdir("","".join(f"/{dos[y]}" for y in range(x+1)))

# update launcher

def update(chem, updfile):
    mkchem(chem)
    try:
        l = urlopen(updfile).read().decode("utf-8").split("\n")
        for e in l:
            comp = str(e).split(" ")
            commande = comp[0].strip()
            arg = "".join(comp[1:]).split(",")
            if commande == "mkd":
                mkdir(chem, arg[0])
            elif commande == "wgt":
                wget(chem, arg[0],arg[1])
            elif commande != "":
                print(lang["cmd err"].format(commande))
    except HTTPError: print(lang["url err"].format(updfile))

# cli

def run():   # sourcery no-metrics
    while True:
        ipt = input("~} ").split(" ")
        for _ in range(10 - len(ipt)): ipt.append("")
        commande = ipt[0]
        if commande == "lang":
            if ipt[1] == "en": lang = en
            elif ipt[1] == "fr": lang = fr
            else: print(lang["arg err"].format(ipt[1]))
        elif commande == "dl":
            try: update(ipt[1],ipt[2])
            except: print(lang["url err"])
        elif commande in ["help", "h"]:
            print(lang["help"])
        elif commande in ["road", "r"]:
            if ipt[1] in ["list", "l"]:
                print(road)
            elif ipt[1] in ["add", "a"]:
                road.append(ipt[2])
            elif ipt[1] in ["del", "d"]:
                try: road.remove(ipt[2])
                except: print(lang["url err"])
            elif ipt[1] in ["read", "r"]:
                for r in road:
                    print(f"road: {r}")
                    for l in urlopen(r).read().decode("utf-8").split("\n"):
                        print(f"  {l}")
            else: print(lang["arg err"].format(ipt[1]))
        elif commande == "rdl":
            done = False
            for r in road:
                for l in urlopen(r).read().decode("utf-8").split("\n"):
                    l = str(l).split(",")
                    if l[0] == ipt[2]:
                        update(ipt[1],l[1].strip())
                        done = True
                        break
            if not done: print(lang["name err"].format(ipt[2]))
        else: print(lang["cmd err"].format(commande))

if __name__ == "__main__":
    run()