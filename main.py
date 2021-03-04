#============================================#
#               CitadelNerdBot               #
#  Written by Red X 500/RedX1000/CrownMauler #
#                                            #
#                                            #
#                                            #
#                                            #
#============================================#

import discord
import os
import requests
import json
import urllib
import sqlalchemy
import sqlite3
import playerDatabase
import numpy as np
import csv
import math
from prettytable import PrettyTable

#New Idea, add it later
#Consider comparing the new xp value with the old xp value of a player and then
#update the last time they logged in.
#I'll do this after everything is written.

conn = playerDatabase.connect()
playerDatabase.create_tables(conn)
clanListUrl = "http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName="#Todo: Add Clan Name Here


client = discord.Client()

#def urlParser(str):
#    link = urllib.parse.quote(str)
#    return link

def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " ~" + json_data[0]['a']
    return quote

def refresh():
    try:
        os.remove("members_lite.ws")
    except FileNotFoundError:
        print("File does not exist on device... yet...")

    response = requests.get(clanListUrl, allow_redirects=True)
    open('members_lite.ws', 'wb').write(response.content)

    playerList = list(csv.reader(open("members_lite.ws")))
    print(playerList)

    for x in range(0,len(playerList)):
        playerList[x][0] = playerList[x][0].replace('\xa0', ' ')

    print(playerList)

    for x in range(0,len(playerList)):
        if playerList[x][1] == "Recruit":
            print("Recruit")
            playerList[x][1] = 1
        elif playerList[x][1] == "Corporal":
            playerList[x][1] = 2
        elif playerList[x][1] == "Sergeant":
            playerList[x][1] = 3
        elif playerList[x][1] == "Lieutenant":
            playerList[x][1] = 4
        elif playerList[x][1] == "Captain":
            playerList[x][1] = 5
        elif playerList[x][1] == "General":
            playerList[x][1] = 6
        elif playerList[x][1] == "Admin":
            playerList[x][1] = 7
        elif playerList[x][1] == "Organizer":
            playerList[x][1] = 8
        elif playerList[x][1] == "Coordinator":
            playerList[x][1] = 9
        elif playerList[x][1] == "Overseer":
            playerList[x][1] = 10
        elif playerList[x][1] == "Deputy Owner":
            playerList[x][1] = 11
        elif playerList[x][1] == "Owner":
            playerList[x][1] = 12

    print(playerList)

    #Index column 0 and 1 are strings
    #Index column 2 and 3 are integers
    #Column 1 is Name      #Column 2 is Rank
    #Column 3 is Total Xp  #Column 4 is Kills

    #todo: Add a check to see if a name exists.
    #todo: It will help prevent duplicates.

    """for x in playerList:
        for y in playerList[x]:
            if y == 2 or y == 3:
                pass
            else:
                playerList[x][y] = playerList[x][y].replace("\xa0"," ")"""

    for x in range(len(playerList)):
        if x == 0:
            pass
        else:
            playerDatabase.fill_database(conn, playerList[x][0], playerList[x][1], playerList[x][2], playerList[x][3])

def clanList(command):

    # Make a list of 2d lists equal to number of rows divided by 10 rounded up
    # Place 2d lists equal to 20 total rows, so if there were 65 rows in the database
    # you'd make an array of size 4, and have 3 cells with a 2d array with 20 rows
    # and a cell with a 2d array with 5 rows.
    try:
        rows = playerDatabase.get_row_count(conn)
        rowsCeil = math.ceil(rows[0][0] / 20)
        print(command)
        dbInfo = playerDatabase.get_players(conn, command)
        print(dbInfo) #Find out why clanlist isnt being printed -_-
        finalList = []
        val = 0

        for x in range(rowsCeil):
            tempList = []
            for y in range(20):
                tempListTwo = []
                for z in range(6):
                    try:
                        tempListTwo.append(dbInfo[val][z])
                    except Exception:
                        pass
                val += 1
                tempList.append(tempListTwo)
            finalList.append(tempList)
        return finalList

    except IndexError:
        string = "Database is empty or your result does not exist. Type $refresh and try again."
        return string



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        f = open("text/helpdocument.txt","r")
        await message.channel.send(f.read())

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$reset'):
        await message.channel.send("Resetting table")
        playerDatabase.drop_table(conn)
        playerDatabase.create_tables(conn)
        refresh()
        await message.channel.send("Table reset.")

    if message.content.startswith('$inspire'):
        quote = getQuote()
        await message.channel.send(quote)

    if message.content.startswith('$update'):
        await message.channel.send("Your database has been updated... if there was a database to update...")



    if message.content.startswith('$refresh'):
        await message.channel.send("Refreshing. Stand by...")
        refresh()
        await message.channel.send("Database refreshed.")

    if message.content.startswith('$clanlist'):
        msg = str(message.content).split(" ")
        if str(message.content) == "$clanlist" or str(message.content) == "$clanlist id":
            print("clanlist id")
            db = clanList("id")
            print(db)
            check = isinstance(db, str)
            if check == True:
                await message.channel.send(db)
            else:
                for x in range(len(db)):
                    tempList = db[x]
                    myTable = PrettyTable()
                    myTable.field_names = ["ID", "Username", "Clan Rank", "XP", "Kills", "Citadel"]
                    for y in range(len(tempList)):
                        try:
                            strId = tempList[y][0]
                            strName = tempList[y][1]
                            strRank = ""

                            if tempList[y][2] == 1:
                                tempList[y][2] = "Recruit"
                            elif tempList[y][2] == 2:
                                tempList[y][2] = "Corporal"
                            elif tempList[y][2] == 3:
                                tempList[y][2] = "Sergeant"
                            elif tempList[y][2] == 4:
                                tempList[y][2] = "Lieutenant"
                            elif tempList[y][2] == 5:
                                tempList[y][2] = "Captain"
                            elif tempList[y][2] == 6:
                                tempList[y][2] = "General"
                            elif tempList[y][2] == 7:
                                tempList[y][2] = "Admin"
                            elif tempList[y][2] == 8:
                                tempList[y][2] = "Organiyer"
                            elif tempList[y][2] == 9:
                                tempList[y][2] = "Coordinator"
                            elif tempList[y][2] == 10:
                                tempList[y][2] = "Overseer"
                            elif tempList[y][2] == 11:
                                tempList[y][2] = "Deputy Owner"
                            elif tempList[y][2] == 12:
                                tempList[y][2] = "Owner"

                            strRank = tempList[y][2]
                            strXp = tempList[y][3]
                            strKills = tempList[y][4]
                            strCitadel = ""

                            if tempList[y][5] == 0:
                                strCitadel = "No Visit"
                            elif tempList[y][5] == 1:
                                strCitadel = "Visited"
                            elif tempList[y][5] == 2:
                                strCitadel = "Capped"
                            elif tempList[y][5] == 3:
                                strCitadel = "Private"

                            myTable.add_row([strId, strName, strRank, strXp, strKills, strCitadel])

                        except Exception:
                            pass

                    myTable.align["ID"] = "r"
                    myTable.align["Username"] = "l"
                    myTable.align["Clan Rank"] = "l"
                    myTable.align["XP"] = "l"
                    myTable.align["Kills"] = "l"
                    myTable.align["Citadel"] = "c"
                    playerInfoStr = "```\n" + myTable.get_string() + "\n```"
                    await message.channel.send(playerInfoStr)
                await message.channel.send("```Clan list displayed. *XP  = XP gained since joined```")
        elif(len(msg) != 2):
            await message.channel.send("State clanlist order: $clanlist <id|alpha|rank|citadel>")
        else:
            commands = ["alpha","rank","citadel"]
            if any(x in msg[1] for x in commands):
                db = clanList(msg[1])
                check = isinstance(db, str)
                if check == True:
                    await message.channel.send(db)
                else:
                    for x in range(len(db)):
                        tempList = db[x]
                        myTable = PrettyTable()
                        myTable.field_names = ["ID", "Username", "Clan Rank", "XP", "Kills", "Citadel"]
                        for y in range(len(tempList)):
                            try:
                                strId = tempList[y][0]
                                strName = tempList[y][1]
                                strRank = ""

                                if tempList[y][2] == 1:
                                    tempList[y][2] = "Recruit"
                                elif tempList[y][2] == 2:
                                    tempList[y][2] = "Corporal"
                                elif tempList[y][2] == 3:
                                    tempList[y][2] = "Sergeant"
                                elif tempList[y][2] == 4:
                                    tempList[y][2] = "Lieutenant"
                                elif tempList[y][2] == 5:
                                    tempList[y][2] = "Captain"
                                elif tempList[y][2] == 6:
                                    tempList[y][2] = "General"
                                elif tempList[y][2] == 7:
                                    tempList[y][2] = "Admin"
                                elif tempList[y][2] == 8:
                                    tempList[y][2] = "Organiyer"
                                elif tempList[y][2] == 9:
                                    tempList[y][2] = "Coordinator"
                                elif tempList[y][2] == 10:
                                    tempList[y][2] = "Overseer"
                                elif tempList[y][2] == 11:
                                    tempList[y][2] = "Deputy Owner"
                                elif tempList[y][2] == 12:
                                    tempList[y][2] = "Owner"

                                strRank = tempList[y][2]
                                strXp = tempList[y][3]
                                strKills = tempList[y][4]
                                strCitadel = ""

                                if tempList[y][5] == 0:
                                    strCitadel = "No Visit"
                                elif tempList[y][5] == 1:
                                    strCitadel = "Visited"
                                elif tempList[y][5] == 2:
                                    strCitadel = "Capped"
                                elif tempList[y][5] == 3:
                                    strCitadel = "Private"

                                myTable.add_row([strId, strName, strRank, strXp, strKills, strCitadel])

                            except Exception:
                                pass

                        myTable.align["ID"] = "r"
                        myTable.align["Username"] = "l"
                        myTable.align["Clan Rank"] = "l"
                        myTable.align["XP"] = "l"
                        myTable.align["Kills"] = "l"
                        myTable.align["Citadel"] = "c"
                        playerInfoStr = "```\n" + myTable.get_string() + "\n```"
                        await message.channel.send(playerInfoStr)
                await message.channel.send("```Clan list displayed. *XP  = XP gained since joined```")
            else:
                await message.channel.send("State clanlist order: $clanlist <id|alpha|rank|citadel>")

    if message.content.startswith('$remove'):
        try:
            msg = str(message.content).split(" ", 2)
            print(msg)
            print(msg[1] + " " + "name")
            print(msg[1] + " " + "id")
            if msg[1] == "name":
                await message.channel.send("Removing "+msg[2]+"...")
                print("Removing from database")
                playerDatabase.remove_player_by_name(conn, msg[2])
                print("removed.")
                await message.channel.send("Removed successfully!")

            elif msg[1] == "id":
                val = int(msg[2])
                await message.channel.send("Removing user at ID "+msg[2]+"...")
                playerDatabase.remove_player_by_id(conn, val)
                print("removed.")
                await message.channel.send("Removed successfully!")
            else:
                await message.channel.send("Insert a name: $remove <name|id> <username|database ID>")

        except Exception:
            await message.channel.send("Insert a name: $remove <name|id> <username|database ID>")

    #https://apps.runescape.com/runemetrics/profile/profile?user=XXX&activities=20

client.run('')#Todo: Add Discord bot token here