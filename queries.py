import re
import time
from pprint import pprint
from re import search

import requests, inspect
from requests.exceptions import HTTPError
from apikey import SteamWeb_Api_Key


def checkUserExists(steam64id):
    print(f"---\nStarting: {inspect.stack()[0][3]}")
    try:
        response = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={SteamWeb_Api_Key}&steamids={steam64id}&relationship=friend')
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        print(f"{inspect.stack()[0][3]}: JSON response")
        print(f"{response.url}")
        return jsonResponse
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def getFriendsList(steam64id):
    print(f"---\nStarting: {inspect.stack()[0][3]}")
    try:
        response = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={SteamWeb_Api_Key}&steamid={steam64id}&relationship=friend')
        response.raise_for_status()
        # access JSON content
        jsonResponse = response.json()
        print(f"{inspect.stack()[0][3]}: JSON response")
        print(f"{response.url}")
        return jsonResponse

    except HTTPError as http_err:
        if http_err.errno == None:
            print(f"Accessed denied due to user privacy\nHTTPError:")
            raise
        else:
            print(f"HTTPError: {http_err.errno}")

    except Exception as err:
        print(type(err))


def getFriendListDataAll(steam64id):
    print(f"---\nStarting: {inspect.stack()[0][3]}")
    try:
        # TODO: Check if privacy is Friends/Private before calling friends list
        friend_steam64id = getFriendsList(steam64id)

        friendID_list = []
        friendsListData_dict = []

        for x in friend_steam64id["friendslist"]["friends"]:
            friendID_list.append(x["steamid"])

        print(f"Fetching friend list data.")

        # batch calls for steam friends, limited to 100 per call
        batchSize = (len(friendID_list) - 1) // 100 + 1
        for i in range(batchSize):
            batch = friendID_list[i * 100:(i + 1) * 100]

            # join steam64ids together and query Steam Web API for their data
            # TODO: Fix dictionary merging
            query = ",".join(batch)
            tempDict = checkUserExists(query)["response"]["players"]
            friendsListData_dict = friendsListData_dict + tempDict
            print(len(friendsListData_dict))

        return friendsListData_dict

    except HTTPError as http_err:
        print(http_err.errno)

    except Exception as err:
        print(type(err))
        print(f'{inspect.stack()[0][3]} - Other error occurred:{err}')


def getOwnedGames(steam64id):
    try:
        response = requests.get(
            f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1?key={SteamWeb_Api_Key}&steamid={steam64id}&include_appinfo=true&include_played_free_games=true")
        response.raise_for_status()
        # access JSON content
        jsonResponse = response.json()
        print(response.url)
        if jsonResponse["response"] == {}:
            return [{}]
        else:
            return jsonResponse["response"]["games"]

    except HTTPError as http_err:
        if http_err.errno == None:
            print(f"Accessed denied due to user privacy\nHTTPError:")
            raise
        else:
            print(f"HTTPError: {http_err.errno}")
    except Exception as err:
        print(f'Other error occurred: {err}')


def batchData(batchSize, dataSize, data):
    """
    Takes the data and runs the for loop in batches TODO: use with friends list to batch 100 steamIDs in getting friend data
    :param batchSize:
    :param dataSize:
    :param data:
    :return:
    """
    chunks = (dataSize - 1) // batchSize + 1
    for i in range(chunks):
        batch = data[i * batchSize:(i + 1) * batchSize]
        print(len(batch))


def getSelectedFriendsGames(steam64id_list):
    # KEY = appID, VALUES = index 0 is app info, index 1 is players who own it
    friends_games = {}

    for steam64id in steam64id_list:
        friends_games[steam64id] = getOwnedGames(steam64id)

    return friends_games


def checkCommonGames(friends_games):
    owned_games = {}

    for friend, games in friends_games.items():
        for game in games:

            try:
                if game["appid"] in owned_games:
                    owned_games[game["appid"]]["owned_by"].append(friend)
                else:
                    owned_games[game["appid"]] = {"info": {"name": game["name"],
                                                           "playtime": game["playtime_forever"],
                                                           "last_played": game["rtime_last_played"]},
                                                  "owned_by": [friend]}

            except KeyError:
                continue

    common_owned_games = {}

    for game in owned_games:
        if len(owned_games[game]["owned_by"]) == len(friends_games.keys()):
            common_owned_games[game] = owned_games[game]

    pprint(common_owned_games)

    # To get image using image hash
    # http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg
    # https://cdn.cloudflare.steamstatic.com/steam/apps/20/header.jpg

    return common_owned_games


def fromVanityURL(vanityurl):
    try:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={SteamWeb_Api_Key}&vanityurl={vanityurl}")
        response.raise_for_status()
        # access JSON content
        jsonResponse = response.json()
        print(response.url)

        if jsonResponse["response"]["success"] == 42:  # 42 = invalid vanity url
            raise InvalidVanityURL("Invalid vanity URL")

        return jsonResponse["response"]["steamid"]

    except HTTPError as http_err:
        if http_err.errno is None:
            print(f"Access denied:\nHTTPError:")
            print(HTTPError)
            raise
        else:
            print(f"HTTPError: {http_err.errno}")

    except Exception as err:
        print(f'Other error occurred: {err}')
        raise


def fromSteamID(steamid):
    x_y_z = steamid[6:].split(":")

    x = int(x_y_z[0])
    y = int(x_y_z[1])
    z = int(x_y_z[2])

    # W=Z*2+V+Y
    return 76561197960265728 + (z * 2 + y)


def getSteam64ID(steamid):
    # checks if the ID was given straight away
    try:

        # Checks for Steam64IDs
        match = re.findall(r"\b76561198\d{9}\b", steamid)
        if match:
            return match[0]

        # Checks for SteamIDs
        match = re.findall(r"\bSTEAM_\d:[01]:[0-9]{1,17}\b", steamid)
        if match:
            return fromSteamID(match[0])

        # Checks for vanity ID in url
        match = re.findall(r"steamcommunity\.com/id/([\w\d]+)", steamid)
        if match:
            return fromVanityURL(match[0])

        match = re.findall(r"([\w\d]+)", steamid)
        if match:
            return fromVanityURL(match[0])

    except Exception as err:
        print("Input could not be used to find a profile.")
        raise


class InvalidVanityURL(Exception):
    pass


if __name__ == '__main__':
    # checkUserExists("76561198050567488")
    # getFriendListDataAll(getFriendsList("76561198050567488"))

    # data = getFriendListDataAll(getFriendsList("76561198050567488"))
    # print(f"Length of data: {len(data)}\nData:\n{data}")
    #
    # for x in data:
    #     print(f"Player Nickname {x['personaname']}")
    #     print(f"Player Steam64ID {x['steamid']}")
    #     print(f"Player Steam Profile {x['profileurl']}")
    #
    # newlist = sorted(data, key=lambda d: d['personaname'])
    #
    # for x in newlist:
    #     print(f"Player Nickname {x['personaname']}")
    #     print(f"Player Steam64ID {x['steamid']}")
    #     print(f"Player Steam Profile {x['profileurl']}")

    # pprint(getOwnedGames(76561198050567488))

    # data = checkCommonGames(getSelectedFriendsGames(["76561198050567488", "76561198084835416", "76561197978271378", "76561198017922807"]))

    # pprint(fromSteamID("STEAM_0:0:45150880"))

    # print("URL with steam64id", getSteam64ID("https://steamcommunity.com/profiles/76561198055291268"))
    # print()
    # print("SteamID", getSteam64ID("STEAM_0:0:45150880"))
    # print()
    # print("steam64id", getSteam64ID("76561198055291268"))
    # print()
    # print("Vanity URL", getSteam64ID("https://steamcommunity.com/id/spikej/"))
    print()
    print("Vanity", getSteam64ID("spikej21312312321"))
