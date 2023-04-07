from flask import Flask
from flask import render_template, request, redirect, url_for

import queries, inspect
from forms import UserFriendsList

app = Flask(__name__)
app.config['SECRET_KEY'] = '37bda0c866a9d9446eb72b23f1b56d20204cf7a78d5388de'


@app.route('/')
def hello_world():  # put application's code here
    return home()


@app.route("/home/", methods=['GET', 'POST'])
def home():  # home landing page
    return render_template("home.html")


@app.route("/steam_intersect/", methods=['GET', 'POST'])
def steam_intersect():  # home landing page
    if request.method == 'GET':
        return render_template("steam_intersect.html")

    if request.method == 'POST':
        try:

            user = request.form["steamid"]
            queries.getSteam64ID(user)  # checks if the input is valid
            return redirect(url_for("steam_friends_get", user=user))

        except Exception as err:
            print(err)
            error = "Unable to get Steam profile."
            return render_template("steam_intersect.html", error=f"{error}")


@app.route("/steam_intersect/<user>", methods=['GET'])
def steam_friends_get(user):
    print(f"Entering: {inspect.stack()[0][3]}")
    print("friends list")
    # Gets the community (steam64id) for API calls
    steam64id = queries.getSteam64ID(user)

    try:
        friendsListData = queries.getFriendListDataAll(steam64id)
        user = queries.checkUserExists(steam64id)["response"]["players"][0]
        sortedFLD = sorted(friendsListData, key=lambda d: d['personaname'])
        print("SHOULD BE WORKING")
        return render_template("steam_intersect_user_friends.html", output=sortedFLD, user=user)
    except TypeError as e:
        print(e, e.with_traceback())
        output = f"User privacy settings likely blocking view of friends list."
        return render_template("steam_intersect_user_friends.html", error=output)

    except Exception as e:
        output = f"{e}"
        print(output)
        return render_template("steam_intersect_user_friends.html", exception=e)


@app.route("/steam_intersect/<user>/", methods=['GET'])
def steam_friends_post(user):
    print(f"Entering: {inspect.stack()[0][3]}")

    # TODO Handle profiles with private games
    # TODO Have a placeholder image if game has no header.jpg
    # TODO Add a "Sort of shared" games section

    # Gets the community (steam64id) for API calls
    steam64id = queries.getSteam64ID(user)

    try:
        selected_friends = request.args.getlist("ids[]")
        selected_friends.append(steam64id)

        print(selected_friends)

        shared_games = queries.checkCommonGames(queries.getSelectedFriendsGames(selected_friends))

        print(f"This is the shared games in app.py {shared_games}")
        return render_template("steam_intersect_games.html", shared_games=shared_games, input=steam64id)
    except TypeError as e:
        output = f"User privacy settings likely blocking view of friends list."
        return render_template("steam_intersect_games.html", error=output)

    except Exception as e:
        output = f"{e}"
        print(output)
        return render_template("steam_intersect_games.html", error=e)


if __name__ == '__main__':
    app.run()
