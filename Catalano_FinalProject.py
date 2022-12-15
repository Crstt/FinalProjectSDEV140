# SDEV 140 - M08 Final Project 
# Catalano Matteo
# 11/21/2022
# Play sorry with two die, and one peg. Move your piece down the board first. 
# But rolling certain numbers will change the pace of the game.

from tkinter import *
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

def gridDef(row,col):     
    # Define rows dictionary with first row
    rows = {1:{ 0:Label(root, text="", width=defaultW, height=defaultH)}}
    # Set counter variable to 1
    count = 1
    # Loop through number of rows
    for i in range(1,row+1):
        # Add empty dictionary for each row
        rows[i] = { 0:Label(root, text="", width=defaultW, height=defaultH)}
        # If current row number is even, reverse range of column numbers
        if(i%2 == 0):
            rng = reversed(rng)
        else:
            # Otherwise, leave range as is
            rng = range(col)
        # Loop through range of column numbers
        for k in rng:
            # Add label for current row and column
            rows[i][k] = addLable(i,k, count)
            # Increment counter by 1
            count += 1
    # Return rows dictionary
    return rows

def addLable(i,k, count):    
    return Label(root, name= str(i)+","+str(k), text=str(count), width=defaultW, height=defaultH, bg="#b3e5fc")

def gridDeploy():       
    # Loop through rows in rows dictionary
    for i in rows:
        # Set row variable to current row dictionary
        row = rows[i]
        # Loop through labels in current row
        for k in row: 
            # Set elem variable to current label
            elem = row[k]
            # Deploy label using grid method
            elem.grid(row=i,column=k, padx=(1, 1), pady=(1, 1))

def gridAdd(element, row=-1, col=-1):
    # If row not provided, set to last key in rows dictionary
    if row == -1:
        row = list(rows.keys())[-1]
    # If row not a key in rows dictionary, add empty dictionary for row
    if not row in rows:
        rows[row] = {0:Label(root, text="", width=5, height=2)}
        
    # If column not provided, set to last key in row dictionary plus 1
    if col == -1:        
        col = list(rows[row].keys())[-1]+1
        # Add empty label for new column in 0th row
        rows[0][col] = Label(root, text="", width=25)
    # Add element to row at specified column
    rows[row][col] = element

def posToCoord(pos):
    # Calculate row number by dividing pos by 7 and rounding up
    row = (pos//7)
    # If remainder of pos divided by 7 is not 0, increment row number by 1
    if pos%7 != 0:
        row += 1

    # If row number is even, calculate column number based on remainder of pos divided by 7
    if(row%2 == 0):
        col =(7-pos%7)
        # If remainder is 0, set column number to 0
        if pos%7 == 0:
            col = 0
    # If row number is odd, calculate column number based on remainder of pos divided by 7
    else:
        col =(pos%7)-1        
        # If remainder is 0, set column number to 6
        if pos%7 == 0:
            col = 6

    # Return list of row and column numbers
    return [row, col]

def playerToCell(player=0, pos=0):
    # Convert position to row and column numbers
    coord = posToCoord(pos)
    row = coord[0]
    col = coord[1]
        
    # Retrieve current text of label at specified row and column
    txt = rows[row][col].cget("text")        
    # Append new line character and player's icon to text
    txt += "\n" + playersIcons[player]    
    # Set text of label to updated string
    rows[row][col].config(text=txt)
    # Exit function without returning any value
    return 

def swap(player, swappedPlayer):
    # Set swapPos to position of swappedPlayer
    swapPos = playersPos[swappedPlayer]
    # Set playerPos to position of player
    playerPos = playersPos[player]
    # Swap positions of player and swappedPlayer using move function
    move(player, swapPos)
    move(swappedPlayer, playerPos)

def move(player, pos):
    # check if the new position is greater than 50
    if pos> 50:        
        print("Player", playersName[player], "Overshoot the end. Lost turn")
        return
    else:
        # remove the player from their current position
        removePlayer(player)
        
        # check if the new position is 50, indicating that the player has won the game
        if pos == 50:
            sendToEnd(player)
            print("Player", playersName[player], "won! (in ",turn,"turns)")    
            endScreen(player)
            return
        
        # check if the new position is less than or equal to 0, indicating that the player has moved off the game board
        if pos <= 0:            
            sendToStart(player)
        else:
            # check if the new position is already occupied by another player
            if(pos in playersPos):    
                playerInCell = playersPos.index(pos)        
                print("Removing",playersName[playerInCell],"from", pos)
                removePlayer(playerInCell)
                if playerInCell != player:
                    sendToStart(playerInCell)

            # move the current player to the new position
            playerToCell(player,pos)
            playersPos[player] = pos
    
def removePlayer(player):
    # If player's position is 0, remove from start and exit function
    if playersPos[player] == 0:
        removeFromStart(player)
        return
    # Convert player's position to row and column numbers
    coord = posToCoord(playersPos[player])
    row = coord[0]
    col = coord[1]
    # Retrieve current text of label at specified row and column
    txt = rows[row][col].cget("text")     
    # Split text into list of strings at each new line character
    splitTxt = txt.split("\n")    
    # Set text of label to first string in list (original text before player's icon added)
    rows[row][col].config(text=splitTxt[0])


def sendToStart(player):
    # Update player's position to 0
    playersPos[player] = 0
    # Append player's icon to start label
    start.config(text=start.cget("text")+ playersIcons[player])
    # Print message indicating player sent to start
    print("Player",playersName[player], "sent to start")

def sendToEnd(player):
    # Update player's position to 50
    playersPos[player] = 50
    # Append player's icon to end label
    end.config(text=end.cget("text")+ " " + playersIcons[player])
    # Disable rollBtn button
    rollBtn["state"] = DISABLED

def removeFromStart(player):
    # Remove player's icon from start label
    start.config(text=start.cget("text").replace(playersIcons[player], ""))

def dieRoll():
    # Generate two random integers between 1 and 6
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    
    # Return list of integers
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
    # Set global nPlayers and playersPos variables to numP and list of 0s with length equal to numP
    global nPlayers, playersPos
    nPlayers = numP
    playersPos = [0]*numP

def btnRoll():
    # Increment global turn variable by 1
    global turn
    # Simulate active player rolling dice and call diceConditions function on active player and dice roll values
    diceConditions(activePlayer,dieRoll())    
    turn +=1

def openPlayerSelectW():
    # Create new window for player selection
    global playerSelectW, lblPlayer, entPlayer, addPlayerBtn
    playerSelectW = Toplevel(root)
    playerSelectW.title("Players")
    # Create list of player labels and entry fields
    lblPlayer = []
    entPlayer = []
    for i in range(4):
        lblPlayer.append(Label(playerSelectW, text ="Name of player"+str(i+1)))
        entPlayer.append(Entry(playerSelectW, width=20))
    # Display player labels and entry fields in grid layout
    for i in range(2):
        lblPlayer[i].grid(row = i, column=1)
        entPlayer[i].grid(row = i, column=2)
    # Create addPlayerBtn and startGameBtn buttons
    addPlayerBtn = Button(playerSelectW, text="Add Player", command=addPlayer,width=(defaultW*2))
    addPlayerBtn.grid(row = 6, column=1, columnspan=1)

    startGameBtn = Button(playerSelectW, text="Start!", command=startGame,width=(defaultW*2))
    startGameBtn.grid(row = 6, column=2, columnspan=1)
    # Bring playerSelectW window to front
    playerSelectW.lift()
    playerSelectW.attributes('-topmost',True)
    # Hide root window
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
    root.update_idletasks()

def defineGame():
    global rows, start, end, rollBtn, activePlayer, activePlayerConsecTurns, gameStarted, turn, lastMoveLbl, playerIconlLbl, playerNamelLbl, rollImg

    # initialize the game state variables
    activePlayer = 0
    activePlayerConsecTurns = 0
    gameStarted = False
    turn = 0

    # create the roll button
    rollImg = PhotoImage(file = "dieRolling.png").subsample(8)
    rollBtn = Button(root, text="ROLL!", command=btnRoll, image=rollImg, compound = LEFT)
    rollBtn.grid(row = 7, column=8, columnspan=4, rowspan=2)

    # create the starting position label
    playerIconString = ""
    for i in range(nPlayers):
        playerIconString += playersIcons[i]

    start = Label(root, text="START"+ "\n"+ playerIconString, width=(defaultW*7)+1*7, height=defaultH, bg="#82b3c9")
    start.grid(row = 0, column=0, columnspan=7)

    # create the game board grid
    rows = gridDef(7,7)

    # create the ending position label
    end = Label(root, text="50 - END"+ "\n", width=(defaultW*7)+1*7, height=defaultH, bg="#82b3c9")
    end.grid(row = 8, column=0, columnspan=7)

    # create player icons and names
    playerIconlLbl = [Label()]*4
    playerNamelLbl = [Label()]*4
    for i in range(nPlayers):
        playerIconlLbl[i] = Label(root, text=playersIcons[i], width=(defaultW*2), font=("Arial", 20))
        playerNamelLbl[i] = Label(root, text=playersName[i], width=(defaultW*2), font=("Arial", 12))
        playerIconlLbl[i].grid(row = 0, column=8+i, columnspan=1)
        playerNamelLbl[i].grid(row = 1, column=8+i, columnspan=1)

    # create a label to show the last move
    lastMoveLbl = Label(root, text="", width=(defaultW*3)*nPlayers, font=("Arial", 10))
    lastMoveLbl.grid(row = 2, column=8, columnspan=4, rowspan=5)
    
def endScreen(player):
    global winImg, endScreenW

    # Hide root window
    root.withdraw()

    # Create new window for end screen
    endScreenW = Toplevel(root)
    endScreenW.title("End screen")

    #Creates win lable
    wPlayer = Label(endScreenW, text = playersName[player]+" won in "+str(turn)+" turns!", font=("Arial", 25))
    wPlayer.grid(row = 0, column=0, columnspan=2)

    #Creates images
    winImg = PhotoImage(file = "winnerWinnerChickenDinner.gif")
    image = Label(endScreenW, image=winImg, text="Win Image")
    image.grid(row = 1, column=0, columnspan=2)

    #Creates restart button
    restartGameBtn = Button(endScreenW, text="Restart", command=restartGame,width=(defaultW*2))
    restartGameBtn.grid(row = 2, column=0, columnspan=1)

    #Creates Exit button
    quitBtn = Button(endScreenW, text="Exit", command=quit,width=(defaultW*2))
    quitBtn.grid(row = 2, column=1, columnspan=1)

def restartGame():
    global nPlayers, playersName, playerIconlLbl, playerNamelLbl, lastMoveLbl
    
    #Sets global variables to default values
    nPlayers = 2
    playersName = ["","","",""]
    for i in range(4):
        #destroyes player description on root window
        playerIconlLbl[i].destroy()
        playerNamelLbl[i].destroy()

    #destroyes end screen window
    endScreenW.destroy()
    #destroyes turn description lable on root window
    lastMoveLbl.destroy()
    #opens player select windows to start the game again
    openPlayerSelectW()
    
#definitions
root = Tk()
root.title("Sorrier Than Ever")

#opens player select windows to start the game
openPlayerSelectW()

#Tkinter main loop
root.mainloop()