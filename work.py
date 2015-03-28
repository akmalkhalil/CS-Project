from tkinter import *
from tkinter.ttk import *
import sqlite3
from math import floor
from random import randint

def save(note):
    seconds = 0
    try:
        #covert hours, minutes and seconds into seconds
        seconds += timeHIn.get() * 60*60
        seconds += timeMIn.get() * 60
        seconds += timeSIn.get()
        if timeHIn.get()>4:
            note.set("time must be less than 5 hours")
            return
        if timeMIn.get()>=60:#make sure minutes are less than 60 as minutes should be
            note.set("minutes cannot be greater than 60")
            return
        if timeSIn.get()>=60:#make sure seconds are less than 60 as seconds should be
            note.set("seconds cannot be greater than 60")
            return
    except ValueError:#incase non numberical characters have been entered
        note.set("hours,minutes and seconds must each be integers")
        return

    db = sqlite3.connect("runningDB2/running.db")#conenct to database
    q = db.cursor()
    #checking to make sure no time has already been entered for this event and runner
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
    if runnerID == 0:#incase the admin hasn't selected a runner
        note.set("No runner has been selected")
    elif eventsIn.get() == "No Event Selected":#incase the user didn't select an event from the combobox
         note.set("No event has been selected")
    elif not exists:
        sql = "INSERT INTO times(runner_id, event_id, time,checked) VALUES(?,?,?,?)"
        q.execute(sql, [runnerID, eventsIn.get().split(':')[0], seconds,0])
        db.commit()
        note.set("Saved")
    
    q.close()
    db.close()

def getEvents():#the events in the dropdown box for saving event
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
        #convert seconds stored in DB to hr/min/sec
        hours = floor(data[i][-2]/3600)
        minutes = floor((data[i][-2]-hours*3600)/60)
        seconds = data[i][-2]-hours*3600-minutes*60
        if data[i][-1] == 1:#if the time has been checked and approved by teacher
            checker = '✓'
        else:
            checker = '✗'
        #i decided to store all the data after editing back in the same array that I got
        data[i] = [data[i][x] for x in range(len(data[i])-2)]
        data[i].append(str(hours) + ':' + str(minutes) + ':' + str(seconds))
        data[i].append(checker)
    #see the tree sections for a bit more notes on this
    insertIntoTree(tree, data)
    tree.grid(row =1,column =1, sticky = NSEW)#NSEW makes sure that the tree fills the grid cell
    #these two lines are from Urvis' code
    yscroll.grid(row =1, column = 1, sticky = E+NS)#E+NS sticks the scrollbar to the right of the screen and makes it span from top to bottom

    exitVTB.grid(row=2, column = 1)#puts the button on the screen
    viewTimesFrm.pack()#adds the whol display times section to the screen

def mapRange(val, start0, stop0, start1, stop1):#maps a value from one range to a second
    range0 = stop0-start0#calcualte the first range
    range1 = stop1-start1#calculate the second
    Pcent = (val -start0)/range0#how far through the 1st range is the val
    finalV = range1 * Pcent + start1#move throgh the 2nd range the same %age distance
    return finalV

def loadData(ID,locID):#Used to get the times needed to generate a graph
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    sql = """SELECT time FROM times, runners, events, locations
WHERE times.runner_id = runners.id
AND events.location_id = locations.id
AND times.event_id = events.id
AND runners.id = ?
AND locations.id = ?
"""
    q.execute(sql,[ID,locID])
    fetched = q.fetchall()

    q.close()
    db.close()
    return fetched

def adminOpts(opt):#opt can only take 3 values as it's all hard coded into this system
    #when an admin clicks on one of the buttons in the admin menu, it'll open up that section
    #this procedure is used to make sure that the other admin sections close
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
    try:#make sure that the user entered an integer for the ID
        int(ID)
    except ValueError:
        newRNote.set("ID must be an integer")
        return
    if len(ID) != 4:#ID must be 4digits long
        newRNote.set("ID must be four digits long")
        return
    elif int(ID)<0:#ensure ID is positive
        newRNote.set("ID cannot be negative")
        return
    
    un = lname+str(ID)#username is created by concatenating lastname and ID
    pw = genRanLetters(5)#password is a random 5 letter string
    
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    
    sql = "INSERT INTO runners(id, fName, lName, form,username,password) VALUES(?,?,?,?,?,?)"
    try:
        q.execute(sql, [ID, fname, lname, form,un,pw])
        newRNote.set("Username: "+un+", Password= "+pw)
    except sqlite3.IntegrityError:#if a runner with the id = ID already exists
        newRNote.set("Runner with that ID exists")
##    except sqlite3.OperationalError(" database is locked"):
##        print("broken")
    
    db.commit()
    q.close()
    db.close()
    

def genRanLetters(l):
    #generates a string of letter that are l characters long
    #first an using a list compreshension with an if statement to choose between upper and lowercase
    #the list of letters is then joined to an empty string craeting the string of random letters    
    string = ''.join([chr(randint(65,90)) if randint(0,1) == 0 else chr(randint(97,122)) for x in range(l)])
    return string

def getLocs():#when adding events need the location and for the graph
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    sql = "SELECT * FROM locations"
    q.execute(sql)
    returned = q.fetchall()
    q.close()
    db.close()
    return returned

def saveEvent(eventID,locID, eventN, dateD,dateM,dateY, note):#save a new created event
    try:#make sure that only integer values are entered into the date
        date = str(dateY.get()) + '-' + str(dateM.get()) + '-' + str(dateD.get())#puts the date in a format to be saved
    except ValueError:
        note.set("Each part of the date must be an integer")
        return
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    try:#make sure that the event ID added is an integer
        sql = "SELECT id FROM events"
        if (int(eventID),) in q.execute(sql).fetchall():#fetchall returns a tuple of tuples
            #checking to ensure the new ID is unique
            note.set("You must enter a unique ID for the event")
        elif dateD.get()<1 or dateD.get() >31:#make sure date is correcntly formatted
            note.set("dates must be DD/MM/YYYY\nthe day must be in between 1 and 31, inclusive")
        elif dateM.get()<1 or dateM.get()>12:#make sure date is correcntly formatted
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
    #this function gets all the event IDs then finds
    #then first one not in consecutive order
    #then outputs a counter as the new ID
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
    try:#make sure that the ID entered by the user is an integer
        ID = int(ID)
    except ValueError:
        ID = 0

    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    
    if len(fname) == 0 and len(lname) == 0 and ID == 0:#if all the search criteria are blank
        sql = "SELECT * FROM runners"#get all the runners
        q.execute(sql)
    else:#if atleast one search criteria has been entered
        sql ="""SELECT * FROM runners
WHERE fName LIKE ?
OR lName LIKE ?
OR id LIKE ?
"""#find any runner mathcing atleast on of the criteria
        q.execute(sql, [fname, lname,ID])
    runners = q.fetchall()
    q.close()
    db.close()

    insertIntoTree(tree, runners)

def emptyTreeview(tree):
    for i in tree.get_children():#get_children returns the identifiers for each row in the table
        tree.delete(i)#delete that row from the table

def createTree(tree, cols, yscroll, widths):#len(widths) must >= len(cols)
    #This procedure is used to initialise the tree, creating the table with column headings and a scrollbar
    for i in range(len(cols)):
        tree.heading('#'+str(i+1), text = cols[i], anchor = W)#creates each column, with the heading= cols[i].
        #the anchor is because the table goes from left to right
    tree.column('#0', stretch=NO, minwidth=0, width=0)#this is needed
    for i in range(len(cols)):
        tree.column('#'+str(i+1), stretch = NO, minwidth = widths[i], width = widths[i])#sets the minimum width of each column to widths[i]
    tree.configure(yscroll=yscroll.set)#tells the program the yscroll for this tree is set to the yscrollbar we created
    
def insertIntoTree(tree, values):
    if len(tree.get_children()) > 0:
        #otherwise results from the previous search will remain in the table
        emptyTreeview(tree)
    for i in values:#inserts one row at a time
        tree.insert("", END, "", values=i, tag='rowFont')

def testUNPW3(unIn, pwIn, note):#test username and password version 3
    global runnerID, failedLogins
    if failedLogins >= 5:#if 5 wrong usernames or passwords have been entered
        note.set("LOCKED OUT")
        return
    elif unIn == "admin" and pwIn == "RUNN1ng":#if the admin username or password has been entered
        signInFrm.pack_forget()#close the sign in frame
        adminFrm.pack()#open up the admin frame
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()
    sql = """SELECT id, fname, lname, form FROM runners
WHERE runners.username = ?
AND runners.password = ?
"""
    q.execute(sql,[unIn, pwIn])#check that the username and password entered are stored in the database somewhere
    runner = q.fetchall()
    if len(runner) !=1:#if there's not one person with both the entered username and password
        note.set("Username or password are incorrect")
        failedLogins+=1
    else:#otherwise login
        note.set("logging in")
        runner =  runner[0]
        checkOut.set(runner)#display the runner's name
        runnerID = runner[0]#set the global variable runnerID to the selected runner's ID
        signInFrm.pack_forget()#close the sign in frame
        welcomeFrm.pack()#open the welcome frame
    q.close()
    db.close()

def selectRunner(tree):
    global runnerID
    if tree.focus() != '':#if something is highlighted in the view runners section
        runnerID = tree.item(tree.focus())['values'][0]#set the globabl variable runnerID to the highlighted runner's ID
        selectedUserOut.set(str(tree.item(tree.focus())['values'][1])+' '+str(tree.item(tree.focus())['values'][2]))#set the name so that it can be displayed on the second window
        adminRunnerDBOptsTL.deiconify()#show the second window
        #make sure the edting runner and time frames are closed
        editingRunnerFrm.grid_forget()
        editingTimeFrm.grid_forget()
        

def addNewLoc(ID,name,addr,dist,locA,note):
    global newEventLocCB#the combobox which displays all the locations for the new event section
    #this is needed so that the new location can be added as an option
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = "SELECT id FROM locations"
    locids = q.execute(sql).fetchall()
    try:#make sure the location ID is an integer
        if (int(ID),) in locids:#make sure that there isnt already an event with the same ID as the new one
            note.set("ID is not unique")
            return
        elif int(ID) == 0:#check incase the user enters the new location ID as 0
            note.set("ID cannot be 0")
            return
    except ValueError:
        note.set("ID must be an integer")
        return
    try:#make sure that the distance entered is a number
        if float(dist) <= 0:#and is positive
            note.set("The distance must be greater than 0")
            return
    except ValueError:
        note.set("The distance must be a number")
        return
    
    sql = "INSERT INTO locations(id,name,address,length) VALUES(?,?,?,?)"
    q.execute(sql, [int(ID),name,addr,float(dist)])#save the new location
    
    db.commit()
    q.close()
    db.close()
    
    newLoc = str(ID) +','+ name+','+ addr+' '+str(dist)
    locA.append(newLoc)#add the new location to the global array used in the combobox
    newEventLocCB['values'] = locA#update the combobox
    note.set("New location added")
    

def editRunnerDetails(ID,runnerDetailsA):#retrieves the data to be editied
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()

    sql = "SELECT form,fName,lName,username,password FROM runners WHERE id = ?"

    q.execute(sql, [ID])
    returned = q.fetchall()[0]#as we get a tuple of tuples, we have to select the first(,only) one in the tuple
    for i in range(5):
        runnerDetailsA[i].set(returned[i])#set the StringVar()s to the values stored in the DB
    q.close()
    db.close()
    editingTimeFrm.grid_forget()#makes sure the editing time frame is not displayed
    editingRunnerFrm.grid(row =3,column = 1, columnspan = 2)#displays the edit runner frame

def deleteRunner(ID):
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()

    sql = """DELETE FROM runners
WHERE id = ?
"""
    q.execute(sql, [ID])#delete the runner
    sql = """DELETE FROM times
WHERE runner_id = ?
"""
    q.execute(sql, [ID])#and all of the times for that runner

    db.commit()
    q.close()
    db.close()

    adminRunnerDBOptsTL.withdraw()#closes the second window

def saveRunnerEdits(ID, runnerDetailsA):#this procedure saves the changes made to the runners details
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()

    sql = """UPDATE runners
SET form = ?,fName = ?, lName = ?, username = ?, password = ?
WHERE id = ?
"""
    q.execute(sql, [runnerDetailsA[0].get(),runnerDetailsA[1].get(), runnerDetailsA[2].get(), runnerDetailsA[3].get(), runnerDetailsA[4].get(), ID])
    db.commit()
    q.close()
    db.close()

    selectedUserOut.set(runnerDetailsA[1].get()+' '+runnerDetailsA[2].get())#change the name displayed in the second window to whatever it's been set to

def editRunnerTimes(ID, timesTree, timesFrm, timeA,note):#retrieves the data to be editied
    db = sqlite3.connect('runningDB2/running.db')
    q = db.cursor()
    
    selectedTime = timesTree.item(timesTree.focus())['values']#the values of the highlighted row in the display times column
    if selectedTime == '':#if no time has been highlighted
        note.set("please select a time first")
    else:#if a time has been highlighted
        sql = """SELECT id, name, date FROM events
WHERE id = ?
"""
        q.execute(sql, [selectedTime[0]])#[0] needed as thats the event id for the selected time
        event = str(selectedTime[0])+':'+selectedTime[1]+':'+selectedTime[4]#the details of the event as is in the combobox
        #timeA stores the following
        #[event, hours, minutes, seconds, checked,eventID]
        timeA[5] = selectedTime[0]
        timeA[0].set(event)#store the details for the event

        time = selectedTime[5].split(':')
        timeA[1].set(int(time[0]))#store the hours
        timeA[2].set(int(time[1]))#the minutes
        timeA[3].set(int(time[2]))#and the seconds

        timeA[4].set(selectedTime[6])#stores whether it's been checked

        note.set('')
        

    editingRunnerFrm.grid_forget()#make sure the edit runner frame is not being displayed
    editingTimeFrm.grid(row = 4,column = 1, columnspan = 2)#display the edit time frame

def deleteTime(ID,timeA,note):#deletes the selected time.
    eventID =  int(timeA[0].get().split(':')[0])#the ID will be the first part of the first item in the array
    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()
    q.execute("DELETE FROM times WHERE event_id = ? AND runner_id = ?",[eventID, ID])
    db.commit()
    q.close()
    db.close()
    #reset the values for the items in the array
    timeA[0].set('')
    for i in range(3):
        timeA[i+1].set(0)
    timeA[4].set('')
    timeA[5] = 0
    editingTimeFrm.grid_forget()#remove the edit times frame from the display
    
def saveEditTime(ID,timeA,note):#update the database with the new details for the time
    try:#make sure the time entered is made up of integers
        if timeA[1].get()>4 or timeA[2].get()>59 or timeA[3].get() > 59:
            #for this program the hours must be less than 5
            #minutes and seconds must always be less than 60
            note.set("Time incorrectly input")
            return
    except ValueError:
        note.set("Time incorrectly input")
        return
    
    eventID = int(timeA[0].get().split(':')[0])#the first part of the first item in the array is the event's ID
    #convert new time to seconds
    seconds = 0
    seconds += timeA[3].get()
    seconds += timeA[2].get() * 60
    seconds += timeA[1].get() * 60**2

    if timeA[4] == '✗':
        checked = 0
    else:
        checked = 1

    db = sqlite3.connect("runningDB2/running.db")
    q = db.cursor()

    sql = """UPDATE times
SET event_id = ?, time = ?, checked = ?
WHERE event_id = ?
AND runner_id = ?
"""
    q.execute(sql, [eventID, seconds,checked, eventID, runnerID])
    db.commit()
    q.close()
    db.close()
    note.set('Saved')
    
    
    
#global variables
runnerID = 0#used to identify to the program the current runner logged in or the selected runner
checked = False

failedLogins = 0#number of times an incorrect username or password has been entered

#getLocs() returns all the data in the locations table of the DB
#this is needed so that it's in the correct form to be displayed in the combobox
locsRaw = getLocs()
locsA = []
for i in range(len(locsRaw)):
    loc = ''
    for j in range(len(locsRaw[i])):
        loc += str(locsRaw[i][j])+ ', '
    locsA.append(loc)





myGUI = Tk()
myGUI.title("Cross Country Program")



myMenuBar = Menu(myGUI)
runnerOptsMenu = Menu(myMenuBar)#umm rename???
runnerOptsMenu.add_command(label = "Input times", command = lambda: timeEntryFrm.pack())
runnerOptsMenu.add_command(label = "View Times", command = lambda: disTs(runnerID,viewTimesTree,viewTsyscroll))
runnerOptsMenu.add_command(label = "ViewGraph", command = lambda: graphFrm.pack())
myMenuBar.add_cascade(label = "Runner Options", menu = runnerOptsMenu)

myGUI.config(menu = myMenuBar)

"""signing in
what they'll see at the start of the program"""
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


"""welcome frame
if a runner logs in this is the section they'll see
their name and form will be shown
"""
welcomeFrm = Frame(myGUI)

checkLbl = Label(welcomeFrm, text = "Welcome Back")
checkLbl.grid(row = 4, column =1)
checkOut = StringVar()
checkOutTB = Entry(welcomeFrm, textvariable = checkOut, state = "readonly")
checkOutTB.grid(row = 4, column =2, columnspan = 2)


"""entering their times
the runners enter their own times before teacher can check it
the teacher can also access this section
"""
timeEntryFrm = Frame(myGUI)

eventsLbl = Label (timeEntryFrm, text = "Event")
eventsLbl.grid(row = 1, column = 1)

#placing the events in the combobox
eventsIn = StringVar()
eventsIn.set("No Event Selected")
eventsRaw = getEvents()
eventsA = []
for i in range(len(eventsRaw)):
    eventsA.append(str(eventsRaw[i][0])+':'+str(eventsRaw[i][2])+':'+eventsRaw[i][3])
eventsCB = Combobox(timeEntryFrm, values = eventsA, textvariable = eventsIn)
eventsCB.grid(row = 1, column =2, columnspan = 3)

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

"""
viewTimesFrm = Frame(myGUI)

viewTsCols = ("E_ID", "Event Name", "Location", "Distance", "Date", "Time", "Checked")
viewTimesTree = Treeview(viewTimesFrm,columns = viewTsCols,selectmode = 'browse', height = 5)
viewTsyscroll = Scrollbar(viewTimesFrm, orient='vertical', command=viewTimesTree.yview)
createTree(viewTimesTree, viewTsCols, viewTsyscroll, (50,150,150,75,100,100,50))

exitVTB = Button(viewTimesFrm, text = "Done", command = lambda: viewTimesFrm.pack_forget())





"""the graph
This section is kinda complicated

"""
graphFrm = Frame(myGUI)

graphLocIn = StringVar()#the choice made in the combobox
graphLocIn.set("0,choose a location")
findGraphLoc = Combobox(graphFrm, textvariable = graphLocIn, values = locsA)
findGraphLoc.pack()

selectLocB = Button(graphFrm, text = "Select Location", command = lambda:genGraph())
selectLocB.pack()

graphFrames = []#all the graphs that have been created during this run of the program
exitGraphsBs = []#the exit graph buttons associated with those frames


def genGraph():
    #the frame for the graph that's being created is the last one in the list
    graphFrames.append(Frame(graphFrm))
    graphFrames[-1].pack(side = LEFT)#if more graphs are added, they go from left to right

    localishIndex = graphFrames.index(graphFrames[-1])#the index of the frame at the end of the graph frames list
    #there must be a reason i didn't just do len(graphFrames)
    localishButton = Button(graphFrames[-1],#put it on the current frame
                            text = "Close Graph",
                            command = lambda: destroyGraph(localishIndex))#make sure it only destroys the current one    
    
    exitGraphsBs.append(localishButton)#add the button to the end of the exit buttons array
    exitGraphsBs[-1].pack()

    if graphLocIn.get()[0] == '0':#if noe location has been selected
        errorLbl = Label(graphFrames[-1], text = 'Location must be selected')
        errorLbl.pack()#instead of displaying the graph, an error note is displayed
        #as these notes are defined differently, they're called errorLbl and are only used once in the run of the proceudre
        return
    elif runnerID == 0:#only applies to the admin, when they haven't selected a runner
        errorLbl = Label(graphFrames[-1], text = 'There is no runner selected')
        errorLbl.pack()
        return
    runnerData = loadData(runnerID, graphLocIn.get().split(',')[0])
    if len(runnerData) == 0:#if there are no times at the selected location for the runner
        errorLbl = Label(graphFrames[-1], text = 'There is no data for this location')
        errorLbl.pack()
        return

    times = []
    for i in range(len(runnerData)):
        times.append(runnerData[i][0])

    #the maximum y value on the graph
    yMax = floor((max(times)/10**(len(str(max(times)))-1)+1))*10**(len(str(max(times)))-1)
    #constants
    windowW =  300
    windowH = 400
    margin = 20
    sqrx = int((windowW - margin)/10)
    sqry = int((windowH - margin)/10)
    #Tsize = 11

    #the graph is draw on a canvas with a grey background
    graphC = Canvas(master = graphFrames[-1], width = windowW, height = windowH, bg = "grey")#C for canvas-
    graphC.pack()

    #axis
    graphC.create_line(0, windowH - margin, windowW, windowH - margin, fill = "red", width = 5)
    graphC.create_line(margin, 0,margin, windowH, fill = "red", width = 5)
    #grid and axis labels for Y
    for i in range(windowH - margin, 0, -sqry):
        graphC.create_line(0,i, windowW, i)#lines from right to left spaced sqry apart
        ytext = str(mapRange(windowH - i, 20, windowH, 0,yMax))#what that line represts in seconds
        yLbl = Label(graphFrames[-1], text = ytext)
        yLbl.place(x = 0, y = i)
    #x-axis
    for i in range(margin, windowW, sqrx):
        graphC.create_line(i, 0, i, windowH)#lines from top to bottom spaced sqrx apart
        xLbl = Label(graphFrames[-1], text = str((i-margin)/sqrx))#the lines are labelled 0-10
##        if (i-margin)/sqrx < len(dates):
##            xLbl = Label(graphFrames[-1],  text = dates[int((i-margin)/sqrx)])
            
        xLbl.place(x = i,y = windowH-margin)
        
    #the line
    for i in range(0, len(times)-1, 1):
        yp = times[i]*(windowH - margin)/yMax
        yp2 = times[i+1]*(windowH - margin)/yMax
        #the lines are drawn sqrx apart
        graphC.create_line(i*sqrx + margin, windowH - yp, (i+1)*sqrx + margin, windowH - yp2, fill = "blue")
    
    

def destroyGraph(num):#this procedure is assigned to each exit graph button
    #therefore it's important that it destroys the correct graph
    graphFrames[num].pack_forget()
    graphFrames[num] = None
    exitGraphsBs[num] = None
    

        
exitGraphB = Button(graphFrm, text = "Done", command = lambda: graphFrm.pack_forget())
exitGraphB.pack()


"""the admin frame?
once the admin/teacher whatever you wanna call it logs in this frame will be displayed
this frame will just contain the buttons
the teacher/admin will still have access to the runner options
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

newEventNote = StringVar()
newEventNoteLbl = Label(newEventFrm, textvariable = newEventNote)
newEventNoteLbl.grid(row =4, column = 3, columnspan = 2)


newEventLocCB = Combobox(newEventFrm,textvariable = newEventLocIn, values = locsA,width = 30)
newEventLocCB.grid(row = 3, column = 2)

createNewLocB = Button(newEventFrm, text = "need a new Location", command = lambda:newLocFrm.pack())
createNewLocB.grid(row =3, column = 3)

addNewEventB = Button(newEventFrm, text = "Add the Event", command = lambda:saveEvent(newEventIDIn.get(),int(newEventLocIn.get().split(',')[0]), newEventNIn.get(), newEDateDIn,newEDateMIn,newEDateYIn, newEventNote))
addNewEventB.grid(row =4 , column = 2)

newEventNextIDB = Button(newEventFrm, text = "find next ID", command = lambda: newEventIDIn.set(findNextEID()))
newEventNextIDB.grid(row = 2, column = 4)#so it's under the ID TB


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

use treeviews
"""
viewRunnerFrm = Frame(myGUI)


findRunnerFrm = Frame(viewRunnerFrm)
viewRunnerTreeFrm = Frame(viewRunnerFrm)

findRunnerFrm.pack()
viewRunnerTreeFrm.pack()

adminRunnerDBOptsTL = Toplevel()
adminRunnerDBOptsTL.withdraw()

#ok so they type in name/form/id 
#get a list of the runners
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


selectedUserLbl = Label(adminRunnerDBOptsTL, text = "Selected User:")
selectedUserOut = StringVar()
selectedUserTB = Entry(adminRunnerDBOptsTL, textvariable = selectedUserOut, state = DISABLED)

selectedUserLbl.grid(row = 1, column = 1)
selectedUserTB.grid(row = 1, column = 2)


editingRunnerFrm = Frame(adminRunnerDBOptsTL)

editFormLbl = Label(editingRunnerFrm, text = "Form")
editFormLbl.grid(row = 1, column = 1)
editFormIn = StringVar()
editFormTB = Entry(editingRunnerFrm, textvariable = editFormIn)
editFormTB.grid(row = 1, column =2)

editFNameLbl = Label(editingRunnerFrm, text = "First Name")
editFNameLbl.grid(row = 2, column = 1)
editFNameIn = StringVar()
editFNameTB = Entry(editingRunnerFrm, textvariable = editFNameIn)
editFNameTB.grid(row = 2, column =2)

editSNameLbl = Label(editingRunnerFrm, text = "Surname")
editSNameLbl.grid(row = 3, column = 1)
editSNameIn = StringVar()
editSNameTB = Entry(editingRunnerFrm, textvariable = editSNameIn)
editSNameTB.grid(row = 3, column = 2)

editUNLbl = Label(editingRunnerFrm, text = "Username")
editUNLbl.grid(row = 4, column = 1)
editUNIn = StringVar()
editUNTB = Entry(editingRunnerFrm, textvariable = editUNIn)
editUNTB.grid(row= 4, column =2)

editPWLbl = Label(editingRunnerFrm, text = "Password")
editPWLbl.grid(row = 5, column =1)
editPWIn = StringVar()
editPWTB = Entry(editingRunnerFrm, textvariable = editPWIn)
editPWTB.grid(row = 5, column = 2)

editingDetailsA = [editFormIn,editFNameIn,editSNameIn,editUNIn,editPWIn]

delRunnerB = Button(editingRunnerFrm, text = "DeleteRunner", command = lambda:deleteRunner(runnerID))
delRunnerB.grid(row = 6, column =1)
saveEditRunnerB = Button(editingRunnerFrm, text = "Save changes", command = lambda:saveRunnerEdits(runnerID, editingDetailsA))
saveEditRunnerB.grid(row = 6, column = 2)


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
editCheckVar = StringVar()
editCheckB = Checkbutton(editingTimeFrm, variable = editCheckVar)
editCheckB.grid(row = 3, column = 2)

editTimeNote = StringVar()
editTimeNoteLbl = Label(editingTimeFrm, textvariable = editTimeNote)
editTimeNoteLbl.grid(row = 3, column = 3, columnspan = 2)

editingTimeA = [editTimeEventIn, editTimeHIn, editTimeMIn, editTimeSIn, editCheckVar,0]



deleteTimeB = Button(editingTimeFrm, text = 'Delete Time', command = lambda: deleteTime(runnerID, editingTimeA,editTimeNote))
deleteTimeB.grid(row  = 4, column =2, columnspan =3)

saveEditTimeB = Button(editingTimeFrm, text= "Save Edits", command = lambda: saveEditTime(runnerID,editingTimeA,editTimeNote))
saveEditTimeB.grid(row = 4, column = 1)



editRunnerB = Button(adminRunnerDBOptsTL, text = "Edit Runner", command = lambda: editRunnerDetails(runnerID, editingDetailsA))
editRunnerB.grid(row = 2, column = 1)
#within the edit menus thee will be a delete button/option
editRunnerTimesB = Button(adminRunnerDBOptsTL, text = "Edit Time", command = lambda:editRunnerTimes(runnerID, viewTimesTree, viewTimesFrm,editingTimeA,editTimeNote))
editRunnerTimesB.grid(row =2, column = 2)


#this is supposed to stop it getting destroyed
adminRunnerDBOptsTL.protocol('WM_DELETE_WINDOW', lambda:adminRunnerDBOptsTL.withdraw())
#so you can click x on the window
#and then open it up again



myGUI.mainloop()

print("PROGRAM END")

