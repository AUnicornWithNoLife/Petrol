import random # used for picking ascii art
import json # used for reading map files
import os
import importlib
import platform
import sys

import pretty # adds ability to print colors

import petrolasset as asset
import petrolextra as extra

# log only works on UNIX based systems, do not enable on release, beta or alpha versions of this software.

dolog = False

logdata = ""

if dolog:
    import log

    # create log, and create event for load

    logdata = log.log()
    logdata.add("Loaded Petrol")

def addlog(msg, ltype = "INFO"):
    if dolog:
        logdata.add(msg, ltype)

# title function shows the title and info at the begining
def title(version):
    if platform.system() == "Windows":
        asset.clear()

        pretty.pprint("<GREEN>Petrol<ENDC>")
    else:
        asset.clear()

        #this loads in the file, defining how many variations of the ascii art their are
        logoa = asset.openfi("ASSETS/LOGO/A.txt", "r")

        logoaa = int(logoa.read())

        logoa.close()
        logoa = None
        #-----

        #this loads in one of the ascii art logos and displays it alongside other info
        logo = asset.openfi("ASSETS/LOGO/" + str(random.randint(0,logoaa)) + ".txt", "r")

        pretty.pprint("<GREEN>", logo.read(), "<ENDC>")

        logo.close()
        logo = None
    
    pretty.pprint()
    pretty.pprint("<BLUE>V:<ENDC> " + version)
    pretty.pprint()
    pretty.pprint("[PRESS <RED>ENTER<ENDC> TO <GREEN>START<ENDC>]")
    pretty.pprint("for extra options type extra")
    pretty.pprint()
    #-----

#this is the main loop the code runs on
while True:
    #open the settings file and set the settings acordingly

    try:
        d = asset.openfi("ASSETS/SETTINGS/config.txt", "r")
        settings = d.read()
        settingspl = settings.split("\n")
        de = settingspl[0]
        d.close()

        debug = bool(de)

        addlog("Settings loaded in")
    except Exception as Ex:
        addlog("Failed loading settings - " + Ex.__str__(), "FATAL")
        
        pretty.pprint(Ex)

        break

    #-----

    #open STATS file

    try:
        d = asset.openfi("ASSETS/STATS/data.txt", "r")
        stats = d.read()
        stats = asset.stats(stats.split(";")[0], stats.split(";")[1])
        d.close()

        addlog("Loaded stats")
    except Exception as Ex:
        addlog("Failed loading stats - " + Ex.__str__(), "FATAL")

        pretty.pprint(Ex)
        
        break

    #---

    info = asset.info()

    a = "++more cheese++"

    while a != "":
        last = None
        
        title(info.version)
        
        a = input()

        if a.upper() == "EXTRA":
            extra.menu(info, stats)

            #reopen the settings file because settings may have been changed by the menu

            try:
                d = asset.openfi("ASSETS/SETTINGS/config.txt", "r")
                settings = d.read()
                settings = settings.split("\n")
                de = settings[0]
                d.close()

                debug = bool(de)

                addlog("Settings loaded in")
            except Exception as Ex:
                addlog("Failed loading settings", "FATAL")

                pretty.pprint(Ex)

                break

            #-----

    pretty.pprint("starting game")

    #this loads in the possible maps and asks the user wich one they want to play

    ids = []

    for i in range(6):
        data = None
        good = None

        try:
            data = "<GREEN>" + asset.loadData(str(i))[0] + "<ENDC>"

            good = True

            if (asset.loadData(str(i))[0] == "INV"):
                data = "<RED>Empty<ENDC>"
                
                good = False
        except:
            data = "<RED>Empty<ENDC>"

            good = False
        
        ids.append([str(i), data, good])

    asset.clear()
    
    for i in ids:
        pretty.pprint(i[0] + " ~ " + i[1])
    
    print()

    sid = input("ID? ")

    print()
    
    load = ids[int(sid)][2]

    if load:
        print()

        print("Do you want to overwrite that save?")

        load = input().upper() == "Y"

    p1 = None
    mapd = None
    setup = None
    mapname = None
    
    if load:
        asset.clear()
        
        loda = asset.load(sid)

        p1 = loda[0]
        mapd = loda[1]
        mapname = loda[2]

        setup = importlib.import_module("ASSETS.MAPS." + mapname + ".setup")

        callback = setup.callset(p1, loda[3], True)
    else:
        choice = None
        
        posmaps = []
        colors = []
        desc = []

        try:
            posmaps = os.listdir("./ASSETS/MAPS")
        except:
            posmaps = os.listdir("./SRC/ASSETS/MAPS")

        possib = True

        for ma in posmaps:
            colors.append(json.loads(asset.openfi("ASSETS/MAPS/" + ma + "/info.json", 'r').read())['color'])
            desc.append(json.loads(asset.openfi("ASSETS/MAPS/" + ma + "/info.json", 'r').read())['desc'])

        while possib:
            asset.clear()

            pretty.pprint("MAPS:")
            print()

            i = 0

            for posm in posmaps:
                pretty.pprint(i.__str__() + ": " + colors[i] + posm + " ~ " + desc[i] + "<ENDC>")

                i += 1

            pretty.pprint()
            choice = input("? ")

            try:
                mapfi = asset.openfi("ASSETS/MAPS/" + posmaps[int(choice)] + "/map.json", "r")
                setup = importlib.import_module("ASSETS.MAPS." + posmaps[int(choice)] + ".setup")

                possib = False
            except Exception as e:
                pretty.pprint(e)

                input()

                pass

            maptxt = mapfi.read()
            mapfi.close()
            mapfi = None

            mapd = json.loads(maptxt)
            maptxt = None

            asset.clear()
            
            pretty.pprint("playing on map: " + posmaps[int(choice)])
            pretty.pprint()

            mapname = posmaps[int(choice)]

            addlog("Chossen map: " + choice)
        #-----
    
        #this sets up the player variable, and the place where all the custom map code is run

        try:
            p1 = asset.player(mapd)

            callback = setup.callset(p1, [], False)

            addlog("Player setup")
        except Exception as Ex:
            addlog("Failed setting up Player", "FATAL")

            pretty.pprint(Ex)

            break

        #-----

    #this loop is where the gameplay happens
    while p1.health >= 0:
        if last != p1.posi():
            pretty.pprint()
            callback.newroom(p1.posi(), mapd, p1)
    
        callback.room(p1, p1.posi())
    
        pretty.pprint()

        last = p1.posi()

        asset.save(p1, mapd, mapname, callback.npcs, sid)

        com = pretty.iinput("<BOLD><UNDER><RED>>><ENDC> ")

        addlog("Player command: " + com)

        if com[:2].upper() == "GO":
            posib = []

            for u in mapd[p1.posi()]["dirs"]:
                posib.append(u)

            posib = asset.settogo(posib)

            if com.upper() in posib:
                if com.upper() == "GO NORTH":
                    p1.pos.gonorth()
                elif com.upper() == "GO EAST":
                    p1.pos.goeast()
                elif com.upper() == "GO SOUTH":
                    p1.pos.gosouth()
                elif com.upper() == "GO WEST":
                    p1.pos.gowest()
            else:
                pretty.pprint("sorry you cant travel that way") 
        elif com[:4].upper() == "KILL":
            callback.attack(p1.fist, "fist", com[5:], p1.pos)
        elif com.upper() == "BACKPACK":
            pretty.pprint()
            pretty.pprint(p1.inventory.__str__())
        elif com[:6].upper() == "PICKUP":
            # allows you to pickup items, still need to add functoins to allow you to drop items

            for item in mapd[p1.posi()]["items"]:
                try:
                    if item.upper() == com[7:].upper():
                        p1.inventory.items.append(item.upper())
                        mapd[p1.posi()]["items"] = None

                        pretty.pprint("picked up " + com[7:].upper())
                    else:
                        pretty.pprint("sorry could not find " + com[7:].upper())
                except:
                    pretty.pprint("sorry could not find " + com[7:].upper())
        elif com[:3].upper() == "USE":
            pos = p1.inventory.items
            cando = False

            for p in pos:
                if p.__str__().upper() == com[4:].upper():
                    cando = True

                    break

            if cando:
                callback.interact(com[4:], p1)
            else:
                pretty.pprint("sorry you dont have that item")
        elif com.upper() == "CREDITS":
            asset.clear()

            credd = asset.openfi("ASSETS/MAPS/SCHOOL/INFO.json", "r")
        
            cred = credd.read()
            credd.close()

            asset.petrolcredits(cred)

            asset.clear()

            last = None
        elif com[:5].upper() == "SPEAK":
            callback.speak(p1,com[6:])
        elif com[:4].upper() == "DROP":
            did = False

            for item in p1.inventory.items:
                if item.__str__().upper() == com[5:].upper():
                    did = True

                    p1.inventory.items.remove(item.__str__())

                    try:
                        mapd[p1.pos.__str__()]["items"].append(item.__str__())
                    except AttributeError:
                        mapd[p1.pos.__str__()]["items"] = []

                        mapd[p1.pos.__str__()]["items"].append(item.__str__())

                    pretty.pprint("Dropped")

                if not(did):
                    pretty.pprint("Cound not drop " + com[5:].upper())
        elif com.upper() == "END":
            pretty.pprint("Exiting")
            pretty.pprint()
            
            sys.exit()
        else:
            # all debug commands go here, they are only execed when debug flag is set, this is disabled in release builds.

            if debug:
                if com.upper() == "TP":
                    pretty.pprint("[DEBUG]")
                    pretty.pprint("debug command - not garanteed to work")
                    pretty.pprint()

                    p1.pos = asset.position(input("x: "), input("y: "))
                elif com.upper() == "WIN":
                    pretty.pprint("[DEBUG]")
                    pretty.pprint("debug command - not garanteed to work")
                    pretty.pprint()

                    p1.won = True
                    p1.health = -1
                elif com.upper() == "LOOSE":
                    pretty.pprint("[DEBUG]")
                    pretty.pprint("debug command - not garanteed to work")
                    pretty.pprint()

                    p1.won = False
                    p1.health = -1
                else:
                    pretty.pprint("<RED><BOLD>invalid command<ENDC> " + '"' + com.upper() + '"' + ", if you believe this is an error please report in on the issues page, on the github repository")
            else:
                pretty.pprint("<RED><BOLD>invalid command<ENDC> " + '"' + com.upper() + '"' + ", if you believe this is an error please report in on the issues page, on the github repository")

    asset.clear()

    #this handles the endgame stuff
    pretty.pprint()
    
    if p1.won:
        stats.addwin()
        
        if platform.system() == "Windows":
            pretty.pprint("You Won!")
        else:
            out = asset.openfi("ASSETS/END/WIN.txt")

            pretty.pprint(out.read())

            out.close()
    else:
        stats.addloose()
        
        if platform.system() == "Windows":
            pretty.pprint("You Lost!")
        else:
            out = asset.openfi("ASSETS/END/LOST.txt")

            pretty.pprint(out.read())

            out.close()

    d = asset.openfi("ASSETS/STATS/data.txt", "w")
    stat = str(stats.win) + ";" + str(stats.loose)
    d.write(stat)
    d.close()

    pretty.pprint()
    input()
