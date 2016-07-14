from app import app
import config

''' Run the app with variables in config file '''
app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
