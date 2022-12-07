# SDEV 140 - M08 Final Project 
# Catalano Matteo
# 11/21/2022
# Play sorry with two die, and one peg. Move your piece down the board first. 
# But rolling certain numbers will change the pace of the game.

from tkinter import *
#from PIL import ImageTk, Image
import random

defaultW = 5 #default Width for cells in board
defaultH = 2 #default Height for cells in board
playersIcons = ["♥","♦","♣","♠"]
playersName = ["","","",""]
nPlayers = 2
activePlayer = 0
activePlayerConsecTurns = 0
gameStarted = False
turn = 0

def spiral(m, n):
    k = 0
    l = 0
 
    ''' k - starting row index
        m - ending row index
        l - starting column index
        n - ending column index
        i - iterator '''
 
    while (k < m and l < n):
 
        # Print the first row from
        # the remaining rows
        for i in range(l, n):
            print(k,i, "a")
 
        k += 1
 
        # Print the last column from
        # the remaining columns
        for i in range(k, m):
            print(i,n - 1, "b")
 
        n -= 1
 
        # Print the last row from
        # the remaining rows
        if (k < m):
 
            for i in range(n - 1, (l - 1), -1):
                print(m - 1,i, "c")
 
            m -= 1
 
        # Print the first column from
        # the remaining columns
        if (l < n):
            for i in range(m - 1, k - 1, -1):
                print(i,l, "d")
 
            l += 1

def gridDef(row,col):     
    rows = {1:{ 0:Label(root, text="", width=defaultW, height=defaultH)}}
    count = 1
    for i in range(1,row+1):
        rows[i] = { 0:Label(root, text="", width=defaultW, height=defaultH)}
        rng = range(col)
        if(i%2 == 0):
            rng = reversed(rng)

        for k in rng:
            rows[i][k] = addLable(i,k, count)
            count += 1
    return rows

def gridDefSpiral(row,col):     
    k = 1
    m = row+1
    l = 0
    n = col
    #rows = {0:{ 0:Label(root, text="START"+ "\n ♥♦♣♠", width=defaultW*7, height=defaultH, bg="gray")}}
    rows = {1:{ 0:Label(root, text="", width=defaultW, height=defaultH)}}
    for i in range(1,row+1):
        rows[i] = { 0:Label(root, text="", width=defaultW, height=defaultH)}        
    count = 1

    while (k < m and l < n):
        rows[k] = { 0:Label(root, text="", width=defaultW, height=defaultH)}

        for i in range(l, n):
            print(k,i, count, "a")
            rows[k][i] = addLable(k,i, count)
            count += 1        
        k += 1

        for i in range(k, m):
            print(i,n - 1, count, "b") 
            rows[i][n - 1] = addLable(i,n - 1, count)            
            count += 1    
        n -= 1

        if (k < m): 
            for i in range(n - 1, (l - 1), -1):
                print(m - 1,i, count, "c")                 
                rows[m-1][i] =addLable(m-1,i, count)            
                count += 1   
            m -= 1

        if (l < n):
            for i in range(m - 1, k - 1, -1):
                print(i,l, count, "d")                                
                rows[i][l] = addLable(i,l, count)            
                count += 1   
            l += 1

    return rows

def addLable(i,k, count):    
    return Label(root, name= str(i)+","+str(k), text=str(count), width=defaultW, height=defaultH, bg="#b3e5fc")

def gridDeploy():       
    #i = k = 0
    for i in rows:
        row = rows[i]
        for k in row: 
            elem = row[k]
            #print(elem.)
            elem.grid(row=i,column=k, padx=(1, 1), pady=(1, 1))

def gridAdd(element, row=-1, col=-1):
    if row == -1:
        row = list(rows.keys())[-1]
    if not row in rows:
        rows[row] = {0:Label(root, text="", width=5, height=2)}
        
    if col == -1:        
        col = list(rows[row].keys())[-1]+1
        rows[0][col] = Label(root, text="", width=25)
    rows[row][col] = element

def posToCoord(pos):

    row = (pos//7)
    if pos%7 != 0:
        row += 1

    if(row%2 == 0):
        col =(7-pos%7)
        if pos%7 == 0:
            col = 0
    else:
        col =(pos%7)-1        
        if pos%7 == 0:
            col = 6

    return [row, col]

def playerToCell(player=0, pos=0):

    coord = posToCoord(pos)
    row = coord[0]
    col = coord[1]
        
    txt = rows[row][col].cget("text")        
    txt += "\n" + playersIcons[player]    
    rows[row][col].config(text=txt)
    #print(player, playersIcons[player], pos, str(row)+ "-"+str(col))

    return 
    for row in rows:
        for col in rows[row]:            
            playerInCell = -1
            txt = rows[row][col].cget("text").split("\n")
            if(len(txt)>1):
                playerInCell = playersIcons.index(txt[1].strip()) 
            cnt = int(txt[0])
            pos = rows[row][col]._name
            if cnt == pos:
                print(cnt, pos,playerInCell)

def swap(player, swappedPlayer):
    swapPos = playersPos[swappedPlayer]
    playerPos = playersPos[player]
    move(player, swapPos)
    move(swappedPlayer, playerPos)

def move(player, pos):    

    if pos> 50:        
        print("Player", playersName[player], "Overshoot the end. Lost turn")
        return
    else:
        removePlayer(player)
        if pos == 50:
            sendToEnd(player)
            print("Player", playersName[player], "won! (in ",turn,"turns)")    
            endScreen(player)
            return
        
        if pos <= 0:            
            sendToStart(player)
        else:
            if(pos in playersPos):    
                playerInCell = playersPos.index(pos)        
                print("Removing",playersName[playerInCell],"from", pos)
                removePlayer(playerInCell)
                if playerInCell != player:
                    sendToStart(playerInCell)

            playerToCell(player,pos)
            playersPos[player] = pos   
    
def removePlayer(player):
    if playersPos[player] == 0:
        removeFromStart(player)
        return
    coord = posToCoord(playersPos[player])
    row = coord[0]
    col = coord[1]
    txt = rows[row][col].cget("text")     
    splitTxt = txt.split("\n")    
    rows[row][col].config(text=splitTxt[0])

def sendToStart(player):
    playersPos[player] = 0
    start.config(text=start.cget("text")+ playersIcons[player])
    print("Player",playersName[player], "sent to start")

def sendToEnd(player):
    playersPos[player] = 50
    end.config(text=end.cget("text")+ " " + playersIcons[player])
    rollBtn["state"] = DISABLED

def removeFromStart(player):
    start.config(text=start.cget("text").replace(playersIcons[player], ""))

def dieRoll():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    
    return [d1, d2]

def turnDecision(player, double): #return true if it should skip a turn

    global activePlayer, activePlayerConsecTurns, gameStarted

    #Game start with double
    if not gameStarted:                
        if double:
            gameStarted = True
            print("GAME STARTED!")
        else:
            activePlayer = 0 if player+1 == nPlayers else player + 1
            print("Can't start without a double.")
            return True
    
    #sets next player
    if double : #player rolls double, gets extra turn
        if activePlayerConsecTurns == 0:            
            activePlayer = player
            activePlayerConsecTurns += 1
        else: #Start over when player rolls double two times
            print("Rolled double two times. Start over")
            move(player,0)
            activePlayerConsecTurns = 0
            activePlayer = 0 if player+1 == nPlayers else player + 1
            return True
    else:
        activePlayerConsecTurns = 0
        activePlayer = 0 if player+1 == nPlayers else player + 1

    return False

def diceConditions(player, dieRes):

    global lastMoveLbl
    print("------------")
    #move(player,50) 
    #return

    roll = dieRes[0] + dieRes[1]
    #determins if rolled a double
    double = False
    if dieRes[0] == dieRes[1]:
        double = True
    
    moveString = playersName[player] + " " + playersIcons[player] 
    moveString += " rolled " + str(dieRes[0]) + "+" + str(dieRes[1]) + " = " + str(roll) 
    moveString += " DOUBLE" if double else " not a double" 
    moveString += ".\nTurn started in cell " + str(playersPos[player])
    
    print(playersName[player], playersIcons[player], "rolled",
        dieRes[0] ,"+", dieRes[1],"=", roll,
        "DOUBLE" if double else "not a double" ,
         ". Turn started in cell",playersPos[player])

    if turnDecision(player, double): 
        moveString += "\nCan not start without a double."
        lastMoveLbl.config(text=moveString)
        return
            
    match roll: #plays out roll
        case 2|3|6|9|10: #move forward
            move(player, playersPos[player] + roll)
            print("Move by", roll, "to cell", playersPos[player])
            moveString += "\nMove by " + str(roll) + " to cell " + str(playersPos[player])
        case 4: #move backward by 1
            move(player,playersPos[player]-1)
            print("Move back by 1 to cell", playersPos[player])
            moveString += "\nMove back by 1 to cell " + str(playersPos[player])
        case 5: #move backward by 2
            move(player,playersPos[player]-2)
            print("Move back by 2 to cell", playersPos[player])
            moveString += "\nMove back by 2 to cell " + str(playersPos[player])
        case 7: #Swap spots with the leading player / or nothing if player is in lead
            leadingPlayer = playersPos.index(max(playersPos))
            swap(player, leadingPlayer)
            print("Swap spots with the leading player, now you are on cell", playersPos[player])
            moveString += "\nSwap spots with the leading player, \nnow you are on cell "+ str(playersPos[player])
        case 8: #lose your turn (no move)
            print("Lose your turn.")
            moveString += "\nLose your turn"
        case 11: #Swap spots with the last player / or do nothing if player is last.
            lastPlayer = playersPos.index(min(playersPos))
            swap(player, lastPlayer)
            print("Swap spots with the last player, now you are on cell", playersPos[player])
            moveString += "\nSwap spots with the last player, \nnow you are on cell " +  str(playersPos[player])
        case 12: #Start Over
            move(player,0)
            print("Start Over")
            moveString += "\nStart Over"
        case _:
            print("You shouldn't have rolled this:", roll)

    lastMoveLbl.config(text=moveString)

def playerDef(numP):
    global nPlayers, playersPos
    nPlayers = numP
    playersPos = [0]*numP

def callback():
    #print(sv.get())
    return True

def btnRoll():
    global turn
    diceConditions(activePlayer,dieRoll())    
    turn +=1

def openPlayerSelectW():

    global playerSelectW, lblPlayer, entPlayer, addPlayerBtn
    playerSelectW = Toplevel(root)
    playerSelectW.title("Players")
    #playerSelectW.geometry("500x200")
    lblPlayer = []
    entPlayer = []
    for i in range(4):
        lblPlayer.append(Label(playerSelectW, text ="Name of player"+str(i+1)))
        entPlayer.append(Entry(playerSelectW, width=20))

    for i in range(2):
        lblPlayer[i].grid(row = i, column=1)
        entPlayer[i].grid(row = i, column=2)

    addPlayerBtn = Button(playerSelectW, text="Add Player", command=addPlayer,width=(defaultW*2))
    addPlayerBtn.grid(row = 6, column=1, columnspan=1)

    startGameBtn = Button(playerSelectW, text="Start!", command=startGame,width=(defaultW*2))
    startGameBtn.grid(row = 6, column=2, columnspan=1)

    playerSelectW.lift()
    playerSelectW.attributes('-topmost',True)
    #playerSelectW.after_idle(playerSelectW.attributes,'-topmost',False)
    root.withdraw()
    
def addPlayer():
    if nPlayers<4:
        lblPlayer[nPlayers].grid(row = nPlayers, column=1)
        entPlayer[nPlayers].grid(row = nPlayers, column=2)
        playerDef(nPlayers+1)        
        if nPlayers == 4:
            addPlayerBtn["state"] = DISABLED

def startGame():
    for i in range(nPlayers):
        text = entPlayer[i].get()
        if text == "":
            print(f"Player {i+1} name is not valid")
            return
        playersName[i] = entPlayer[i].get()
        

    playerDef(nPlayers)  
    defineGame()
    gridDeploy()
    playerSelectW.destroy()
    root.deiconify()

def defineGame():
    global rows, start, end, rollBtn, activePlayer, activePlayerConsecTurns, gameStarted, turn, lastMoveLbl, playerIconlLbl, playerNamelLbl

    activePlayer = 0
    activePlayerConsecTurns = 0
    gameStarted = False
    turn = 0

    rollBtn = Button(root, text="ROLL!", command=btnRoll,width=(defaultW*3)+1*3)
    rollBtn.grid(row = 8, column=8, columnspan=4)

    playerIconString = ""
    for i in range(nPlayers):
        playerIconString += playersIcons[i]

    start = Label(root, text="START"+ "\n"+ playerIconString, width=(defaultW*7)+1*7, height=defaultH, bg="#82b3c9")
    start.grid(row = 0, column=0, columnspan=7)

    rows = gridDef(7,7)

    end = Label(root, text="50 - END"+ "\n", width=(defaultW*7)+1*7, height=defaultH, bg="#82b3c9")
    end.grid(row = 8, column=0, columnspan=7)

    playerIconlLbl = [Label()]*4
    playerNamelLbl = [Label()]*4
    for i in range(nPlayers):
        playerIconlLbl[i] = Label(root, text=playersIcons[i], width=(defaultW*2), font=("Arial", 20))
        playerNamelLbl[i] = Label(root, text=playersName[i], width=(defaultW*2), font=("Arial", 12))
        playerIconlLbl[i].grid(row = 0, column=8+i, columnspan=1)
        playerNamelLbl[i].grid(row = 1, column=8+i, columnspan=1)
    lastMoveLbl = Label(root, text="", width=(defaultW*3)*nPlayers, font=("Arial", 10))
    lastMoveLbl.grid(row = 2, column=8, columnspan=4, rowspan=5)

def endScreen(player):
    global winImg, endScreenW, playerNamelLbl, playerNamelLbl

    root.withdraw()

    endScreenW = Toplevel(root)
    endScreenW.title("End screen")

    wPlayer = Label(endScreenW, text = playersName[player]+" won in "+str(turn)+" turns!", font=("Arial", 25))
    wPlayer.grid(row = 0, column=0, columnspan=2)

    winImg = PhotoImage(file = "winnerWinnerChickenDinner.gif")
    image = Label(endScreenW, image=winImg, text="Win Image")
    image.grid(row = 1, column=0, columnspan=2)

    restartGameBtn = Button(endScreenW, text="Restart", command=restartGame,width=(defaultW*2))
    restartGameBtn.grid(row = 2, column=0, columnspan=1)

    quitBtn = Button(endScreenW, text="Quit", command=quit,width=(defaultW*2))
    quitBtn.grid(row = 2, column=1, columnspan=1)

def restartGame():
    global nPlayers, playersName, playerIconlLbl, playerNamelLbl
    nPlayers = 2
    playersName = ["","","",""]
    for i in range(4):
        playerIconlLbl[i].destroy()
        playerNamelLbl[i].destroy()

    endScreenW.destroy()
    openPlayerSelectW()
    

#definitions
root = Tk()
root.title("M06 Programming Assignment")
#root.resizable(width=False, height=False)

openPlayerSelectW()

"""
#sv = StringVar()
#e = Entry(root, width=20)
#e2 = Entry(root, textvariable=sv, validate="focusout", validatecommand=callback)
#for i in range(1,52):
#    asd =input("ENTER to roll...")
#    move(0,i)
#print(rows[1][0]._name)


asd =input("ENTER to roll...")
diceConditions(0,6)
asd =input("ENTER to roll...")
diceConditions(0,12)
asd =input("ENTER to roll...")
diceConditions(1,11)

asd =input("ENTER to roll...")
move(2,diceRoll())
asd =input("ENTER to roll...")
move(3,diceRoll())
print("---")
asd =input("ENTER to roll...")
move(0,playersPos[0] + diceRoll())
asd =input("ENTER to roll...")
move(1,playersPos[1] + diceRoll())
asd =input("ENTER to roll...")
move(2,playersPos[2] + diceRoll())
asd =input("ENTER to roll...")
move(3,playersPos[3] + diceRoll())


for i in range(100):
    btnRoll()
    if 50 in playersPos:
        break
"""

root.mainloop()