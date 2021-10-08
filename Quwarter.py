from tkinter import *
from math import ceil, fabs
from time import sleep
from random import randint
import pickle
import images

font = ("Comic Sans MS",20)
smallfont = ("Comic Sans MS",18)
tinyfont = ("Comic Sans MS",10)
largefont = ("Comic Sans Ms",50)

class quwarter():

    red = "#FF0000"
    blue = "#0000FF"
    green = "#00FF00"
    yellow = "#FFFF00"

    
    teamlist = []
    baselist = []
    trooplist = []
    boardlist = [[None for x in range(20)] for y in range(20)]
    currentbuttons = []
    assets = []
    otherassets = []
    hud = []
    goldlist = []
    currentturn = 0
    
    root = Tk()
    root.geometry("870x622")
    root.title("quWARter")
    canvas = Canvas(root,width=872,height=624,bg="white",highlightthickness=0, relief='ridge')
    canvas.pack(fill=BOTH,expand=1)
    
    title, board, tutorial1, tutorial2, tutorial3, tutorial4, tutorial5 = images.initialiseTitle()

    redflag, blueflag, greenflag, yellowflag, spawntiles, movetiles, attacktiles,viewtiles,explode1,explode2,loaded,movable,selecttile,gold = images.initialiseTokens()

    redScout,blueScout,greenScout,yellowScout,redInfantry,blueInfantry,greenInfantry,yellowInfantry,redSniper,blueSniper,greenSniper,yellowSniper,redBomber,blueBomber,greenBomber,yellowBomber,redShield,blueShield,greenShield,yellowShield,redMortar,blueMortar,greenMortar,yellowMortar,redMissle,blueMissle,greenMissle,yellowMissle,redNuke,blueNuke,greenNuke,yellowNuke = images.initialiseTroops()
    
    def titlescreen():

        quwarter.drawtitle()

        quwarter.root.mainloop()

    def drawtitle():
        quwarter.destroybuttons()
        quwarter.destroyassets()
        quwarter.destroyotherassets()
        
        quwarter.canvas.create_image(0,0,image=quwarter.title,anchor=NW)

        twoplayer = Button(quwarter.canvas,text="2 Player",font=font,command=lambda: quwarter.startgame(2),bg=quwarter.red)
        twoplayer.place(x=675,y=100,width=150,height=50)
        quwarter.currentbuttons.append(twoplayer)

        fourplayer = Button(quwarter.canvas,text="4 Player",font=font,command=lambda: quwarter.startgame(4),bg=quwarter.green)
        fourplayer.place(x=675,y=200,width=150,height=50)
        quwarter.currentbuttons.append(fourplayer)

        load = Button(quwarter.canvas,text="Load Game",font=font,command=quwarter.loadgame,bg=quwarter.yellow)
        load.place(x=675,y=300,width=150,height=50)
        quwarter.currentbuttons.append(load)

        tutorial = Button(quwarter.canvas,text="Tutorial",font=font,command=quwarter.tutorial,bg=quwarter.blue)
        tutorial.place(x=675,y=400,width=150,height=50)
        quwarter.currentbuttons.append(tutorial)

    def tutorial():
        quwarter.destroybuttons()

        Screen = quwarter.canvas.create_image(0,0,image=quwarter.tutorial1,anchor=NW)
        quwarter.assets.append(Screen)
        
        quwarter.tutorialstate = 1

        homebutton = Button(quwarter.canvas,text="Home",font=font,command=quwarter.drawtitle,bg=quwarter.green)
        homebutton.place(x=30,y=550,width=100,height=50)
        quwarter.currentbuttons.append(homebutton)
        
        nextbutton = Button(quwarter.canvas,text="Next",font=font,command=quwarter.NextTutorial,bg=quwarter.yellow)
        nextbutton.place(x=150,y=550,width=100,height=50)
        quwarter.currentbuttons.append(nextbutton)
        
        backbutton = Button(quwarter.canvas,text="Back",font=font,command=quwarter.BackTutorial,bg=quwarter.red)
        backbutton.place(x=270,y=550,width=100,height=50)
        quwarter.currentbuttons.append(backbutton)

    def NextTutorial():
        if quwarter.tutorialstate != 5:
            quwarter.tutorialstate += 1
            quwarter.destroyassets()
            Screen = quwarter.canvas.create_image(0,0,image=eval("quwarter.tutorial{}".format(quwarter.tutorialstate)),anchor=NW)
            quwarter.assets.append(Screen)

    def BackTutorial():
        if quwarter.tutorialstate != 1:
            quwarter.tutorialstate -= 1
            quwarter.destroyassets()
            Screen = quwarter.canvas.create_image(0,0,image=eval("quwarter.tutorial{}".format(quwarter.tutorialstate)),anchor=NW)
            quwarter.assets.append(Screen)
        else:
            quwarter.drawtitle()

    def loadgame():
        quwarter.initgame(0)
        quwarter.destroybuttons()
        with open("quWARtersave.p","rb") as f:
            quwarter.teamlist = pickle.load(f)
            quwarter.baselist = pickle.load(f)
            quwarter.trooplist = pickle.load(f)
            quwarter.currentturn = pickle.load(f)
            quwarter.goldlist = pickle.load(f)
            quwarter.main()

        quwarter.drawhealth(quwarter.selected)
        
        for i in quwarter.teamlist + quwarter.trooplist + quwarter.baselist + quwarter.goldlist:
            i.draw()

        for i in quwarter.trooplist:
            quwarter.boardlist[i.grid[0]][i.grid[1]] = i

        for i in range(0,3):
            for j in range(0,3):
                quwarter.boardlist[i][j] = quwarter.teamlist[0]
                quwarter.boardlist[i+17][j] = quwarter.teamlist[1]
                quwarter.boardlist[i][j+17] = quwarter.teamlist[3]
                quwarter.boardlist[i+17][j+17] = quwarter.teamlist[2]


    def startgame(action):
        quwarter.destroybuttons()
        if action == 2:
            quwarter.initgame(2)
            quwarter.main()
        elif action == 4:
            quwarter.initgame(4)
            quwarter.main()

    def main():

        quwarter.menubuttons()

        quwarter.root.bind("<Button 1>",quwarter.boardhandler)
        


    def initgame(players):
        quwarter.haswon = False
        quwarter.gamestate = "menu"
        quwarter.selected = None
        quwarter.canvas.create_image(0,0,anchor=NW,image=quwarter.board)

        quwarter.teamlist = [Team("red",2,2),
                             Team("green",529,2),
                             Team("yellow",529,529),
                             Team("blue",2,529)]

        if players == 2:
            quwarter.teamlist[1].hp = 0
            quwarter.teamlist[3].hp = 0
            quwarter.clearteam(quwarter.teamlist[1])
            quwarter.clearteam(quwarter.teamlist[3])

        quwarter.baselist = [Base((5,5),True),
                             Base((13,5),True),
                             Base((5,13),True),
                             Base((13,13),True),
                             Base((9,9),False)]

        quwarter.baselist[-1].controllable = False

        for i in range(0,3):
            for j in range(0,3):
                quwarter.boardlist[i][j] = quwarter.teamlist[0]
                quwarter.boardlist[i+17][j] = quwarter.teamlist[1]
                quwarter.boardlist[i][j+17] = quwarter.teamlist[3]
                quwarter.boardlist[i+17][j+17] = quwarter.teamlist[2]

        quwarter.drawhealth(quwarter.selected)

    def drawhealth(selected):
        Health = Canvas(quwarter.canvas,bg="white",highlightthickness=0, relief='ridge')
        Health.place(x=675,y=150,width=150,height=50)
        Health.create_rectangle(0,0,149,49,fill="white",outline="black")
        
        if selected == None:
            entity = quwarter.teamlist[quwarter.currentturn]
        else:
            entity = selected

        if entity.hp/entity.maxhp > 0.67:
            colour = quwarter.green
        elif 0.33 < entity.hp/entity.maxhp <= 0.67:
            colour = quwarter.yellow
        else:
            colour = quwarter.red
            
        Health.create_rectangle(1,1,round(entity.hp*148/entity.maxhp),48,fill=colour,outline=colour)
        Health.create_text(75,25,font=font,text="{}/{}".format(entity.hp,entity.maxhp))
        quwarter.currentbuttons.append(Health)

    def drawname(selected):
        if selected == None:
            selected = quwarter.teamlist[quwarter.currentturn]
        NameLabel = Label(text="{} {}".format(selected.colour.title(),selected.__class__.__name__),bg=eval("quwarter.{}".format(selected.colour)),font=smallfont)
        NameLabel.place(x=660,y=70,width=180,height=50)
        quwarter.currentbuttons.append(NameLabel)

    def boardhandler(origin):
        
        if origin.widget == quwarter.canvas and not quwarter.haswon:
            x, y = quwarter.getgridreference(origin.x,origin.y)
            currentteam = quwarter.teamlist[quwarter.currentturn]
            if 0 <= x <= 19 and 0 <= y <= 19 and quwarter.gamestate != "animation":
                selected = quwarter.selected

                if quwarter.boardlist[x][y] is not None and not quwarter.gamestate == "attack":
                    if quwarter.gamestate == "move" and selected == quwarter.boardlist[x][y] and selected.attacked >= 1:
                        quwarter.gamestate = "attack"
                        selected.showradius()
                    elif quwarter.boardlist[x][y].hp > 0:
                        quwarter.boardlist[x][y].interface(currentteam)
                    else:
                        quwarter.backtomenu()

                elif quwarter.gamestate.startswith("place"):

                    spawntiles = []

                    for i in quwarter.teamlist:
                        if i.control == currentteam.colour:
                            spawntiles += i.spawnabletiles
                    
                    if (x,y) in spawntiles:
                        if quwarter.boardlist[x][y] == None:
                            quwarter.place(currentteam,quwarter.gamestate[5:],x,y)
                    else:
                        quwarter.backtomenu()
                        quwarter.gamestate = "menu"

                elif quwarter.gamestate == "move":
                    if quwarter.boardlist[x][y] is None and (x,y) in selected.movable:
                        quwarter.boardlist[selected.grid[0]][selected.grid[1]] = None
                        quwarter.boardlist[x][y] = selected
                        changeinx = x-selected.grid[0] 
                        changeiny = y-selected.grid[1]
                        quwarter.canvas.move(selected.entity,changeinx*31,changeiny*31)

                        if selected.loaded is not None:
                            quwarter.canvas.move(selected.loaded,changeinx*31,changeiny*31)
                        if selected.canmove is not None:
                            quwarter.canvas.move(selected.canmove,changeinx*31,changeiny*31)
                                                
                        selected.move -= fabs(changeinx)+fabs(changeiny)
                        selected.grid = (x,y)
                        selected.interface(currentteam)
                        selected.refreshhud()
                        quwarter.checkgold(x,y,currentteam)
                    else:
                        quwarter.resetstate()
                        
                elif quwarter.gamestate == "attack":
                    if (x,y) == selected.grid:
                        selected.interface(currentteam)
                    elif (x,y) in selected.attackable:
                        selected.attack(x,y)
                        selected.refreshhud()
                    else:
                        quwarter.resetstate()

                elif quwarter.gamestate == "menu":
                    pass

                else:
                    quwarter.resetstate()
                    
    def backbutton():
        Back = Button(quwarter.canvas,text="Back",font=font,command=quwarter.backtomenu,bg=quwarter.red)
        Back.place(x=700,y=20,height=30,width=100)
        quwarter.currentbuttons.append(Back)

    def savebutton():
        Back = Button(quwarter.canvas,text="Save",font=font,command=quwarter.save,bg=quwarter.green)
        Back.place(x=700,y=20,height=30,width=100)
        quwarter.currentbuttons.append(Back)

    def save():
        if not quwarter.haswon:
            with open("quWARtersave.p","wb") as f:
                pickle.dump(quwarter.teamlist,f)
                pickle.dump(quwarter.baselist,f)
                pickle.dump(quwarter.trooplist,f)
                pickle.dump(quwarter.currentturn,f)
                pickle.dump(quwarter.goldlist,f)

    def attackbutton():
        if quwarter.selected.attacked >= 1:
            def changetoattack():
                quwarter.gamestate = "attack"
                quwarter.selected.showradius()
            Attack = Button(quwarter.canvas,text="Attack",font=font,command=changetoattack,bg=quwarter.red)
            Attack.place(x=700,y=250,height=50,width=100)
            quwarter.currentbuttons.append(Attack)

    def viewbutton():
        View = Button(quwarter.canvas,text="View",font=font,command=lambda :quwarter.selected.showradius(viewing=True),bg=quwarter.yellow)
        View.place(x=700,y=310,height=50,width=100)
        quwarter.currentbuttons.append(View)

    def movebutton():
        if quwarter.selected.move >= 1:
            def changetomove():
                quwarter.gamestate = "move"
                quwarter.selected.interface(quwarter.teamlist[quwarter.currentturn])
            Move = Button(quwarter.canvas,text="Move",font=font,command=changetomove,bg=quwarter.green)
            Move.place(x=700,y=370,height=50,width=100)
            quwarter.currentbuttons.append(Move)

    def incomebutton():
        currentteam = quwarter.teamlist[quwarter.currentturn]
        cost = int(((currentteam.income-1)/2)**2+1)
        if currentteam.money >= cost:
            background = quwarter.green
            relief = "RAISED"
        else:
            background = "#969696"
            relief = "SUNKEN"
        Income = Button(quwarter.canvas,text="Upgrade Income\nCost: "+str(cost),font=tinyfont,bg=background,relief=eval(relief),command=lambda: quwarter.increaseincome(currentteam,cost))
        Income.place(x=675,y=300,width=150,height=50)
        quwarter.currentbuttons.append(Income)

    def increaseincome(currentteam,cost):
        if currentteam.money >= cost:
            currentteam.money -= cost
            currentteam.income += 2

            quwarter.backtomenu()

    def resetstate():
        quwarter.selected = None
        quwarter.gamestate = "menu"
        quwarter.backtomenu()

    def getgridreference(x,y):
        return (ceil(x/31)-1),(ceil(y/31)-1)

    def menubuttons():

        currentteam = quwarter.teamlist[quwarter.currentturn]
        
        NextTurn = Button(quwarter.canvas,text="Next Turn",font=font,command=quwarter.changeturn)
        NextTurn.place(x=665,y=530)
        quwarter.currentbuttons.append(NextTurn)

        money = quwarter.canvas.create_text(680,200,font=font,text="Money: "+str(currentteam.money),anchor=NW)
        quwarter.assets.append(money)

        income = quwarter.canvas.create_text(680,250,font=font,text="Income: "+str(currentteam.income+currentteam.incomebonus),anchor=NW)
        quwarter.assets.append(income)

        quwarter.savebutton()

        quwarter.drawname(None)

        quwarter.incomebutton()

        if currentteam.money >= Scout.cost:
            BuyScout = Button(quwarter.canvas,image=eval("quwarter.{}Scout".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Scout",currentteam),relief=RIDGE)
            BuyScout.place(x=668,y=410)
            quwarter.currentbuttons.append(BuyScout)

        if currentteam.money >= Infantry.cost:
            BuyInfantry = Button(quwarter.canvas,image=eval("quwarter.{}Infantry".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Infantry",currentteam),relief=RIDGE)
            BuyInfantry.place(x=708,y=410)
            quwarter.currentbuttons.append(BuyInfantry)

        if currentteam.money >= Sniper.cost:
            BuySniper = Button(quwarter.canvas,image=eval("quwarter.{}Sniper".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Sniper",currentteam),relief=RIDGE)
            BuySniper.place(x=748,y=410)
            quwarter.currentbuttons.append(BuySniper)

        if currentteam.money >= Bomber.cost:
            BuyBomber = Button(quwarter.canvas,image=eval("quwarter.{}Bomber".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Bomber",currentteam),relief=RIDGE)
            BuyBomber.place(x=788,y=410)
            quwarter.currentbuttons.append(BuyBomber)

        if currentteam.money >= Shield.cost:
            BuyShield = Button(quwarter.canvas,image=eval("quwarter.{}Shield".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Shield",currentteam),relief=RIDGE)
            BuyShield.place(x=668,y=450)
            quwarter.currentbuttons.append(BuyShield)

        if currentteam.money >= Mortar.cost:
            BuyMortar = Button(quwarter.canvas,image=eval("quwarter.{}Mortar".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Mortar",currentteam),relief=RIDGE)
            BuyMortar.place(x=708,y=450)
            quwarter.currentbuttons.append(BuyMortar)

        if currentteam.money >= Missle.cost:
            BuyMissle = Button(quwarter.canvas,image=eval("quwarter.{}Missle".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Missle",currentteam),relief=RIDGE)
            BuyMissle.place(x=748,y=450)
            quwarter.currentbuttons.append(BuyMissle)

        if currentteam.money >= Nuke.cost:
            BuyNuke = Button(quwarter.canvas,image=eval("quwarter.{}Nuke".format(currentteam.colour)),bg="white",command=lambda: quwarter.create("Nuke",currentteam),relief=RIDGE)
            BuyNuke.place(x=788,y=450)
            quwarter.currentbuttons.append(BuyNuke)

    def create(troop,currentteam):
        quwarter.destroyassets()
        quwarter.destroybuttons()
        quwarter.backbutton()

        spawntiles = []

        for i in quwarter.teamlist:
            if i.control == currentteam.colour:
                spawntiles += i.spawnabletiles

        for i in spawntiles:
            if quwarter.boardlist[i[0]][i[1]] is None:
                quwarter.assets.append(quwarter.canvas.create_image(((i[0]+1)*31-29,(i[1]+1)*31-29),image=quwarter.spawntiles,anchor=NW))

        description = quwarter.canvas.create_text(650,100,font=font,text=eval("{}.description".format(troop)),anchor=NW)
        quwarter.assets.append(description)

        money = quwarter.canvas.create_text(650,60,font=font,text="Money: "+str(currentteam.money),anchor=NW)
        quwarter.assets.append(money)

        quwarter.gamestate = "place"+troop

    def place(currentteam,troop,x,y):
        currentteam.money -= eval("{}.cost".format(troop))
        NewTroop = eval("{}('{}',{})".format(troop,currentteam.colour,(x,y)))
        quwarter.trooplist.append(NewTroop)
        quwarter.boardlist[x][y] = NewTroop
        NewTroop.showactions()
        if currentteam.money < eval("{}.cost".format(troop)):
            quwarter.gamestate = "menu"
            quwarter.backtomenu()
        else:
            oldtext = quwarter.assets.pop()
            quwarter.canvas.delete(oldtext)
            money = quwarter.canvas.create_text(650,60,font=font,text="Money: "+str(currentteam.money),anchor=NW)
            quwarter.assets.append(money)
            

    def backtomenu():
        quwarter.gamestate = "menu"
        for i in quwarter.currentbuttons:
            i.destroy()
        quwarter.destroyassets()
        quwarter.menubuttons()
        quwarter.drawhealth(None)
        quwarter.drawname(None)

        quwarter.selected = None

    def destroyassets():
        for i in quwarter.assets:
            quwarter.canvas.delete(i)

    def destroybuttons():
        for i in quwarter.currentbuttons:
            i.destroy()

    def destroyotherassets():
        for i in quwarter.otherassets:
            i.destroy()

    def changeturn():

        quwarter.generategold()
        quwarter.teamlist[quwarter.currentturn].money += quwarter.teamlist[quwarter.currentturn].income + quwarter.teamlist[quwarter.currentturn].incomebonus

        for i in quwarter.trooplist:
            i.deletehud()
            
        quwarter.currentturn += 1
        if quwarter.currentturn >= 4:
            quwarter.currentturn = 0

        for i in quwarter.trooplist:
            i.nextturn()
        quwarter.baselist[-1].allowcapture()
            
        while quwarter.teamlist[quwarter.currentturn].hp <= 0:
            quwarter.generategold()
            quwarter.currentturn += 1
            if quwarter.currentturn >= 4:
                quwarter.currentturn = 0
            
            for i in quwarter.trooplist:
                i.nextturn()

            quwarter.baselist[-1].allowcapture()

        quwarter.teamlist[quwarter.currentturn].incomebonus = 0
        for i in quwarter.teamlist+quwarter.baselist:
            if i.hp <= 0 and i.control == quwarter.teamlist[quwarter.currentturn].control:
                quwarter.teamlist[quwarter.currentturn].incomebonus += 1

        for i in quwarter.trooplist:
            if i.colour == quwarter.teamlist[quwarter.currentturn].colour:
                i.showactions()

        quwarter.checkifcapture()

        quwarter.backtomenu()
        quwarter.gamestate = "menu"
        quwarter.selected = None

    def checkifcapture():
        for i in quwarter.teamlist + quwarter.baselist:
            if i.hp <= 0:
                colour = None
                capture = True
                AllNone = True
                for j in i.capturetiles:
                    if quwarter.boardlist[j[0]][j[1]] is not None:
                        if colour is None:
                            colour = quwarter.boardlist[j[0]][j[1]].colour
                        elif colour != quwarter.boardlist[j[0]][j[1]].colour:
                            capture = False
                        AllNone = False

                if capture and not AllNone:
                    i.capture(colour)

    def clearteam(team):

        quwarter.canvas.delete(team.base)
        
        team.base = quwarter.canvas.create_rectangle(team.x,team.y,team.x+90,team.y+90,fill="white",outline="white")

        removetroops = []
        for i in quwarter.trooplist:
            if i.colour == team.colour:
                removetroops.append(i)

        for i in removetroops:
            i.hp = 0
            i.deletehud()
            quwarter.canvas.delete(i.entity)
            quwarter.boardlist[i.grid[0]][i.grid[1]] = None
            quwarter.trooplist.remove(i)

        destroycount = 0
        for i in quwarter.teamlist:
            if i.hp <= 0:
                destroycount += 1

        if destroycount == 3:
            quwarter.win(quwarter.teamlist[quwarter.currentturn])
            quwarter.haswon = True

    def generategold():
        if randint(1,16) == 1:
            x = randint(0,19)
            y = randint(0,19)

            for i in quwarter.goldlist:
                if i.grid == (x,y):
                    return
            if quwarter.boardlist[x][y] == None:
                quwarter.goldlist.append(Gold((x,y)))

    def checkgold(x,y,currentteam):
        for i in quwarter.goldlist:
            if (x,y) == i.grid:
                currentteam.money += 3
                quwarter.canvas.delete(i.entity)
                quwarter.goldlist.remove(i)

    def win(team):

        winner = Label(quwarter.canvas,text="{} Wins!".format(team.colour).title(),bg=eval("quwarter.{}".format(team.colour)),font=largefont)
        winner.place(x=311,y=50,anchor=CENTER)
        quwarter.otherassets.append(winner)
        
        playagain = Button(quwarter.canvas,text="Play Again",font=font,command=quwarter.resetgame)
        playagain.place(x=311,y=400,width=150,height=50,anchor=CENTER)
        quwarter.otherassets.append(playagain)

    def resetgame():
        if quwarter.gamestate != "animation":
            quwarter.drawtitle()

class Team():
    def __init__(self,colour,x,y):
        self.colour = colour
        if colour == "red":
            self.drawcolour = quwarter.red
            self.x = 2
            self.y = 2
            self.spawnabletiles = self.capturetiles = [(3,0),(3,1),(3,2),(0,3),(1,3),(2,3)]
        elif colour == "blue":
            self.drawcolour = quwarter.blue
            self.x = 2
            self.y = 529
            self.spawnabletiles = self.capturetiles = [(0,16),(1,16),(2,16),(3,17),(3,18),(3,19)]
        elif colour == "green":
            self.drawcolour = quwarter.green
            self.x = 529
            self.y = 2
            self.spawnabletiles = self.capturetiles = [(16,0),(16,1),(16,2),(17,3),(18,3),(19,3)]
        else:
            self.drawcolour = quwarter.yellow
            self.x = 529
            self.y = 529
            self.spawnabletiles = self.capturetiles = [(16,17),(16,18),(16,19),(17,16),(18,16),(19,16)]
            
        self.base = quwarter.canvas.create_rectangle(x,y,x+90,y+90,fill=self.drawcolour,outline=self.drawcolour)

        self.income = 3

        self.incomebonus = 0

        self.money = 1

        self.hp = self.maxhp = 500

        self.control = colour

        self.flag = None

    def interface(self,currentteam):
        if currentteam == self:
            if quwarter.gamestate != "menu":
                quwarter.backtomenu()
        elif self.hp > 0:
            quwarter.destroyassets()
            quwarter.destroybuttons()
            quwarter.backbutton()
            quwarter.drawhealth(self)
            quwarter.drawname(self)
            quwarter.gamestate = "view"
            money = quwarter.canvas.create_text(680,200,font=font,text="Money: "+str(self.money),anchor=NW)
            quwarter.assets.append(money)
            income = quwarter.canvas.create_text(680,250,font=font,text="Income: "+str(self.income+self.incomebonus),anchor=NW)
            quwarter.assets.append(income)

    def capture(self,control):
        if self.flag is not None:
            quwarter.canvas.delete(self.flag)
        self.flag = quwarter.canvas.create_image(self.x+13,self.y+13,image=eval("quwarter.{}flag".format(control)),anchor=NW)
        self.control = control

    def draw(self):
        if self.hp <= 0:
            quwarter.canvas.delete(self.base)
            self.base = quwarter.canvas.create_rectangle(self.x,self.y,self.x+90,self.y+90,fill="white",outline="white")
            if self.control is not None and self.control != self.colour:
                self.flag = quwarter.canvas.create_image(self.x+13,self.y+13,image=eval("quwarter.{}flag".format(self.control)),anchor=NW)

class Base():
    def __init__(self,grid,controllable):
        self.hp = 0
        self.control = None
        self.flag = None
        self.controllable = controllable
        self.grid = grid
        self.capturenumber = 0
        self.captureafter = randint(25,35)

        quwarter.boardlist[grid[0]][grid[1]] = self
        quwarter.boardlist[grid[0]+1][grid[1]] = self
        quwarter.boardlist[grid[0]][grid[1]+1] = self
        quwarter.boardlist[grid[0]+1][grid[1]+1] = self

        self.capturetiles = [(self.grid[0],self.grid[1]-1),
                             (self.grid[0]+1,self.grid[1]-1),
                             (self.grid[0]-1,self.grid[1]),
                             (self.grid[0]-1,self.grid[1]+1),
                             (self.grid[0]+2,self.grid[1]),
                             (self.grid[0]+2,self.grid[1]+1),
                             (self.grid[0],self.grid[1]+2),
                             (self.grid[0]+1,self.grid[1]+2)]

        self.x = (grid[0]+1)*31-29
        self.y = (grid[1]+1)*31-29

        if self.controllable:
            self.base = quwarter.canvas.create_rectangle(self.x,self.y,self.x+59,self.y+59,fill="#969696",outline="#969696")
        else:
            self.base = quwarter.canvas.create_rectangle(self.x,self.y,self.x+59,self.y+59,fill="#FFFFFF",outline="#FFFFFF")


    def capture(self,control):
        if self.controllable:
            if self.flag is not None:
                quwarter.canvas.delete(self.flag)
            self.flag = quwarter.canvas.create_image(self.x,self.y,image=eval("quwarter.{}flag".format(control)),anchor=NW)
            self.control = control

    def allowcapture(self):
        self.capturenumber += 1
        if self.capturenumber >= self.captureafter and not self.controllable:
            self.controllable = True
            quwarter.canvas.delete(self.base)
            self.base = quwarter.canvas.create_rectangle(self.x,self.y,self.x+59,self.y+59,fill="#969696",outline="#969696")

    def draw(self):
        if self.controllable:
            self.base = quwarter.canvas.create_rectangle(self.x,self.y,self.x+59,self.y+59,fill="#969696",outline="#969696")
        else:
            self.base = quwarter.canvas.create_rectangle(self.x,self.y,self.x+59,self.y+59,fill="#FFFFFF",outline="#FFFFFF")

        if self.control is not None:
            self.flag = quwarter.canvas.create_image(self.x,self.y,image=eval("quwarter.{}flag".format(self.control)),anchor=NW)

class Troop():
    def __init__(self,colour,grid):
        self.maxhp = self.hp = self.damage = self.range = self.attacked = self.move = 0
        self.grid = grid
        self.colour = colour
        self.movable = []
        self.attackable = []
        self.loaded = None
        self.canmove = None

    def interface(self,currentteam):
        quwarter.destroybuttons()
        quwarter.destroyassets()
        quwarter.backbutton()
        quwarter.drawhealth(self)
        quwarter.drawname(self)
        
        if currentteam.colour == self.colour:
            self.showmovements()
            quwarter.gamestate = "move"
            quwarter.selected = self
            quwarter.attackbutton()
            quwarter.viewbutton()
            quwarter.movebutton()
        else:
            self.showradius(viewing=True)

    def showactions(self):
        
        if self.attacked >= 1:
            self.loaded = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,image=quwarter.loaded,anchor=NW)
        else:
            quwarter.canvas.delete(self.loaded)
            self.loaded = None
        if self.move >= 1:
            self.canmove = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,image=quwarter.movable,anchor=NW)
        else:
            quwarter.canvas.delete(self.canmove)
            self.canmove = None

    def deletehud(self):
        if self.loaded is not None:
            quwarter.canvas.delete(self.loaded)
        if self.canmove is not None:
            quwarter.canvas.delete(self.canmove)

    def refreshhud(self):
        self.deletehud()
        self.showactions()

    def getmovabletiles(self,gridx,gridy,moves):
        movable = []
        if moves == 0:
            return movable
        if gridx + 1 <= 19:
            if quwarter.boardlist[gridx+1][gridy] == None:
                movable.append((gridx+1,gridy))
                movable += self.getmovabletiles(gridx+1,gridy,moves-1)
        if gridx - 1 >= 0:
            if quwarter.boardlist[gridx-1][gridy] == None:
                movable.append((gridx-1,gridy))
                movable += self.getmovabletiles(gridx-1,gridy,moves-1)
        if gridy + 1 <= 19:
            if quwarter.boardlist[gridx][gridy+1] == None:
                movable.append((gridx,gridy+1))
                movable += self.getmovabletiles(gridx,gridy+1,moves-1)
        if gridy -1 >= 0:
            if quwarter.boardlist[gridx][gridy-1] == None:
                movable.append((gridx,gridy-1))
                movable += self.getmovabletiles(gridx,gridy-1,moves-1)

        return set(movable)
    
    def showmovements(self):
        quwarter.destroyassets()
        self.movable = self.getmovabletiles(self.grid[0],self.grid[1],self.move)

        for i in self.movable:
            tile = quwarter.canvas.create_image((i[0]+1)*31-29,(i[1]+1)*31-29,image=quwarter.movetiles,anchor=NW)
            quwarter.assets.append(tile)

        selected = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,image=quwarter.selecttile,anchor=NW)
        quwarter.assets.append(selected)

    def showradius(self,viewing=False):

        if viewing == True:
            quwarter.gamestate = "view"

        quwarter.destroyassets()
        
        self.attackable = []
        for i in range(20):
            for j in range(20):
                xcomponent = i-self.grid[0]
                ycomponent = j-self.grid[1]

                if quwarter.boardlist[i][j].__class__.__name__ == "Base":
                    pass

                elif (xcomponent**2 + ycomponent**2)**0.5 <= self.range:

                    if xcomponent == ycomponent == 0:
                        pass

                    else:
                        blockingpath = False

                        vector = [xcomponent/50,ycomponent/50]
                        current = [self.grid[0],self.grid[1]]
                        while True:                                
                            current[0] += vector[0]
                            current[1] += vector[1]

                            if round(current[0]) == i and round(current[1]) == j:
                                break

                            elif 0 <= round(current[0]) <= 19 and 0 <= round(current[1]) <= 19:

                                if quwarter.boardlist[round(current[0])][round(current[1])].__class__.__name__ == "Shield":
                                    if quwarter.boardlist[round(current[0])][round(current[1])].colour != self.colour:
                                        blockingpath = True
                                        break
                                elif quwarter.boardlist[round(current[0])][round(current[1])].__class__.__name__ == "Base" or quwarter.boardlist[round(current[0])][round(current[1])].__class__.__name__ == "Team":
                                    blockingpath = True
                                    break

                            else:
                                break

                        if not blockingpath:
                            self.attackable.append((i,j))

        for i in self.attackable:
            if not viewing:
                tile = quwarter.canvas.create_image((i[0]+1)*31-29,(i[1]+1)*31-29,image=quwarter.attacktiles,anchor=NW)
            else:
                tile = quwarter.canvas.create_image((i[0]+1)*31-29,(i[1]+1)*31-29,image=quwarter.viewtiles,anchor=NW)
            quwarter.assets.append(tile)

        selected = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,image=quwarter.selecttile,anchor=NW)
        quwarter.assets.append(selected)

    def attack(self,x,y):
        if quwarter.boardlist[x][y] is not None:
            if quwarter.boardlist[x][y].hp > 0:
                quwarter.gamestate = "animation"
                self.attacked -= 1
                vector = [(x-self.grid[0])/20,(y-self.grid[1])/20]
                bullet = quwarter.canvas.create_oval((self.grid[0]+1)*31-20,(self.grid[1]+1)*31-19,(self.grid[0]+1)*31-10,(self.grid[1]+1)*31-9,fill=eval("quwarter.{}".format(self.colour)))
                damage = self.randomdamage(self.damage)
                target = quwarter.boardlist[x][y]
                target.hp -= damage
                self.movebullet(bullet,vector,0,x,y,damage)
        

    def movebullet(self,bullet,vector,repeats,x,y,damage):
        if repeats < 20:
            repeats += 1
            quwarter.canvas.move(bullet,vector[0]*31,vector[1]*31)
            quwarter.root.update()
            quwarter.root.after(20,lambda: self.movebullet(bullet,vector,repeats,x,y,damage))
        else:
            quwarter.canvas.delete(bullet)
            self.dealdamage(x,y,damage)

    def randomdamage(self,damage):
        return round(randint(80,120)*damage/100)

    def dealdamage(self,x,y,damage):
        if quwarter.boardlist[x][y].__class__.__name__ != "Team":
            if quwarter.boardlist[x][y].hp <= 0:
                quwarter.boardlist[x][y].deletehud()
                quwarter.canvas.delete(quwarter.boardlist[x][y].entity)
                quwarter.trooplist.remove(quwarter.boardlist[x][y])
                quwarter.boardlist[x][y] = None
            self.showdamage(damage,x,y)
        elif quwarter.boardlist[x][y].__class__.__name__ == "Team":
            if quwarter.boardlist[x][y].hp <= 0:
                quwarter.clearteam(quwarter.boardlist[x][y])
                if quwarter.boardlist[x][y].colour == self.colour:
                    quwarter.changeturn()
            self.showdamage(damage,x,y)

    def showdamage(self,damage,x,y):
        Damage = Label(text=str(damage),bg=quwarter.red,font=tinyfont,relief="ridge")
        Damage.place(x=(x+1)*31-26,y=(y+1)*31-27)
        quwarter.root.after(1000,lambda: self.removewidget(Damage))
        if self.attacked < 1:
            if self.hp > 0:
                self.interface(quwarter.teamlist[quwarter.currentturn])
        elif self.attacked >= 1:
            quwarter.gamestate = "attack"
        else:
            quwarter.backtomenu()

    def removewidget(self,widget):
        widget.destroy()
        
        

class Scout(Troop):
    cost = 1
    description = "Scout:\nCost: "+str(cost)+"\nLow Health\nHigh Move\nLow Dmg\nLow range"

    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 30
        self.range = 1.5
        self.move = 5
        self.attacked = 0
        self.hp = self.maxhp = 30
        self.name = colour.title()+" Scout"
        self.draw()

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Scout")))

    def nextturn(self):
        self.move = 5
        self.attacked = 1

class Infantry(Troop):
    cost = 2
    description = "Infantry:\nCost: "+str(cost)+"\nModerate Health\nModerate Move\nModerate Dmg\nModerate Range\nCan shoot twice"

    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 50
        self.range = 3
        self.move = 0
        self.attacked = 0
        self.hp = self.maxhp = 100
        self.name = colour.title()+" Infantry"
        self.draw()

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Infantry")))
        
    def nextturn(self):
        self.move = 3
        self.attacked = 2
        
class Sniper(Troop):
    cost = 3
    description = "Sniper:\nCost: "+str(cost)+"\nLow Health\nLow Move\nHigh Dmg\nHigh Range\nSlow Reload"

    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 110
        self.range = 7
        self.move = 0
        self.reload = 0
        self.attacked = 0
        self.hp = self.maxhp = 30
        self.name = colour.title()+" Sniper"
        self.draw()

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Sniper")))

    def nextturn(self):
        if self.attacked < 1:
            self.reload += 0.125

            if self.reload >= 1:
                self.attacked = 1
                self.reload = 0

        self.move = 2

    def interface(self,currentteam):
        quwarter.destroybuttons()
        quwarter.destroyassets()
        quwarter.backbutton()
        quwarter.drawhealth(self)
        quwarter.drawname(self)
        
        if currentteam.colour == self.colour:
            self.showmovements()
            quwarter.gamestate = "move"
            quwarter.selected = self
            quwarter.attackbutton()
            quwarter.viewbutton()
            quwarter.movebutton()
        else:
            self.showradius(viewing=True)
        if self.reload < 1 and self.attacked < 1:
            reload = quwarter.canvas.create_text(680,200,font=font,text="Reload: {}%".format(round((self.reload/1)*100)),anchor=NW)
        else:
            reload = quwarter.canvas.create_text(680,200,font=font,text="Reloaded".format(round((self.reload/1)*100)),anchor=NW)
        quwarter.assets.append(reload)

class Bomber(Troop):
    cost = 4
    description = "Bomber:\nCost: "+str(cost)+"Low Health\nModerate Move\nHigh Dmg\nModerate Range\nSplash Damage"

    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 150
        self.splash = 0.7
        self.range = 3
        self.move = 0
        self.attacked = 0
        self.hp = self.maxhp = 75
        self.name = colour.title()+" Bomber"
        self.splashradius = 1.5
        self.inaccuracy = 0
        self.draw()

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Bomber")))

    def nextturn(self):
        self.move = 3
        self.attacked = 1

    def attack(self,x,y):
        self.damagelist = []
        self.SplashedTiles = []
        
        inaccuracyx = randint(-self.inaccuracy,self.inaccuracy)
        inaccuracyy = randint(-self.inaccuracy,self.inaccuracy)
        x,y = x+inaccuracyx,y+inaccuracyy
        quwarter.gamestate = "animation"
        self.attacked -= 1
        vector = [(x-self.grid[0])/20,(y-self.grid[1])/20]
        
        bullet = quwarter.canvas.create_oval((self.grid[0]+1)*31-20,(self.grid[1]+1)*31-19,(self.grid[0]+1)*31-10,(self.grid[1]+1)*31-9,fill=eval("quwarter.{}".format(self.colour)))
        
        damage = self.randomdamage(self.damage)

        if quwarter.boardlist[x][y] is not None:
            if quwarter.boardlist[x][y].hp > 0:
                if quwarter.boardlist[x][y].__class__.__name__ == "Shield":
                    damage = round(damage/4)
                    
                if quwarter.boardlist[x][y].__class__.__name__ != "Base":
                    quwarter.boardlist[x][y].hp -= damage
                    self.damagelist.append([(x,y),damage])

        for i in range(20):
            for j in range(20):
                if ((i-x)**2 + (j-y)**2)**0.5 <= self.splashradius and (i,j) != (x,y):
                    self.SplashedTiles.append((i,j))

        for i in self.SplashedTiles:
            if quwarter.boardlist[i[0]][i[1]] is not None:
                if quwarter.boardlist[i[0]][i[1]].hp > 0:
                    if quwarter.boardlist[i[0]][i[1]].__class__.__name__ == "Shield" or quwarter.boardlist[i[0]][i[1]].__class__.__name__ == "Team":
                        damage = self.randomdamage((self.damage*self.splash)/4)
                    else:
                        damage = self.randomdamage((self.damage*self.splash))
                    quwarter.boardlist[i[0]][i[1]].hp -= damage
                    self.damagelist.append([i,damage])

        quwarter.root.after(1400,self.removesplashtiles)
        
        self.movebullet(bullet,vector,0,x,y,self.damagelist)

    def movebullet(self,bullet,vector,repeats,x,y,damage):
        if repeats < 20:
            repeats += 1
            quwarter.canvas.move(bullet,vector[0]*31,vector[1]*31)
            quwarter.root.update()
            quwarter.root.after(20,lambda: self.movebullet(bullet,vector,repeats,x,y,damage))
        else:
            quwarter.canvas.delete(bullet)
            self.dealdamage(x,y,damage)

    def randomdamage(self,damage):
        return round(randint(80,120)*damage/100)

    def dealdamage(self,x,y,damage):
        self.showsplash(x,y)
        if len(damage) > 0:
            for i in damage:
                splashx = i[0][0]
                splashy = i[0][1]
                if quwarter.boardlist[splashx][splashy] == None:
                    pass
                elif quwarter.boardlist[splashx][splashy].__class__.__name__ != "Team":
                    if quwarter.boardlist[splashx][splashy].hp <= 0:
                        quwarter.boardlist[splashx][splashy].deletehud()
                        quwarter.canvas.delete(quwarter.boardlist[splashx][splashy].entity)
                        quwarter.trooplist.remove(quwarter.boardlist[splashx][splashy])
                        quwarter.boardlist[splashx][splashy] = None
                    self.showdamage(i[1],splashx,splashy)
                elif quwarter.boardlist[splashx][splashy].__class__.__name__ == "Team":
                    if quwarter.boardlist[splashx][splashy].hp <= 0:
                        quwarter.clearteam(quwarter.boardlist[splashx][splashy])
                        if quwarter.boardlist[splashx][splashy].colour == self.colour:
                            quwarter.changeturn()
                    self.showdamage(i[1],splashx,splashy)

    def showsplash(self,x,y):
        
        quwarter.assets.append(quwarter.canvas.create_image(((x+1)*31-29,(y+1)*31-29),image=quwarter.explode1,anchor=NW))

        for i in self.SplashedTiles:
            quwarter.assets.append(quwarter.canvas.create_image(((i[0]+1)*31-29,(i[1]+1)*31-29),image=quwarter.explode2,anchor=NW))

    def showdamage(self,damage,x,y):
        
        Damage = Label(text=str(damage),bg=quwarter.red,font=tinyfont,relief="ridge")
        Damage.place(x=(x+1)*31-26,y=(y+1)*31-27)
        quwarter.root.after(1000,lambda: self.removewidget(Damage))

    def removewidget(self,widget):
        if widget is not None:
            widget.destroy()
        

    def removesplashtiles(self):
        for i in range(len(self.SplashedTiles)+1):
            quwarter.canvas.delete(quwarter.assets.pop(-1))
        if self.attacked < 1:
            if self.hp > 0:
                self.interface(quwarter.teamlist[quwarter.currentturn])
            else:
                quwarter.backtomenu()
        else:
            quwarter.gamestate = "attack"
    

class Shield(Troop):
    cost = 10
    description = "Shield:\nCost: "+str(cost)+"\nHigh Health\nModerate Move\nLow Range\nBlocks Shots"
    
    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 100
        self.range = 1.5
        self.move = 0
        self.attacked = 0
        self.hp = self.maxhp = 500
        self.name = colour.title()+" Shield"
        self.splash = 0.5
        
        self.draw()

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Shield")))
        
    def nextturn(self):
        self.move = 2
        self.attacked = 1

class Mortar(Bomber):
    cost = 15
    description = "Mortar:\nCost: "+str(cost)+"\nModerate Health\nLow Move\nHigh Dmg\nHigh Range\nSlow Reload\nInaccurate\nBlind Spot\nSplash Damage"
    
    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 200
        self.range = 8
        self.blindspot = 3.2
        self.splash = 0.5
        self.inaccuracy = 1
        self.reload = 0
        self.move = 0
        self.attacked = 0
        self.hp = self.maxhp = 100
        self.name = colour.title()+" Mortar"

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Mortar")))
        
    def nextturn(self):
        if self.attacked < 1:
            self.reload += 0.084

            if self.reload >= 1:
                self.attacked = 1
                self.reload = 0

        self.move = 1
        
    def showradius(self,viewing=False):

        if viewing == True:
            quwarter.gamestate = "view"

        quwarter.destroyassets()
        
        self.attackable = []
        for i in range(20):
            for j in range(20):
                if self.blindspot <= ((i-self.grid[0])**2 + (j-self.grid[1])**2)**0.5 <= self.range:
                    self.attackable.append((i,j))

        for i in self.attackable:
            if not viewing:
                tile = quwarter.canvas.create_image((i[0]+1)*31-29,(i[1]+1)*31-29,image=quwarter.attacktiles,anchor=NW)
            else:
                tile = quwarter.canvas.create_image((i[0]+1)*31-29,(i[1]+1)*31-29,image=quwarter.viewtiles,anchor=NW)
            quwarter.assets.append(tile)


    def interface(self,currentteam):
        quwarter.destroybuttons()
        quwarter.destroyassets()
        quwarter.backbutton()
        quwarter.drawhealth(self)
        quwarter.drawname(self)
        
        if currentteam.colour == self.colour:
            self.showmovements()
            quwarter.gamestate = "move"
            quwarter.selected = self
            quwarter.attackbutton()
            quwarter.viewbutton()
            quwarter.movebutton()
        else:
            self.showradius(viewing=True)
        if self.reload < 1 and self.attacked < 1:
            reload = quwarter.canvas.create_text(680,200,font=font,text="Reload: {}%".format(round((self.reload/1)*100)),anchor=NW)
        else:
            reload = quwarter.canvas.create_text(680,200,font=font,text="Reloaded".format(round((self.reload/1)*100)),anchor=NW)
        quwarter.assets.append(reload)

class Missle(Mortar):
    cost = 30
    description = "Missle:\nCost: "+str(cost)+"\nModerate Health\nLow Move\nLow Dmg\nHigh Range\nBlind Spot\nSplash Damage\nCan shoot 3 times"
    
    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 40
        self.range = 8
        self.blindspot = 2.5
        self.splash = 0.5
        self.splashradius = 1
        self.inaccuracy = 0
        self.move = 0
        self.attacked = 0
        self.hp = self.maxhp = 100
        self.name = colour.title()+" Missle"

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Missle")))

    def nextturn(self):
        self.move = 1
        self.attacked = 3

class Nuke(Mortar):
    cost = 100
    description = "Nuke:\nCost: "+str(cost)+"\nModerate Health\nVery Low Move\nMassive Dmg\nMassive Range\nMassive Splash\nVery Long Reload"
    
    def __init__(self,colour,grid):
        super().__init__(colour,grid)
        self.damage = 500
        self.range = 10
        self.blindspot = 0
        self.splash = 0.5
        self.splashradius = 2.5
        self.inaccuracy = 0
        self.reload = 0
        self.move = 0
        self.movereload = 0
        self.attacked = 0
        self.hp = self.maxhp = 100
        self.name = colour.title()+" Nuke"

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=eval("quwarter.{}".format(self.colour+"Nuke")))
        
    def nextturn(self):
        if self.attacked < 1:
            self.reload += 0.025

            if self.reload >= 1:
                self.attacked = 1
                self.reload = 0

        if self.move < 1:
            self.movereload += 0.2

            if self.movereload >= 1:
                self.move = 1
                self.movereload = 0

class Gold():
    def __init__(self,grid):
        self.grid = grid
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=quwarter.gold)

    def draw(self):
        self.entity = quwarter.canvas.create_image((self.grid[0]+1)*31-29,(self.grid[1]+1)*31-29,anchor=NW,image=quwarter.gold)

if __name__ == "__main__":
    quwarter.titlescreen()
