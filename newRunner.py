from tkinter import *
from tkinter.ttk import *
import sqlite3

def addNewRunner(ID, form, fname, lname):
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    
    sql = "INSERT INTO runners(id, fName, lName, form) VALUES(?,?,?,?)"
    q.execute(sql, [ID, fname, lname, form])
    
    db.commit()
    q.close()
    db.close()

myGUI = Tk()

newRunnerFrm = Frame(myGUI)
testLbl = Label(newRunnerFrm, text = "abcdefghijklmnopqrstuvwxyz")
#testLbl.grid(row =1, column = 1)
newFormLbl = Label(newRunnerFrm, text = "Form:")
newFormLbl.grid(row = 1, column =1)
newFormIn = StringVar()
newFormTB = Entry(newRunnerFrm, textvariable = newFormIn, width = 5)
newFormTB.grid(row = 1, column =2)

newNameLbl = Label(newRunnerFrm, text = "Name:")
newNameLbl.grid(row = 2, column = 1)
newFnameIn = StringVar()
newFnameTB = Entry(newRunnerFrm, textvariable = newFnameIn, width = 10)
newFnameTB.grid(row = 2, column = 2)
newSnameIn = StringVar()
newSnameTB = Entry(newRunnerFrm, textvariable = newSnameIn, width = 10)
newSnameTB.grid(row = 2, column =3)
newRunnerFrm.pack()

addRunnerB = Button(newRunnerFrm, text = "add runner", command = lambda:addNewRunner(10,newFormIn.get(), newFnameIn.get(),newSnameIn.get(), ))
addRunnerB.grid(row = 3, column =2)




myGUI.mainloop()
