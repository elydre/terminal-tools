##### importation ####
from system.mod.ColorPrint import colorprint, colorinput
from system.mod.sunbreaker import sunbreaker
import system.mod.cytron as cy
from os import system, name

##### setup #####
def login_setup():
    global logins, bad, islogin, user_liste, islogin_l
    logins = []
    islogin_l = []
    bad = []
    login_liste = cy.cy_rfil_rela("/system/","login.txt")
    print(cy.cy_ls("/"))
    user_liste = login_liste.split("\n")

def clear():
    system('cls' if name == 'nt' else 'clear')

def done_bad_co(is_login = True, co_login_="" ,add=True, done = False):
    global logins, bad, islogin_l
    if add:
        if not is_login:
            temp = "".join("•" for _ in range(len(list(co_login_))))
            co_login_ = temp
        logins.append(co_login_)
        bad.append(done)
        islogin_l.append(is_login)
    for x in range(len(logins)):
        if islogin_l[x]: colorprint("login","darkpurple")
        else: colorprint("password","darkpurple")
        colorprint("-} ","darkpurple", "k")
        print(logins[x],end="")
        if islogin_l[x]: pass
        elif bad[x]: colorprint(" √","green","k")
        else: colorprint(" x","red","k")
        print("\n")

def pw(co_login):
    colorprint("password","darkpurple")
    co_passw = colorinput("-} ","darkpurple")
    done = False
    for user in user_liste:
        name, mdp = user.split("/")[0], user.split("/")[1]
        if co_login != "" and co_passw != "" and int(name) == sunbreaker(co_login) and int(mdp) == sunbreaker(co_passw):
            clear()
            done_bad_co(False,co_passw,True,True)
            done = True
            break
    if not done:
        clear()
        done_bad_co(False,co_passw,True)
        login()

def login():
    co_login = ""
    global USER
    while co_login == "":
        colorprint("login","darkpurple")
        co_login = colorinput("-} ","darkpurple")
        print()
        USER = co_login
        logins.append(co_login)
        bad.append(True)
        islogin_l.append(True)

    if sunbreaker(co_login) != 188326779898774147196118067464521:
        pw(co_login)

def StartLogin():
    clear()
    login()
    return(USER)