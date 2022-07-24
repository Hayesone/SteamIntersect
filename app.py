from flask import Flask
from flask import render_template, request

import queries
from forms import UserFriendsList

app = Flask(__name__)
app.config['SECRET_KEY'] = '37bda0c866a9d9446eb72b23f1b56d20204cf7a78d5388de'


@app.route('/')
def hello_world():  # put application's code here
    return home()


@app.route("/home/", methods=['GET', 'POST'])
def home():  # home landing page
    return render_template("templates/home.html")


@app.route("/steam_intersect/", methods=['GET', 'POST'])
def steam_intersect():  # home landing page
    form = UserFriendsList(request.form)
    if request.method == 'POST' and form.validate():
        form_steam64id = form.steam64id.data
        try:
            return steam_friends(form_steam64id)
        except:
            return render_template("templates/steam_intersect.html", form=form)
    return render_template("templates/steam_intersect.html", form=form)


@app.route("/steam_intersect/friendList=<steam64id>", methods=['GET', 'POST'])
def steam_friends(steam64id):
    print("friends list")
    form = UserFriendsList(request.form)

    try:
        output = queries.getFriendListDataAll(queries.getFriendsList(steam64id))
        sortedoutput = sorted(output, key=lambda d: d['personaname'])
        return render_template("templates/steam_intersect_user_friends.html", form=form, output=sortedoutput, input=steam64id)
    except:
        output = "Error steam64id not found."
        print(output)
        return render_template("templates/steam_intersect_user_friends.html", form=form, output=output)


if __name__ == '__main__':
    app.run()
