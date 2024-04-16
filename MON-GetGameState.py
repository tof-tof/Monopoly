import json
from get_game_state import getState


def lambda_handler(event, context):
    params = event["body"]
    jsonret = json.dumps(params)
    print(jsonret)
    ret = getState(params["PlayerIndex"], params["PlayerIds"], params["GeneralGameState"])
    jsonret = json.dumps(ret)
    print(jsonret)
    return ret