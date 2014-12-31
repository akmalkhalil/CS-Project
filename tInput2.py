#what about adding a new event
#or adding a new runner
#admin rights bro





from tkinter import *
from tkinter.ttk import *
import sqlite3, time
from math import floor

def exitT():
    timeEntryFrm.pack_forget()
def showTimesIn():
    timeEntryFrm.pack()
def save():
    #dont run unless it's been checked
    #ie checked == True
    seconds = 0
    seconds += timeHIn.get() * 60*60
    seconds += timeMIn.get() * 60
    seconds += timeSIn.get()
    print(seconds)
    secondsLbl = Label(timeEntryFrm, text = str(seconds))
    secondsLbl.grid(row = 3, column = 2)

#to stop me creating hundreds of entrys in the DB
##    db = sqlite3.connect("runningDB/running.db")
##    q = db.cursor()
##    sql = "INSERT INTO times(runner_id, event_id, time) VALUES(?,?,?)"
##    q.execute(sql, [runnerID, '4', seconds])#SHOULD HAVE TO CHECK IF THERES ALREADY AN ENTRY
##    print(runnerID)
##    q.close()
##    db.commit()
##    db.close()

def checkN():
    #edit so that search by form first, then by sname the fname, until we have 1person
    global runnerID
    IDout=0
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = "SELECT * FROM runners"
    q.execute(sql)
    runners = q.fetchall()
    q.close()
    db.close()

    #print(formIn.get())
    #first we check the form
    if len(formIn.get()) != 0 :
        for i in range(len(runners)):
            #print(runners[i])
            if runners[i][3] != formIn.get():
                #print("kill me")
                runners.remove(runners[i])
    #print()
    #print(runners)
    if len(runners) == 1:#then we have our runner
        checkOut.set(runners[0])
        #then leave this
    else:#check names
        runnersFN = []#firstnames
        runnersSN = []#surnames
        IDs = []
        for i in range(len(runners)):
            runnersFN.append(runners[i][1].lower())
            runnersSN.append(runners[i][2].lower())
            IDs.append(runners[i][0])
            
        for i in range(len(runnersFN if runnersFN != [] else runenrsSN)):#why would runnersFN ever be empty??
            if fnameIn.get().lower() == runnersFN[i] and snameIn.get().lower() == runnersSN[i]:
            #if nameIn.get() == runnersN[i] or nameIn.get() == runnersFN:
                #print("we has a match")
                #the one in runners with ID == IDs[i]
                #print(IDs[i])
                IDout = IDs[i]
        for i in range(len(runners)):
            if runners[i][0] == IDout:
                checkOut.set(runners[i])
                runnerID = IDout

                showGraph()



            
def getEvents():#the events in the dropdown box
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = "SELECT * FROM events"
    q.execute(sql)
    returned = q.fetchall()
    q.close()
    #db.commit()
    db.close()
    return returned


def disTs(ID):#display times
    #need to chenge this function to work ith this program
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = """ SELECT * FROM times, runners, events, locations
WHERE times.runner_id = runners.id
AND events.location_id = locations.id
AND times.event_id = events.id
AND runners.id = (?)

"""
    q.execute(sql, [ID])

    blob = q.fetchall()

    q.close()
    db.close()
    #return blob
    data = blob
    


    otherThing = []
    #lab = Label(myGUI, text = "time_ID,")
    headings = ("T_ID", "E_ID", "time", "R_ID", "fname", "sname", "form", "E_ID", "L_ID", "E_name",'date', "L_ID", "L_name",'address')
    for i in range(len(data)):
        if i == 0:
            for j in range(len(headings)):
                lab = Label(viewTimesFrm, text = headings[j])
                lab.grid(row = 1, column = j)
        otherThing.append(data[i])
        otherThing.append('\n')
        lab = Label(viewTimesFrm, text = data[i])
        #lab.pack()
        
        for j in range(len(data[i])):
            lab = Label(viewTimesFrm, text = data[i][j])
            lab.grid(row = i + 2, column = j)
        #print(i+2)
        #print(len(data)+2)


    exitVTB.grid(row = len(data) +2, column = 1, columnspan = 3)
    viewTimesFrm.pack()



#functions for graph
    #https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter
def motion(event):
    x,y = event.x, event.y
    ##print('{},{}'.format(x,y))
    for i in range(0,len(times),1):
        yp = mapRange(times[i], 0,yMax, 0, windowH - margin)
        if calcDist(x, y, i*sqrx+margin, windowH-yp) <= 15:
            print('{},{}'.format(x,y))
####  for (i = 0; i<times.length; i++) {
####    yp = map(times[i], 0, 2000, 0, height - margin);
####    if (dist(mouseX,mouseY,i*sqrx + margin, height -yp)<=15) {
####      pointx = i;
####      pointy = times[i];
####    } /*else {
####      pointx = 0;
####      pointy = 0;
####    } */
####  }    

def mapRange(val, start0, stop0, start1, stop1):
    range0 = stop0-start0
    range1 = stop1-start1
    Pcent = (val -start0)/range0
    finalV = range1 * Pcent + start1
    return finalV
def calcDist(x1,y1,x2,y2):
    xSqr = (x1 - x2)**2
    ySqr = (y1 - y2)**2
    dist = (xSqr + ySqr)**0.5
    return dist

def loadData(ID):
##    Fname = input("first name of runner:  ")
##    Lname = input("last name of runner:  ")
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = """ SELECT * FROM times, runners, events, locations
WHERE times.runner_id = runners.id
AND events.location_id = locations.id
AND times.event_id = events.id
AND runners.id = ?
AND locations.id = 2
"""
    #q.execute(sql, [Fname, Lname])
    q.execute(sql,[ID])
    blob = q.fetchall()

    q.close()
    db.close()
    return blob
#functionsfor graph

    



runnerID = 0
checked = False

myGUI = Tk()
#myGUI.geometry("400x300+450+150")
myGUI.title("times input")

myMenuBar = Menu(myGUI)
fileMenu = Menu(myMenuBar)
fileMenu.add_command(label = "Input times", command = showTimesIn)
fileMenu.add_command(label = "View Times", command = lambda: disTs(runnerID))
fileMenu.add_command(label = "ViewGraph", command = lambda: graphFrm.pack())
myMenuBar.add_cascade(label = "File", menu = fileMenu)

myGUI.config(menu = myMenuBar)


#name and form
nameEntryFrm = Frame(myGUI)
nameEntryFrm.pack()

nameLbl = Label(nameEntryFrm, text = "Name:")
nameLbl.grid(row = 2, column = 1)
fnameIn = StringVar()
fnameTB = Entry(nameEntryFrm, textvariable = fnameIn, width = 10)
fnameTB.grid(row = 2, column = 2)
snameIn = StringVar()
snameTB = Entry(nameEntryFrm, textvariable = snameIn, width = 10)
snameTB.grid(row = 2, column =3)

formLbl = Label(nameEntryFrm, text = "Form:")
formLbl.grid(row = 1, column =1)
formIn = StringVar()
formTB = Entry(nameEntryFrm, textvariable = formIn, width = 5)
formTB.grid(row = 1, column =2)
#check the name
checkB = Button(nameEntryFrm, text = "Find Me!", command = checkN)
checkB.grid(row = 3, column =1)
checkLbl = Label(nameEntryFrm, text = "is this you")
checkLbl.grid(row = 4, column =1)
checkOut = StringVar()
checkOutTB = Entry(nameEntryFrm, textvariable = checkOut)
checkOutTB.grid(row = 4, column =2, columnspan = 2)

timeEntryFrm = Frame(myGUI)
#timeEntryFrm.pack()
eventsLbl = Label (timeEntryFrm, text = "Event")
eventsLbl.grid(row = 1, column = 1)
events = StringVar()
#events.set
#cant do this until urv replys
# i need to get the vals from the list gen in getEvents() and put them in the OM
#i'm using a combobox
eventsRaw = getEvents()
eventsA = []
for i in range(len(eventsRaw)):
    print(eventsRaw[i])
    eventsA.append(str(eventsRaw[i][2])+':'+eventsRaw[i][3])
eventsCB = Combobox(timeEntryFrm, values = eventsA)
eventsCB.grid(row = 1, column =2, columnspan = 3)
testThingLbl = Label(timeEntryFrm, textvariable = eventsCB.current())
testThingLbl.grid(row = 4, column =2)

#time label and entry box
timeLbl = Label(timeEntryFrm, text = "Time")
timeLbl.grid(row = 2, column = 1)

timeHIn = IntVar()#hours
timeHTB = Entry(timeEntryFrm, textvariable = timeHIn, width = 2)
timeHTB.grid(row = 2, column = 2, sticky = W)
testLbl1 = Label(timeEntryFrm, text = "h")#ive tried hrs and hours but doesn't look good
testLbl1.grid(row = 2, column = 2, sticky = E)
timeMIn = IntVar()#minutes
timeMTB = Entry(timeEntryFrm, textvariable = timeMIn, width = 2)
timeMTB.grid(row = 2, column = 3)
timeSIn = IntVar()#seconds
timeSTB = Entry(timeEntryFrm, textvariable = timeSIn, width = 2)
timeSTB.grid(row = 2, column = 4)


saveB = Button(timeEntryFrm, text = "save", command = save)
saveB.grid(row = 3, column = 1)

exitTimesB = Button(timeEntryFrm, text = "done", command = exitT)
exitTimesB.grid(row =3, column = 3)



#now to view their times
viewTimesFrm = Frame(myGUI)

exitVTB = Button(viewTimesFrm, text = "Done", command = lambda: viewTimesFrm.pack_forget())



#and now the amazing graph
graphFrm = Frame(myGUI)
def showGraph():
    runnerData = loadData(runnerID)
    dates = []
    for i in range(len(runnerData)):
        dates.append(runnerData[i][10])
    print(dates)
    times = []
    for i in range(len(runnerData)):
        times.append(runnerData[i][2])
    print(times)
    for i in runnerData:
        print(i)

    yMax = floor((max(times)/10**(len(str(max(times)))-1)+1))*10**(len(str(max(times)))-1)
    print(yMax)
    windowW =  400
    windowH = 500
    margin = 20
    sqrx = int((windowW - margin)/10)
    sqry = int((windowH - margin)/10)
    Tsize = 12

    graphC = Canvas(master = graphFrm, width = windowW, height = windowH, bg = "grey")#C for canvas
    graphC.pack()

    #axis
    graphC.create_line(0, windowH - margin, windowW, windowH - margin, fill = "red", width = 5)
    graphC.create_line(margin, 0,margin, windowH, fill = "red", width = 5)
    #grid and axis labels for Y
    for i in range(windowH - margin, 0, -sqry):
        graphC.create_line(0,i, windowW, i)
        #yLbl = Label(myGUI, text = str(i))
        yLbl = Label(graphFrm, text = str(mapRange(windowH - i, 20, windowH, 0,yMax)))
        yLbl.place(x = 0, y = i)
    #x-axis
    for i in range(margin, windowW, sqrx):
        graphC.create_line(i, 0, i, windowH)
        xLbl = Label(graphFrm, text = str((i-margin)/sqrx))
        if (i-margin)/sqrx < len(dates):
            xLbl = Label(graphFrm,  text = dates[int((i-margin)/sqrx)])
            
        xLbl.place(x = i,y = windowH-margin)
        
    #the line
    for i in range(0, len(times)-1, 1):
        #print(i)
        yp = times[i]*(windowH - margin)/yMax
        yp2 = times[i+1]*(windowH - margin)/yMax
        #xp???
        
        graphC.create_line(i*sqrx + margin, windowH - yp, (i+1)*sqrx + margin, windowH - yp2, fill = "blue")
    exitGraphB.pack()
#graphFrm.pack()
#showGraph()
exitGraphB = Button(graphFrm, text = "Done", command = lambda: graphFrm.pack_forget())



myGUI.mainloop()
