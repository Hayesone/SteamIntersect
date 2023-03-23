from flask import Flask
from flask import render_template, request

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


@app.route("/steam_intersect/", methods=['GET'])
def steam_intersect():  # home landing page
    form = UserFriendsList(request.form)
    return render_template("steam_intersect.html", form=form)

@app.route("/steam_intersect/", methods=['POST'])
def steam_intersect_post():  # home landing page
    form = UserFriendsList(request.form)
    if request.method == 'POST' and form.validate():
        try:
            sid = queries.getSteam64ID(form.steam64id.data)
            return steam_friends_get(sid)

        except Exception as err:
            error = "Unable to get Steam profile."
            return render_template("steam_intersect.html", form=form, error=f"{error}")




@app.route("/steam_intersect/<steam64id>", methods=['GET'])
def steam_friends_get(steam64id):
    print(f"Entering: {inspect.stack()[0][3]}")
    print("friends list")
    form = UserFriendsList(request.form)

    # Gets the community (steam64id) for API calls
    sid = queries.getSteam64ID(steam64id)

    try:
        output = queries.getFriendListDataAll(sid)
        sortedoutput = sorted(output, key=lambda d: d['personaname'])
        return render_template("steam_intersect_user_friends.html", form=form, output=sortedoutput, input=sid)
    except TypeError as e:
        output = f"User privacy settings likely blocking view of friends list."
        return render_template("steam_intersect_user_friends.html", form=form, error=output)

    except Exception as e:
        output = f"{e}"
        print(output)
        return render_template("steam_intersect_user_friends.html", form=form, exception=e)


@app.route("/steam_intersect/<steam64id>", methods=['POST'])
def steam_friends_post(steam64id):
    print(f"Entering: {inspect.stack()[0][3]}")

    # TODO Handle profiles with private games
    # TODO Have a placeholder image if game has no header.jpg
    # TODO Add a "Sort of shared" games section

    try:
        sid = queries.getSteam64ID(steam64id)
        selected_friends = request.form.getlist("ids[]")
        selected_friends.append(sid)

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
