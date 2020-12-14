from flask import request, render_template, redirect, url_for, session
from Overwatch_Scrim_Engine import app, forms, player_handler
import pickle, os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Used to force client to use HTTPS instead of http.
@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/')
def hello():
    """Renders a sample page."""
    return "<a href=\"/teamSelect\">Team Select</a>"


@app.route("/teamSelect", methods=['GET', 'POST'])
def teamSelect():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        return redirect(url_for("authPage"))
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())


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



# ###### GOOGLE SHEETS API AUTH SECTION ######
SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
HOST = os.environ.get('SERVER_HOST', 'localhost')

@app.route("/authPage")
def authPage():    
    if not os.path.exists('token.pickle'):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json', SCOPE)
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        session['state'] = state
        return redirect(authorization_url)
    return "<h1>Auth already done</h1>"

@app.route("/oauth2callback")
def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      'credentials.json', scopes=SCOPE, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials

    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    return redirect(url_for('teamSelect'))
