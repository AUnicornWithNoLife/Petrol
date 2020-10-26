import random
import time
import json
import os

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
        self.inventory = inventory('TORCH')

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
    def __init__(self, *items):
        self.items = []

        for itemm in items:
            self.items.append(item(itemm))

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

class item:
    def __init__(self, code):
        self.code = code.__str__()

    def __str__(self):
        out = self.code.__str__()

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

    time.sleep(0.5)

    for i in c["creedits"]:
        print()
        print(c["creedits"][i])

        time.sleep(0.5)

    time.sleep(1)
    
    print()

#function desined to test that the map works, currently a bug makes it say True all the time, im working on fxing ths
def checkmap(mapu):
    done = []

    current = mapu["SPAWN"]["coord"]

    todo = []

    while True:
        tch = mapu[current]["dirs"]

        for u in tch:
            i = tch[u]

            c = "0"
            nc = "pp"

            if i == "N":
                c = "S"
                nc = current[0] + "/" + str(int(current[2]) - 1)
            elif i == "E":
                c = "W"
                nc = str(int(current[0]) - 1) + "/" + current[2]
            elif i == "S":
                c = "N"
                nc = current[0] + "/" + str(int(current[2]) + 1)
            elif i == "W":
                c = "E"
                nc = str(int(current[0]) + 1) - "/" + current[2]
            else:
                return False
            
            if nc not in done:
                todo.append(nc)
            try:
                todo.remove(current)
            except:
                pass
                
            done.append(current)

            notin = True

            for p in mapu[nc]["dirs"]:
                pp = mapu[nc]["dirs"][p]

                if pp == c:
                    notin = False

                    break

            if notin:
                print(nc)

                return False

            if len(todo) == 0:
                return True
            
            current = todo[0]

def openfi(name, method = "r"):
    out = None

    try:
        try:
            out = open("./" + name.__str__(), method.__str__())
        except:
            out = open("./SRC/" + name.__str__(), method.__str__())
    except Exception as e:
        print(e)

        out = e

    return out

def clear(): 
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear') 