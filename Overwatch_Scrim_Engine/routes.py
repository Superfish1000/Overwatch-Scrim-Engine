from flask import request, render_template
from Overwatch_Scrim_Engine import app, forms

@app.route('/')
def hello():
    """Renders a sample page."""
    return "<a href=\"/teamSelect\">Team Select</a>"


@app.route("/teamSelect", methods=['GET', 'POST'])
def testSearch():
    my_sample_form = forms.SampleForm(request.form)

    overbuff_url = "https://www.overbuff.com/players/pc/"
    players_list = ["Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666"]

    # if request.method == "POST":
    #     first_name = request.form["first_name"]
    #     last_name = request.form["last_name"]
    #     panther_id = request.form["panther_id"]
    #     start_date = request.form["start_date"]
    #     major = request.form["major"]
    #     campus = request.form["campus"]

    #     response = [first_name, last_name, panther_id, start_date, major, campus]

    #     return render_template('testResults.html', response=response, form=my_sample_form, major=major)

    return render_template('playerSelect.html', overbuff_url=overbuff_url, players=players_list)