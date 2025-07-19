from flask import Flask
from routes.bookings import booking_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(booking_bp)

if __name__ == "__main__":
    app.run(debug=True)
