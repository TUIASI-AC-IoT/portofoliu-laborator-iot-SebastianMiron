from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, jwt_required,
    get_jwt
)
from datetime import timedelta


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'celmaismechersecretvazutvreodata'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)


users = {
    'user1': {'password': 'parola1', 'role': 'admin'},
    'user2': {'password': 'parola2', 'role': 'owner'},
    'user3': {'password': 'parolaX', 'role': 'owner'}
}


invalid_tokens = set()


@app.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)

    if user and user['password'] == password:
        access_token = create_access_token(
            identity=username,
            additional_claims={'role': user['role']}
        )
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'Message': 'Invalid username or password'}), 401


@app.route('/auth/jwtStore', methods=['GET'])
@jwt_required()
def validate():
    jwt_data = get_jwt()
    jti = jwt_data['jti']
    if jti in invalid_tokens:
        return jsonify(msg='Token invalidated'), 404

    return jsonify({'username': get_jwt_identity(), 'role':jwt_data.get('role')}), 200


@app.route('/auth/jwtStore', methods=['DELETE'])
@jwt_required()
def logout():
    jwt_data = get_jwt()
    jti = jwt_data['jti']
    invalid_tokens.add(jti)
    return jsonify({'Message': 'Logged out'}), 200

