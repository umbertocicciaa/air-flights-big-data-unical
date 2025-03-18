from flask import Flask
from controllers.etlcontroller import etl_blueprint

app = Flask(__name__)
app.register_blueprint(etl_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)