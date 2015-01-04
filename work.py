from tkinter import *
from tkinter.ttk import *
import sqlite3, time
from math import floor

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


    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = "INSERT INTO times(runner_id, event_id, time) VALUES(?,?,?)"
    q.execute(sql, [runnerID, '4', seconds])#SHOULD HAVE TO CHECK IF THERES ALREADY AN ENTRY
    print(runnerID)
    q.close()
    db.commit()
    db.close()

def checkN(out):
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
        out.set(runners[0])
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
                out.set(runners[i])
                runnerID = IDout

                #showGraph()

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


def disTs(ID, tree, yscroll):#display times
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = """ SELECT events.id, events.name, locations.name, events.length, events.date, times.time, times.checked
FROM events, locations, times, runners
WHERE events.id = times.event_id
AND events.location_id = locations.id
AND times.runner_id = runners.id
AND runners.id = ?
ORDER BY events.date

"""
    
    q.execute(sql, [ID])

    data = q.fetchall()

    q.close()
    db.close()
    
    insertIntoTree(tree, data)
    tree.grid(row =1,column =1, sticky = NSEW)
    yscroll.grid(row =1, column = 1, sticky = E+NS)

    exitVTB.grid(row = len(data) +2, column = 1, columnspan = 3)
    viewTimesFrm.pack()




def mapRange(val, start0, stop0, start1, stop1):
    range0 = stop0-start0
    range1 = stop1-start1
    Pcent = (val -start0)/range0
    finalV = range1 * Pcent + start1
    return finalV


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

def testUNPW(unIn,pwIn):
    global runnerID#need to figure out what's going to happen here
    #ok so we need to check UN and PW
    global failedLogins
    if failedLogins >=5:
        print("tried more than 5 times. LOCKED OUT")
    elif unIn != UN and unIn != RUNNERUN:
        print("wrong UN")
        failedLogins += 1
    elif unIn == UN and pwIn != PW:
        print("wrong PW")
        failedLogins +=1
    elif unIn == RUNNERUN and pwIn != RUNNERPW:
        print("wrong PW")
        failedLogins +=1


    
##    elif pwIn != PW and pwIn != RUNNERPW:
##        print("wrong PW")
##        failedLogins +=1
    elif unIn == UN and pwIn == PW:
        print("we're in")
        signInFrm.pack_forget()
        adminFrm.pack()
    elif unIn == RUNNERUN and RUNNERPW:
        print("go to the tInputs stuffs")
        signInFrm.pack_forget()
        nameEntryFrm.pack()
        checkOut.set("1 Mickey Mouse 5ABC")#needs changing
        runnerID = 1#again this needs changing
        showGraph()
        """that should really be retrieved from the database
SELECT stuffs FROM runners WHERE UN = (?) AND PW = (?)
obviously won't be UN/PW in DB
?s will be unIn, pwIn
"""
        
        
    else:
        print("shouldn't be here")


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
        
        

def newRunner():
    print("yep this is how you create a new runner")
def newEvent():
    print("clearly creating a new event")
def newTime():
    print("use code from tInputs")
def checkTimes():
    print("""the runners are able to enter their own times
this is so Dr.H can check it""")
def adminViewRunner():
    print("this is getting rid of the prev 2")
    print("maybe i can still use the things in the menu")


def addNewRunner(ID, form, fname, lname):
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    
    sql = "INSERT INTO runners(id, fName, lName, form) VALUES(?,?,?,?)"
    q.execute(sql, [ID, fname, lname, form])
    
    db.commit()
    q.close()
    db.close()
    print("stuffs")

def getLocs():#when adding events need the location
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = "SELECT * FROM locations"
    q.execute(sql)
    returned = q.fetchall()
    q.close()
    #db.commit()
    db.close()
    return returned

def saveEvent(eventID,locID, eventN, dateD,dateM,dateY):
    date = str(dateY.get()) + '-' + str(dateM.get()) + '-' + str(dateD.get())
    print(date)
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()

    
    
    sql = "INSERT INTO events(id, location_id, name, date) VALUES(?,?,?,?)"
    q.execute(sql, [eventID,locID, eventN, date])
    db.commit()
    q.close()
    db.close()

def findNextEID():
    db = sqlite3.connect("runningDB/running.db")
    q = db.cursor()
    sql = "SELECT * FROM events ORDER BY id"
    q.execute(sql)
    allEs = q.fetchall()
    q.close()
    db.close()

    count = 0
    running = True
    while running:
        if count == len(allEs)-1:
            running = False
            count+=1
        elif allEs[count][0] + 1 != allEs[count+1][0]:
            running = False
            count += 1
        count+=1
    return count

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

def testUNPW3(unIn, pwIn, note):
    global DB, runnerID, failedLogins
    if failedLogins >= 5:
        note.set("LOCKED OUT MWAHAHAHA")
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
        note.set("Username or Password are incorrect")
    else:
        note.set("logging in")
        runner =  runner[0]
        checkOut.set(runner)
        runnerID = runner[0]
        signInFrm.pack_forget()
        nameEntryFrm.pack()
        showGraph()
    q.close()
    db.close()

runnerID = 0
checked = False

UN = "bob"
PW = "blob"
failedLogins = 0
RUNNERUN = "blob"
RUNNERPW = "bob"




myGUI = Tk()
#myGUI.geometry("400x300+450+150")
myGUI.title("Runenrs thing")


#should only add this once they've signed in!!!
myMenuBar = Menu(myGUI)
fileMenu = Menu(myMenuBar)
fileMenu.add_command(label = "Input times", command = lambda: timeEntryFrm.pack())
fileMenu.add_command(label = "View Times", command = lambda: disTs(runnerID,viewTimesTree,viewTsyscroll))
fileMenu.add_command(label = "ViewGraph", command = lambda: graphFrm.pack(side = RIGHT))
myMenuBar.add_cascade(label = "File", menu = fileMenu)

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
#userNIn.set("are you bob")
userNTB = Entry(signInFrm, textvariable = userNIn)
userNTB.grid(row = 1, column =2)
passWIn = StringVar()
passWIn = Entry(signInFrm, textvariable = passWIn)
passWIn.grid(row = 2, column =2)

loginNote = StringVar()
loginNote.set("enter your surnam and ID as username and your 5 character password")
loginNoteLbl = Label(signInFrm, textvariable = loginNote)
loginNoteLbl.grid(row = 3, column = 2)

signInB = Button(signInFrm,text = "Sign In", command = lambda:testUNPW3(userNIn.get(), passWIn.get(),loginNote))
signInB.grid(row = 3, column =1)


"""students name and form
will be shown once students have logged in

need to get rid of them entering their names"""
#name and form
nameEntryFrm = Frame(myGUI)


####formLbl = Label(nameEntryFrm, text = "Form:")
####formLbl.grid(row = 1, column =1)
####formIn = StringVar()
####formTB = Entry(nameEntryFrm, textvariable = formIn, width = 5)
####formTB.grid(row = 1, column =2)
####
####nameLbl = Label(nameEntryFrm, text = "Name:")
####nameLbl.grid(row = 2, column = 1)
####fnameIn = StringVar()
####fnameTB = Entry(nameEntryFrm, textvariable = fnameIn, width = 10)
####fnameTB.grid(row = 2, column = 2)
####snameIn = StringVar()
####snameTB = Entry(nameEntryFrm, textvariable = snameIn, width = 10)
####snameTB.grid(row = 2, column =3)
####
#####check the name
####checkB = Button(nameEntryFrm, text = "Find Me!", command = lambda: checkN(checkOut))
####checkB.grid(row = 3, column =1)
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
    #print(eventsRaw[i])
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
timeHTB.grid(row = 2, column = 2)
timeMIn = IntVar()#minutes
timeMTB = Entry(timeEntryFrm, textvariable = timeMIn, width = 2)
timeMTB.grid(row = 2, column = 3)
timeSIn = IntVar()#seconds
timeSTB = Entry(timeEntryFrm, textvariable = timeSIn, width = 2)
timeSTB.grid(row = 2, column = 4)


saveB = Button(timeEntryFrm, text = "save", command = save)
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
i remmeber i had a problem that it may be too big to view on the screen
need to solve taht"""
graphFrm = Frame(myGUI)
def showGraph():
    print(runnerID)
    runnerData = loadData(runnerID)
    if len(runnerData) == 0:
        return
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

exitGraphB = Button(graphFrm, text = "Done", command = lambda: graphFrm.pack_forget())



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
#need new location or should i put that in new event
#i could have a dropdown/text box
#you type in if it's new and you use dropdown
#or top level thingy???



newRunnerFrm = Frame(myGUI)
newRunnerLbl = Label(newRunnerFrm, text = "Add a new runner")
newRunnerLbl.grid(row = 0, column =1, columnspan = 3)
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

newNameLbl = Label(newRunnerFrm, text = "Name:")
newNameLbl.grid(row = 2, column = 1)
newFnameIn = StringVar()
newFnameTB = Entry(newRunnerFrm, textvariable = newFnameIn, width = 10)
newFnameTB.grid(row = 2, column = 2)
newSnameIn = StringVar()
newSnameTB = Entry(newRunnerFrm, textvariable = newSnameIn, width = 10)
newSnameTB.grid(row = 2, column =3)

#ok now we actually gotta add him
#i'm gonna do this in the other thign sto start with so i don't mess up anything here
addRunnerB = Button(newRunnerFrm, text = "add runner", command = lambda:addNewRunner(newIDIn.get(),newFormIn.get(), newFnameIn.get(),newSnameIn.get(), ))
addRunnerB.grid(row = 3, column =2)


exitNewRunnerB = Button(newRunnerFrm, text = "done adding", command = lambda: newRunnerFrm.pack_forget())
exitNewRunnerB.grid(row = 6, column  = 1)

"""
adding an event to the DB
need the event's name/location/date
i've had to put a frame on the frame in order to have the date input all look pretty
the way i've got locID from the CB may create problems - so check that

need a way to input a new event

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

newEventIDIn = IntVar()
newEventIDLbl = Label(newEventFrm, text = "ID:")
newEventIDLbl.grid(row = 1, column = 3)
newEventIDTB = Entry(newEventFrm, textvariable = newEventIDIn)
newEventIDTB.grid(row= 1, column = 4)


newEventDateLbl = Label(newEventFrm, text = "Date:")
newEventDateLbl.grid(row= 2, column =1)
newEventDateIn = StringVar()
#####################adding a new date do it!!!

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
locsRaw = getLocs()
locsA = []
for i in range(len(locsRaw)):
    loc = ''
    #print(locsRaw[i])
    for j in range(len(locsRaw[i])):
        loc += str(locsRaw[i][j])+ ', '
    locsA.append(loc)
#print(locsA)
testA = [x for x in range(10)]
newEventLocCB = Combobox(newEventFrm,textvariable = newEventLocIn, values = locsA,width = 30)
newEventLocCB.grid(row = 3, column = 2)

#date = (newEDateDIn.get(), newEDateMIn.get(), newEDateYIn.get())

addNewEventB = Button(newEventFrm, text = "Add The Event", command = lambda:saveEvent(newEventIDIn.get(),int(newEventLocIn.get().split(',')[0]), newEventNIn.get(), newEDateDIn,newEDateMIn,newEDateYIn))
addNewEventB.grid(row =4 , column = 2)

newEventNextIDB = Button(newEventFrm, text = "find next ID", command = lambda: newEventIDIn.set(findNextEID()))
newEventNextIDB.grid(row = 4, column = 3)
#need to get eventID
#need to get figure out locID based on combobox
#and date
#####newEventLocInID = newEventLocIn.get().split(',')[0]
exitNewEventB = Button(newEventFrm, text = "bye bye", command = lambda:newEventFrm.pack_forget())
exitNewEventB.grid(row =5, column = 1)



#ok adding a time



#these two will nick code from tInput
#adding a time
#adding checking time's for a user
"""
ok this is what the admining person can do with the runners
they need to be able to view their data, times and data stored in DB
change anything if needed
and the usual stuffs that a runner can do for themselves

use treeviews- nick a bit of code from urvis???
"""

viewRunnerFrm = Frame(myGUI)

#ok so they type in name/form/id summat
#i get a list of the runners
#they chose from the list

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
yscrollbar = Scrollbar(viewRunnerFrm, orient='vertical', command=runnersTreeview.yview)
createTree(runnersTreeview, viewRunnersCols,yscrollbar,(90,150,150,150))


#i think i need a better name
yscrollbar.grid(row=3, column=1,columnspan = 3, sticky=E+NS)


#insted of doing columnspan in the final prgogram just stick it on another frame
runnersTreeview.grid(row = 3, column= 1,columnspan = 3, sticky = NSEW)



viewRunnersTsCols = ('Event ID', 'Event Name', 'Location', 'Time')
timesTreeview = Treeview(viewRunnerFrm, columns = viewRunnersTsCols, selectmode = "extended", height = 5)
yscroll2 = Scrollbar(viewRunnerFrm, orient = "vertical", command = timesTreeview.yview)
#that's why i need a better name
createTree(timesTreeview, viewRunnersTsCols,yscroll2,(90,150,150,100))

timesTreeview.grid(row =4, column = 1, columnspan = 3, sticky = NSEW)
yscroll2.grid(row = 4 , column = 1, columnspan = 3, sticky=E+NS)

#still need to be able to edit/add times





myGUI.mainloop()

print("and we're done")

