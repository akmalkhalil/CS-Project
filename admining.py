from tkinter import *
from tkinter.ttk import *
import sqlite3, time
from math import floor

def testUNPW(unIn,pwIn):
    #ok so we need to check UN and PW
    global failedLogins
    if failedLogins >=5:
        print("tried more than 5 times. LOCKED OUT")
    elif unIn != UN:
        print("wrong UN")
        failedLogins += 1
    elif pwIn != PW:
        print("wrong PW")
        failedLogins +=1
    elif unIn == UN and pwIn == PW:
        print("we're in")
        signInFrm.pack_forget()
        adminFrm.pack()



def newRunner():
    print("yep this is how you create a new runner")
def newEvent():
    print("clearly creating a new event")
def newTime():
    print("use code from tInputs")
def checkTimes():
    print("""the runners are able to enter their own times
this is so Dr.H can check it""")

def addR(ID,form,fname,sname, out = ''):
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = "INSERT INTO runners(id, fName, lName, form) VALUES(?,?,?,?)"
    #q.execute(
    #db.commit()
    q.close()
    db.close()



myGUI = Tk()
myGUI.title("admin stuffs")

UN = "bob"
PW = "blob"
failedLogins = 0

signInFrm = Frame(myGUI)
signInFrm.pack()

userNLbl = Label(signInFrm, text = "Username: ")
userNLbl.grid(row = 1, column = 1)
passWLbl = Label(signInFrm, text = "Password: ")
passWLbl.grid(row = 2, column = 1)

userNIn = StringVar()
#userNIn.set("are you bob")
userNTB = Entry(signInFrm, textvariable = userNIn)
userNTB.grid(row = 1, column =2)
passWIn = StringVar()
passWIn = Entry(signInFrm, textvariable = passWIn)
passWIn.grid(row = 2, column =2)

signInB = Button(signInFrm,text = "Sign In", command = lambda:testUNPW(userNIn.get(), passWIn.get()))
signInB.grid(row = 3, column =1)






adminFrm = Frame(myGUI)#ok is it actually admin or is that just a word i'm using

welcomeLbl = Label(adminFrm, text = "WELCOME")
welcomeLbl.grid(row = 0, column = 1, columnspan =2)

newRunnerB = Button(adminFrm, text = "Add a New Runner", command = lambda: newRunnerFrm.pack())
newRunnerB.grid(row = 1, column = 1)
newEventB = Button(adminFrm, text = "Add a New Event", command = newEvent)
newEventB.grid(row = 1, column = 2)
addTimesB = Button(adminFrm, text = "Add Time", command = newTime)
addTimesB.grid(row = 2, column = 1)
checkTimesB = Button(adminFrm, text = "Check times", command = checkTimes)
checkTimesB.grid(row = 2, column =2)




newRunnerFrm = Frame(myGUI)
testLbl = Label(newRunnerFrm, text = "abcdefghijklmnopqrstuvwxyz")
#testLbl.grid(row =1, column = 1)
newFormLbl = Label(newRunnerFrm, text = "Form:")
newFormLbl.grid(row = 1, column =1)
newFormIn = StringVar()
newFormTB = Entry(newRunnerFrm, textvariable = newFormIn, width = 5)
newFormTB.grid(row = 1, column =2)
newIDLbl = Label(newRunnerFrm, text = "ID:")
newIDLbl.grid(row =1, column = 3)
newIDIn = StringVar()
newIDTB = Entry(newRunnerFrm, textvariable = newIDIn, width = 4)
newIDTB.grid(row = 1, column = 4)

newNameLbl = Label(newRunnerFrm, text = "Name:")
newNameLbl.grid(row = 2, column = 1)
newFnameIn = StringVar()
newFnameTB = Entry(newRunnerFrm, textvariable = newFnameIn, width = 10)
newFnameTB.grid(row = 2, column = 2)
newSnameIn = StringVar()
newSnameTB = Entry(newRunnerFrm, textvariable = newSnameIn, width = 10)
newSnameTB.grid(row = 2, column =3)

addB = Button(newRunnerFrm, text = "Add runner", command = lambda: addR(newIDIn.get(),newFormIn,get(), newFnameIn.get(), newSnameIn.get()))
addB.grid(row = 4,column = 1)
exitNewRunnerB = Button(newRunnerFrm, text = "done adding", command = lambda: newRunnerFrm.pack_forget())
exitNewRunnerB.grid(row = 6, column  = 1)

myGUI.mainloop()




