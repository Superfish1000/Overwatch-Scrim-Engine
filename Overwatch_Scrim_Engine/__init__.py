from flask import Flask
import hashlib, os

app = Flask(__name__)

secretKey = os.environ.get('SECRET_KEY', "SuperSecretWow").encode()

hashedKey = hashlib.sha256(secretKey).hexdigest()

app.config['SECRET_KEY'] = hashedKey

from Overwatch_Scrim_Engine import routes