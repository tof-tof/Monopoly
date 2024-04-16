import json
from visualiser import convert_game_state


# Nothing to do
def lambda_handler(event, context):
    params = event["body"]
    jsonret = json.dumps(params)
    print(jsonret)
    ret = convert_game_state(params["PlayerIds"], params["GeneralGameState"])
    jsonret = json.dumps(ret)
    print(jsonret)
    return ret