from flask import Flask
import hashlib

app = Flask(__name__)

secretKey = b"SuperSecretWow"

hashedKey = hashlib.sha256(secretKey).hexdigest()

app.config['SECRET_KEY'] = hashedKey

from Overwatch_Scrim_Engine import routes