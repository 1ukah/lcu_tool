from lcu_driver import Connector
from time import sleep
from urllib3 import disable_warnings
from os import system
import ctypes
import sys
import psutil

disable_warnings()

def newLine():
    print("="*35)

def globalSleep():
    sleep(3.5)

ctypes.windll.kernel32.SetConsoleTitleW("▶ Requests ◀")

# Initializing LCU_DRIVER
connector = Connector()

# If LeagueClient is running we continue, if not we return
if "LeagueClient.exe" in (p.name() for p in psutil.process_iter()):
    print("[▲] The League Client was found.")
    sleep(2.5)
else:
    print("[▶] League Client was not found. Open or restart the client!")
    sleep(10)
    sys.exit()

def Menu():
    system('cls')
    print("           ▶ Requests ◀")
    newLine()
    print("""[1] -> Change Availability
[2] -> Icon Changer
[3] -> Background Changer
[4] -> Remove all friends
[5] -> Practice Tool with bots
[6] -> Auto Accept
[7] -> Aram Boost
[8] -> Lobby Crasher
[9] -> Get free Tristana + Riot Girl skin
[0] -> Exit """)

async def getOption(connection):
    global menuOption
    newLine()
    menuOption = int(input("[▲] Function: "))
    system('cls')

async def getInfo(connection):
    response = await connection.request("GET", "/lol-summoner/v1/current-summoner")
    if response.status == 200:
        data = await response.json()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

    print(f"Name: {data['displayName']}")
    print(f"Level: {data['summonerLevel']}")

async def setOnline(connection):
    response = await connection.request("PUT", "/lol-chat/v1/me", data={"availability": "chat"})
    if response.status == 201:
        print("[▲] The request was successfully done, your status was set to Online!")
        globalSleep()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

async def setOffline(connection):
    response = await connection.request("PUT", "/lol-chat/v1/me", data={"availability": "offline"})
    if response.status == 201:
        print("[▲] The request was successfully done, your status was set to Offline!")
        globalSleep()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

async def setAway(connection):
    response = await connection.request("PUT", "/lol-chat/v1/me", data={"availability": "away"})
    if response.status == 201:
        print("[▲] The request was successfully done, your status was set to Away!")
        globalSleep()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

async def setMobile(connection):
    response = await connection.request("PUT", "/lol-chat/v1/me", data={"availability": "mobile"})
    if response.status == 201:
        print("[▲] The request was successfully done, your status was set to LoL+!")
        globalSleep()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

async def setIcon(connection):
    id = int(input("[▲] Icon ID: "))
    response = await connection.request("PUT", "/lol-chat/v1/me", data={"icon": id})
    if response.status == 201:
        print("[▲] The request was successfully done, your icon has been changed!")
        globalSleep()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

async def setBackground(connection):
    id = int(input("[▲] Background ID: "))
    response = await connection.request("POST", "/lol-summoner/v1/current-summoner/summoner-profile", data={"key": "backgroundSkinId", "value": id})
    if response.status == 200:
        print("[▲] The request was successfully done, your profile background has been changed!")
        globalSleep()
    else:
        print(f"[▶] The operation was stopped due to an error during the request. ERROR CODE: {response.status}")
        globalSleep()

async def deleteFriends(connection):
    friends = await connection.request("GET", "/lol-chat/v1/friends")
    if friends.status == 200:
        response = await friends.json()
        dados = response
        choice = str(input("[▲] Are you sure that you wanna delete all your friends?([Y]es/[N]o): ").upper())
        if choice == "YES" or "Y":
            for d in dados:
                x = d["id"]
                name = d["name"]
                delete = await connection.request("DELETE", f"/lol-chat/v1/friends/{x}")
                if delete.status == 204:
                    print(f"[▲] The summoner '{name}' has been deleted from your friend list.")
                    print("[▲] The operation was successfully done, your friend list has been cleared!")
        elif choice == "NO" or "N":
            print(f"[▶] The operation was stopped.")
    globalSleep()
      
async def practiceTool(connection):
    LobbyConfig = {
    'customGameLobby': {
        'configuration': {
        'gameMode': 'PRACTICETOOL', 
        'gameMutator': '', 
        'gameServerRegion': '', 
        'mapId': 11, 
        'mutators': {'id': 1}, 
        'spectatorPolicy': 'AllAllowed', 
        'teamSize': 5
        },
        'lobbyName': 'PRACTICETOOL',
        'lobbyPassword': ''
    },
    'isCustom': True
    }
    await connection.request("POST", "/lol-lobby/v2/lobby", data = LobbyConfig)
    print("[▲] The Practice Tool lobby has been crated.")
    globalSleep()

async def autoAccept(connection):
    while True:
        response = await connection.request("GET", "/lol-lobby/v2/lobby/matchmaking/search-state")
        status = await response.json()
        system('cls')
        print("[▲] Searching match...")
        globalSleep()
        if status['searchState'] == "Found":           
            await connection.request("POST", "/lol-matchmaking/v1/ready-check/accept")
            print("[▲] The match was successfully accepted!")
            sleep(11)
            select = await connection.request("GET", "/lol-champ-select/v1/session")
            if select.status == 200:
                break
            else:
                print("[▶] The match was not accepted.")       
        elif status['searchState'] == "Invalid":
            print("[▶] You are not in queue.") 
            globalSleep()   
            break    

async def aramBoost(connection):
    select = await connection.request("GET", "/lol-champ-select/v1/session")
    response = await select.json()

    if select.status == 404:
        print("[▶] You are only able to use Aram Boost during a champion select.")
        globalSleep()

    elif response["isCustomGame"] == True:
        print(response)
        print("[▶] You can not use Aram Boost in a custom game.")
        globalSleep()

    elif select.status == 200:
        print("[▲] Press any key to use the Aram Boost.")
        input()
        await connection.request("POST", '/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["", "teambuilder-draft", "activateBattleBoostV1", ""]')
        system('cls')
        print("[▲] The request was successfully done, your Aram lobby has been boosted!")
        globalSleep()
        
async def lobbyCrasher(connection):
    await connection.request("POST", "/lol-gameflow/v1/session/request-enter-gameflow")
    await connection.request("DELETE", "/lol-lobby/v2/lobby")
    queue = {'queueId': 1110}
    await connection.request("POST", "/lol-lobby/v2/matchmaking/quick-search", data=queue)
    print("[▲] The lobby has been successfully crashed.")
    globalSleep()

async def getTristana(connection):
    await connection.request("POST", "/lol-login/v1/session/invoke?destination=inventoryService&method=giftFacebookFan&args=[]")
    print("[▲] The Tristana + Riot Girl skin has been activated. Please restart your client!")
    sleep(10)
    sys.exit()

@connector.ready
async def connect(connection):
    Menu()
    newLine()
    await getInfo(connection)
    await getOption(connection)
    while menuOption !=0:
        if menuOption == 1:
            system('cls')
            newLine()
            print("""[1] -> Online
[2] -> Offline
[3] -> Away
[4] -> LoL+
[5] -> Return to menu""")
            newLine()
            escolha = int(input("[▲] Mode: "))
            if escolha == 1:
                await setOnline(connection)
                Menu()
                await getOption(connection)
            elif escolha == 2:
                await setOffline(connection)
                Menu()
                await getOption(connection)
            elif escolha == 3:
                await setAway(connection)
                Menu()
                await getOption(connection)
            elif escolha == 4:
                await setMobile(connection)
                Menu()
                await getOption(connection)
            elif escolha == 5:
                globalSleep()
                Menu()
                await getOption(connection)
            else:
                print("[▶] You have chosen an invalid mode.")
                globalSleep()
                Menu()
                await getOption(connection)
        elif menuOption == 2:
            await setIcon(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 3:
            await setBackground(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 4:
            await deleteFriends(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 5:
            await practiceTool(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 6:
            await autoAccept(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 7:
            await aramBoost(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 8:
            await lobbyCrasher(connection)
            Menu()
            await getOption(connection)
        elif menuOption == 9:
            await getTristana(connection)
            Menu()
            await getOption(connection)
        else:
            print("[▶] You have chosen an invalid option.")
            globalSleep()
            Menu()
            await getOption(connection)    
    else:
        print("[▶] The program has been closed.")
        globalSleep()
        sys.exit()

@connector.close
async def disconnect(connection):
    print("[▶] Disconnected.")

connector.start()