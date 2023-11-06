from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# users = {
#     1: {"name": "Igor", "email": "igor@example.com"},
#     2: {"name": "Oleg", "email": "oleg@example.com"},
#     3: {"name": "Alan", "email": "alan@example.com"},
#     4: {"name": "Sanya", "email": "sanya@example.com"},
#     5: {"name": "Kir", "email": "kir@example.com"},
#     6: {"name": "Denys", "email": "denys@example.com"},
# }
# categories = {
#      1: {"name": "Girls", "description": "Categories related to girls"},
#      2: {"name": "Games", "description": "Categories related to games"},
#      3: {"name": "Food", "description": "Categories related to food"},
#      4: {"name": "Cars", "description": "Categories related to cars"},
#      5: {"name": "Education", "description": "Categories related to education"},
#      6: {"name": "Travels", "description": "Categories related to travels"},
# }
expenses = []


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    default_currency = db.Column(db.String(3), nullable=False, default='USD')


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    default_currency = fields.Str()


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()


class ExpenseSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    category_id = fields.Int()
    time = fields.DateTime()
    amount = fields.Float()


class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Float(required=True)


# Створення користувача
@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_schema = UserSchema()
    try:
        user = user_schema.load(user_data)
    except ValidationError as e:
        return jsonify({'error': 'Некоректні дані', 'messages': e.messages}), 400

    return jsonify(user), 201


# Отримання користувача за ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'Користувача не знайдено'}), 404

        user_data = UserSchema().dump(user)
        return jsonify(user_data)
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Видалити користувача за ID
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'message': 'Користувача не знайдено'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'Користувач видалений'}), 200
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Отримати всіх користувачів
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = UserSchema(many=True).dump(users)
        return jsonify(users_data)
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Створення категорії витрат
@app.route('/category', methods=['POST'])
def create_category():
    try:
        data = CategorySchema().load(request.json)
        category = Category(**data)
        db.session.add(category)
        db.session.commit()
        result = CategorySchema().dump(category)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Отримання списку категорій
@app.route('/category', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        categories_data = CategorySchema(many=True).dump(categories)
        return jsonify(categories_data)
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Видалення категорії витрат за ID
@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if category is None:
            return jsonify({'message': 'Категорію не знайдено'}), 404

        db.session.delete(category)
        db.session.commit()

        category_schema = CategorySchema()
        category_data = category_schema.dump(category)

        return jsonify({'message': 'Категорія видалена', 'category': category_data}), 200
    except ValidationError as ve:
        return jsonify({'error': 'Помилка серіалізації', 'message': ve.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Створення запису про витрати
@app.route('/record', methods=['POST'])
def create_expense():
    try:
        data = ExpenseSchema().load(request.json)
        expense = Expense(**data)
        db.session.add(expense)
        db.session.commit()
        result = ExpenseSchema().dump(expense)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Отримання списку записів
@app.route('/record', methods=['GET'])
def get_expenses():
    try:
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')
        if user_id is None and category_id is None:
            return jsonify({'message': 'Вкажіть хоча б один параметр: user_id або category_id'}), 400

        query = Expense.query
        if user_id:
            query = query.filter(Expense.user_id == user_id)
        if category_id:
            query = query.filter(Expense.category_id == category_id)

        expenses = query.all()
        expenses_data = ExpenseSchema(many=True).dump(expenses)
        return jsonify(expenses_data)
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Ендпоінт для додавання доходу
@app.route('/income', methods=['POST'])
def add_income():
    try:
        data = request.json
        user_data = UserSchema().load(data)
        user_id = user_data['id']
        amount = data.get('amount')
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Користувача не знайдено'}), 404

        account = Account.query.filter_by(user_id=user_id).first()

        if not account:
            account = Account(user_id=user_id, balance=amount)
            db.session.add(account)
        else:
            account.balance += amount

        db.session.commit()

        account_data = AccountSchema().dump(account)

        return jsonify({'message': 'Дохід додано', 'user_id': user_id, 'amount': amount, 'account': account_data}), 201
    except ValidationError as ve:
        return jsonify({'error': 'Помилка валідації', 'message': ve.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=10000, host='0.0.0.0')
