import tkinter as tk
import tkinter.messagebox
import random

LABEL_FONT = ("Verdana", 12)
p2Name = "Player 2"
frames = {}
board = ["", "", "", "", "", "", "", "", ""]
winPositions = [
    [0, 1, 2],
    [0, 3, 6],
    [0, 4, 8],
    [2, 5, 8],
    [2, 4, 6],
    [6, 7, 8],
    [3, 4, 5],
    [1, 4, 7]
]
flag = 0 #to keep track for ties
bclick = True #btn True for first player automatically
gameMode = 0 #game mode set to PvP = 0 automatically, PvC(easy) = 1, PvC(hard) = 2
firstPlayerMarker = "X"
secondPlayerMarker = "O"
currentPlayerMarker = firstPlayerMarker
gameOn = True #when false, ComputerMode will stop running
dialog = {
    "WindowTitlePane": "Group 1: Tic Tac Toe",
    "TitleScreenLabel": "Here is the Title Screen for our game",
    "OptionScreenLabel": "Here is the Options window",
    "SeriesScreenLabel": "Play a Series",
    "DifficultyScreenLabel": "Set computer opponent difficulty"
}

class PlainButton(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.config(width=30, relief="ridge")

    def setPlayerLabels(self, name):
        global frames
        frames[GameScreen].playerLabels[0].config(text="Player 1")
        frames[GameScreen].playerLabels[1].config(text=name)

class GameButton(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.config(width=1, height=1, text="none", borderwidth=1)
        value = 0
        pos = "none"

    def onClick(self):
        #when the buttons are clicked then the markers are placed in the empty cell. Checks to make sure the cells are empty and who's
        #turn it is.
        #first player is always bClick = True
        #second player is always bclick = False
        global bclick, currentPlayerMarker, flag
        # self.value += 1
        # self["text"] = str(self.pos) + "\nvalue: " + str(self.value)
        if self["text"] == " " and bclick == True:
            self["text"] = currentPlayerMarker
            bclick = False
            flag +=1
            continueGameOrEnd()
        elif self["text"] == " " and bclick == False:
            self["text"] = currentPlayerMarker
            bclick = True
            flag +=1
            continueGameOrEnd()
        
#!!!Not implemented yet
class CurrentTheme:
    font = {
        "f1": "Verdana",
        "f2": "Arial",
        "f3": "Helvetica"
    }

    fontSize = {
        "fs1": "8",
        "fs2": "10",
        "fs3": "12"
    }
    bgColor = {
        "bg1": "#4da6ff",
        "bg2": "#99ffdd",
        "bg3": "#ff8080"
    }

    fgColor = {
        "fg1": "#4da6ff",
        "fg2": "#99ffdd",
        "fg3": "#ff8080"
    }

class GameApp(tk.Tk):
    global frames
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, dialog.get("WindowTitlePane"))
        window = tk.Frame(self)

        self.geometry("480x600+200+200")
        self.minsize(480, 600)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        #loop through all level frames, add them to the dictionary
        for F in (TitleScreen, GameScreen, OptionsScreen, DifficultyScreen, SeriesScreen):
            frame = F(window, self)
            frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(TitleScreen)

    #Show the appropriate level/screen
    def showFrame(self, cont):
        frame = frames[cont]
        frame.tkraise()

    def quit(self):
        self.destroy()

class TitleScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg1")
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))
        self.config(bg=bgColor)

        self.lbls = [tk.Label(self) for i in range(1)]
        for i in range(1):
            self.lbls[i].config(font=titleFont, bg=bgColor)
            self.lbls[i].place(relx=0.5, rely=0.05, anchor="center")

        self.btns = [PlainButton(self) for i in range(4)]
        for i in range(3):
            self.btns[i].config(text="text: " + str(i))
            self.btns[i].place(relx=0.5, rely=0.3 + (0.05 * i), anchor="center")

        TS_lbl = self.lbls[0]
        TS_lbl.config(text=dialog.get("TitleScreenLabel"))

        GameVsP_btn = self.btns[0]
        GameVsP_btn.config(text="VS Player", command=lambda: [controller.showFrame(SeriesScreen), GameVsP_btn.setPlayerLabels("Player 2"), setGameMode(0)])

        GameVsC_btn = self.btns[1]
        GameVsC_btn.config(text="VS Computer", command=lambda: [controller.showFrame(DifficultyScreen), GameVsC_btn.setPlayerLabels("Computer")])

        Quit_btn = self.btns[2]
        Quit_btn.config(text="Quit", command=quit)

def setGameMode(mode):
    global gameMode
    gameMode = mode

def getGameMode():
    global gameMode
    return gameMode

def changePlayerMarker():
    #changes the current player marker from X to O or vice versa.
    #also checks if it is computer turn and if so then calls easyComputerMode()
    global currentPlayerMarker
    
    if currentPlayerMarker == firstPlayerMarker:
        marker = secondPlayerMarker
    elif currentPlayerMarker == secondPlayerMarker:
        marker = firstPlayerMarker
    
    currentPlayerMarker = marker
    
def easyComputerMode(): 
    #easy mode(completed)
    #checks to make sure gameOn is true, then continuously loops through the board with randomly chosen cells till it finds another
    global frames, bclick, gameOn, board, flag
    if(gameOn):
        isItCompTurn = True
        while(isItCompTurn):
            randomChosenCell = random.randint(0, 8) 
            if board[randomChosenCell] == "":
                frames[GameScreen].btns[randomChosenCell + 1].config(text=currentPlayerMarker)
                updateBoard(randomChosenCell)
                isItCompTurn = False
                bclick = True
                flag += 1
                continueGameOrEnd()

def hardComputerMode():
    #first, computer will check if the middle space is free(best space for more possible win patterns)
    #if not, then it will check if there is a cell where, if it placed its marker in that cell, will that cell return true for 
    #checkForWinner(). It does so by creating a tempBoard that is a replica of the global board array, and it will go through each empty
    #element and place a marker there and use checkForWinner() on the tempBoard. If there is a winning position then the marker will be placed there
    #on the board array and on the actual visual board. 
    #if there is winning position for the computer, then it checks if the opponent has a possible winning by doing the same thing, but
    #checks with the opponents marker instead. If it finds a spot where the opponent will win, then the computer will place its marker
    #there to prevent the opponent from winnnig
    global frames, bclick, gameOn, board, currentPlayerMarker, flag
    if(gameOn):
        isItCompTurn = True
        while(isItCompTurn): #constantly check for the best cell to click
            computerMoveTracker = 0

            for i in board: #to check if the computer has made any moves yet, if not try and place a marker in the middle(best position)
                if i == currentPlayerMarker:
                    computerMoveTracker += 1
            if computerMoveTracker == 0 and board[4] == "": 
                frames[GameScreen].btns[5].config(text=currentPlayerMarker)
                updateBoard(4)
                bclick = True
                flag += 1
                break

            for i in range(len(board)):#check if computer has a winning move
                if board[i] != "":
                    continue

                tempBoard = board.copy()
                tempBoard[i] = currentPlayerMarker
                if checkForWinner(tempBoard, currentPlayerMarker):
                    isItCompTurn = False
                    frames[GameScreen].btns[i + 1].config(text=currentPlayerMarker)
                    updateBoard(i)
                    bclick = True
                    flag += 1
                    break

            if isItCompTurn == False: #if there was a winning spot found, break out of the while loop
                break

            for i in range(len(board)):#check if the opponent has a winning move, if so place our marker there
                if board[i] != "":
                    continue

                tempBoard = board.copy()
                tempBoard[i] = firstPlayerMarker
                if checkForWinner(tempBoard, firstPlayerMarker):
                    isItCompTurn = False
                    frames[GameScreen].btns[i +1].config(text=currentPlayerMarker)
                    updateBoard(i)
                    bclick = True
                    flag += 1
                    break

            if isItCompTurn == False: #if there was a spot to prevent opponent from winning found, break out of the while loop
                break

            randomChosenCell = random.randint(0, 8) #if theres no other best spot, pick a random one
            if board[randomChosenCell] == "":
                frames[GameScreen].btns[randomChosenCell + 1].config(text=currentPlayerMarker)
                updateBoard(randomChosenCell)
                isItCompTurn = False
                bclick = True
                flag += 1
                
        continueGameOrEnd()
            
def checkTie(): 
    #checks to see if all the cells are filled
    #also disables the buttons so they are no longer clickable in both PvP and PvC
    #can be edited(or discarded) if need to, just needed to make sure the buttons were disabling after the board was filled
    global flag
    if flag == 9:
        print("Tie game")
        return True
    return False

def endGame():
    #disables the buttons from being clickable
    #sets gameOn as false to prevent computerModes from running
    global gameOn
    gameOn = False
    for i in range(10):
        frames[GameScreen].btns[i].config(state=tk.DISABLED)

def checkForWinner(board, marker):
    #checking for a win by comparing the winPositions array to the board array and the specified index elements and checks if the markers are
    #the same to each other
    #It is required to pass in what board to check and what marker to check for because it is possible to check a duplicate of the 
    #main board in hardComputerMode() and hardComputerMode() checks if both X or O win.
    global winPositions
    for i in winPositions:
        position1 = i[0]
        position2 = i[1]
        position3 = i[2]
        if board[position1] == marker and board[position2] == marker and board[position3] == marker:
            print("Winner " + marker)
            return True
    return False

def checkComputerGameMode():
    #used for computer mode to determine which mode to play
    #if it is not computer mode then this function will not run and PvP will run normally
    global gameMode, currentPlayerMarker, gameOn
    gameMode = getGameMode()
    if gameMode == 1 and currentPlayerMarker == secondPlayerMarker and gameOn == True: #Easy PvC
        easyComputerMode()
    if gameMode == 2 and currentPlayerMarker == secondPlayerMarker and gameOn == True: #Hard PvC
        hardComputerMode()

def updateBoard(index): 
    #to maintain/keep track of the cells that are clicked 
    #needed for checkForWinner() and ComputerMode() functions
    global currentPlayerMarker, board
    if board[index] == "":
        board[index] = currentPlayerMarker

def continueGameOrEnd():
    #this function is meant for the code to be more organized
    #it checks for a winner or a Tie and if there is then end the game
    #if not then change the player's marker and check if its computer mode.
    if checkForWinner(board, currentPlayerMarker) or checkTie():
        endGame()
    changePlayerMarker()
    checkComputerGameMode()

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg2")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        self.playerLabels = [tk.Label(self, font=titleFont, bg=bgColor) for i in range(2)]
        for i in range(2):
            self.playerLabels[i].place(rely=0)
            if i == 0:
                self.playerLabels[i].place(relx=0, anchor="nw")
            else:
                self.playerLabels[i].place(relx=1, anchor="ne")

        self.btns = [GameButton(self) for i in range(10)]
        for i in range(10):
            btn = self.btns
            rowOffset = int((i-1)/3)
            columnOffset= int((i-1)%3)

            # btn[i].value = 0
            # btn[i].pos = "cell: " + str(i)
            btn[i].config(text=' ', command=lambda c=i: [updateBoard(c - 1), btn[c].onClick()])
            btn[i].place(relx=(columnOffset*0.2)+.3, rely=(rowOffset*0.2)+.4, anchor="center", relheight=0.2, relwidth=0.2)

        back_button = PlainButton(self, text="Back to title screen", command=lambda: controller.showFrame(TitleScreen))
        back_button.place(relx=0.5, rely=0.2, anchor="center")

class OptionsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        label = tk.Label(self, text=dialog.get("OptionScreenLabel"), font=titleFont, bg=bgColor)
        label.place(relx=0.5, rely=0.05, anchor="center")

        button = PlainButton(self, text="Go back to the Title Screen", command=lambda: controller.showFrame(TitleScreen))
        button.place(relx=0.5, rely=0.3, anchor="center")

        diff_button = PlainButton(self, text="Set difficulty for computer opponent", command=lambda: controller.showFrame(DifficultyScreen))
        diff_button.place(relx=0.5, rely=0.35, anchor="center")

        series_button = PlainButton(self, text="Play a series", command=lambda: controller.showFrame(SeriesScreen))
        series_button.place(relx=0.5, rely=0.4, anchor="center")

class SeriesScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        label = tk.Label(self, text=dialog.get("SeriesScreenLabel"), font=titleFont, bg=bgColor)
        label.place(relx=0.5, rely=0.5, anchor="center")

        three_button = PlainButton(self, text="Best-of-three", command=lambda: controller.showFrame(GameScreen))
        three_button.place(relx=0.5, rely=0.3, anchor="center")

        five_button = PlainButton(self, text="Best-of-five", command=lambda: controller.showFrame(GameScreen))
        five_button.place(relx=0.5, rely=0.35, anchor="center")

        seven_button = PlainButton(self, text="Best-of-seven", command=lambda: controller.showFrame(GameScreen))
        seven_button.place(relx=0.5, rely=0.4, anchor="center")

        back_button = PlainButton(self, text="Back to title screen", command=lambda: controller.showFrame(TitleScreen))
        back_button.place(relx=0.5, rely=0.45, anchor="center")

class DifficultyScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        label = tk.Label(self, text=dialog.get("DifficultyScreenLabel"), font=titleFont, bg=bgColor)
        label.place(relx=0.5, rely=0.5, anchor="center")

        easy_button = PlainButton(self, text="Easy", command=lambda: [controller.showFrame(GameScreen), setGameMode(1)])
        easy_button.place(relx=0.5, rely=0.3, anchor="center")

        hard_button = PlainButton(self, text="Hard", command=lambda: [controller.showFrame(GameScreen), setGameMode(2)])
        hard_button.place(relx=0.5, rely=0.35, anchor="center")

        back_button = PlainButton(self, text="Back to title screen", command=lambda: controller.showFrame(TitleScreen))
        back_button.place(relx=0.5, rely=0.4, anchor="center")

app = GameApp()
app.mainloop()