import random
import time
import json
import os
import pickle

class npc:
    def __init__(self, name, position, health, relation, damage):
        self.name = name
        self.position = position
        self.health = float(health)
        self.relation = relation
        self.damage = float(damage)

    def __str__(self):
        out = "[" + self.name + "] - " + self.position.__str__() + " - [H" + str(self.health) + "] - [R" + str(self.relation) + "]"
        
        return out

class player:
    def __init__(self, mapd):
        print("[SETUP]")
        print()
        print("name: ")
        self.name = input()
        print()

        self.health = 10

        inv = []

        for i in mapd["SPAWN"]["items"]:
            inv.append(i.upper())

        self.inventory = inventory(inv)

        self.pos = position(int(mapd["SPAWN"]["coord"][0]),int(mapd["SPAWN"]["coord"][2]))

        self.fist = float(4)

        self.won = False

    def __str__(self):
        out = "[" + self.name + "] - [H" + str(self.health) + "] - " + self.pos.__str__() + " - " + self.inventory.__str__()

        return out

    def addinv(self, item):
        self.inventory.append(item)

    def reminv(self, item):
        self.inventory.remove(item)

    def posi(self):
        out = self.pos.__str__()

        return out

class position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def gonorth(self):
        self.y -= 1

    def goeast(self):
        self.x += 1

    def gosouth(self):
        self.y += 1

    def gowest(self):
        self.x -= 1

    def __str__(self):
        out = str(self.x) + "/" + str(self.y)

        return out

class inventory:
    def __init__(self, items):
        self.items = []

        for itemm in items:
            self.items.append(itemm)

    def size(self):
        out = len(self.items)

        return out

    def __len__(self):
        out = self.size()

        return out

    def __str__(self):
        out = ""

        for item in self.items:
            out += item.__str__() + ", "

        out = out[:-2]

        return out

class stats:
    def __init__(self, win, loose):
        self.win = int(win)
        self.loose = int(loose)

    def addwin(self):
        self.win += 1

    def addloose(self):
        self.loose += 1

    def total(self):
        out = self.win - self.loose

        return out

    def __str__(self):
        out = str(self.win) + " - " + str(self.loose)

        return out

class info:
    def __init__(self):
        datafi = openfi("ASSETS/INFO/INFO.json", "r")
        data = json.loads(datafi.read())
        datafi.close()

        self.repo = data["REPO"]
        self.owner = data["OWNER"]
        self.version = data["VERSION"]

    def __str__(self):
        out = "REPO: " +  self.repo + ", OWNER: " + self.owner + ", VERSION: " + self.version

        return out

def settogo(stuff):
    out = []

    for i in stuff:
        do = i.replace("N", "GO NORTH")

        if do == "GO NORTH":
            out.append(do)
        
        do = i.replace("E", "GO EAST")

        if do == "GO EAST":
            out.append(do)

        do = i.replace("S", "GO SOUTH")

        if do == "GO SOUTH":
            out.append(do)

        do = i.replace("W", "GO WEST")

        if do == "GO WEST":
            out.append(do)

    return out

def settoin(stuff):
    out = []

    for i in stuff:
        do = i.replace("N", "NORTH")

        if "NORTH" in do:
            out.append(do)
        
        do = i.replace("E", "EAST")

        if "EAST" in do:
            out.append(do)

        do = i.replace("S", "SOUTH")

        if "SOUTH" in do:
            out.append(do)

        do = i.replace("W", "WEST")

        if "WEST" in do:
            out.append(do)

    return out

def petrolcredits(cred):
    c = json.loads(cred)

    print()
    print(c["c"])

    time.sleep(0.75)

    for i in c["creedits"]:
        print()
        print(c["creedits"][i])

        time.sleep(0.75)

    time.sleep(1)
    
    print()

def openfi(name, method = "r"):		
    out = None		

    try:
        try:
            try:
                out = open("./" + name.__str__(), method.__str__())		
            except:		
                out = open("./SRC/" + name.__str__(), method.__str__())		
        except:		
            out = open("./Petrol.zip/" + name.__str__(), method.__str__())	

        return out
    except:
        print("FAILURE")

def clear(): 		
    if os.name == 'nt': 		
        os.system('cls') 		
    else: 		
        os.system('clear')  

def settingsset(ar):
    out = ""

    for i in ar:
        out += i + "\n"

    return out

def save(player, mapd, mapname, npc, sid):
    with openfi('ASSETS/SAVES/' + sid + '/player.config', 'wb') as player_f:
        pickle.dump(player, player_f)
    with openfi('ASSETS/SAVES/' + sid + '/map.config', 'wb') as map_f:
        pickle.dump(mapd, map_f)
    with openfi('ASSETS/SAVES/' + sid + '/name.config', 'wb') as name:
        pickle.dump(mapname, name)
    with openfi('ASSETS/SAVES/' + sid + '/npc.config', 'wb') as npcs:
        pickle.dump(npc, npcs)
    with openfi('ASSETS/SAVES/' + sid + '/data.config', 'wb') as dataf:
        data = [player.name]
        pickle.dump(data, dataf)

def load(sid):
    player = None
    mapd = None
    mapname = None
    npc = None
    data = None
    
    with openfi('ASSETS/SAVES/' + sid + '/player.config', 'rb') as player_f:
        player = pickle.load(player_f)
    with openfi('ASSETS/SAVES/' + sid + '/map.config', 'rb') as map_f:
        mapd = pickle.load(map_f)
    with openfi('ASSETS/SAVES/' + sid + '/name.config', 'rb') as name:
        mapname = pickle.load(name)
    with openfi('ASSETS/SAVES/' + sid + '/npc.config', 'rb') as npcs:
        npc = pickle.load(npcs)
    with openfi('ASSETS/SAVES/' + sid + '/data.config', 'rb') as dataf:
        data = pickle.load(dataf)

    out = [player, mapd, mapname, npc, data]

    return out

def saveINV(sid):
    with openfi('ASSETS/SAVES/' + sid + '/data.config', 'wb') as dataf:
        pickle.dump("INV", dataf)

def loadData(sid):
    data = None

    with openfi('ASSETS/SAVES/' + sid + '/data.config', 'rb') as dataf:
        data = pickle.load(dataf)

    return data