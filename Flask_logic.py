from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes

DB_USER = 'postgres'
DB_PASS = '+lQue=tp]4tjSi5^'
DB_NAME = 'postgres' 
INSTANCE_CONNECTION_NAME = "lloyds-hack-grp-37:us-west2:pg-fr-hack1298"

# load env vars
db_user = DB_USER # e.g. 'my-database-user'
db_pass = DB_PASS  # e.g. 'my-database-password'
db_name = DB_NAME  # e.g. 'my-database'
instance_connection_name = INSTANCE_CONNECTION_NAME  # e.g. 'project:region:instance'

# Python Connector database connection function
def getconn():
    with Connector() as connector:
        conn = connector.connect(
            instance_connection_name, # Cloud SQL Instance Connection Name
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )
        return conn


app = Flask(__name__)

# configure Flask-SQLAlchemy to use Python Connector
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
# initialize db (using app!)
db = SQLAlchemy(app)

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.String, nullable=False)
    goal_name = db.Column(db.String, nullable=False)
    trustee_name = db.Column(db.String, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    payment_frequency = db.Column(db.String, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)
    payment_limit = db.Column(db.Integer, nullable=True)
    

# Sample data store
trustees = [
    {"id": 1, "name": "Trustee 1", "account_no": "123456", "relation": "Husband", "contact_no": "123-456-7890", "max_amount": 1000},
    {"id": 2, "name": "Trustee 2", "account_no": "654321", "relation": "Wife", "contact_no": "098-765-4321", "max_amount": 500}
]
goal =[]

@app.route('/api/trustees', methods=['GET'])
def get_trustees():
    return jsonify(trustees), 200

@app.route('/api/trustees', methods=['POST'])
def add_trustee():
    data = request.json
    if not all(key in data for key in ["name", "account_no", "relation", "contact_no"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_id = max(trustee["id"] for trustee in trustees) + 1 if trustees else 1
    new_trustee = {
        "id": new_id,
        "name": data["name"],
        "account_no": data["account_no"],
        "relation": data["relation"],
        "contact_no": data["contact_no"]
       # "max_amount": data.get("max_amount", 0)  # Default max_amount if not provided
    }

    trustees.append(new_trustee)
    return jsonify(new_trustee), 201

@app.route('/api/goals', methods=['GET'])
def get_goals():
    #goals = Goal.query.all()
    goals = Goal.query.filter_by(master_id='Incredible').all()
    return jsonify([{
        'id' : goal.id,
        'master_id' : goal.master_id,
        'goal_name' : goal.goal_name,
        'trustee_name' : goal.trustee_name,
        'Amount' : goal.amount,
        'Payment_Frequency' : goal.payment_frequency,
        'frequency' : goal.frequency,
        'Payment_Limit' : goal.payment_limit
    } for goal in goals]), 201

if __name__ == '__main__':
    app.run(debug=True)
