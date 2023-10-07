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


# Створення категорії витрат
@app.route('/category', methods=['POST'])
def create_category():
    data = request.json
    category_id = len(categories) + 1
    category = {
        'id': category_id,
        'name': data['name']
    }
    categories[category_id] = category
    return jsonify(category), 201


# Видалення категорії витрат за ID
@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = categories.get(category_id)
    if category is None:
        return jsonify({'message': 'Категорію не знайдено'}), 404
    del categories[category_id]
    return jsonify({'message': 'Категорія видалена'}), 200


# Отримання списку категорій
@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values()))




if __name__ == '__main__':
    app.run(debug=True)
