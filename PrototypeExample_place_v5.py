import tkinter as tk
from tkinter import messagebox
import random

LABEL_FONT = ("Verdana", 12)
p2Name = "Player 2"
frames = {}
# the empty board array
board = ["", "", "", "", "", "", "", "", ""]
# all possible win positions
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
# to keep track for ties
flag = 0
# btn True for first player automatically
bclick = True
# game mode set to PvP = 0 automatically, PvC(easy) = 1, PvC(hard) = 2
gameMode = 0
firstPlayerMarker = "X"
secondPlayerMarker = "O"
# global counter variables for player 1 and player 2, used in series
p1_counter = 0
p2_counter = 0
# default marker is "X"
currentPlayerMarker = firstPlayerMarker
# when false, ComputerMode will stop running
gameOn = True
dialog = {
    "WindowTitlePane": "Group 1: Tic-Tac-Toe",
    "TitleScreenLabel": "Welcome to Tic-Tac-Toe",
    "SeriesScreenLabel": "Choose a One-off Game or Play a Series",
    "DifficultyScreenLabel": "Set Computer Opponent Difficulty"
}

def setP1Count(count):
    # increments player 1's win counter for use in series games
    global p1_counter, frames
    count = count + 1
    p1_counter = count

def setP2Count(count):
    # increments player 2's win counter for use in series games
    global p2_counter, frames
    count = count + 1
    p2_counter = count

def getP1Count():
    # returns player 1's win counter
    global p1_counter, frames
    return p1_counter

def getP2Count():
    # returns player 2's win counter
    global p2_counter, frames
    return p2_counter

def resetSeries():
    # resets win counters for player 1 and player 2 upon completion of a series
    global p1_counter, p2_counter
    p1_counter = 0
    p2_counter = 0

def enableNext():
    # re-enables the "Next" after returning to title screen from SeriesGame
    frames[SeriesGame].next_button.config(state=tk.NORMAL)

def endSeries():
    # disables the "Next" button upon completion of a series, so user can only return to title screen
    frames[SeriesGame].next_button.config(state=tk.DISABLED)

def checkSeriesCounter(mode):
    # mode corresponds to the length of the series and is passed in to determine number of wins required
    # called in the "checkForWinner" function after each game so game ends when a series is finished
    # determines if either player has won a majority of games given length of series
    # if either one has, displays a game over message, ends the game and resets the series counter
    global p1_counter, p2_counter, frames, board, gameMode, gameOn, flag, currentPlayerMarker
    if mode == 3:
        if getP1Count() > 1 or getP2Count() > 1:
            if getP1Count() > getP2Count():
                messagebox.showinfo("Series Over", "Player 1 Wins! Final Score: " + str(getP1Count()) + " - " + str(getP2Count()))
                endGame()
                endSeries()
                resetSeries()
            else:
                messagebox.showinfo("Series Over", "Player 2 Wins! Final Score: " + str(getP1Count()) + " - " + str(getP2Count()))
                endGame()
                endSeries()
                resetSeries()
    elif mode == 5:
        if getP1Count() > 2 or getP2Count() > 2:
            if getP1Count() > getP2Count():
                messagebox.showinfo("Series Over", "Player 1 Wins! Final Score: " + str(getP1Count()) + " - " + str(getP2Count()))
                endGame()
                endSeries()
                resetSeries()
            else:
                messagebox.showinfo("Series Over", "Player 2 Wins! Final Score: " + str(getP1Count()) + " - " + str(getP2Count()))
                endGame()
                endSeries()
                resetSeries()
    elif mode == 7:
        if getP1Count() > 3 or getP2Count() > 3:
            if getP1Count() > getP2Count():
                messagebox.showinfo("Series Over", "Player 1 Wins! Final Score: " + str(getP1Count()) + " - " + str(getP2Count()))
                endGame()
                endSeries()
                resetSeries()
            else:
                messagebox.showinfo("Series Over", "Player 2 Wins! Final Score: " + str(getP1Count()) + " - " + str(getP2Count()))
                endGame()
                endSeries()
                resetSeries()

def resetDefaults():
    # resets the board to all default values to be used again
    # called when "Return to title screen" button is pressed and when "Next game" button is pressed in series
    global board, currentPlayerMarker, flag, bclick, gameMode, gameOn
    board = ["", "", "", "", "", "", "", "", ""]
    for btn in frames[GameScreen].btns:
        btn.config(text=" ", state=tk.NORMAL)
    for btn in frames[SeriesGame].btns:
        btn.config(text=" ", state=tk.NORMAL)
    currentPlayerMarker = firstPlayerMarker
    flag = 0
    bclick = True
    gameOn = True

def resetGameMode():
    # resets the game mode to default (0)
    global gameMode
    gameMode = 0

class PlainButton(tk.Button):
    # button class for non-game buttons and labels
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.config(width=20, relief="raised", font=("Sitka", 12))

    def setPlayerLabels(self, name):
        global frames, p1_counter, p2_counter, gameMode
        frames[GameScreen].playerLabels[0].config(text="Player 1")
        frames[GameScreen].playerLabels[1].config(text=name)
        frames[SeriesGame].playerLabels[0].config(text="Player 1")
        frames[SeriesGame].playerLabels[1].config(text=name)

class GameButton(tk.Button):
    # button class for game buttons which populate the 3x3 grid
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.config(width=1, height=1, text="none", borderwidth=1, font=("Verdana", 48))
        value = 0
        self.pos = ""

    def onClick(self):
        #when the buttons are clicked then the markers are placed in the empty cell. Checks to make sure the cells are empty and who's
        #turn it is.
        #first player is always bClick = True
        #second player is always bclick = False
        global bclick, currentPlayerMarker, flag, p1_counter, p2_counter

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

class CurrentTheme:
    # fonts and colors used for the GUI
    font = {
        "f1": "Palatino Linotype",
        "f2": "Arial",
        "f3": "Helvetica"
    }

    fontSize = {
        "fs1": "8",
        "fs2": "10",
        "fs3": "18"
    }

    bgColor = {
        "bg1": "#7debd9",
        "bg2": "#37474f",
        "bg3": "#1fb299"
    }

    fgColor = {
        "fg1": "#4da6ff",
        "fg2": "#99ffdd",
        "fg3": "#ff8080"
    }

class GameApp(tk.Tk):
    # the main game app which generates and configures the game window and all frames
    global frames
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, dialog.get("WindowTitlePane"))
        window = tk.Frame(self)

        self.geometry("480x600+200+200")
        self.minsize(480, 600)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # loop through all level frames, add them to the dictionary
        for F in (TitleScreen, GameScreen, DifficultyScreen, SeriesScreen, SeriesGame):
            frame = F(window, self)
            frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(TitleScreen)

    # Show the appropriate level/screen
    def showFrame(self, cont):
        frame = frames[cont]
        frame.tkraise()

    def quit(self):
        self.destroy()

class TitleScreen(tk.Frame):
    # Title Screen for the game
    # allows user to select a game mode (PvP or PvC) and transitions to next frame accordingly
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg1")
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))
        self.config(bg=bgColor)

        self.lbls = [tk.Label(self) for i in range(1)]
        for i in range(1):
            self.lbls[i].config(font=titleFont, bg=bgColor)
            self.lbls[i].place(relx=0.5, rely=0.08, anchor="center")

        self.btns = [PlainButton(self) for i in range(4)]
        for i in range(3):
            self.btns[i].config(text="text: " + str(i))
            self.btns[i].place(relx=0.5, rely=0.4 + (0.08 * i), anchor="center")

        TS_lbl = self.lbls[0]
        TS_lbl.config(text=dialog.get("TitleScreenLabel"))

        GameVsP_btn = self.btns[0]
        GameVsP_btn.config(text="VS Player", command=lambda: [controller.showFrame(SeriesScreen), GameVsP_btn.setPlayerLabels("Player 2")])

        GameVsC_btn = self.btns[1]
        GameVsC_btn.config(text="VS Computer", command=lambda: [controller.showFrame(DifficultyScreen), GameVsC_btn.setPlayerLabels("Computer")])

        Quit_btn = self.btns[2]
        Quit_btn.place(rely=.72)
        Quit_btn.config(text="Quit", command=quit)

def setGameMode(mode):
    # sets the game mode
    # 0 = one-off, 1 = easy computer opponent, 2 = hard computer opponent, 3 = best-of-three series, 5 = best-of-five series, 7 = best-of-seven series
    global gameMode
    gameMode = mode

def getGameMode():
    # returns the game mode
    global gameMode
    return gameMode

def changePlayerMarker():
    # changes the current player marker from X to O or vice versa.
    # also checks if it is computer turn and if so then calls easyComputerMode()
    global currentPlayerMarker

    if currentPlayerMarker == firstPlayerMarker:
        marker = secondPlayerMarker
    elif currentPlayerMarker == secondPlayerMarker:
        marker = firstPlayerMarker

    currentPlayerMarker = marker

def easyComputerMode():
    # easy mode(completed)
    # checks to make sure gameOn is true, then continuously loops through the board with randomly chosen cells till it finds another
    global frames, bclick, gameOn, board, flag
    if(gameOn):
        isItCompTurn = True
        while(isItCompTurn):
            randomChosenCell = random.randint(0, 8)
            if board[randomChosenCell] == "":
                # place the marker at the determined cell
                frames[GameScreen].btns[randomChosenCell + 1].config(text=currentPlayerMarker)
                updateBoard(randomChosenCell)
                isItCompTurn = False
                # so the opponent can begin to make a move
                bclick = True
                flag += 1
                continueGameOrEnd()

def hardComputerMode():
    # first, computer will check if the middle space is free(best space for more possible win patterns)
    # if not, then it will check if there is a cell where, if it placed its marker in that cell, will that cell return true for
    # checkForWinner(). It does so by creating a tempBoard that is a replica of the global board array, and it will go through each empty
    # element and place a marker there and use checkForWinner() on the tempBoard. If there is a winning position then the marker will be placed there
    # on the board array and on the actual visual board.
    # if there is winning position for the computer, then it checks if the opponent has a possible winning by doing the same thing, but
    # checks with the opponents marker instead. If it finds a spot where the opponent will win, then the computer will place its marker
    # there to prevent the opponent from winning
    global frames, bclick, gameOn, board, currentPlayerMarker, flag
    if(gameOn):
        isItCompTurn = True
        # constantly check for the best cell to click
        while(isItCompTurn):
            computerMoveTracker = 0

            # to check if the computer has made any moves yet, if not try and place a marker in the middle(best position)
            for i in board:
                if i == currentPlayerMarker:
                    computerMoveTracker += 1
            if computerMoveTracker == 0 and board[4] == "":
                frames[GameScreen].btns[5].config(text=currentPlayerMarker)
                updateBoard(4)
                # so the opponent can begin to make a move
                bclick = True
                flag += 1
                break

            # check if computer has a winning move
            for i in range(len(board)):
                # skipping over the non empty index's in board array
                if board[i] != "":
                    continue

                # duplicate the global array board
                tempBoard = board.copy()
                # place a marker in the tempboard
                tempBoard[i] = currentPlayerMarker
                if checkForWinner(tempBoard, currentPlayerMarker):
                    isItCompTurn = False
                    # place the marker at the determined cell
                    frames[GameScreen].btns[i + 1].config(text=currentPlayerMarker)
                    updateBoard(i)
                    # so the opponent can begin to make a move
                    bclick = True
                    flag += 1
                    break

            # if there was a winning spot found, break out of the while loop
            if isItCompTurn == False:
                break

            # check if the opponent has a winning move, if so place our marker there
            for i in range(len(board)):
                # skipping over the non empty index's in board array
                if board[i] != "":
                    continue

                tempBoard = board.copy()
                tempBoard[i] = firstPlayerMarker
                if checkForWinner(tempBoard, firstPlayerMarker):
                    isItCompTurn = False
                    # place the marker at the determined cell
                    frames[GameScreen].btns[i + 1].config(text=currentPlayerMarker)
                    updateBoard(i)
                    # so the opponent can begin to make a move
                    bclick = True
                    flag += 1
                    break

            # if there was a spot to prevent opponent from winning found, break out of the while loop
            if isItCompTurn == False:
                break

            # if theres no other best spot, pick a random one
            randomChosenCell = random.randint(0, 8)
            if board[randomChosenCell] == "":
                frames[GameScreen].btns[randomChosenCell + 1].config(text=currentPlayerMarker)
                updateBoard(randomChosenCell)
                isItCompTurn = False
                bclick = True
                flag += 1

        continueGameOrEnd()

def checkTie():
    # checks to see if all the cells are filled
    # also disables the buttons so they are no longer clickable in both PvP and PvC
    # can be edited(or discarded) if need to, just needed to make sure the buttons were disabling after the board was filled
    global flag
    if flag == 9:
        messagebox.showinfo("Game Over", "It's a Tie")
        return True
    return False

def endGame():
    # disables the buttons from being clickable
    # sets gameOn as false to prevent computerModes from running
    global gameOn
    gameOn = False
    for i in range(10):
        frames[GameScreen].btns[i].config(state=tk.DISABLED)
        frames[SeriesGame].btns[i].config(state=tk.DISABLED)

def checkForWinner(board, marker):
    # checking for a win by comparing the winPositions array to the board array and the specified index elements and checks if the markers are
    # the same to each other
    # It is required to pass in what board to check and what marker to check for because it is possible to check a duplicate of the
    # main board in hardComputerMode() and hardComputerMode() checks if both X or O win.
    global winPositions, p1_counter, p2_counter
    for i in winPositions:
        position1 = i[0]
        position2 = i[1]
        position3 = i[2]
        if board[position1] == marker and board[position2] == marker and board[position3] == marker:
            return True
    return False

def checkComputerGameMode():
    # used for computer mode to determine which mode to play
    # if it is not computer mode then this function will not run and PvP will run normally
    global gameMode, currentPlayerMarker, gameOn
    gameMode = getGameMode()
    # Easy PvC
    if gameMode == 1 and currentPlayerMarker == secondPlayerMarker and gameOn == True:
        easyComputerMode()
    # Hard PvC
    if gameMode == 2 and currentPlayerMarker == secondPlayerMarker and gameOn == True:
        hardComputerMode()

def updateBoard(index):
    # to maintain/keep track of the cells that are clicked
    # needed for checkForWinner() and ComputerMode() functions
    global currentPlayerMarker, board
    if board[index] == "":
        board[index] = currentPlayerMarker

def continueGameOrEnd():
    # this function is meant for the code to be more organized
    # it checks for a winner or a Tie and if there is then end the game
    # if not then change the player's marker and check if its computer mode
    # modified to display all game results message boxes and corresponding series messages
    # also calls checkSeriesCounter to check series progress if applicable
    global p1_counter, p2_counter, gameMode
    if checkForWinner(board, currentPlayerMarker):
        endGame()
        if currentPlayerMarker == "X":
            messagebox.showinfo("Game Over", "Player 1 Wins")
            if gameMode > 2:
                setP1Count(p1_counter)
                messagebox.showinfo("Series Progress", "Current score: " + str(getP1Count()) + " - " + str(getP2Count()))
                checkSeriesCounter(getGameMode())
        else:
            if gameMode == 1 or gameMode == 2:
                messagebox.showinfo("Game Over", "Computer opponent wins")
            else:
                messagebox.showinfo("Game Over", "Player 2 Wins")
            if gameMode > 2:
                setP2Count(p2_counter)
                messagebox.showinfo("Series Progress", "Current score: " + str(getP1Count()) + " - " + str(getP2Count()))
                checkSeriesCounter(getGameMode())
    elif checkTie():
        endGame()
    changePlayerMarker()
    checkComputerGameMode()

class GameScreen(tk.Frame):
    # the game screen used in PvC games and one-off PvP games
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg2")
        bgColorLabels = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        self.playerLabels = [tk.Label(self, font=titleFont, bg=bgColorLabels, borderwidth=2, relief="sunken", padx=3, pady=3) for i in range(2)]
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

            btn[i].config(text=' ', command=lambda c=i: [updateBoard(c - 1), btn[c].onClick()])
            btn[i].place(relx=(columnOffset*0.2)+.3, rely=(rowOffset*0.2)+.42, anchor="center", relheight=0.2, relwidth=0.2)

        back_button = PlainButton(self, text="Back to Title Screen", command=lambda: [resetDefaults(), resetGameMode(), controller.showFrame(TitleScreen)])
        back_button.place(relx=0.5, rely=0.2, anchor="center")

class SeriesGame(tk.Frame):
    # the game screen used in PvP series games
    def __init__(self, parent, controller):
        global p1_counter, p2_counter
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg2")
        bgColorLabels = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        self.playerLabels = [tk.Label(self, font=titleFont, bg=bgColorLabels, borderwidth=2, relief="sunken", padx=3, pady=3) for i in range(2)]

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

            btn[i].config(text=' ', command=lambda c=i: [updateBoard(c - 1), btn[c].onClick()])
            btn[i].place(relx=(columnOffset*0.2)+.3, rely=(rowOffset*0.2)+.42, anchor="center", relheight=0.2, relwidth=0.2)

        back_button = PlainButton(self, text="Back to Title Screen", command=lambda: [resetDefaults(), resetGameMode(), enableNext(), controller.showFrame(TitleScreen)])
        back_button.place(relx=0.5, rely=0.16, anchor="center")

        self.next_button = PlainButton(self, text="Next Game", command=lambda: [resetDefaults()])
        self.next_button.place(relx=0.5, rely=0.24, anchor="center")

class SeriesScreen(tk.Frame):
    # screen shown when PvP is selected at Title Screen
    # allows user to select one-off or series game, and length of series if chosen
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        label = tk.Label(self, text=dialog.get("SeriesScreenLabel"), font=titleFont, bg=bgColor)
        label.place(relx=0.5, rely=0.08, anchor="center")

        one_button = PlainButton(self, text="One-Off", command=lambda: [controller.showFrame(GameScreen), setGameMode(0)])
        one_button.place(relx=0.5, rely=0.32, anchor="center")

        three_button = PlainButton(self, text="Best-of-Three", command=lambda: [controller.showFrame(SeriesGame), setGameMode(3)])
        three_button.place(relx=0.5, rely=0.4, anchor="center")

        five_button = PlainButton(self, text="Best-of-Five", command=lambda: [controller.showFrame(SeriesGame), setGameMode(5)])
        five_button.place(relx=0.5, rely=0.48, anchor="center")

        seven_button = PlainButton(self, text="Best-of-Seven", command=lambda: [controller.showFrame(SeriesGame), setGameMode(7)])
        seven_button.place(relx=0.5, rely=0.56, anchor="center")

        back_button = PlainButton(self, text="Back to Title Screen", command=lambda: [resetDefaults(), resetGameMode(), controller.showFrame(TitleScreen)])
        back_button.place(relx=0.5, rely=0.72, anchor="center")

class DifficultyScreen(tk.Frame):
    # screen shown when PvC is selected at Title Screen
    # allows user to set difficulty of computer opponent to easy or hard
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        label = tk.Label(self, text=dialog.get("DifficultyScreenLabel"), font=titleFont, bg=bgColor)
        label.place(relx=0.5, rely=0.08, anchor="center")

        easy_button = PlainButton(self, text="Easy", command=lambda: [controller.showFrame(GameScreen), setGameMode(1)])
        easy_button.place(relx=0.5, rely=0.32, anchor="center")

        hard_button = PlainButton(self, text="Hard", command=lambda: [controller.showFrame(GameScreen), setGameMode(2)])
        hard_button.place(relx=0.5, rely=0.4, anchor="center")

        back_button = PlainButton(self, text="Back to Title Screen", command=lambda: [resetDefaults(), resetGameMode(), controller.showFrame(TitleScreen)])
        back_button.place(relx=0.5, rely=0.72, anchor="center")

app = GameApp()
app.mainloop()
