#viewing the runner's times

from tkinter import *
from tkinter.ttk import *
import sqlite3
from math import floor

def searchRunners(tree,fname = '', lname = ''):
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql ="""SELECT * FROM runners
WHERE fName LIKE ?
OR lName LIKE ?
"""
    q.execute(sql, [fname, lname])
    runners = q.fetchall()
    q.close()
    db.close()

    insertIntoTree(tree, runners)

    

def emptyTreeview(tree):
    for i in tree.get_children():
        tree.delete(i)

def createTree(tree, cols):
    global yscrollbar
    #creates headings
    for i in range(len(cols)):
        tree.heading('#'+str(i+1), text = cols[i], anchor = W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=90, width=90)
    tree.column('#2', stretch=NO, minwidth=150, width=150)
    tree.column('#3', stretch=NO, minwidth=150, width=150)
    tree.column('#4', stretch=NO, minwidth=150, width=150)

##    styleTree = Style()
##    styleTree.configure('Treeview', rowheight=35)
##    tree.configure(yscroll=yscrollbar.set)
    #need to figure out a way to get the scroll bar working

    
def insertIntoTree(tree, values):
    if len(tree.get_children()) > 0:
        emptyTreeview(tree)
    

    for i in values:
        tree.insert("", END, "", values=i, tag='rowFont')


def findRunnerTimes(tree):
    runnerA = tree.item(tree.focus())['values']#an array with the runners data
    #just got ID name form

    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = """SELECT times.event_id, events.name, locations.name, times.time FROM times, events, locations, runners
WHERE events.id = times.event_id
AND locations.id = events.location_id
AND runners.id = times.runner_id
AND times.runner_id = ?
"""
    if len(runnerA) != 0:
        q.execute(sql, [runnerA[0]])

        times = q.fetchall()
    q.close()
    db.close()
    for i in range(len(times)):
        hours = floor(times[i][-1]/3600)
        minutes = floor((times[i][-1]-hours*3600)/60)
        seconds = times[i][-1]-hours*3600-minutes*60
        times[i] = [times[i][x] for x in range(len(times[i])-1)]
        times[i].append(str(hours) + ':' + str(minutes) + ':' + str(seconds))

    return times
    
    
    

    

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


viewRSearchB = Button(viewRunnerFrm, text = "Find Name", command = lambda:searchRunners(runnersTreeview, viewRFNameIn.get(), viewRSNameIn.get()))
viewRSearchB.grid(row = 2, column =1)

viewRFindTsB = Button(viewRunnerFrm, text = "Find Times", command = lambda: insertIntoTree(timesTreeview,findRunnerTimes(runnersTreeview)))
viewRFindTsB.grid(row = 2, column = 2)



#ok how about i have 2 treeviews
#fist one a smaller one with the runners
#when a runner's selected, the second one shows their times and stuff
viewRunnersCols = ('ID', 'First Name', 'Surname', 'Form')
runnersTreeview = Treeview(viewRunnerFrm, columns = viewRunnersCols, selectmode = "browse", height = 3)
createTree(runnersTreeview, viewRunnersCols)
yscrollbar = Scrollbar(viewRunnerFrm, orient='vertical', command=runnersTreeview.yview)

#i think i need a better name
yscrollbar.grid(row=3, column=1,columnspan = 3, sticky=E+NS)


#insted of doing columnspan in the final prgogram just stick it on another frame
runnersTreeview.grid(row = 3, column= 1,columnspan = 3, sticky = NSEW)



viewRunnersTsCols = ('Event ID', 'Event Name', 'Location', 'Time')
timesTreeview = Treeview(viewRunnerFrm, columns = viewRunnersTsCols, selectmode = "extended", height = 5)
createTree(timesTreeview, viewRunnersTsCols)

timesTreeview.grid(row =4, column = 1, columnspan = 3, sticky = NSEW)



myGUI.mainloop()


print("viewRunner.py end")

#still need to be able to edit/add times
