from Overwatch_Scrim_Engine import app


if __name__ == '__main__':
    import os
    WORKING_DIRECTORY = os.environ.get('WORKING_DIRECTORY', os.getcwd())
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    os.chdir(WORKING_DIRECTORY)
    print("APP SETTINGS: Host:", str(HOST) + ", Port:", str(PORT) + ", Working Directory:", WORKING_DIRECTORY)

    context = ('cert.pem', 'key.pem')#certificate and key files
    app.run(HOST, PORT, ssl_context=context)
    # app.run(HOST, PORT)
