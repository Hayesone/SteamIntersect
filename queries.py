from functools import reduce
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
        # access JSOn content
        jsonResponse = response.json()
        print(f"{inspect.stack()[0][3]}: JSON response")
        print(f"{response.url}")

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return jsonResponse


def getFriendListDataAll(steam64id):
    print(f"---\nStarting: {inspect.stack()[0][3]}")
    try:

        friendIDs = []
        friendsDict = []

        for x in steam64id["friendslist"]["friends"]:
            friendIDs.append(x["steamid"])

        print(f"Fetching friend list data.")

        # batch calls for steam friends, limited to 100 per call
        batchSize = (len(friendIDs) - 1) // 100 + 1
        for i in range(batchSize):
            batch = friendIDs[i * 100:(i + 1) * 100]

            # join steam64ids together and query Steam Web API for their data
            # TODO: Fix dictionary merging
            query = ",".join(batch)
            tempDict = checkUserExists(query)["response"]["players"]
            friendsDict = friendsDict + tempDict
            print(len(friendsDict))

        return friendsDict

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def getOwnedGames(steam64id):
    try:
        response = requests.get(
            f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1?key={SteamWeb_Api_Key}&steamid={steam64id}&include_appinfo=true&include_played_free_games=true")
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        print(f"{inspect.stack()[0][3]}: JSON response")
        print(f"{response.url}")

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return jsonResponse["response"]


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


def getFriendData():
    friendData = {'players': [
        {'steamid': '76561198973864368', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Ed Sheeran',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561198973864368/',
         'avatar': 'https://avatars.akamai.steamstatic.com/65d3d9c3dd454973bee7e24eb1914d0862b3d056.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/65d3d9c3dd454973bee7e24eb1914d0862b3d056_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/65d3d9c3dd454973bee7e24eb1914d0862b3d056_full.jpg',
         'avatarhash': '65d3d9c3dd454973bee7e24eb1914d0862b3d056', 'lastlogoff': 1658282012, 'personastate': 0,
         'primaryclanid': '103582791429521408', 'timecreated': 1561831950, 'personastateflags': 0},
        {'steamid': '76561198279871552', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Viper',
         'profileurl': 'https://steamcommunity.com/id/widdlebiscuit/',
         'avatar': 'https://avatars.akamai.steamstatic.com/c33f2eb861848f512a473d9a5e1004733e93a2d3.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/c33f2eb861848f512a473d9a5e1004733e93a2d3_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/c33f2eb861848f512a473d9a5e1004733e93a2d3_full.jpg',
         'avatarhash': 'c33f2eb861848f512a473d9a5e1004733e93a2d3', 'lastlogoff': 1520507394, 'personastate': 0,
         'realname': 'widdlebiscuit', 'primaryclanid': '103582791455550643', 'timecreated': 1453998525,
         'personastateflags': 0},
        {'steamid': '76561198315051607', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'spongeboob',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/id/TerribleSmurf/',
         'avatar': 'https://avatars.akamai.steamstatic.com/9dcf8ef1224bab6c7be25afce1184b9e1a318246.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/9dcf8ef1224bab6c7be25afce1184b9e1a318246_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/9dcf8ef1224bab6c7be25afce1184b9e1a318246_full.jpg',
         'avatarhash': '9dcf8ef1224bab6c7be25afce1184b9e1a318246', 'lastlogoff': 1654112626, 'personastate': 0,
         'primaryclanid': '103582791455580864', 'timecreated': 1467519796, 'personastateflags': 0,
         'loccountrycode': 'ZW', 'locstatecode': '08'},
        {'steamid': '76561198363905350', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'ashjdbss',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561198363905350/',
         'avatar': 'https://avatars.akamai.steamstatic.com/298dcc4d22992e4d2121658dace89a1caebdb44d.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/298dcc4d22992e4d2121658dace89a1caebdb44d_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/298dcc4d22992e4d2121658dace89a1caebdb44d_full.jpg',
         'avatarhash': '298dcc4d22992e4d2121658dace89a1caebdb44d', 'lastlogoff': 1658510574, 'personastate': 0,
         'primaryclanid': '103582791429521408', 'timecreated': 1485887018, 'personastateflags': 0},
        {'steamid': '76561198799394728', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'L O P O',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/id/LopoOfficial/',
         'avatar': 'https://avatars.akamai.steamstatic.com/06551cf32c0cd4a09524ba040c8dc9bc570e651a.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/06551cf32c0cd4a09524ba040c8dc9bc570e651a_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/06551cf32c0cd4a09524ba040c8dc9bc570e651a_full.jpg',
         'avatarhash': '06551cf32c0cd4a09524ba040c8dc9bc570e651a', 'lastlogoff': 1658537551, 'personastate': 0,
         'primaryclanid': '103582791469319472', 'timecreated': 1514245914, 'personastateflags': 0,
         'loccountrycode': 'PT', 'locstatecode': '13'},
        {'steamid': '76561199199084183', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'LiiSunia',
         'profileurl': 'https://steamcommunity.com/profiles/76561199199084183/',
         'avatar': 'https://avatars.akamai.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg',
         'avatarhash': 'fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb', 'lastlogoff': 1640483372, 'personastate': 0,
         'primaryclanid': '103582791429521408', 'timecreated': 1629050352, 'personastateflags': 0},
        {'steamid': '76561198307319292', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'mizzox',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/id/mizzox/',
         'avatar': 'https://avatars.akamai.steamstatic.com/73a8a60cbee74dfec0b9a7473b82b943a8bbcf76.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/73a8a60cbee74dfec0b9a7473b82b943a8bbcf76_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/73a8a60cbee74dfec0b9a7473b82b943a8bbcf76_full.jpg',
         'avatarhash': '73a8a60cbee74dfec0b9a7473b82b943a8bbcf76', 'lastlogoff': 1657836296, 'personastate': 0,
         'realname': '༼;´༎ຶ \u06dd ༎ຶ༽  🏴\u200d☠️ Nowhere', 'primaryclanid': '103582791430393093',
         'timecreated': 1464002352, 'personastateflags': 0},
        {'steamid': '76561198353437380', 'communityvisibilitystate': 3, 'profilestate': 1,
         'personaname': 'Daddy Nature', 'profileurl': 'https://steamcommunity.com/profiles/76561198353437380/',
         'avatar': 'https://avatars.akamai.steamstatic.com/ae3fc93bec8ba59ad7467f3cf1f403eba4d0fc69.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/ae3fc93bec8ba59ad7467f3cf1f403eba4d0fc69_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/ae3fc93bec8ba59ad7467f3cf1f403eba4d0fc69_full.jpg',
         'avatarhash': 'ae3fc93bec8ba59ad7467f3cf1f403eba4d0fc69', 'lastlogoff': 1658526610, 'personastate': 0,
         'realname': 'Charlie', 'primaryclanid': '103582791429521408', 'timecreated': 1482682080,
         'personastateflags': 0, 'loccountrycode': 'GB', 'locstatecode': 'G5'},
        {'steamid': '76561198993005632', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Cilit Bang',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561198993005632/',
         'avatar': 'https://avatars.akamai.steamstatic.com/1b215c6e8025ab69de3b0d75b4e98b5fdfa2b21a.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/1b215c6e8025ab69de3b0d75b4e98b5fdfa2b21a_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/1b215c6e8025ab69de3b0d75b4e98b5fdfa2b21a_full.jpg',
         'avatarhash': '1b215c6e8025ab69de3b0d75b4e98b5fdfa2b21a', 'lastlogoff': 1652704724, 'personastate': 0,
         'primaryclanid': '103582791429521408', 'timecreated': 1569371867, 'personastateflags': 0},
        {'steamid': '76561198302919112', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'RSWReece',
         'profileurl': 'https://steamcommunity.com/id/RSWReece/',
         'avatar': 'https://avatars.akamai.steamstatic.com/5542cfff6739463753b4be80acdce2c3ba9619f7.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/5542cfff6739463753b4be80acdce2c3ba9619f7_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/5542cfff6739463753b4be80acdce2c3ba9619f7_full.jpg',
         'avatarhash': '5542cfff6739463753b4be80acdce2c3ba9619f7', 'lastlogoff': 1658345508, 'personastate': 0,
         'realname': 'Reece Williams', 'primaryclanid': '103582791435513948', 'timecreated': 1462119202,
         'personastateflags': 0, 'loccountrycode': 'GB', 'locstatecode': '18'},
        {'steamid': '76561198328334201', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'wotzeeheck',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/id/jenniferx/',
         'avatar': 'https://avatars.akamai.steamstatic.com/cd0903a426ac47261d84b8ce945e319fd80bc4c2.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/cd0903a426ac47261d84b8ce945e319fd80bc4c2_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/cd0903a426ac47261d84b8ce945e319fd80bc4c2_full.jpg',
         'avatarhash': 'cd0903a426ac47261d84b8ce945e319fd80bc4c2', 'lastlogoff': 1658529094, 'personastate': 0,
         'primaryclanid': '103582791429618449', 'timecreated': 1472680137, 'personastateflags': 0,
         'loccountrycode': 'GB'},
        {'steamid': '76561199034113934', 'communityvisibilitystate': 1, 'profilestate': 1, 'personaname': 'glizzly',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561199034113934/',
         'avatar': 'https://avatars.akamai.steamstatic.com/71f02ee38d998de6213289568b3d9c67c62fa25b.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/71f02ee38d998de6213289568b3d9c67c62fa25b_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/71f02ee38d998de6213289568b3d9c67c62fa25b_full.jpg',
         'avatarhash': '71f02ee38d998de6213289568b3d9c67c62fa25b', 'lastlogoff': 1654008921, 'personastate': 0,
         'personastateflags': 0},
        {'steamid': '76561198281483220', 'communityvisibilitystate': 3, 'profilestate': 1,
        'personaname': 'ˢᴵᴿ ๖ۣۜkhalif ツ',
        'profileurl': 'https://steamcommunity.com/id/sirkhalif/',
        'avatar': 'https://avatars.akamai.steamstatic.com/06cf7223d73704b6e5b602e882714007a56383fc.jpg',
        'avatarmedium': 'https://avatars.akamai.steamstatic.com/06cf7223d73704b6e5b602e882714007a56383fc_medium.jpg',
        'avatarfull': 'https://avatars.akamai.steamstatic.com/06cf7223d73704b6e5b602e882714007a56383fc_full.jpg',
        'avatarhash': '06cf7223d73704b6e5b602e882714007a56383fc', 'lastlogoff': 1564669000,
        'personastate': 0, 'realname': 'khalif', 'primaryclanid': '103582791456275818',
        'timecreated': 1454628068, 'personastateflags': 0, 'loccountrycode': 'DE',
        'locstatecode': '07'},
        {'steamid': '76561199030976117', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'george',
         'profileurl': 'https://steamcommunity.com/profiles/76561199030976117/',
         'avatar': 'https://avatars.akamai.steamstatic.com/8f4d8b824e57e7d482a745f9ac97412b7c9a2302.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/8f4d8b824e57e7d482a745f9ac97412b7c9a2302_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/8f4d8b824e57e7d482a745f9ac97412b7c9a2302_full.jpg',
         'avatarhash': '8f4d8b824e57e7d482a745f9ac97412b7c9a2302', 'lastlogoff': 1624468427, 'personastate': 0,
         'primaryclanid': '103582791429521408', 'timecreated': 1583252746, 'personastateflags': 0},
        {'steamid': '76561198282643543', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'VipeR',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561198282643543/',
         'avatar': 'https://avatars.akamai.steamstatic.com/09d5ed8a3746693eeec99f9856da7e7991f858bf.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/09d5ed8a3746693eeec99f9856da7e7991f858bf_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/09d5ed8a3746693eeec99f9856da7e7991f858bf_full.jpg',
         'avatarhash': '09d5ed8a3746693eeec99f9856da7e7991f858bf', 'lastlogoff': 1658524607, 'personastate': 0,
         'primaryclanid': '103582791440125546', 'timecreated': 1455027788, 'personastateflags': 0},
        {'steamid': '76561198354541352', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Viper_265A',
         'profileurl': 'https://steamcommunity.com/profiles/76561198354541352/',
         'avatar': 'https://avatars.akamai.steamstatic.com/d9e2708ba1333ad4c60687a65bd9ef1d09eae3b1.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/d9e2708ba1333ad4c60687a65bd9ef1d09eae3b1_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/d9e2708ba1333ad4c60687a65bd9ef1d09eae3b1_full.jpg',
         'avatarhash': 'd9e2708ba1333ad4c60687a65bd9ef1d09eae3b1', 'lastlogoff': 1658442027, 'personastate': 0,
         'realname': 'Jonathan', 'primaryclanid': '103582791429521408', 'timecreated': 1482755658,
         'personastateflags': 0, 'loccountrycode': 'GB'},
        {'steamid': '76561198443764145', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'king john',
         'profileurl': 'https://steamcommunity.com/id/chaosyy/',
         'avatar': 'https://avatars.akamai.steamstatic.com/98bdea75fa7e3195c7c36878ad521edfc4cf861d.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/98bdea75fa7e3195c7c36878ad521edfc4cf861d_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/98bdea75fa7e3195c7c36878ad521edfc4cf861d_full.jpg',
         'avatarhash': '98bdea75fa7e3195c7c36878ad521edfc4cf861d', 'lastlogoff': 1658478538, 'personastate': 3,
         'realname': 'King John', 'primaryclanid': '103582791456078798', 'timecreated': 1509980313,
         'personastateflags': 0, 'gameextrainfo': 'Black Desert', 'gameid': '582660', 'loccountrycode': 'TR',
         'locstatecode': '76'},
        {'steamid': '76561198271663439', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Maxsell',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561198271663439/',
         'avatar': 'https://avatars.akamai.steamstatic.com/94b3feee6d4affa2aab1bc2fdee2f98411146ace.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/94b3feee6d4affa2aab1bc2fdee2f98411146ace_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/94b3feee6d4affa2aab1bc2fdee2f98411146ace_full.jpg',
         'avatarhash': '94b3feee6d4affa2aab1bc2fdee2f98411146ace', 'lastlogoff': 1658540885, 'personastate': 0,
         'realname': 'Marko', 'primaryclanid': '103582791429837180', 'timecreated': 1450986898, 'personastateflags': 0},
        {'steamid': '76561199055156236', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'TED',
         'profileurl': 'https://steamcommunity.com/id/tedtastic/',
         'avatar': 'https://avatars.akamai.steamstatic.com/e57abf7cd9e7b2153d2644bbfffcce495d3b32c5.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/e57abf7cd9e7b2153d2644bbfffcce495d3b32c5_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/e57abf7cd9e7b2153d2644bbfffcce495d3b32c5_full.jpg',
         'avatarhash': 'e57abf7cd9e7b2153d2644bbfffcce495d3b32c5', 'lastlogoff': 1658536948, 'personastate': 3,
         'primaryclanid': '103582791469359284', 'timecreated': 1588791389, 'personastateflags': 0,
         'loccountrycode': 'DK'},
        {'steamid': '76561198269088217', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Mister',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/id/mistersurf/',
         'avatar': 'https://avatars.akamai.steamstatic.com/b0d773eb2fe937f76ffba9a97008da98edd9dfdd.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/b0d773eb2fe937f76ffba9a97008da98edd9dfdd_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/b0d773eb2fe937f76ffba9a97008da98edd9dfdd_full.jpg',
         'avatarhash': 'b0d773eb2fe937f76ffba9a97008da98edd9dfdd', 'lastlogoff': 1658445203, 'personastate': 0,
         'realname': 'Quentin', 'primaryclanid': '103582791461872561', 'timecreated': 1450523450,
         'personastateflags': 0, 'loccountrycode': 'FR', 'locstatecode': 'B6'},
        {'steamid': '76561199034396384', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'GeorgeLAD',
         'profileurl': 'https://steamcommunity.com/profiles/76561199034396384/',
         'avatar': 'https://avatars.akamai.steamstatic.com/c4e109bbe15f86566621a6c5db0124a6b3777147.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/c4e109bbe15f86566621a6c5db0124a6b3777147_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/c4e109bbe15f86566621a6c5db0124a6b3777147_full.jpg',
         'avatarhash': 'c4e109bbe15f86566621a6c5db0124a6b3777147', 'lastlogoff': 1658394704, 'personastate': 0,
         'primaryclanid': '103582791435027062', 'timecreated': 1584406879, 'personastateflags': 0,
         'loccountrycode': 'GB'},
        {'steamid': '76561199193257580', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'comex321',
         'profileurl': 'https://steamcommunity.com/profiles/76561199193257580/',
         'avatar': 'https://avatars.akamai.steamstatic.com/b10c3b2a6e9730965b6c9d7f45f2a2051197aed3.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/b10c3b2a6e9730965b6c9d7f45f2a2051197aed3_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/b10c3b2a6e9730965b6c9d7f45f2a2051197aed3_full.jpg',
         'avatarhash': 'b10c3b2a6e9730965b6c9d7f45f2a2051197aed3', 'lastlogoff': 1658537639, 'personastate': 1,
         'primaryclanid': '103582791472191579', 'timecreated': 1627398184, 'personastateflags': 0,
         'loccountrycode': 'GB'},
        {'steamid': '76561198281029297', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Mindless',
         'commentpermission': 2, 'profileurl': 'https://steamcommunity.com/profiles/76561198281029297/',
         'avatar': 'https://avatars.akamai.steamstatic.com/9b04389f7cfc0f42b0d7ec829a887c7c79ef137d.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/9b04389f7cfc0f42b0d7ec829a887c7c79ef137d_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/9b04389f7cfc0f42b0d7ec829a887c7c79ef137d_full.jpg',
         'avatarhash': '9b04389f7cfc0f42b0d7ec829a887c7c79ef137d', 'lastlogoff': 1628450331, 'personastate': 0,
         'primaryclanid': '103582791441325183', 'timecreated': 1454453757, 'personastateflags': 0,
         'loccountrycode': 'GB'},
        {'steamid': '76561198370835548', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'Swag',
         'profileurl': 'https://steamcommunity.com/profiles/76561198370835548/',
         'avatar': 'https://avatars.akamai.steamstatic.com/fb75fc30f9c3a6371cb046b351d82049e7d945e5.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/fb75fc30f9c3a6371cb046b351d82049e7d945e5_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/fb75fc30f9c3a6371cb046b351d82049e7d945e5_full.jpg',
         'avatarhash': 'fb75fc30f9c3a6371cb046b351d82049e7d945e5', 'lastlogoff': 1658124051, 'personastate': 0,
         'primaryclanid': '103582791430365175', 'timecreated': 1488586800, 'personastateflags': 0,
         'loccountrycode': 'US', 'locstatecode': 'FL'},
        {'steamid': '76561198833516130', 'communityvisibilitystate': 1, 'profilestate': 1, 'personaname': 'Albanyreed',
         'commentpermission': 1, 'profileurl': 'https://steamcommunity.com/profiles/76561198833516130/',
         'avatar': 'https://avatars.akamai.steamstatic.com/e6b3a79724b0276187bbae3426f086589449c613.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/e6b3a79724b0276187bbae3426f086589449c613_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/e6b3a79724b0276187bbae3426f086589449c613_full.jpg',
         'avatarhash': 'e6b3a79724b0276187bbae3426f086589449c613', 'lastlogoff': 1656766061, 'personastate': 0,
         'personastateflags': 0},
        {'steamid': '76561199076832796', 'communityvisibilitystate': 3, 'profilestate': 1, 'personaname': 'WelshApollo',
         'profileurl': 'https://steamcommunity.com/profiles/76561199076832796/',
         'avatar': 'https://avatars.akamai.steamstatic.com/b2a734431d40a6c110b7c09b1b3b65ad5819c79f.jpg',
         'avatarmedium': 'https://avatars.akamai.steamstatic.com/b2a734431d40a6c110b7c09b1b3b65ad5819c79f_medium.jpg',
         'avatarfull': 'https://avatars.akamai.steamstatic.com/b2a734431d40a6c110b7c09b1b3b65ad5819c79f_full.jpg',
         'avatarhash': 'b2a734431d40a6c110b7c09b1b3b65ad5819c79f', 'lastlogoff': 1655070684, 'personastate': 0,
         'primaryclanid': '103582791429521408', 'timecreated': 1595605964, 'personastateflags': 0}]}
    return friendData


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

    data = getOwnedGames("76561198328334201")