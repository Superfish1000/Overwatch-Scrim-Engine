from flask import request, render_template
from Overwatch_Scrim_Engine import app, forms, player_handler

@app.route('/')
def hello():
    """Renders a sample page."""
    return "<a href=\"/teamSelect\">Team Select</a>"


@app.route("/teamSelect", methods=['GET', 'POST'])
def testSearch():
    my_sample_form = forms.SampleForm(request.form)

    player_profile_url = "https://playoverwatch.com/en-us/career/pc/"

    players_list = ["Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666"]

    players_list = player_handler.formatAllForWeb(player_handler.extractBattleNet(player_handler.getPlayers()))

    # if request.method == "POST":
    #     first_name = request.form["first_name"]
    #     last_name = request.form["last_name"]
    #     panther_id = request.form["panther_id"]
    #     start_date = request.form["start_date"]
    #     major = request.form["major"]
    #     campus = request.form["campus"]

    #     response = [first_name, last_name, panther_id, start_date, major, campus]

    #     return render_template('testResults.html', response=response, form=my_sample_form, major=major)

    return render_template('playerSelect.html', player_profile_url=player_profile_url, players=players_list)