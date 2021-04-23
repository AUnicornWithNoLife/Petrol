import os

import petrolasset as asset
import pretty

def menu(info, stats):
    d = asset.openfi("ASSETS/SETTINGS/config.txt", "r")
    settings = d.read()
    settings = settings.split("\n")
    de = settings[0]
    d.close()

    debug = bool(de)

    last = None

    dodo = True

    while dodo:
        asset.clear()

        print("[EXTRA]")
        print()

        print("0: Settings")
        print("1: Petrol Credits")
        print("2: Source")
        print("3: License")
        print("4: Stats")
        print("5: Info")
        print("6: Exit")
        print()

        a = int(input("? "))

        print()

        if a == 0:
            dododo = True

            while dododo:
                asset.clear()
                
                print("[settings]")
                print()
                print("0: Debug - " + str(debug))
                print("1: Back")
                print()
                print("You may have to reload for settings to update")
                print()

                b = int(input("? "))

                if b == 0:
                    debug = not(debug)

                    togo = None

                    if debug:
                        togo = "1"
                    else:
                        togo = "0"

                    togofi = asset.openfi("ASSETS/SETTINGS/config.txt", "w")
                    settings = togo.split(';')

                    togofi.write(asset.settingsset(settings))

                    togofi.close()
                elif b == 1:
                    dododo = False
                else:
                    print("Error")
                
        elif a == 1:
            print("Petrol Made by AUnicornWithNoLife")

            input()
        elif a == 2:
            print(info.repo)

            input()
        elif a == 3:
            li = asset.openfi("ASSETS/LI/LICENSE", "r")
            print(li.read())
            li.close()

            input()
        elif a == 4:
            asset.clear()
            
            print("Wins: " + str(stats.win))
            print("Looses: " + str(stats.win))

            input()
        elif a == 5:
            print(info)

            input()
        elif a == 6:
            asset.clear()

            dodo = False
        else:
            print("Error")

            input()

        print()

def editsave():
    while True:
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

        delno = input("DEL? ")

        if delno == "exit":
            return

        asset.saveINV(delno)