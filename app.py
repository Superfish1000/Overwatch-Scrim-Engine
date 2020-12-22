from Overwatch_Scrim_Engine import app
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

if __name__ == '__main__':
    import os
    #Attempt to get working directory, else use launch directory
    WORKING_DIRECTORY = os.environ.get('WORKING_DIRECTORY', os.getcwd())

    #Attempt to get working host address/URL, else use localhost
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    #Set directory for all file access in program code
    os.chdir(WORKING_DIRECTORY) 

    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555')) #Attempt to get 
    except ValueError:
        PORT = 5555
    
    print("APP SETTINGS: Host:", str(HOST) + ", Port:", str(PORT) + ", Working Directory:", WORKING_DIRECTORY)

    context = ('cert.pem', 'key.pem') #certificate and key files
    app.run(HOST, PORT, ssl_context=context)
    # app.run(HOST, PORT) # Non HTTPS.  Does not work with Google sheets and OAuth2
