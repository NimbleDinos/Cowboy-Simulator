import requests

baseUrl = "http://localhost:8081/"


def join_game_request(user_id, user_name):
    try:
        join_game_url = baseUrl + "join?userId={0}&userName={1}".format(user_id, user_name)
        response = requests.get(join_game_url)
        print(response.status_code)
        if response.status_code == 200:
            return "You have joined the game " + user_name + "!"
        else:
            return "Whoops, something went wrong"
    except:
        return "Whoops, something went wrong"


def move_to_request(user_id, location, time):
    try:
        move_to_url = baseUrl + "movePlayer?userId={0}&place={1}&time={2}".format(user_id, location, time)
        response = requests.get(move_to_url)
        print(response.status_code)
        if response.status_code == 200:
            return "You are moving to " + location + "!"
        else:
            return "Whoops, something went wrong"
    except:
        return "Whoops, something went wrong"
