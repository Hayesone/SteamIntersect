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


@app.route("/steam_intersect/", methods=['POST'])
def steam_intersect():  # home landing page

    # TODO Fix page not loading

    form = UserFriendsList(request.form)
    if request.method == 'POST' and form.validate():
        form_steam64id = form.steam64id.data
        try:
            return steam_friends_get(form_steam64id)
        except:
            return render_template("steam_intersect.html", form=form)
    return render_template("steam_intersect.html", form=form)


@app.route("/steam_intersect/<steam64id>", methods=['GET'])
def steam_friends_get(steam64id):
    print(f"Entering: {inspect.stack()[0][3]}")
    print("friends list")
    form = UserFriendsList(request.form)

    try:
        output = queries.getFriendListDataAll(steam64id)
        sortedoutput = sorted(output, key=lambda d: d['personaname'])
        return render_template("steam_intersect_user_friends.html", form=form, output=sortedoutput, input=steam64id)
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
        selected_friends = request.form.getlist("ids[]")
        selected_friends.append(steam64id)

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
