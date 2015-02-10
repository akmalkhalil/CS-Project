from tkinter import *
from tkinter.ttk import *
import sqlite3
from math import floor
from random import randint

def save(note):
    seconds = 0
    try:
        seconds += timeHIn.get() * 60*60
        seconds += timeMIn.get() * 60
        seconds += timeSIn.get()
        if timeHIn.get()>4:
            note.set("time must be less than 5 hours")
            return
        if timeMIn.get()>=60:
            note.set("minutes cannot be greater than 60")
            return
        if timeSIn.get()>=60:
            note.set("seconds cannot be greater than 60")
            return
    except ValueError:
        note.set("hours,minutes and seconds must each be integers")
        return
    
    #note.set(str(seconds))
##    secondsLbl = Label(timeEntryFrm, textvariable = savingNote)
##    secondsLbl.grid(row = 4, column = 2)

    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = """SELECT runner_id, event_id FROM times
WHERE runner_id = ?

"""
    q.execute(sql, [runnerID])
    times = q.fetchall()
    exists = False
    for i in range(len(times)):
        if str(times[i][1]) == eventsIn.get().split(':')[0]:
            exists = True
            note.set("A record for this event already exists")
    if runnerID == 0:
        note.set("No runner has been selected")
    elif eventsIn.get() == "No Event Selected":
        note.set("No event has been selected")
    elif not exists:
        sql = "INSERT INTO times(runner_id, event_id, time,checked) VALUES(?,?,?,?)"
        q.execute(sql, [runnerID, eventsIn.get().split(':')[0], seconds,0])
        db.commit()
        note.set("Saved")
    
    q.close()
    db.close()

def getEvents():#the events in the dropdown box
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    sql = "SELECT * FROM events"
    q.execute(sql)
    returned = q.fetchall()
    q.close()
    db.close()
    return returned

def disTs(ID, tree, yscroll):#display times
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = """ SELECT events.id, events.name, locations.name, locations.length, events.date, times.time, times.checked
FROM events, locations, times, runners
WHERE events.id = times.event_id
AND events.location_id = locations.id
AND times.runner_id = runners.id
AND runners.id = ?
ORDER BY events.date DESC

"""
    
    q.execute(sql, [ID])

    data = q.fetchall()

    q.close()
    db.close()


    for i in range(len(data)):
        hours = floor(data[i][-2]/3600)
        minutes = floor((data[i][-2]-hours*3600)/60)
        seconds = data[i][-2]-hours*3600-minutes*60
        if data[i][-1] == 1:
            checker = '✓'
        else:
            checker = '✗'
        data[i] = [data[i][x] for x in range(len(data[i])-2)]
        data[i].append(str(hours) + ':' + str(minutes) + ':' + str(seconds))
        data[i].append(checker)
    
    insertIntoTree(tree, data)
    tree.grid(row =1,column =1, sticky = NSEW)
    yscroll.grid(row =1, column = 1, sticky = E+NS)

    exitVTB.grid(row=2, column = 1)
    viewTimesFrm.pack()

def mapRange(val, start0, stop0, start1, stop1):
    range0 = stop0-start0
    range1 = stop1-start1
    Pcent = (val -start0)/range0
    finalV = range1 * Pcent + start1
    return finalV

def loadData(ID,locID):
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    sql = """ SELECT * FROM times, runners, events, locations
WHERE times.runner_id = runners.id
AND events.location_id = locations.id
AND times.event_id = events.id
AND runners.id = ?
AND locations.id = ?
"""
    q.execute(sql,[ID,locID])
    blob = q.fetchall()

    q.close()
    db.close()
    return blob

def adminOpts(opt):
    if opt == "NEWRUNNER":
        newRunnerFrm.pack()
        newEventFrm.pack_forget()
        viewRunnerFrm.pack_forget()
    elif opt == "NEWEVENT":
        newEventFrm.pack()
        newRunnerFrm.pack_forget()
        viewRunnerFrm.pack_forget()
    elif opt == "VIEWRUNNER":
        viewRunnerFrm.pack()
        newRunnerFrm.pack_forget()
        newEventFrm.pack_forget()

def addNewRunner(ID, form, fname, lname):

    try:
        int(ID)
    except ValueError:
        newRNote.set("ID must be an integer")
        return#move rest of code up into try
    #what about -ves
    if len(ID) != 4:
        newRNote.set("ID must be four digits long")
        print("here")
    
    un = lname+str(ID)
    pw = genRanLetters(5)
    
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    
    sql = "INSERT INTO runners(id, fName, lName, form,username,password) VALUES(?,?,?,?,?,?)"
    try:
        q.execute(sql, [ID, fname, lname, form,un,pw])
        newRNote.set("Username: "+un+", Password= "+pw)
    except sqlite3.IntegrityError:
        newRNote.set("Runner with that ID exists")
##    except sqlite3.OperationalError(" database is locked"):
##        print("broken")
    
    db.commit()
    q.close()
    db.close()
    

def genRanLetters(l):
    string = ''.join([chr(randint(65,90)) if randint(0,1) == 0 else chr(randint(97,122)) for x in range(l)])
    return string

def getLocs():#when adding events need the location
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    sql = "SELECT * FROM locations"
    q.execute(sql)
    returned = q.fetchall()
    q.close()
    db.close()
    return returned

def saveEvent(eventID,locID, eventN, dateD,dateM,dateY, note):
    date = str(dateY.get()) + '-' + str(dateM.get()) + '-' + str(dateD.get())
    
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    try:
        sql = "SELECT id FROM events"
        if (int(eventID),) in q.execute(sql).fetchall():
            note.set("You must enter a unique ID for the event")
        elif dateD.get()<1 or dateD.get() >31:
            note.set("dates must be DD/MM/YYYY\nthe day must be in between 1 and 31, inclusive")
        elif dateM.get()<1 or dateM.get()>12:
            note.set("dates must be DD/MM/YYYY\nthe month must be in between 1 and 12, inclusive")
        else:
        
            sql = "INSERT INTO events(id, location_id, name, date) VALUES(?,?,?,?)"
            q.execute(sql, [int(eventID),locID, eventN,date])
            db.commit()
            note.set("Added: "+str(eventID)+', '+eventN+', '+date)
    except ValueError:
        note.set("ID must be an integer")

    
    q.close()
    db.close()

    

def findNextEID():
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    sql = "SELECT id FROM events ORDER BY id"
    q.execute(sql)
    allEs = q.fetchall()
    q.close()
    db.close()

    count = 0
    running = True
    while running:
        count+=1
        if count == len(allEs)-1:
            running = False
            count+=1
        elif allEs[count][0] + 1 != allEs[count+1][0]:
            running = False
            count += 1
    count+=1
    return count

def searchRunners(tree,fname, lname, ID):
    try:
        ID = int(ID)
    except ValueError:
        ID = 0

    
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    
    if len(fname) == 0 and len(lname) == 0 and ID == 0:
        sql = "SELECT * FROM runners"
        q.execute(sql)
    else:
        sql ="""SELECT * FROM runners
WHERE fName LIKE ?
OR lName LIKE ?
OR id Like ?
"""
    
        q.execute(sql, [fname, lname,ID])
    runners = q.fetchall()
    q.close()
    db.close()

    insertIntoTree(tree, runners)

def emptyTreeview(tree):
    for i in tree.get_children():
        tree.delete(i)

def createTree(tree, cols, yscroll, widths):#len(widths) must >= len(cols)
    #creates headings
    for i in range(len(cols)):
        tree.heading('#'+str(i+1), text = cols[i], anchor = W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    for i in range(len(cols)):
        tree.column('#'+str(i+1), stretch = NO, minwidth = widths[i], width = widths[i])
    tree.configure(yscroll=yscroll.set)

def insertIntoTree(tree, values):
    if len(tree.get_children()) > 0:
        emptyTreeview(tree)
    

    for i in values:
        tree.insert("", END, "", values=i, tag='rowFont')

def findRunnerTimes(tree):
    runnerA = tree.item(tree.focus())['values']#an array with the runners data
    #just got ID name form

    db = sqlite3.connect("runningDB2/running.db")
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

def testUNPW3(unIn, pwIn, note):
    global DB, runnerID, failedLogins
    if failedLogins >= 5:
        note.set("LOCKED OUT")
        return
    elif unIn == "bob" and pwIn == "blob":
        signInFrm.pack_forget()
        adminFrm.pack()
    note.set("loading")
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()
    sql = """SELECT id, fname, lname, form FROM runners
WHERE runners.username = ?
AND runners.password = ?
"""
    q.execute(sql,[unIn, pwIn])
    runner = q.fetchall()
    if len(runner) !=1:
        note.set("Username or password are incorrect")
        failedLogins+=1
    else:
        note.set("logging in")
        runner =  runner[0]
        checkOut.set(runner)
        runnerID = runner[0]
        signInFrm.pack_forget()
        nameEntryFrm.pack()
        #genGraph()
    q.close()
    db.close()

def selectRunner(tree):
    global runnerID
    if tree.focus() != '':
        runnerID = tree.item(tree.focus())['values'][0]
        selectedUserOut.set(str(tree.item(tree.focus())['values'][1])+' '+str(tree.item(tree.focus())['values'][2]))
        adminRunnerDBOptsTL.deiconify()

def addNewLoc(ID,name,addr,dist,locA,note):
    global newEventLocCB
    
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = "SELECT id FROM locations"
    locids = q.execute(sql).fetchall()
    try:
        if (int(ID),) in locids:
            note.set("ID is not unique")
            return
        elif int(ID) == 0:
            note.set("ID cannot be 0")
            return
    except ValueError:
        note.set("ID must be an integer")
        return
    try:
        if float(dist) <= 0:
            note.set("Distance be greater than 0")
            return
    except ValueError:
        note.set("The distance must be a number")
        return
    
    sql = "INSERT INTO locations(id,name,address,length) VALUES(?,?,?,?)"
    q.execute(sql, [int(ID),name,addr,float(dist)])
    
    db.commit()
    q.close()
    db.close()
    
    newLoc = str(ID) +','+ name+','+ addr+' '+str(dist)
    locA.append(newLoc)
    newEventLocCB['values'] = locA
    note.set("New location added")
    

def editRunnerDetails(ID,runnerDetailsA):
    #ok so we get all the runners stuffs from DB
    #stick it in Entry boxes
    #then a save changes button
    #ugh i'm gonna have a frame within a frame within a frame on the main GUI
    
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()

    sql = "SELECT form,username,password FROM runners WHERE id = ?"

    q.execute(sql, [ID])
    #runnerDetailsA.append(q.fetchall()[0])
    returned = q.fetchall()[0]
    for i in range(3):
        runnerDetailsA[i].set(returned[i])
    q.close()
    db.close()
    editingRunnerFrm.grid(row =3,column = 1, columnspan = 2)

def deleteRunner(ID,TL):
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()

    sql = """DELETE FROM runners
WHERE id = ?
"""
    q.execute(sql, [ID])
    sql = """DELETE FROM times
WHERE runner_id = ?
"""
    q.execute(sql, [ID])

    db.commit()
    q.close()
    db.close()

    adminRunnerDBOptsTL.withdraw()

def saveRunnerEdits(ID, runnerDetailsA):
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()

    sql = """UPDATE runners
SET form = ?, username = ?, password = ?
WHERE id = ?
"""
    q.execute(sql, [runnerDetailsA[0].get(), runnerDetailsA[1].get(), runnerDetailsA[2].get(), ID])
    db.commit()
    q.close()
    db.close()

def editRunnerTimes(ID, timesTree, timesFrm, timeA):
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()
    print(ID)
    print(timesTree.item(timesTree.focus())['values'])
##    timesFrm.pack_forget()
##    timesFrm.pack()
    selectedTime = timesTree.item(timesTree.focus())['values']
    if selectedTime == '':
        print('no times selected and stuff')
    else:
        print("need to load this data into TBs so that it can be updated")
        
        sql = """SELECT id, name, date FROM events
WHERE id = ?
"""
        q.execute(sql, [selectedTime[0]])
        print(q.fetchall())
        event = str(selectedTime[0])+':'+selectedTime[1]+':'+selectedTime[4]
        timeA[5] = selectedTime[0]
        timeA[0].set(event)

        time = selectedTime[5].split(':')
        timeA[1].set(int(time[0]))
        timeA[2].set(int(time[1]))
        timeA[3].set(int(time[2]))

        timeA[4].set(selectedTime[6])
        


    editingTimeFrm.grid(row = 4,column = 1, columnspan = 2)

def deleteTime(ID,timeA):
    eventID = eventID = int(timeA[0].get().split(':')[0])
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    q.execute("DELETE FROM times WHERE event_id = ? AND runner_id = ?",[eventID, ID])
    db.commit()
    q.close()
    db.close()
    
    
def saveEditTime(ID,timeA):
    eventID = int(timeA[0].get().split(':')[0])
    seconds = 0
    seconds += timeA[3].get()
    seconds += timeA[2].get() * 60
    seconds += timeA[1].get() * 60**2
    

    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = """UPDATE times
SET event_id = ?, time = ?, checked = ?
WHERE event_id = ?
AND runner_id = ?
"""
    q.execute(sql, [eventID, seconds,timeA[4].get(), eventID, runnerID])
    db.commit()
    q.close()
    db.close()

    
    
    

runnerID = 0
checked = False

UN = "bob"
PW = "blob"
failedLogins = 0
RUNNERUN = "blob"
RUNNERPW = "bob"


locsRaw = getLocs()
locsA = []
for i in range(len(locsRaw)):
    loc = ''
    #print(locsRaw[i])
    for j in range(len(locsRaw[i])):
        loc += str(locsRaw[i][j])+ ', '
    locsA.append(loc)


    



myGUI = Tk()
#myGUI.geometry("400x300+450+150")
myGUI.title("Cross Country Program")
#myGUI.configure(background = 'black')


#should only add this once they've signed in!!!
myMenuBar = Menu(myGUI)
fileMenu = Menu(myMenuBar)#umm rename???
fileMenu.add_command(label = "Input times", command = lambda: timeEntryFrm.pack())
fileMenu.add_command(label = "View Times", command = lambda: disTs(runnerID,viewTimesTree,viewTsyscroll))
fileMenu.add_command(label = "ViewGraph", command = lambda: graphFrm.pack())
myMenuBar.add_cascade(label = "Runner Options", menu = fileMenu)

myGUI.config(menu = myMenuBar)

"""signing in
what they'll see at the start"""
signInFrm = Frame(myGUI)
signInFrm.pack()

userNLbl = Label(signInFrm, text = "Username: ")
userNLbl.grid(row = 1, column = 1)
passWLbl = Label(signInFrm, text = "Password: ")
passWLbl.grid(row = 2, column = 1)

userNIn = StringVar()
userNTB = Entry(signInFrm, textvariable = userNIn)
userNTB.grid(row = 1, column =2)
passWIn = StringVar()
passWIn = Entry(signInFrm, textvariable = passWIn, show="*")
passWIn.grid(row = 2, column =2)

loginNote = StringVar()
loginNote.set("Enter your surname and ID as username \nand your 5 character password")
loginNoteLbl = Label(signInFrm, textvariable = loginNote)
loginNoteLbl.grid(row = 3, column = 2)

signInB = Button(signInFrm,text = "Sign In", command = lambda:testUNPW3(userNIn.get(), passWIn.get(),loginNote))
signInB.grid(row = 3, column =1)


"""students name and form
will be shown once students have logged in

need to get rid of them entering their names"""
#name and form
nameEntryFrm = Frame(myGUI)

checkLbl = Label(nameEntryFrm, text = "is this you")
checkLbl.grid(row = 4, column =1)
checkOut = StringVar()
checkOutTB = Entry(nameEntryFrm, textvariable = checkOut, state = "readonly")
checkOutTB.grid(row = 4, column =2, columnspan = 2)


"""entering their times
the runners enter their own times before teacher can check it
should have another bit in the table to see if it's been checked
if it's been checked, they can't change it
"""
timeEntryFrm = Frame(myGUI)

eventsLbl = Label (timeEntryFrm, text = "Event")
eventsLbl.grid(row = 1, column = 1)

eventsIn = StringVar()
eventsIn.set("No Event Selected")
eventsRaw = getEvents()
eventsA = []
for i in range(len(eventsRaw)):
    #print(eventsRaw[i])
    eventsA.append(str(eventsRaw[i][0])+':'+str(eventsRaw[i][2])+':'+eventsRaw[i][3])
eventsCB = Combobox(timeEntryFrm, values = eventsA, textvariable = eventsIn)
eventsCB.grid(row = 1, column =2, columnspan = 3)
##testThingLbl = Label(timeEntryFrm, textvariable = eventsCB.current())
##testThingLbl.grid(row = 4, column =2)

#time label and entry box
timeLbl = Label(timeEntryFrm, text = "Time")
timeLbl.grid(row = 2, column = 1)

timeHIn = IntVar()#hours
timeHTB = Entry(timeEntryFrm, textvariable = timeHIn, width = 2)
timeHTB.grid(row = 2, column = 2)
timeMIn = IntVar()#minutes
timeMTB = Entry(timeEntryFrm, textvariable = timeMIn, width = 2)
timeMTB.grid(row = 2, column = 3)
timeSIn = IntVar()#seconds
timeSTB = Entry(timeEntryFrm, textvariable = timeSIn, width = 2)
timeSTB.grid(row = 2, column = 4)

savingNote = StringVar()
savingNoteLbl = Label(timeEntryFrm, textvariable = savingNote)
savingNoteLbl.grid(row = 4,column = 1,columnspan=4)

saveB = Button(timeEntryFrm, text = "save", command = lambda: save(savingNote))
saveB.grid(row = 3, column = 1)

exitTimesB = Button(timeEntryFrm, text = "done", command = lambda: timeEntryFrm.pack_forget())
exitTimesB.grid(row =3, column = 3)

"""viewing the times
yeah it's all in the function:disTs

well i've changed a bit now so that it uses treeview
"""
viewTimesFrm = Frame(myGUI)

viewTsCols = ("E_ID", "Event Name", "Location", "Distance", "Date", "Time", "Checked")
viewTimesTree = Treeview(viewTimesFrm,columns = viewTsCols,selectmode = 'browse', height = 5)
viewTsyscroll = Scrollbar(viewTimesFrm, orient='vertical', command=viewTimesTree.yview)
createTree(viewTimesTree, viewTsCols, viewTsyscroll, (50,150,150,75,100,100,50))

exitVTB = Button(viewTimesFrm, text = "Done", command = lambda: viewTimesFrm.pack_forget())





"""ok the graph
this may be a bit tricky
i desgined this in a really bad way"""
graphFrm = Frame(myGUI)

graphLocIn = StringVar()
graphLocIn.set("0,choose a location")
findGraphLoc = Combobox(graphFrm, textvariable = graphLocIn, values = locsA)
findGraphLoc.pack()

selectLocB = Button(graphFrm, text = "Select Location", command = lambda:genGraph())
selectLocB.pack()

graphFrames = []
exitGraphsBs = []



def genGraph():    
    graphFrames.append(Frame(graphFrm))
    graphFrames[-1].pack(side = LEFT)


    localishButton = Button(graphFrames[-1], text = "Close Graph", command = lambda: destroyGraph(graphFrames.index(graphFrames[-1])))
    
    exitGraphsBs.append(localishButton)
    exitGraphsBs[-1].pack()
    
    runnerData = loadData(runnerID, graphLocIn.get().split(',')[0])
    if len(runnerData) == 0:
        return
    dates = []
    for i in range(len(runnerData)):
        dates.append(runnerData[i][13])
    
    times = []
    for i in range(len(runnerData)):
        times.append(runnerData[i][2])
    

    yMax = floor((max(times)/10**(len(str(max(times)))-1)+1))*10**(len(str(max(times)))-1)
    
    windowW =  300
    windowH = 400
    margin = 20
    sqrx = int((windowW - margin)/10)
    sqry = int((windowH - margin)/10)
    Tsize = 11

    graphC = Canvas(master = graphFrames[-1], width = windowW, height = windowH, bg = "grey")#C for canvas
    graphC.pack()

    #axis
    graphC.create_line(0, windowH - margin, windowW, windowH - margin, fill = "red", width = 5)
    graphC.create_line(margin, 0,margin, windowH, fill = "red", width = 5)
    #grid and axis labels for Y
    for i in range(windowH - margin, 0, -sqry):
        graphC.create_line(0,i, windowW, i)
        #yLbl = Label(myGUI, text = str(i))
        yLbl = Label(graphFrames[-1], text = str(mapRange(windowH - i, 20, windowH, 0,yMax)))
        yLbl.place(x = 0, y = i)
    #x-axis
    for i in range(margin, windowW, sqrx):
        graphC.create_line(i, 0, i, windowH)
        xLbl = Label(graphFrames[-1], text = str((i-margin)/sqrx))
        if (i-margin)/sqrx < len(dates):
            xLbl = Label(graphFrames[-1],  text = dates[int((i-margin)/sqrx)])
            
        xLbl.place(x = i,y = windowH-margin)
        
    #the line
    for i in range(0, len(times)-1, 1):
        yp = times[i]*(windowH - margin)/yMax
        yp2 = times[i+1]*(windowH - margin)/yMax
        
        graphC.create_line(i*sqrx + margin, windowH - yp, (i+1)*sqrx + margin, windowH - yp2, fill = "blue")
    
    

def destroyGraph(num):
    global exitGraphBs
    graphFrames[num].pack_forget()
    graphFrames.remove(graphFrames[num])
    exitGraphsBs.remove(exitGraphsBs[num])

        
exitGraphB = Button(graphFrm, text = "Done", command = lambda: graphFrm.pack_forget())
exitGraphB.pack()


"""the admin frame?
once the admin/teacher whatever you wanna call it logs in
need to think of a secure place to save this password
this frame will just contain the buttons??
or shall i stick it in the menubar at the top???
"""
adminFrm = Frame(myGUI)

welcomeLbl = Label(adminFrm, text = "WELCOME")
welcomeLbl.grid(row = 0, column = 1, columnspan =2)

newRunnerB = Button(adminFrm, text = "Add a New Runner", command = lambda: adminOpts("NEWRUNNER"))
newRunnerB.grid(row = 1, column = 1)
newEventB = Button(adminFrm, text = "Add a New Event", command = lambda: adminOpts("NEWEVENT"))
newEventB.grid(row = 1, column = 2)

viewRunnerB = Button(adminFrm, text = "View Runner", command = lambda: adminOpts("VIEWRUNNER"))
viewRunnerB.grid(row =2, column = 1)



"""
adding a new runner
"""
newRunnerFrm = Frame(myGUI)
newRunnerLbl = Label(newRunnerFrm, text = "Add a new runner")
newRunnerLbl.grid(row = 0, column =1, columnspan = 4)
newFormLbl = Label(newRunnerFrm, text = "Form:")
newFormLbl.grid(row = 1, column =1)
newFormIn = StringVar()
newFormTB = Entry(newRunnerFrm, textvariable = newFormIn, width = 5)
newFormTB.grid(row = 1, column =2)

newIDLbl = Label(newRunnerFrm,text = "ID:")
newIDLbl.grid(row =1, column= 3)
newIDIn = StringVar()
newIDTB = Entry(newRunnerFrm, textvariable = newIDIn, width = 4)
newIDTB.grid(row =1, column = 4)

newFNameLbl = Label(newRunnerFrm, text = "Firstname:")
newFNameLbl.grid(row = 2, column = 1)
newFnameIn = StringVar()
newFnameTB = Entry(newRunnerFrm, textvariable = newFnameIn, width = 10)
newFnameTB.grid(row = 2, column = 2)
newSNameLbl = Label(newRunnerFrm, text = "Surname:")
newSNameLbl.grid(row = 2,column = 3)
newSnameIn = StringVar()
newSnameTB = Entry(newRunnerFrm, textvariable = newSnameIn, width = 10)
newSnameTB.grid(row = 2, column =4)

newRNote = StringVar()
newRNote.set("Username will be Surname and ID\nPassword will be randomly generate 5 letter string")
newRNoteLbl = Label(newRunnerFrm, textvariable = newRNote, anchor  = W)
newRNoteLbl.grid(row = 3, column = 1, columnspan = 4)

#ok now we actually gotta add him
addRunnerB = Button(newRunnerFrm, text = "Add Runner", command = lambda:addNewRunner(newIDIn.get(),newFormIn.get(), newFnameIn.get(),newSnameIn.get(), ))
addRunnerB.grid(row = 4, column =1)


exitNewRunnerB = Button(newRunnerFrm, text = "Done Adding", command = lambda: newRunnerFrm.pack_forget())
exitNewRunnerB.grid(row = 4, column  = 2)

"""
adding an event to the DB
need the event's name/location/date
i've had to put a frame on the frame in order to have the date input all look pretty
the way i've got locID from the CB may create problems - so check that

need a way to input a new location

"""
#adding a new event
newEventFrm = Frame(myGUI)
newEventLbl = Label(newEventFrm, text = "Add a new Event")
newEventLbl.grid(row = 0, column = 1)

newEventNLbl = Label(newEventFrm, text = "Name:")
newEventNLbl.grid(row = 1, column=1)
newEventNIn = StringVar()
newEventNTB = Entry(newEventFrm, textvariable = newEventNIn)
newEventNTB.grid(row = 1, column =2)

newEventIDIn = StringVar()
newEventIDLbl = Label(newEventFrm, text = "ID:")
newEventIDLbl.grid(row = 1, column = 3)
newEventIDTB = Entry(newEventFrm, textvariable = newEventIDIn)
newEventIDTB.grid(row= 1, column = 4)


newEventDateLbl = Label(newEventFrm, text = "Date:")
newEventDateLbl.grid(row= 2, column =1)
newEventDateIn = StringVar()

#adding a new date
newEDateFrm = Frame(newEventFrm)
newEDateFrm.grid(row = 2, column =2)
newEDateDIn = IntVar()
newEDateDTB = Entry(newEDateFrm, textvariable = newEDateDIn, width = 2)
newEDateDTB.grid(row =1 ,column = 1)
Label(newEDateFrm, text = "/").grid(row =1, column = 2)
newEDateMIn = IntVar()
newEDateMInTB = Entry(newEDateFrm, textvariable = newEDateMIn, width = 2)
newEDateMInTB.grid(row = 1, column = 3)
Label(newEDateFrm, text = "/").grid(row =1, column = 4)
newEDateYIn = IntVar()
newEDateYTB = Entry(newEDateFrm, textvariable = newEDateYIn, width = 4)
newEDateYTB.grid(row = 1, column =5)


newEventLocLbl = Label(newEventFrm, text = "Location:")
newEventLocLbl.grid(row =3, column =1)
newEventLocIn = StringVar()
newEventLocIn.set('0')

#the little note that i seem to be using now
newEventNote = StringVar()
newEventNoteLbl = Label(newEventFrm, textvariable = newEventNote)
newEventNoteLbl.grid(row =4, column = 3, columnspan = 2)

#the locA was originally here but i had to move it earlier up

#print(locsA)
#testA = [x for x in range(10)]
newEventLocCB = Combobox(newEventFrm,textvariable = newEventLocIn, values = locsA,width = 30)
newEventLocCB.grid(row = 3, column = 2)

createNewLocB = Button(newEventFrm, text = "need a new Location", command = lambda:newLocFrm.pack())
createNewLocB.grid(row =3, column = 3)

addNewEventB = Button(newEventFrm, text = "Add the Event", command = lambda:saveEvent(newEventIDIn.get(),int(newEventLocIn.get().split(',')[0]), newEventNIn.get(), newEDateDIn,newEDateMIn,newEDateYIn, newEventNote))
addNewEventB.grid(row =4 , column = 2)

newEventNextIDB = Button(newEventFrm, text = "find next ID", command = lambda: newEventIDIn.set(findNextEID()))
newEventNextIDB.grid(row = 2, column = 4)#so it's under the ID TB
#need to get eventID
#need to get figure out locID based on combobox
#and date
#####newEventLocInID = newEventLocIn.get().split(',')[0]
exitNewEventB = Button(newEventFrm, text = "Done Adding", command = lambda:newEventFrm.pack_forget())
exitNewEventB.grid(row =5, column = 1)


"""
we're adding a new location here
this is sort part of the above section
it'll be in it's own frame but'll be used when a button's pressed on newEventFrm
"""

newLocFrm = Frame(myGUI)
#interesting i'm not doing this somewhere else first
newLocNameLbl = Label(newLocFrm, text = "name:")
newLocNameLbl.grid(row = 1, column =1)
newLocNameIn = StringVar()
newLocNameTB = Entry(newLocFrm, textvariable = newLocNameIn)
newLocNameTB.grid(row =1, column = 2)

newLocIDLbl = Label(newLocFrm, text = "ID:")
newLocIDLbl.grid(row = 1, column =3)
newLocIDIn = StringVar()
newLocIDIn.set('0')
newLocIDTB = Entry(newLocFrm, textvariable = newLocIDIn)
newLocIDTB.grid(row = 1,column = 4)

newLocAddrLbl = Label(newLocFrm, text = "Address:")
newLocAddrLbl.grid(row =2, column = 1)
newLocAddrIn = StringVar()
newLocAddrTB = Entry(newLocFrm, textvariable = newLocAddrIn)
newLocAddrTB.grid(row =2, column = 2)

newLocDistLbl = Label(newLocFrm, text = "Distance(km):")
newLocDistLbl.grid(row =2,column = 3)
newLocDistIn = StringVar()
newLocDistIn.set('0.0')
newLocDistTB = Entry(newLocFrm, textvariable = newLocDistIn)
newLocDistTB.grid(row = 2,column = 4)

newLocNote = StringVar()
newLocNoteLbl = Label(newLocFrm, textvariable = newLocNote)
newLocNoteLbl.grid(row = 3, column =2, columnspan = 3)

addNewLocB = Button(newLocFrm, text = "Add Location", command = lambda:addNewLoc(newLocIDIn.get(),newLocNameIn.get(),newLocAddrIn.get(),newLocDistIn.get(),locsA,newLocNote))
addNewLocB.grid(row =3, column = 1)

exitNewLocB = Button(newLocFrm, text = "Done", command = lambda: newLocFrm.pack_forget())
exitNewLocB.grid(row = 4,column = 1)





#ok adding a time



#these two will nick code from tInput
#adding a time
#adding checking time's for a user
"""
ok this is what the admining person can do with the runners
they need to be able to view their data, times and data stored in DB
change anything if needed
and the usual stuffs that a runner can do for themselves

use treeviews- nick a bit of code from urvis
"""
viewRunnerFrm = Frame(myGUI)


findRunnerFrm = Frame(viewRunnerFrm)
viewRunnerTreeFrm = Frame(viewRunnerFrm)

findRunnerFrm.pack()
viewRunnerTreeFrm.pack()

adminRunnerDBOptsTL = Toplevel()
adminRunnerDBOptsTL.withdraw()
#adminRunnerDBOptsFrm = Frame(viewRunnerFrm)
#adminRunnerDBOptsFrm.pack()

#ok so they type in name/form/id summat
#i get a list of the runners
#they chose from the list

viewRFNameIn = StringVar()
viewRSNameIn = StringVar()
viewRNameLbl = Label(findRunnerFrm, text = 'Name:')
viewRNameLbl.grid(row = 1, column = 1)
viewRFNameTB = Entry(findRunnerFrm , textvariable = viewRFNameIn)
viewRFNameTB.grid(row =1, column = 2)
viewRSNameTB = Entry(findRunnerFrm, textvariable = viewRSNameIn)
viewRSNameTB.grid(row = 1, column = 3)

viewRIDIn = StringVar()
viewRIDIn.set('0')
viewRIDLbl = Label(findRunnerFrm, text = "ID:")
viewRIDLbl.grid(row = 2, column = 1)
viewRIDTB = Entry(findRunnerFrm, textvariable = viewRIDIn, width = 4)
viewRIDTB.grid(row = 2, column = 2)


viewRSearchB = Button(findRunnerFrm, text = "Find Runners", command = lambda:searchRunners(runnersTreeview, viewRFNameIn.get(), viewRSNameIn.get(), viewRIDIn.get()))
viewRSearchB.grid(row = 3, column =1)

#viewRFindTsB = Button(findRunnerFrm, text = "Find Times", command = lambda: insertIntoTree(timesTreeview,findRunnerTimes(runnersTreeview)))
#viewRFindTsB.grid(row = 3, column = 2)

viewRSelRunnB = Button(findRunnerFrm, text = "Select Runner", command = lambda: selectRunner(runnersTreeview))
viewRSelRunnB.grid(row =3, column =2)


viewRunnersCols = ('ID', 'First Name', 'Surname', 'Form',"username","password")
runnersTreeview = Treeview(viewRunnerTreeFrm, columns = viewRunnersCols, selectmode = "browse", height = 3)
yscrollbar = Scrollbar(viewRunnerTreeFrm, orient='vertical', command=runnersTreeview.yview)
createTree(runnersTreeview, viewRunnersCols,yscrollbar,(90,150,150,150,150,90))


#i think i need a better name
yscrollbar.grid(row=1, column=1, sticky=E+NS)


runnersTreeview.grid(row = 1, column= 1, sticky = NSEW)



#now then once they've selected the runner what funky things do they wanna do
#delete runner
#edit PW
#edit times - will be an annoyance
#delete time
#those 2 should be done once they're on the viewTimes menu
#how the hell do i program that
#no i should do the first couple and maybe speak to Mrs Harvey???



selectedUserLbl = Label(adminRunnerDBOptsTL, text = "Selected User:")
selectedUserOut = StringVar()
selectedUserTB = Entry(adminRunnerDBOptsTL, textvariable = selectedUserOut, state = DISABLED)

selectedUserLbl.grid(row = 1, column = 1)
selectedUserTB.grid(row = 1, column = 2)


editingRunnerFrm = Frame(adminRunnerDBOptsTL)

editFormLbl = Label(editingRunnerFrm, text = "Form:")
editFormLbl.grid(row = 1, column = 1)
editFormIn = StringVar()
editFormTB = Entry(editingRunnerFrm, textvariable = editFormIn)
editFormTB.grid(row = 1, column =2)

editUNLbl = Label(editingRunnerFrm, text = "Username")
editUNLbl.grid(row = 2, column = 1)
editUNIn = StringVar()
editUNTB = Entry(editingRunnerFrm, textvariable = editUNIn)
editUNTB.grid(row= 2, column =2)

editPWLbl = Label(editingRunnerFrm, text = "Password")
editPWLbl.grid(row = 3, column =1)
editPWIn = StringVar()
editPWTB = Entry(editingRunnerFrm, textvariable = editPWIn)
editPWTB.grid(row = 3, column = 2)

editingDetailsA = [editFormIn,editUNIn,editPWIn]

delRunnerB = Button(editingRunnerFrm, text = "DeleteRunner", command = lambda:deleteRunner(runnerID,adminRunnerDBOptsTL))
delRunnerB.grid(row = 4, column =1)
saveEditRunnerB = Button(editingRunnerFrm, text = "Save changes", command = lambda:saveRunnerEdits(runnerID, editingDetailsA))
saveEditRunnerB.grid(row = 4, column = 2)


#editingtimes
editingTimeFrm = Frame(adminRunnerDBOptsTL)

editTimeEventLbl = Label(editingTimeFrm, text = "event")
editTimeEventLbl.grid(row = 1, column =1)
editTimeEventIn = StringVar()
editTimeEventCB = Combobox(editingTimeFrm,values = eventsA, textvariable = editTimeEventIn)
editTimeEventCB.grid(row =1,column =2, columnspan = 3)

editTimeLbl = Label(editingTimeFrm, text = "Time:")
editTimeLbl.grid(row = 2,column =1)

editTimeHIn = IntVar()
editTimeHTB = Entry(editingTimeFrm, textvariable = editTimeHIn, width = 2)
editTimeHTB.grid(row = 2,column = 2)
editTimeMIn = IntVar()
editTimeMTB = Entry(editingTimeFrm, textvariable = editTimeMIn, width = 2)
editTimeMTB.grid(row = 2, column = 3)
editTimeSIn = IntVar()
editTimeSTB = Entry(editingTimeFrm, textvariable = editTimeSIn, width = 2)
editTimeSTB.grid(row =2, column = 4)

editCheckLbl = Label(editingTimeFrm, text = "checked")
editCheckLbl.grid(row = 3, column = 1)
editCheckVar = IntVar()
editCheckB = Checkbutton(editingTimeFrm, variable = editCheckVar)
editCheckB.grid(row = 3, column = 2)

editingTimeA = [editTimeEventIn, editTimeHIn, editTimeMIn, editTimeSIn, editCheckVar,0]



deleteTimeB = Button(editingTimeFrm, text = 'Delete Time', command = lambda: deleteTime(runnerID, editingTimeA))
deleteTimeB.grid(row  = 4, column =2, columnspan =3)#sticky = E????

saveEditTimeB = Button(editingTimeFrm, text= "Save Edits", command = lambda: saveEditTime(runnerID,editingTimeA))
saveEditTimeB.grid(row = 4, column = 1)



editRunnerB = Button(adminRunnerDBOptsTL, text = "Edit Runner", command = lambda: editRunnerDetails(runnerID, editingDetailsA))
editRunnerB.grid(row = 2, column = 1)
#within the edit menus thee will be a delete button/option
editRunnerTimesB = Button(adminRunnerDBOptsTL, text = "Edit Time", command = lambda:editRunnerTimes(runnerID, viewTimesTree, viewTimesFrm,editingTimeA))
editRunnerTimesB.grid(row =2, column = 2)


#ok i think i may need yet another frame
#starting to think i may have over done it a little with the frames
#or maybe not...




#this is supposed to stop it getting destroyed
adminRunnerDBOptsTL.protocol('WM_DELETE_WINDOW', lambda:adminRunnerDBOptsTL.withdraw())
#so you can click x on the window
#and then open it up again





myGUI.mainloop()

print("and we're done")

