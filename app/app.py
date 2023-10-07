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


# Створення запису про витрати
@app.route('/record', methods=['POST'])
def create_expense():
    data = request.json
    expense_id = len(expenses) + 1
    expense = {
        'id': expense_id,
        'user_id': data['user_id'],
        'category_id': data['category_id'],
        'time': data['time'],
        'amount': data['amount']
    }
    expenses.append(expense)
    return jsonify(expense), 201


# Отримання списку записів
@app.route('/record', methods=['GET'])
def get_expenses():
    print(request.args.get('user_id'))
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    if user_id is None and category_id is None:
        return jsonify({'message': 'Вкажіть хоча б один параметр: user_id або category_id'}), 400
    id_exp = []
    if user_id:
        id_exp += [expense for expense in expenses if expense['user_id'] == int(user_id)]
    if category_id:
        id_exp += [expense for expense in expenses if expense['category_id'] == int(category_id)]
    return jsonify(id_exp)


if __name__ == '__main__':
    app.run(debug=True)
