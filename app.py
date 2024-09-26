from flask import Flask

from mission_bp import missions_bp  # יבוא הבלופרינט
from db import db
app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/normal_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(missions_bp)



with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
