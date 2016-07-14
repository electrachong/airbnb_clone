from app import app
import config

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
