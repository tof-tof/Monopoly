import random
import time
import json
import copy


def Valid_PayRent(gamestate, userMove, player_ids, player_index):
    current_location=gamestate["player_info"][player_id[player_index]]["current_location"]
    current_location_place_index= gamestate["board"][int(current_location/4)][current_location-4*int(current_location/4)]
    if not "target" in userMove:
        return "Error: no target place to pay rent to specified"
    elif not isinstance(userMove["target"],int):
        return "Error: Invalid key: target must be a place_index (int type)"
    elif userMove["target"] != current_location_place_index:
        return "Error: place specified is not current location, As a penalty, double rent will be paid"
    elif "Rent" in gamestate["place_database"][userMove["target"]] and gamestate["place_database"][current_location_place_index]["owner"]!=-1 : # checking that the place can be paid rent to can also be checked by owner = -2
        rent = gamestate["place_database"][userMove["target"]]["Rent"]
        player_value = total_assets(gamestate,player_index, player_ids)
        # NB:this function is the only way a player can become bankcrupt
        if "price" in userMove:
            if not isinstance(userMove["price"],int):
                return "Error: Invalid key: price must be a integer"
            elif userMove["price"] != rent:
                if player_value < rent*2: # checking bankcruptcy
                    return "Error: price specified is not the Rent price. "+player_ids[player_index]+" cannot afford increased rent and so is bankcrupt"
                else:
                    return "Error: price specified is not the Rent price. As a penalty, double rent will be paid"
            else:
                if player_value < rent:
                    return player_ids[player_index] + " bankrupt"
                elif gamestate["player_info"][player_ids[player_index]]["money"] < rent: # got the value right, but have you got the money to pay?
                    return "Error: insufficient funds"
                else:
                    return ""
        else:
            return "Error: price specified is not the Rent price. As a penalty, double rent will be paid"
    # your trying to pay rent to go or in jail
    else:
        return "Error: Cannot pay rent to this place"



def Valid_Command(userMove):
    commands = ["buy", "pay rent", "chance", "pay bribe", "skip"]
    if "command" in userMove:
        userMove["command"] = userMove["command"].lower()
        if userMove["command"] in commands:
            return ''
        else:
            return "Error: Invalid command has been made"
    else:
        return "Error: no command made"

# place index = their current location
def Valid_Skip(gamestate, place_index, player_id):
    # check they don't have to pay rent
    owner = gamestate["place_database"][place_index]["owner"]
    if owner == -2 or owner == -1 or owner == player_id:
        return ""
    else:
        return "Error: must pay rent. As a penalty, double rent will be paid "

def Valid_Bribe(gamestate, player_id):
    # checking if they have enough money to pay the bribe
    if gamestate["player_info"][player_id]["money"] < gamestate["bribe"]:
        return "Error: insufficient funds"
    elif not gamestate["player_info"][player_id]["in_jail"]:
        return "Error: Not in jail"
    else:
        return ""


def Valid_Buy(gamestate, userMove, player_ids, player_index):
    # checking the place is free to be bought
    if "target" in userMove:
        place_index=userMove["target"]
        owner = gamestate["place_database"][place_index]["owner"]
        current_location=gamestate["player_info"][player_ids[player_index]]["current_location"]
        current_location_place_index=gamestate["board"][int(current_location/4)][current_location-4*int(current_location/4)]
        if "buyPrice" in gamestate["place_database"][place_index]:
            buyPrice = gamestate["place_database"][place_index]["buyPrice"]
        else:
            # why are you trying to buy go?
            return "Error: place cannot be owned"
        if not "price" in userMove:
            return "Error: no price specified."
        elif userMove["price"] != buyPrice:  # got the buy price wrong
            return "Error: price specified is not the buy price."
        # checking the place is free to be bought
        elif owner == player_index:
            return "Error: place already owned"
        elif owner != -1:
            return "Error: place owned by someone else"
        elif gamestate["player_info"][player_ids[player_index]]["money"] < buyPrice:
            return "Error: insufficient funds"
        elif current_location_place_index !=place_index:
            return "Error: not on place trying to buy"
        else:
            return ""
    else:
        return "Error: No target place specified for buy"



def Valid_UseGOJ(gamestate, player_id):
    if gamestate["player_info"][player_id]["hasGOJ"]:
        return ""
    else:
        return "Error: player doesn't have get out of jail free card"


def Valid_Sell(gamestate, place_index, player_index): #called for every place in sell list
    # checking the place belongs to the player
    try:
        inRange = place_index<0 or place_index>15
    except TypeError:
        return "Error: Invalid type: sell targets must be place_indexes (int)"
    else:
        if place_index<0 or place_index>15:
            return "Error: invalid index given"
        elif gamestate["place_database"][place_index]["owner"] != player_index:
            return 'Error: not owner of the place'
        else:
            return ''

def Valid_Chance(userMove):
   if check_c(player_id,player_index,general_game_state)!="":
       return check_c(player_id,player_index,general_game_state)
   try:
       res = userMove["target"] >= 0 and userMove["target"] <= 2
   except KeyError:
       return "Error: No target place specified for chance"
   else:
       if res:
           return ""
       else:
           return "Error: Invalid target card specified for chance"

def check_in_jail(player_id,player_index,board_size,general_game_state):
   if general_game_state["player_info"][player_id[player_index]]["current_location"] == board_size*2:
       return ""
   else:
       return "Error: not in jail"

def check_c(player_id,player_index,general_game_state):
   if general_game_state["place_database"][general_game_state["player_info"][player_id[player_index]]["current_location"]]["name"] in ["chance","Community Chest"]:
       return ""
   else:
       return "Error: Not on community chest or chance"

def sell(move,general_game_state,player_id,player_index):
   try:
       target = move["sell"]
   except KeyError:
       return [general_game_state,'']
   else:
       valid_sell=True
       # make sure they give us a list rather than a value, and turn it into a singleton list if they do provide a value
       if isinstance(target, list):
           for place_id in target:
               if Valid_Sell(general_game_state,place_id,player_index) != '':
                   valid_sell=False
                   StepText = Valid_Sell(general_game_state,place_id,player_index)
                   return [general_game_state, StepText]
       else:
           vaild_sell = False
           StepText = "Error: Invalid value: sell must be of type list"
           return [general_game_state, StepText]
   if valid_sell:
           StepText=""
           for place_id in target:
               general_game_state["place_database"][place_id]["owner"] = -1
               general_game_state["player_info"][player_id[player_index]]["money"] += 0.5*general_game_state["place_database"][place_id]["buyPrice"]
               StepText += player_id[player_index]+" sold "+general_game_state["place_database"][place_id]["name"]+". "
           return [general_game_state,StepText]



def roll_dice(player_id,player_index,general_game_state):
    if not general_game_state["player_info"][player_id[player_index]]["in_jail"]:    #Checks whether player in jail
        dice=random.randrange(1,7,1)        #Produce random number in 1,2,3,4,5,6
        name=player_id[player_index]
        general_game_state["player_info"][name]["current_location"]+=dice   #Move the player forward by dice spaces
        if general_game_state["player_info"][name]["current_location"] >= general_game_state["board_size"]*4:
            general_game_state["player_info"][name]["current_location"] -= general_game_state["board_size"]*4
            general_game_state["player_info"][name]["money"] += general_game_state["go_money"]                  #Add start money if the player does
        if general_game_state["player_info"][name]["current_location"] == general_game_state["board_size"]*2:
            general_game_state["player_info"][player_id[player_index]]["in_jail"] = True
    return general_game_state

def shuffle_sides(general_game_state):
    side0 = [i for i in range(1, general_game_state["board_size"])]     #first side made of locations go ,1,2...board_size-1
    side2 = [i for i in range(general_game_state["board_size"] * 2 + 1, general_game_state["board_size"] * 3)]  #third side made of go to jail,2*board_size+1...3*board_size-1
    random.shuffle(side0)   #Shuffle all the moveable locations
    random.shuffle(side2)
    side0 = [0] + side0     #Add start back to the first side
    side2 = [2*general_game_state["board_size"]] + side2   #Add go to jail back to third side
    general_game_state["board"][0] = side0  #update the board
    general_game_state["board"][2] = side2
    random.shuffle(general_game_state["board"][1])     #All locations on second and forth sides are moveable so shuffle directly
    random.shuffle(general_game_state["board"][3])
    return general_game_state

def total_assets(general_game_state,player_index,player_id):
    asset = general_game_state["player_info"][player_id[player_index]]["money"]
    for place_id in general_game_state["place_database"]:
        if general_game_state["place_database"][place_id]["owner"]==player_index:
            asset += general_game_state["place_database"][place_id]["buyPrice"]*0.5
    return asset
# return porperty back to the bank
def return_props(gamestate,player_index):
   for place in gamestate["place_database"]:
       if gamestate["place_database"][place]["owner"] == player_index:
           gamestate["place_database"][place]["owner"] = -1
   return gamestate

def count_survivors(general_game_state,player_id):        #Count the number of people still in game
   survivors = 0
   for player in player_id:
       if general_game_state["player_info"][player]["in_game"]:
           survivors += 1
   return survivors

def find_winner(general_game_state,player_id):              #Find winner by bankruptting everyone else
   for i in range(len(general_game_state["player_info"])):
       if general_game_state["player_info"][player_id[i]]["in_game"]:
           return i

def find_winners(general_game_state,player_id):             #Find winner when move limit is reached
   asset_list = []
   player_list =[]
   for i in range(len(general_game_state["player_info"])):  # player_list and asset_list are connected lists
       if general_game_state["player_info"]["in_game"]: # player info is indexed on player_id
           player_list.append(i)
           asset=total_assets(general_game_state,i,player_id)
           asset_list.append(asset)
   max_asset=max(asset_list)
   winners_indexes = []
   for j in range(len(player_id)):
       if asset_list[j]==max_asset:
           winners_indexes.append(player_id.index(player_list[j]))
   return winners_indexes

def bankrupt(general_gamestate,player_id,player_index,asset,owner):
    general_gamestate["player_info"][player_id[player_index]]["in_game"] = False
    general_gamestate = return_props(general_gamestate, player_index)
    general_gamestate["player_info"][player_id[owner]]["money"]+=asset
    return general_gamestate

def str_to_int(place_database):
    place_database_int = {}
    for place in place_database:  # Make the key of dictionary that stores place data into integers
        place_id = int(place)
        place_database_int[place_id] = place_database[place]
    return place_database_int

# move should not be called if general_gamestate["player_info"][player_id[player_index]]["in_game"] == False
# player_id is a list of bot names
# player_index is the index of the current player moving
def move(player_index, player_id, general_gamestate, move):
    general_gamestate["place_database"]= str_to_int(general_gamestate["place_database"])
    current_time = time.time()*1000
    if current_time >= general_gamestate["response_deadline"] :
        if count_survivors(general_gamestate, player_id) == 2:
            general_gamestate["player_info"][player_id[player_index]]["in_game"] = False
            general_gamestate = return_props(general_gamestate,player_index)
            general_gamestate["Mover"] = -1
            winner_index = find_winner(general_gamestate, player_id)
            general_gamestate["GameStatus"] = "PLAYER_" +str(winner_index)+"_WON_BY_TIMEOUT"
            new_game_state = {
                "Result": "GAME_HAS_ENDED_BY_TIMEOUT",
                "StepText": player_id[player_index]+ " has timed out. One player left standing",
                "NewDeal": False,
                "WinnerIndex": winner_index,
                "Announcement": "All other players out of game. " + player_id[winner_index] + " won.",
                "GeneralGameStates": [general_gamestate],
                "SpecificGameState": general_to_specific(player_id, player_index, general_gamestate),
            }
            return new_game_state
        else:
            general_gamestate["player_info"][player_id[player_index]]["in_game"] = False
            general_gamestate = return_props(general_gamestate, player_index)
            new_game_state = {
                "Result": "INVALID_MOVE",
                "ErrorMessage":player_id[player_index]+ " has timed out and lost" ,
                "NewDeal": False,
                "GeneralGameStates": [general_gamestate],
                "SpecificGameState": general_to_specific(player_id, player_index,general_gamestate),
            }
            return new_game_state
    if general_gamestate["move_number"] == general_gamestate["move_limit"] :
        winners = find_winners(general_gamestate,player_id) # list of indexes
        if len(winners) == 1:
            winner_index = winners[0]
        else:
            winner_index = -1
        winners_string = ""
        for winner in winners:
            winners_string+= player_id[winner]+" "
        general_gamestate["Mover"] = -1
        new_game_state = {
            "Result": "GAME_HAS_ENDED",
            "StepText": "move limit reached. Game finished",
            "NewDeal": False,
            "WinnerIndex": winner_index,
            "Announcement": "move limit reached. Game finished. "+winners_string+ "won",
            "GeneralGameStates": [general_gamestate],
            "SpecificGameState": general_to_specific(player_id,player_index,general_gamestate)
        }
        return new_game_state
    """    
        User move is a dictionary/ json
        {"sell": (not nessary, only if they want to sell)[target1,target2 ...], where the values are in
         "command":"buy"/"pay rent"/"chance"/"pay bribe"/"skip", 
         "target": place_id to buy or chance to pick 
         "price": (only put in if "buy" or "pay rent") the price they have to pay}
    """
    current_location = general_gamestate["player_info"][player_id[player_index]]["current_location"]
    location_id= general_gamestate["board"][int(current_location / 4)][current_location - 4 * int(current_location / 4)]
    StepText = ""
    owner = general_gamestate["place_database"][location_id]["owner"]
    total_asset = total_assets(general_gamestate, player_index, player_id)
    if "Rent" in general_gamestate["place_database"][location_id]:
        rent=general_gamestate["place_database"][location_id]["Rent"]
    else:
        rent = -1
    if owner != player_index and total_asset<rent:
        general_gamestate=bankrupt(general_gamestate, player_id, player_index, total_asset, owner)
        StepText = player_id[player_index]+' has to pay '+str(general_gamestate["place_database"][location_id]["Rent"])+' to '+player_id[owner]+" as rent, but does not have sufficient funds. "
        StepText += player_id[player_index] + ' has bankrupted. '
        if count_survivors(general_gamestate,player_id)==1:
            new_game_state = {
                "Result": "GAME_HAS_ENDED",
                "StepText": [StepText],
                "NewDeal": False,
                "WinnerIndex": owner,
                "Announcement": "All other players bankrupt. " + player_id[owner] + " won.",
                "GeneralGameStates": [general_gamestate],
                "SpecificGameState": general_to_specific(player_id, player_index, general_gamestate),
            }
            return new_game_state
        else:
            new_game_state = {
                "Result": "SUCCESS",
                "StepTexts": [StepText],
                "NewDeal": False,
                "GeneralGameStates": [general_gamestate],
                "SpecificGameState": general_to_specific(player_id, player_index, general_gamestate)
            }
            return new_game_state
    if Valid_Command(move) == "":
        if move["command"] == "buy":
            if Valid_Buy(general_gamestate, move, player_id, player_index) == "":
                [general_gamestate,StepText]=sell(move, general_gamestate, player_id, player_index)
                if "Error" not in StepText:
                    target = move["target"]
                    general_gamestate["place_database"][target]["owner"] = player_index
                    general_gamestate["player_info"][player_id[player_index]]["money"] -= general_gamestate["place_database"][target]["buyPrice"]
                    StepText += player_id[player_index] + " bought " + general_gamestate["place_database"][target]["name"]
                else:
                    new_game_state = {
                        "Result": "INVALID_MOVE",
                        "ErrorMessage": StepText
                    }
                    return new_game_state
                if general_gamestate["place_database"][location_id]["owner"] not in [player_index,-1]:    #Actually player on location not owned
                    rent = general_gamestate["place_database"][location_id]["Rent"]*2
                    if total_asset<rent:
                        StepText += player_id[player_index]+" has to pay double rent but does not have enough assets. " + player_id[player_index]+' is bankruptted'
                        general_gamestate["player_info"][player_id[owner]]["money"] += total_asset
                        general_gamestate=return_props(general_gamestate, player_index)
                        general_gamestate["player_info"][player_id[owner]]["in_game"]=False
                        if count_survivors(general_gamestate, player_id) == 1:
                            new_game_state = {
                                "Result": "GAME_HAS_ENDED",
                                "StepText": [StepText],
                                "NewDeal": False,
                                "WinnerIndex": owner,
                                "Announcement": "All other players bankrupt. " + player_id[owner] + " won.",
                                "GeneralGameStates": [general_gamestate],
                                "SpecificGameState": general_to_specific(player_id, player_index, general_gamestate),
                            }
                            return new_game_state
                    else:
                        general_gamestate["player_info"][player_id[player_index]]["money"] -= rent
                        general_gamestate["player_info"][player_id[owner]]["money"] += rent
                        StepText += player_id[player_index] + " should pay rent instead of buy, as a penalty double rent is paid. "
                        StepText += player_id[player_index] + " paid " + player_id[owner] + ' ' + str(rent) + ' as rent.'
            else:
                new_game_state = {
                    "Result": "INVALID_MOVE",
                    "ErrorMessage": Valid_Buy(general_gamestate, move, player_id, player_index),
                }
                return new_game_state
        elif move["command"] == "pay rent":
            valid = Valid_PayRent(general_gamestate, move, player_id,player_index)
            print(valid)
            if  valid == "":
                [general_gamestate,StepText] = sell(move, general_gamestate, player_id, player_index)
                if 'Error' not in StepText:
                    rent = general_gamestate["place_database"][location_id]["Rent"]
                    general_gamestate["player_info"][player_id[player_index]]["money"] -= rent
                    general_gamestate["player_info"][player_id[owner]]["money"] += rent
                    StepText += player_id[player_index]+" paid "+player_id[owner]+" "+str(rent)+" for rent"
                else:
                    new_game_state = {
                        "Result": "INVALID_MOVE",
                        "ErrorMessage": StepText
                    }
                    return new_game_state
            elif "As a penalty, double rent will be paid" in valid:
                [general_gamestate, StepText] = sell(move, general_gamestate, player_id,player_index)
                if 'Error' not in StepText:
                    rent = general_gamestate["place_database"][location_id]["Rent"]*2
                    general_gamestate["player_info"][player_id[player_index]]["money"] -= rent
                    general_gamestate["player_info"][player_id[owner]]["money"] += rent
                    StepText += player_id[player_index] + " paid " + player_id[owner] + " " + str(rent) + " for rent"
                else:
                    new_game_state = {
                        "Result": "INVALID_MOVE",
                        "ErrorMessage": StepText
                    }
                    return new_game_state
            elif "bankcrupt" in valid:
                general_gamestate["player_info"][player_id[player_index]]["in_game"] = False
                if count_survivors(general_gamestate,player_id) == 2:
                    general_gamestate = return_props(general_gamestate, player_index)
                    general_gamestate["player_info"][player_id[owner]]["money"] += total_assets(general_gamestate,player_index,player_id)
                    winner_index = find_winner(general_gamestate, player_id)
                    general_gamestate["GameStatus"] = "PLAYER_" +str(winner_index)+"_WON_BY_TIMEOUT"
                    new_game_state = {
                        "Result": "GAME_HAS_ENDED",
                        "StepText": valid,
                        "NewDeal": False,
                        "WinnerIndex": winner_index,
                        "Announcement" : "All other players bankcrupt. "+player_id[winner_index]+" won.",
                        "GeneralGameStates":[general_gamestate],
                        "SpecificGameState": general_to_specific(player_id,player_index,general_gamestate),
                    }
                    return new_game_state
                else:
                    new_game_state = {
                        "Result": "INVALID_MOVE",
                        "ErrorMessage": valid}
            else:
                new_game_state = {
                    "Result": "INVALID_MOVE",
                    "ErrorMessage": valid}
                return new_game_state
        elif move["command"] == "pay bribe":
            [general_gamestate, StepText] = sell(move, general_gamestate, player_id,player_index)
            if "Error" not in StepText:
                if Valid_Bribe(general_gamestate, player_id[player_index]) == "":
                    if 'Error' not in StepText:
                        general_gamestate["player_info"][player_id[player_index]]["money"] -= general_gamestate["bribe"]
                        general_gamestate["player_info"][player_id[player_index]]["in_jail"] = False
                        StepText += player_id[player_index] + " paid the bribe to get out from jail"
                else:
                    new_game_state = {
                        "Result": "INVALID_MOVE",
                        "ErrorMessage": Valid_Bribe(general_gamestate, player_id[player_index]),
                        "NewDeal": False
                    }
                    return new_game_state
            else:
                new_game_state = {
                    "Result": "INVALID_MOVE",
                    "ErrorMessage": StepText
                }
                return new_game_state
        elif move["command"] == "skip":
            if Valid_Skip(general_gamestate, current_location, player_id[player_index]) == "":
                [general_gamestate, StepText]=sell(move, general_gamestate, player_id, player_index)
                if StepText == '':
                    StepText=player_id[player_index]+" did nothing."
                else:
                    new_game_state = {
                        "Result": "INVALID_MOVE",
                        "ErrorMessage": StepText
                    }
                    return new_game_state
            else:
                location_id = general_gamestate["board"][int(current_location / 4)][current_location - 4 * int(current_location / 4)]
                rent = general_gamestate["place_database"][location_id]["Rent"] * 2
                general_gamestate["player_info"][player_id[player_index]]["money"] -= rent
                owner = general_gamestate["place_database"][location_id]["owner"]
                general_gamestate["player_info"][player_id[owner]]["money"] += rent
                StepText += player_id[player_index] + " paid " + player_id[owner] + " " + str(rent) + " for rent"
                new_game_state = {
                    "Result": "SUCCESS",
                    "ErrorMessage": Valid_Skip(general_gamestate, current_location,player_id[player_index]),
                    "NewDeal": False,
                    "GeneralGameStates": [general_gamestate],
                    "SpecificGameState": general_to_specific(player_id,player_index,general_gamestate),
                }
                return new_game_state
        general_gamestate = shuffle_sides(general_gamestate)
        if not general_gamestate['player_info'][player_id[player_index]]["in_jail"]:
            general_gamestate = roll_dice(player_id, player_index, general_gamestate)
        general_gamestate["Mover"] = (general_gamestate["Mover"] +1) % len(player_id) # two would be changed to the number of players
        general_gamestate["move_number"] += 1

        new_game_state = {
            "Result": "SUCCESS",
            "StepTexts": [StepText],
            "NewDeal": False,
            "GeneralGameStates": [general_gamestate],
            "SpecificGameState": general_to_specific(player_id, player_index, general_gamestate)
        }
        return new_game_state
    else:

        new_game_state = {
            "Result": "INVALID_MOVE",
            "ErrorMessage": Valid_Command(move),
        }
        return new_game_state


def general_to_specific(player_id,player_index,general_gamestate):
    send_database = copy.deepcopy(general_gamestate["place_database"])
    for id in send_database:
        send_database[id].pop("images")

    money=general_gamestate["player_info"][player_id[player_index]]["money"]
    in_jail=general_gamestate["player_info"][player_id[player_index]]["in_jail"]
    location=general_gamestate["player_info"][player_id[player_index]]["current_location"]
    on_CH=general_gamestate["player_info"][player_id[player_index]]["on_CH"]
    hasGOJ=general_gamestate["player_info"][player_id[player_index]]["hasGOJ"]

    place_id=general_gamestate["board"][int(location/4)][location-4*int(location/4)]
    link=random.choice(general_gamestate["place_database"][place_id]["images"])

    specific_game_state = {"Database": send_database,
                           "Money": money,
                           "in_jail": in_jail,
                           "location": location,
                           "hasGOJ": hasGOJ,
                           "on_CH": on_CH,
                           "Link": link
                           }
    return specific_game_state

"""
player_index=0
player_id=["AAA","BBB"]
if __name__ =="__main__" :
    new_game_state=process_move(player_index,player_id,gamestate_happysellbuy,move_happysellbuy)
    print(json.dumps(new_game_state,indent=1))
"""