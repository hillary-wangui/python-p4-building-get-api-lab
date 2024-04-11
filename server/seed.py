from flask import Flask, jsonify
from models import db, Bakery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bakeries.db'
db.init_app(app)

# Models
class Bakery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [{'id': bakery.id, 'name': bakery.name, 'location': bakery.location} for bakery in bakeries]
    return jsonify(bakery_list)

@app.route('/bakeries/<int:bakery_id>')
def get_bakery(bakery_id):
    bakery = Bakery.query.get_or_404(bakery_id)
    bakery_data = {'id': bakery.id, 'name': bakery.name, 'location': bakery.location}
    return jsonify(bakery_data)

if __name__ == '__main__':
    app.run(port=5555,debug=True)
