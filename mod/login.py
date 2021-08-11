##### importation ####
from mod.ColorPrint import Background, Colors, colorprint, colorinput
from mod.sunbreaker import sunbreaker
import mod.cytron as cy
from os import system, name

##### setup #####
global logins, bad, islogin
logins = []
islogin_l = []
bad = []
login_liste = cy.cy_rfil_rela("/sys/","login.txt")
print(cy.cy_ls("/"))
user_liste = login_liste.split("\n")[0]
passw_liste = login_liste.split("\n")[1]
def clear():
    system('cls' if name == 'nt' else 'clear')

def done_bad_co(is_login = True, co_login_="" ,add=True, done = False):
    global logins, bad, islogin_l
    if add:
        if is_login == False:
            temp = ""
            for loop in range(len(list(co_login_))): temp+="•"
            co_login_ = temp
        logins.append(co_login_)
        bad.append(done)
        islogin_l.append(is_login)
    for x in range(len(logins)):
        if islogin_l[x]: colorprint("login",Colors.magenta)
        else: colorprint("password",Colors.magenta)
        colorprint("-} ",Colors.magenta,Background.none,False,False,False)
        print(logins[x],end="")
        if bad[x]: colorprint(" √",Colors.vert)
        else: colorprint(" x",Colors.rouge)

def pw():
    colorprint("password",Colors.magenta)
    co_passw = colorinput("-} ",Colors.magenta)
    done = False
    for all_passw in passw_liste.split("/"):
        if all_passw != "" and co_passw != "":
            if int(all_passw) == int(sunbreaker(co_passw)):
                clear()
                done_bad_co(False,co_passw,True,True)
                done = True
                break
    if done == False:
        clear()
        done_bad_co(False,co_passw,True)
        login()

def login():
    global co_login
    colorprint("login",Colors.magenta)
    co_login = colorinput("-} ",Colors.magenta)
    done = False
    for all_login in user_liste.split("/"):
        if all_login != "" and co_login != "":
            if int(all_login) == int(sunbreaker(co_login)):
                clear()
                done_bad_co(True,co_login,True,True)
                done = True
                pw()
                break
    if done == False:
        clear()
        done_bad_co(True,co_login)
        login()

def StartLogin():
    clear()
    login()
    return(co_login)