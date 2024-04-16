import json
import time
import random
import copy


def initialise(board_size,player_index,player_id,start_money,move_time,game_length, bribe, go_money, move_limit):
    # for generality board_size+4 should be board_size*2, board_size+8 should be board_size*3 and so on,
    board = [[i for i in range(board_size)], [i for i in range(board_size,board_size+4)], [i for i in range(board_size+4,board_size+8)],[i for i in range(board_size+8,board_size+12) ]]
    with open('place_database.txt') as f:
        place_database = json.load(f)
    player_info={}
    for name in player_id:
        player_info[name]={"money":start_money , "in_jail":False , "on_CH":False, "current_location":0 , "hasGOJ":False, "in_game":True}   #initial player info
    response_deadline = int(time.time() * 1000 + move_time)  # Calculate response deadline as an integer
    game_deadline = int(time.time() * 1000 + game_length)  # Calculate the game deadline as an integer
    description="Game of monopoly between "
    for i in range(len(player_id)):
        if i != len(player_id) - 1:
            description += player_id[i] + " and "
        else:
            description += player_id[i]
    place_database=shuffle_price(place_database)
    general_game_state={"board" : board,
                        "board_size" : board_size,
                        "place_database" : place_database,
                        "player_info" : player_info,
                        "mover" : 0,
                        "response_deadline" : response_deadline,
                        "game_deadline" : game_deadline,
                        "move_number" : 0,
                        "bribe": bribe,
                        "go_money": go_money,
                        "move_limit": move_limit,
                        "GameStatus":"RUNNING"}
    send_database = copy.deepcopy(place_database)
    for id in send_database:
        send_database[id].pop("images")

    specific_game_state = {"Database": send_database,
                           "Money": start_money,
                           "in_jail": False,
                           "location": 0,
                           "hasGOJ": False,
                           "on_CH": False,
                           "Link": []
                           }

    initial_game_state = {
        "Result": "SUCCESS",
        "StepTexts": [description],
        "NewDeal": True,
        "SpecificGameState": specific_game_state,
        "GeneralGameStates": [general_game_state]
        }

    return initial_game_state


def shuffle_price(place_database):  #Shuffle price and rent of each place durig start of each game
    place_database_int = {}
    for place in place_database:  # Make the key of dictionary that stores place data into integers
        place_id = int(place)
        place_database_int[place_id] = place_database[place]
    #print(place_database_int)

    place_id = 0
    rent_list = []
    buyPrice_list = []
    valid_place_list = []
    for place in place_database_int:  # Get the rent and buy price of each vaild place into list
        if "Rent" in place_database_int[place]:
            valid_place_list.append(place_id)
            rent_list.append(place_database_int[place]["Rent"])
            buyPrice_list.append(place_database_int[place]["buyPrice"])
        place_id += 1
    random.shuffle(valid_place_list)

    for i in range(len(valid_place_list)):  # Asign rent and buy price to shuffled places
        place_database_int[valid_place_list[i]]["Rent"] = rent_list[i]
        place_database_int[valid_place_list[i]]["buyPrice"] = buyPrice_list[i]
    return place_database_int

"""
if __name__ == '__main__':
    print(json.dumps(initialise(4,[1,2],["aplha", "bewta"],10000,100,250,50,200,100), indent=1))
"""