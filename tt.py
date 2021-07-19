##### importation ####
from os import system, name, popen
from re import T
import keyboard
import cytron

#### clear ####
def clear():
    system('cls' if name == 'nt' else 'clear')

#### print en coulleur ####

def cprint(color,color2,text):
    print(f"{color}{color2}"+text+f"{colors.RESET}")

class colors:
    NOIR = '\033[30m'
    BLUE = '\033[94m'
    VERT = '\033[92m'
    JAUNE = '\033[93m'
    ROUGE = '\033[91m'
    RESET = '\033[0m'
    GRAS = '\033[1m'
    SOULIGNER = '\033[4m'
    SURLIGNER = '\033[47m'

#### setup ####

choix = ["cytron","wsl statut"]

def convert(entre):    #truc maison moche pour enlever les caratères nul XD
	entre = entre.replace(".","yhujgfdx")
	entre = entre.replace("-","gbhnjklm")
	entre = entre.replace("*","qwsxdcfv")
	entre = entre.replace(" ","aqzsedrf")
	entre = entre.replace("\n","gtfrdesz")
	entre = "".join(e for e in entre if e.isalnum())
	entre = entre.replace("aqzsedrf"," ")
	entre = entre.replace("gtfrdesz","\n")
	entre = entre.replace("qwsxdcfv","*")
	entre = entre.replace("gbhnjklm","-")
	entre = entre.replace("yhujgfdx",".")
	return(entre)

#### debut du terminal ####

def bvn_sreen():
    global selct

    clear()

    cprint(colors.GRAS,"","Bienvenue sur terminal tools, utilisé les flèche de votre clavier pour sélectionner l’outil pour validé avec entré\n")
    
    for x in range(len(choix)):
        if selct == x:
            cprint(colors.SURLIGNER,colors.NOIR,choix[x])
        else:
            cprint(colors.RESET,"",choix[x])

    while keyboard.is_pressed('down') == True or keyboard.is_pressed('up') == True or keyboard.is_pressed('enter') == True:
        pass

    while True:
        if keyboard.is_pressed('down'):
            selct += 1
            if selct >= len(choix):
                selct = 0
            
            bvn_sreen()
            break

        elif keyboard.is_pressed('up'):
            selct -= 1
            if selct < 0:
                selct = len(choix) - 1

            bvn_sreen()
            break

        elif keyboard.is_pressed('enter'):
            while keyboard.is_pressed('enter') == True:
                pass
            app()
            break

def app():
    if selct == 0: #cytron
        clear()
        cytron.cy_console_print()
        while cytron.console_o == 0:
            pass
        while cytron.console_o == 1:
            pass
        while keyboard.is_pressed('enter') == True:
            pass
        initi()
    
    if selct == 1:
        aff = ""
        while keyboard.is_pressed('enter') == False:
            acc = convert(popen("wsl --list -v").read())
            if aff != acc:
                aff = acc
                clear()
                print(aff)
                
        initi()

def initi():
    global selct
    selct = 0
    bvn_sreen()

initi()