#viewing the runner's times

from tkinter import *
from tkinter.ttk import *
import sqlite3

def searchRunners(fname, lname):
    pass

def emptyTreeview(tree):
    for i in tree.get_children():
        tree.delete(i)

def createTree(tree, cols):
    #creates headings
    for i in range(len(cols)):
        tree.heading('#'+str(i+1), text = cols[i], anchor = W)
##    tree.heading('#1', text='ID', anchor=W)
##    tree.heading('#2', text='First Name', anchor=W)
##    tree.heading('#3', text='Surname', anchor=W)
##    tree.heading('#4', text='Form', anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=90, width=90)
    tree.column('#2', stretch=NO, minwidth=150, width=150)
    tree.column('#3', stretch=NO, minwidth=150, width=150)
    tree.column('#4', stretch=NO, minwidth=150, width=150)

    
def insertIntoTree(tree, fname = '', lname = ''):
    if len(tree.get_children()) > 0:
        emptyTreeview(tree)
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql ="""SELECT * FROM runners
WHERE fName LIKE ?
AND lName LIKE ?
"""
    q.execute(sql, [fname, lname])
    runners = q.fetchall()
    q.close()
    db.close()

    for runner in runners:
        tree.insert("", END, "", values=runner, tag='rowFont')

    
    

    

myGUI = Tk()

viewRunnerFrm = Frame(myGUI)
viewRunnerFrm.pack()

viewRFNameIn = StringVar()
viewRSNameIn = StringVar()
viewRNameLbl = Label(viewRunnerFrm, text = 'Name:')
viewRNameLbl.grid(row = 1, column = 1)
viewRFNameTB = Entry(viewRunnerFrm , textvariable = viewRFNameIn)
viewRFNameTB.grid(row =1, column = 2)
viewRSNameTB = Entry(viewRunnerFrm, textvariable = viewRSNameIn)
viewRSNameTB.grid(row = 1, column = 3)


viewRSearchB = Button(viewRunnerFrm, text = "Find", command = lambda:insertIntoTree(runnersTreeview, viewRFNameIn.get(), viewRSNameIn.get()))
viewRSearchB.grid(row = 2, column =1)

#ok how about i have 2 treeviews
#fist one a smaller one with the runners
#when a runner's selected, the second one shows their times and stuff
viewRunnersCols = ('ID', 'First Name', 'Surname', 'Form')
runnersTreeview = Treeview(viewRunnerFrm, columns = viewRunnersCols, selectmode = "extended", height = 4)
createTree(runnersTreeview, viewRunnersCols)


#insted of doing columnspan in the final prgogram just stick it on another frame
runnersTreeview.grid(row = 3, column= 1,columnspan = 3, sticky = NSEW)


myGUI.mainloop()


print("viewRunner.py end")
