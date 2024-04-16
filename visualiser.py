import pprint
import json
def convert_game_state(playerIds, gamestate):
    html = '<!DOCTYPE html><html><head>'
    #TODO Add CSS
    html += '</head>'
    html += '<body>'
    board =''
    for side in gamestate["board"]:
        board+=str(side)+'<br>'+'\n'
    html += '<h2>Board</h2>'+'<p>'+board+'</p>'
    html+=  '<h2>Place Database</h2>'+'<pre>'+ pprint.pformat(gamestate["place_database"])+ '</pre>'
    html += '<h2>Player Information</h2>'+'<pre>' + pprint.pformat(gamestate["player_info"]) + '</pre>'
    html += '<h2>Board Size</h2>'+'<p>' + str(gamestate["board_size"]) + '</p>'
    html += '<h2>Mover</h2>'+'<p>' + str(gamestate["Mover"]) + '</p>'
    html += '<h2>Response Deadline</h2>'+'<p>' + str(gamestate["response_deadline"]) + '</p>'
    html += '<h2>Game Deadline</h2>'+'<p>' + str(gamestate["game_deadline"]) + '</p>'
    html += '<h2>Move Number</h2>'+'<p>' + str(gamestate["move_number"]) + '</p>'
    html += '<h2>Bribe</h2>'+'<p>' + str(gamestate["bribe"]) + '</p>'
    html += '<h2>Go Money</h2>'+'<p>' + str(gamestate["go_money"]) + '</p>'
    html += '<h2>Move Limit</h2>'+'<p>' + str(gamestate["move_limit"]) + '</p>'
    html += '</body></html>'
    return {'Result': 'SUCCESS', 'Html': html}




if __name__=="__main__":
    playerIds = ["AAA", "BBB"]
    gamestate= {
        "Result": "SUCCESS",
        "StepTexts": [
            "Game of monopoly between AAA and BBB"
        ],
        "NewDeal": True,
        "SpecificGameState": {
            "Database": {
                0: {
                    "name": "start",
                    "owner": -2
                },
                1: {
                    "name": "The Statue of Liberty",
                    "buyPrice": 10,
                    "Rent": 1,
                    "owner": -1
                },
                2: {
                    "name": "Golden Gate Bridge",
                    "buyPrice": 20,
                    "Rent": 2,
                    "owner": 0
                },
                3: {
                    "name": "Effiel Tower",
                    "buyPrice": 30,
                    "Rent": 3,
                    "owner": -1
                },
                4: {
                    "name": "Community Chest",
                    "owner": -2
                },
                5: {
                    "name": "St. Basil\'s Cathedral",
                    "buyPrice": 40,
                    "Rent": 4,
                    "owner": -1
                },
                6: {
                    "name": " Burj Khalifa",
                    "buyPrice": 50,
                    "Rent": 5,
                    "owner": -1
                },
                7: {
                    "name": "Christ the Redeemer",
                    "buyPrice": 60,
                    "Rent": 6,
                    "owner": -1
                },
                8: {
                    "name": "jail",
                    "owner": -2
                },
                9: {
                    "name": " Sydney Opera House",
                    "buyPrice": 70,
                    "Rent": 7,
                    "owner": -1
                },
                10: {
                    "name": "The Pyramids of Giza",
                    "buyPrice": 80,
                    "Rent": 8,
                    "owner": -1
                },
                11: {
                    "name": " Alcatraz",
                    "buyPrice": 90,
                    "Rent": 9,
                    "owner": -1
                },
                12: {
                    "name": "chance",
                    "owner": -2
                },
                13: {
                    "name": "The Great Wall of China",
                    "buyPrice": 100,
                    "Rent": 10,
                    "owner": -1
                },
                14: {
                    "name": "Taj Mahal",
                    "buyPrice": 110,
                    "Rent": 11,
                    "owner": -1
                },
                15: {
                    "name": "Tower of Pisa",
                    "buyPrice": 120,
                    "Rent": 12,
                    "owner": -1
                }
            },
            "Money": 2000,
            "in_jail": False,
            "location": 1,
            "hasGOJ": False,
            "on_CH": False,
            "Link": []
        },
        "GeneralGameStates": [
            {
                "board": [
                    [
                        0,
                        1,
                        2,
                        3
                    ],
                    [
                        4,
                        5,
                        6,
                        7
                    ],
                    [
                        8,
                        9,
                        10,
                        11
                    ],
                    [
                        12,
                        13,
                        14,
                        15
                    ]
                ],
                "board_size": 4,
                "place_database": {
                    0: {
                        "name": "start",
                        "images": [
                            "Links"
                        ],
                        "owner": -2
                    },
                    1: {
                        "name": "The Statue of Liberty",
                        "buyPrice": 10,
                        "Rent": 1,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    2: {
                        "name": "Golden Gate Bridge",
                        "buyPrice": 20,
                        "Rent": 2,
                        "owner": 0,
                        "images": [
                            "Links"
                        ]
                    },
                    3: {
                        "name": "Effiel Tower",
                        "buyPrice": 30,
                        "Rent": 3,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    4: {
                        "name": "Community Chest",
                        "owner": -2,
                        "images": [
                            "Links"
                        ]
                    },
                    5: {
                        "name": "St. Basil\'s Cathedral",
                        "buyPrice": 40,
                        "Rent": 4,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    6: {
                        "name": " Burj Khalifa",
                        "buyPrice": 50,
                        "Rent": 5,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    7: {
                        "name": "Christ the Redeemer",
                        "buyPrice": 60,
                        "Rent": 6,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    8: {
                        "name": "jail",
                        "owner": -2,
                        "images": [
                            "Links"
                        ]
                    },
                    9: {
                        "name": " Sydney Opera House",
                        "buyPrice": 70,
                        "Rent": 7,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    10: {
                        "name": "The Pyramids of Giza",
                        "buyPrice": 80,
                        "Rent": 8,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    11: {
                        "name": " Alcatraz",
                        "buyPrice": 90,
                        "Rent": 9,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    12: {
                        "name": "chance",
                        "owner": -2,
                        "images": [
                            "Links"
                        ]
                    },
                    13: {
                        "name": "The Great Wall of China",
                        "buyPrice": 100,
                        "Rent": 10,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    14: {
                        "name": "Taj Mahal",
                        "buyPrice": 110,
                        "Rent": 11,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    15: {
                        "name": "Tower of Pisa",
                        "buyPrice": 120,
                        "Rent": 12,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    }
                },
                "player_info": {
                    "AAA": {
                        "money": 2000,
                        "in_jail": False,
                        "on_CH": False,
                        "current_location": 1,
                        "hasGOJ": False,
                        "in_game": True
                    },
                    "BBB": {
                        "money": 2000,
                        "in_jail": False,
                        "on_CH": False,
                        "current_location": 2,
                        "hasGOJ": False,
                        "in_game": True
                    }
                },
                "Mover": 0,
                "response_deadline": 1552489463683000,
                "game_deadline": 1552489562683000,
                "move_number": 0,
                "bribe": 500,
                "go_money": 1000,
                "move_limit": 100
            }
        ]
    }
    f = open("visGameState2.html","w")
    HTML = convert_game_state(playerIds,gamestate["GeneralGameStates"][0])["Html"]
    f.write(HTML)

