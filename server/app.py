#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.to_dict() for b in bakeries]), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict()), 200


# --------------------------------------
# ✅ PATCH: Update a bakery's name
# --------------------------------------
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def bakery_update(id):
    bakery = Bakery.query.get_or_404(id)

    # Request sends form data → request.form
    name = request.form.get("name")
    if name:
        bakery.name = name

    db.session.commit()

    return jsonify(bakery.to_dict()), 200



@app.route('/baked_goods')
def baked_goods():
    baked_goods = BakedGood.query.all()
    return jsonify([bg.to_dict() for bg in baked_goods]), 200


# --------------------------------------
# ✅ POST: Create a new baked good
# --------------------------------------
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get("name")
    price = request.form.get("price")
    bakery_id = request.form.get("bakery_id")

    new_bg = BakedGood(
        name=name,
        price=float(price),
        bakery_id=int(bakery_id)
    )

    db.session.add(new_bg)
    db.session.commit()

    return jsonify(new_bg.to_dict()), 201



# --------------------------------------
# ✅ DELETE: Remove baked good
# --------------------------------------
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good successfully deleted"}), 200



@app.route('/')
def index():
    return '<h1>Bakery API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
