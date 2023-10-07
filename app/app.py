from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
categories = {}
expenses = []


# Створення користувача
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user_id = len(users) + 1
    user = {'id': user_id, 'name': data['name']}
    users[user_id] = user
    return jsonify(user), 201


# Отримання користувача за ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({'message': 'Користувача не знайдено'}), 404
    return jsonify(user)


# Видалення користувача за ID
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({'message': 'Користувача не знайдено'}), 404
    del users[user_id]
    return jsonify({'message': 'Користувач видалений'}), 200


# Отримання списку користувачів
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))





if __name__ == '__main__':
    app.run(debug=True)
