import requests

baseUrl = "http://localhost:8081/"


def join_game_request(user_id, user_name):
    try:
        joinGameUrl = baseUrl + "join?userId={0}&userName={1}".format(user_id, user_name)
        response = requests.get(joinGameUrl)
        print(response.status_code)
        if response.status_code == 200:
            return "You have joined the game " + user_name + "!"
        else:
            return "Whoops, something went wrong"
    except:
        return "Whoops, something went wrong"
