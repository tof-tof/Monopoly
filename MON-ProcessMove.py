import json
from process_move import move


def lambda_handler(event, context):
    params = event["body"]
    jsonret = json.dumps(params)
    print(jsonret)
    ret = move(params["PlayerIndex"], params["PlayerIds"], params["GeneralGameState"], params["Move"])
    jsonret = json.dumps(ret)
    print(jsonret)
    return ret