import json
from initialise_game_state import initialise


def lambda_handler(event, context):
    params = event["body"]
    jsonret = json.dumps(params)
    print(jsonret)
    ret = initialise(params["StyleParameters"]["board_size"], params["PlayerIndex"], params["PlayerIds"], params["StyleParameters"]["start_money"], params["StyleParameters"]["move_time"], params["StyleParameters"]["game_length"], params["StyleParameters"]["bribe"], params["StyleParameters"]["go_money"], params["StyleParameters"]["move_limit"])
    jsonret = json.dumps(ret)
    print(jsonret)
    return ret