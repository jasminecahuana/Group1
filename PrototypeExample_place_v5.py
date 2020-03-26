import tkinter as tk

LABEL_FONT = ("Verdana", 12)
p2Name = "Player 2"
frames = {}
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
        self.value += 1
        self["text"] = str(self.pos) + "\nvalue: " + str(self.value)

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
        for i in range(4):
            self.btns[i].config(text="text: " + str(i))
            self.btns[i].place(relx=0.5, rely=0.3 + (0.05 * i), anchor="center")

        TS_lbl = self.lbls[0]
        TS_lbl.config(text=dialog.get("TitleScreenLabel"))

        GameVsP_btn = self.btns[0]
        GameVsP_btn.config(text="VS Player", command=lambda: [controller.showFrame(GameScreen), GameVsP_btn.setPlayerLabels("Player 2")])

        GameVsC_btn = self.btns[1]
        GameVsC_btn.config(text="VS Computer", command=lambda: [controller.showFrame(GameScreen), GameVsC_btn.setPlayerLabels("Computer")])

        Options_btn = self.btns[2]
        Options_btn.config(text="Options", command=lambda: [controller.showFrame(OptionsScreen)])

        Quit_btn = self.btns[3]
        Quit_btn.config(text="Quit", command=quit)

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

            btn[i].value = 0
            btn[i].pos = "cell: " + str(i)
            btn[i].config(text=btn[i].pos + "\nvalue: " + str(btn[i].value), command=lambda c=i: btn[c].onClick())
            btn[i].place(relx=(columnOffset*0.2)+.3, rely=(rowOffset*0.2)+.4, anchor="center", relheight=0.2, relwidth=0.2)

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

        three_button = PlainButton(self, text="Best-of-three", command=lambda: controller.showFrame(OptionsScreen))
        three_button.place(relx=0.5, rely=0.3, anchor="center")

        five_button = PlainButton(self, text="Best-of-five", command=lambda: controller.showFrame(OptionsScreen))
        five_button.place(relx=0.5, rely=0.35, anchor="center")

        seven_button = PlainButton(self, text="Best-of-seven", command=lambda: controller.showFrame(OptionsScreen))
        seven_button.place(relx=0.5, rely=0.4, anchor="center")

class DifficultyScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bgColor = CurrentTheme.bgColor.get("bg3")
        self.config(bg=bgColor)
        titleFont = (CurrentTheme.font.get("f1"), CurrentTheme.fontSize.get("fs3"))

        label = tk.Label(self, text=dialog.get("DifficultyScreenLabel"), font=titleFont, bg=bgColor)
        label.place(relx=0.5, rely=0.5, anchor="center")

        easy_button = PlainButton(self, text="Easy", command=lambda: controller.showFrame(OptionsScreen))
        easy_button.place(relx=0.5, rely=0.3, anchor="center")

        hard_button = PlainButton(self, text="Hard", command=lambda: controller.showFrame(OptionsScreen))
        hard_button.place(relx=0.5, rely=0.35, anchor="center")

app = GameApp()
app.mainloop()
