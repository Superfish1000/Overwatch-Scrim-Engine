from flask import request, render_template, redirect, url_for, session
from Overwatch_Scrim_Engine import app, forms, player_handler
import pickle, os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

# Used to force client to use HTTPS instead of http.
# Have not yet verified if this functions correctly.
@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/')
def hello():
    # Renders a simple page.
    return "<a href=\"/teamSelect\">Team Select</a>"

# This page serves as the main page for team selection.
@app.route("/teamSelect", methods=['GET', 'POST'])
def teamSelect():
    creds = None

    # Loads token object if it has already been pickled, else redirects to authentication page.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        print("DEBUG: Pickel not found.")
        return redirect(url_for("authPage"))

    # Checks if the creds object pickle was loaded correctly and is valid.
    if not creds or not creds.valid:
        # If creds pickle is found but it has expired, and the refresh_token is found, request a refresh.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("DEBUG: Pickel not valid.")
            return redirect(url_for("authPage"))


    player_profile_url = "https://playoverwatch.com/en-us/career/pc/"

    
    
    # Load player names from spreadsheet, extract player handles and format them to be used in request URLs
    # ############### TODO ###############
    # Add sorting to place players in positionally logical locations based on the role they signed up for.
    # Migrate from a list system to dictonary to allow including of player stat data such as role and SR.
    #
    raw_player_list = player_handler.getPlayers(creds)

    if not raw_player_list:
        players_list = ["Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666", "Superfish-11666"]
    else:
        players_list = player_handler.formatAllForWeb(player_handler.extractBattleNet(raw_player_list))


    # my_sample_form = forms.SampleForm(request.form)

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

# ############### TODO ###############
# Add check for credentials.json file that allows user to upload the required API file
# This would be a good thing to do in browser for usability.
# Currently, if the credentials.json file is not found in the root the system will error.


SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly'] # Specifying the API scope
HOST = os.environ.get('SERVER_HOST', 'localhost') # Used to provide callback URL to GSuite API

@app.route("/authPage")
def authPage():
    # In the case that the credential opject has not been generated and pickled, generate and pickle
    if not os.path.exists('token.pickle'):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json', SCOPE)
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        session['state'] = state
        return redirect(authorization_url)

    # If token pickle does exist then output message to user
    return "<h1>Auth already done</h1>"

@app.route("/oauth2callback")
def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json', scopes=SCOPE, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials

    # Save the credentials object by pickling it for later use
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    # Redirect users to the team select page
    return redirect(url_for('teamSelect'))
