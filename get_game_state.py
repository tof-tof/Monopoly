import time
import json
import copy
import random
def str_to_int(place_database):
    place_database_int = {}
    for place in place_database:  # Make the key of dictionary that stores place data into integers
        place_id = int(place)
        place_database_int[place_id] = place_database[place]
    return place_database_int

#takes general gamestate
def general_to_specific(player_id,player_index,gamestate):
    gamestate["place_database"]= str_to_int(gamestate["place_database"])
    send_database = copy.deepcopy(gamestate["place_database"])
    for id in send_database:
        send_database[id].pop("images")
    money=gamestate["player_info"][player_id[player_index]]["money"]
    in_jail=gamestate["player_info"][player_id[player_index]]["in_jail"]
    location=gamestate["player_info"][player_id[player_index]]["current_location"]
    on_CH=gamestate["player_info"][player_id[player_index]]["on_CH"]
    hasGOJ=gamestate["player_info"][player_id[player_index]]["hasGOJ"]
    place_id=gamestate["board"][int(location/4)][location-4*int(location/4)]
    link=random.choice(gamestate["place_database"][place_id]["images"])


    specific_game_state = {"Database": send_database,
                           "Money": money,
                           "in_jail": in_jail,
                           "location": location,
                           "hasGOJ": hasGOJ,
                           "IsMover": gamestate["Mover"]==player_index,
                           "on_CH": on_CH,
                           "Link": link
                           }
    return specific_game_state

# the gamestate given is the general game state
def getState(player_index, player_ids, gamestate):
    #Check if process move has ended the game
    #Check if the game has timedout

    current_time = time.time() * 1000
    result = "SUCCESS"
    StepText = ''
    announcement = None
    winner = None
    if gamestate["GameStatus"] != "RUNNING":  # If the game has ended
        if "TIMEOUT" in gamestate["GameStatus"]:
            result = "GAME_HAS_ENDED_BY_TIMEOUT"
        else:
            result = "GAME_HAS_ENDED"
        # Calculate who must have won
        winner = -1
        if "0" in gamestate["GameStatus"]:
            winner = 0
        elif "1" in gamestate["GameStatus"]:
            winner = 1
    elif gamestate["response_deadline"] is not None and (time.time()*1000) > gamestate["response_deadline"]:
        result = "GAME_HAS_ENDED_BY_TIMEOUT"

        if gamestate["Mover"] != -1:
            winner = 1 - gamestate["Mover"]
            announcement = "{0} won the game by timeout".format(player_ids[winner])
            description = "{0} won the game by timeout".format(player_ids[winner])
            game_status = "PLAYER_{0}_WON_BY_TIMEOUT".format(winner)
        else:  # If neither of you were due to move
            # The game must have already ended
            result = "GAME_HAS_ENDED"
            # Calculate who must have won
            winner = -1
            if "0" in gamestate["GameStatus"]:
                winner = 0
            elif "1" in gamestate["GameStatus"]:
                winner = 1

    general_game_state = {"board": gamestate["board"],
                          "board_size": gamestate["board_size"],
                          "place_database": gamestate["place_database"],
                          "player_info": gamestate["player_info"],
                          "mover": gamestate["mover"] if result =="SUCCESS" else -1,
                          "response_deadline": gamestate["response_deadline"],
                          "game_deadline":gamestate["game_deadline"] ,
                          "move_number": gamestate["move_number"],
                          "bribe": gamestate["bribe"],
                          "go_money": gamestate["go_money"],
                          "move_limit": gamestate["move_limit"],
                          "GameStatus": gamestate["GameStatus"]}
    specific_game_state = general_to_specific(player_ids, player_index, gamestate)

    if winner is None:
        new_game_state = {
                        "Result": result,
                        "StepTexts": [],
                        "NewDeal": False,
                        "SpecificGameState": specific_game_state,
                        "GeneralGameStates": [general_game_state]
                       }
    else:
        if announcement is None:
            new_game_state = {
                            "Result": result,
                            "WinnerIndex": winner,
                            "NewDeal": False,
                            "SpecificGameState": specific_game_state,
                            "GeneralGameStates": [general_game_state]
                           }
        else:
            new_game_state = {
                            "Result": result,
                            "StepTexts": [StepText],
                            "Announcement": announcement,
                            "WinnerIndex": winner,
                            "NewDeal": False,
                            "SpecificGameState": specific_game_state,
                            "GeneralGameStates": [general_game_state]
                           }

    return new_game_state
"""
input_general={'board': [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'board_size': 4, 'place_database': {0: {'name': 'start', 'images': ['Links'], 'owner': -2}, 1: {'name': 'The Statue of Liberty', 'buyPrice': 10, 'Rent': 1, 'owner': -1, 'images': ['Links']}, 2: {'name': ' Sydney Opera House', 'buyPrice': 20, 'Rent': 2, 'owner': -1, 'images': ['Links']}, 3: {'name': 'The Pyramids of Giza', 'buyPrice': 30, 'Rent': 3, 'owner': -1, 'images': ['Links']}, 4: {'name': 'Community Chest', 'owner': -2, 'images': ['Links']}, 5: {'name': ' Burj Khalifa', 'buyPrice': 40, 'Rent': 4, 'owner': -1, 'images': ['Links']}, 6: {'name': 'Effiel Tower', 'buyPrice': 50, 'Rent': 5, 'owner': -1, 'images': ['Links']}, 7: {'name': 'Golden Gate Bridge', 'buyPrice': 60, 'Rent': 6, 'owner': -1, 'images': ['Links']}, 8: {'name': 'jail', 'owner': -2, 'images': ['Links']}, 9: {'name': 'Tower of Pisa', 'buyPrice': 70, 'Rent': 7, 'owner': -1, 'images': ['Links']}, 10: {'name': 'Taj Mahal', 'buyPrice': 80, 'Rent': 8, 'owner': -1, 'images': ['Links']}, 11: {'name': 'The Great Wall of China', 'buyPrice': 90, 'Rent': 9, 'owner': -1, 'images': ['Links']}, 12: {'name': 'chance', 'owner': -2, 'images': ['Links']}, 13: {'name': ' Alcatraz', 'buyPrice': 100, 'Rent': 10, 'owner': -1, 'images': ['Links']}, 14: {'name': 'Christ the Redeemer', 'buyPrice': 110, 'Rent': 11, 'owner': -1, 'images': ['Links']}, 15: {'name': 'St. Basil’s Cathedral', 'buyPrice': 120, 'Rent': 12, 'owner': -1, 'images': ['Links']}}, 'player_info': {'AAA': {'money': 2000, 'in_jail': False, 'on_CH': False, 'current_location': 0, 'hasGOJ': False, 'in_game': True}, 'BBB': {'money': 2000, 'in_jail': False, 'on_CH': False, 'current_location': 0, 'hasGOJ': False, 'in_game': True}, 'CCC': {'money': 2000, 'in_jail': False, 'on_CH': False, 'current_location': 0, 'hasGOJ': False, 'in_game': True}}, 'mover': 0, 'response_deadline': 1552578642686000, 'game_deadline': 1552578741686000, 'move_number': 0, 'bribe': 500, 'go_money': 1000, 'move_limit': 100,'GameStatus':'RUNNING'}
new=get_game_state(0,['AAA','BBB','CCC'],input_general)
print(json.dumps(new,indent=1))
"""