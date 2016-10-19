import tkinter as tk
from tkinter import simpledialog
import math
from PIL import Image, ImageTk
import pickle
import os

class View(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.frame.bind('<Enter>', self.bound_to_mousewheel)
        self.frame.bind('<Leave>', self.unbound_from_mousewheel)

        self.populate()

    def populate(self):
        self.buttons = []
        global chests
        try:
            chests = pickle.load(open("users/" + currentUser + ".txt", "rb"))
        except IOError:
            self.buttons = self.populateFresh()
        except EOFError:
            self.buttons = self.populateFresh()
        else:
            self.populateContinue()

    def populateFresh(self):
        buttons = []
        global chests
        for name in champions:
            name = self.getInternalName(name)
            buttons += [Champion(name, False)]
            chests += [[name, False]] 

        length = math.ceil(len(buttons) / 10)
        total = len(buttons)
        for row in range(length):
            for col in range(10):
                if row * 10 + col < total:
                    buttons[row * 10 + col].show(self.frame, row, col)
        return buttons

    def getInternalName(self, name):
        if name == "Wukong":
            name = "MonkeyKing"
        if name.find(" ") > 0:
            name = name.replace(" ", "")
        if name.find("'") > 0:
            name = name.replace("'", "")
        if name.find(".") > 0:
            name = name.replace(".", "")
        return name

    def populateContinue(self):
        buttons = []
        foundAtLeastOneNewChampion = False
        if len(champions) > len(chests):
            for champ in champions:
                found = False
                tempName = self.getInternalName(champ)
                for chest in chests:
                    if tempName == chest[0]:
                        found = True
                if not found:
                    #print(champ)
                    foundAtLeastOneNewChampion = True
                    chests.append([tempName, False])

        if foundAtLeastOneNewChampion:
            chests.sort()

        for chest in chests:
            buttons += [Champion(chest[0], chest[1])]
        length = math.ceil(len(buttons) / 10)
        total = len(buttons)
        for row in range(length):
            for col in range(10):
                if row * 10 + col < total:
                    buttons[row * 10 + col].show(self.frame, row, col)
        return buttons

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)   

    def unbound_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>") 

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class Champion:
    def __init__(self, name, chest):
        self.name = name
        self.chest = chest
        self.image = Image.open("C:\\Riot Games\\League of Legends\\RADS\\projects\\lol_air_client\\releases\\" + imagesVersion + "\\deploy\\assets\\images\\champions\\" + name + "_Square_0.png")
        self.frameImg = Image.open("frame.png")
        size = 96, 96
        self.image.thumbnail(size)
        self.img = ImageTk.PhotoImage(self.image.convert("LA"))
    def show(self, master, r, c):
        self.button = tk.Button(master, justify = tk.LEFT, command = self.update)
        self.button.config(bd = 0)
        if self.chest:
            self.chest = False #work around
            #print(self.name)
            self.update()
        else:
            self.button.config(image = self.img, width = "106", height = "106")
        #self.button.pack()
        self.button.grid(row = r, column = c)
    def update(self):
        global chests
        self.chest = not self.chest
        if self.chest:
            self.imageFramed = self.image.copy()
            self.imageFramed.paste(self.frameImg, (0, 0), self.frameImg)
            #self.imageFramed = Image.alpha_composite(self.image, self.frameImg)
            self.img = ImageTk.PhotoImage(self.imageFramed)
            self.button.config(image = self.img, width = "106", height = "106")
        else:
            self.img = ImageTk.PhotoImage(self.image.convert("LA"))
            self.button.config(image = self.img, width = "106", height = "106")
        for pair in chests:
            if pair[0] == self.name:
                pair[1] = self.chest
        #print(self.name + " chest status: " + str(self.chest))
        pickle.dump(chests, open("users/" + currentUser + ".txt", "wb"))

def selectUser(self):
    global currentUser, listbox
    currentUser = listbox.get(listbox.curselection()[0])
    #print(currentUser)
    rootSelect.destroy()

def deleteUser():
    currentUser = listbox.get(listbox.curselection()[0])
    os.remove("users/" + currentUser + ".txt")
    listbox.delete(tk.ANCHOR)

def newUser():
    new = simpledialog.askstring("Input name", "New user name")
    #print(new)
    open("users/" + new + ".txt", 'a').close()
    listbox.insert(tk.END, new)
    
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

if __name__ == "__main__":
    version = "0.9 (alpha)"
    #imagesVersion = "0.0.1.220"
    imagesVersion = os.listdir('C:/Riot Games/League of Legends/RADS/projects/lol_air_client/releases')[-1]
    chests = []
    champions = ["Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Ashe", "Aurelion Sol", "Azir", "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Nidalee", "Nocturne", "Nunu", "Olaf", "Orianna", "Pantheon", "Poppy", "Quinn", "Rammus", "Rek'Sai", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xerath", "Xin Zhao", "Yasuo", "Yorick", "Zac", "Zed", "Ziggs", "Zilean", "Zyra"]        
    currentUser = ""
    rootSelect = tk.Tk()
    rootSelect.title("Select user")
    listbox = tk.Listbox(rootSelect)
    listbox.bind("<Double-Button-1>", selectUser)
    listbox.grid(row = 0, column = 0, columnspan = 2, sticky=tk.W+tk.E+tk.N+tk.S, padx = 10)
    #listbox.pack()

    users = os.listdir("Users")
    for user in users:
        x = user.split(".")
        listbox.insert(tk.END, x[0])
    #print(users)

    newUser = tk.Button(rootSelect, text = "Add user", command = newUser).grid(row = 1, column = 0)
    deleteUser = tk.Button(rootSelect, text = "Delete user", command = deleteUser).grid(row = 1, column = 1)
    center(rootSelect)
    rootSelect.mainloop()
    
    if currentUser != "":
        root=tk.Tk()
        root.title("Champion Chests - " + currentUser + " - v " + version)
        root.minsize(110 * 10, 600)
        root.maxsize(110 * 10, 6000)

        View(root).pack(side="top", fill="both", expand=True)
        root.mainloop()
        #print(chests)
