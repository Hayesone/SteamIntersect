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
    return render_template("home.html")


@app.route("/steam_intersect/", methods=['GET', 'POST'])
def steam_intersect():  # home landing page
    form = UserFriendsList(request.form)
    if request.method == 'POST' and form.validate():
        form_steam64id = form.steam64id.data
        try:
            return steam_friends(form_steam64id)
        except:
            return render_template("steam_intersect.html", form=form)
    return render_template("steam_intersect.html", form=form)


@app.route("/steam_intersect/<steam64id>", methods=['GET', 'POST'])
def steam_friends(steam64id):
    print("friends list")
    form = UserFriendsList(request.form)

    try:
        output = queries.getFriendListDataAll(steam64id)
        sortedoutput = sorted(output, key=lambda d: d['personaname'])
        return render_template("steam_intersect_user_friends.html", form=form, output=sortedoutput, input=steam64id)
    except Exception as e:
        output = f"{e}"
        print(output)
        return render_template("steam_intersect_user_friends.html", form=form)


if __name__ == '__main__':
    app.run()
