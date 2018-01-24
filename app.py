from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
# heroku = Heroku(app)
db = SQLAlchemy(app)


# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'name': self.email}


# homepage set to index.html
@app.route('/')
def index():
    return render_template('index.html')


# return to home page (index.html)
@app.route('/returnHome')
def returnHome():
    return render_template('index.html')


@app.route('/showAllEmails', methods=['GET'])
# protect this route with a required login
def showAllEmails():
    if request.method == 'GET':
        users = db.session.query(User).all()
        return jsonify(emails=[user.serialize for user in users])


# will save e-mail to database and send to success page
@app.route('/enterEmail', methods=['POST'])
def enterEmail():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
        return render_template('success.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
