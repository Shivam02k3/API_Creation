from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(80), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Ensure database tables are created
with app.app_context():
    db.create_all()

@app.route('/add-app', methods=['POST'])
def add_app():
    data = request.json
    if not data or not all(key in data for key in ['app_name', 'version', 'description']):
        return jsonify({"error": "Invalid request body"}), 400

    new_app = App(
        app_name=data['app_name'],
        version=data['version'],
        description=data['description']
    )
    db.session.add(new_app)
    db.session.commit()

    return jsonify({"message": "App added successfully", "id": new_app.id}), 201

@app.route('/get-app/<int:id>', methods=['GET'])
def get_app(id):
    app_instance = App.query.get(id)
    if not app_instance:
        return jsonify({"error": "App not found"}), 404

    return jsonify({
        "id": app_instance.id,
        "app_name": app_instance.app_name,
        "version": app_instance.version,
        "description": app_instance.description
    })

@app.route('/delete-app/<int:id>', methods=['DELETE'])
def delete_app(id):
    app_instance = App.query.get(id)
    if not app_instance:
        return jsonify({"error": "App not found"}), 404

    db.session.delete(app_instance)
    db.session.commit()

    return jsonify({"message": "App deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
