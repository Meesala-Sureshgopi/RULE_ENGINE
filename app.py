import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, render_template
from rule_engine import create_rule, combine_rules, evaluate_rule

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r'config\database.json')
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def get_next_rule_id():
    """Fetch and increment the highest rule ID from Firestore."""
    metadata_ref = db.collection('metadata').document('highest_rule_id')
    metadata_doc = metadata_ref.get()

    if metadata_doc.exists:
        current_id = metadata_doc.to_dict()['value']
        new_id = current_id + 1
    else:
        new_id = 1  # Initialize if no ID exists

    metadata_ref.set({'value': new_id})
    return str(new_id)

@app.route('/')
def index():
    """Render all existing rules from the database on the home page."""
    rules_ref = db.collection('rules').stream()
    rules = {doc.id: doc.to_dict()['rule'] for doc in rules_ref}
    return render_template('index.html', rules=rules)

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json.get('rule')
    try:
        ast = create_rule(rule_string)
        rule_id = get_next_rule_id()
        db.collection('rules').document(rule_id).set({"rule": rule_string})

        return jsonify({"message": f"Rule created with ID: {rule_id}", "rule_id": rule_id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rule_ids = request.json.get('rule_ids')
    rule_asts = []

    for rule_id in rule_ids:
        rule_ref = db.collection('rules').document(rule_id).get()
        if rule_ref.exists:
            rule_asts.append(create_rule(rule_ref.to_dict()['rule']))
        else:
            return jsonify({"error": f"Rule with ID {rule_id} not found"}), 404

    combined_ast = combine_rules(rule_asts)
    combined_rule_string = repr(combined_ast)
    combined_rule_id = get_next_rule_id()
    db.collection('rules').document(combined_rule_id).set({"rule": combined_rule_string})

    return jsonify({"message": f"Combined rule stored with ID: {combined_rule_id}"})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    """Evaluate a rule's AST against user data."""
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')

    rule_ref = db.collection('rules').document(rule_id).get()
    if rule_ref.exists:
        rule_string = rule_ref.to_dict()['rule']
        ast = create_rule(rule_string)
        result = evaluate_rule(ast, data)
        return jsonify({"result": result})
    else:
        return jsonify({"error": f"Rule with ID {rule_id} not found"}), 404

@app.route('/get_all_rules', methods=['GET'])
def get_all_rules():
    """Fetch all rules from Firestore and return them as JSON."""
    rules_ref = db.collection('rules').stream()
    rules = [{"id": int(doc.id), "rule": doc.to_dict()['rule']} for doc in rules_ref]

    sorted_rules = sorted(rules, key=lambda x: x['id'])
    
    return jsonify({"rules": sorted_rules})

if __name__ == '__main__':
    app.run(debug=True)
