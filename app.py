from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_migrate import Migrate
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required
import os
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# Обробник помилки для прострочених токенів
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


# Обробник помилки для недійсних токенів
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed.", "error": "invalid_token"}),
        401,
    )


# Обробник помилки для немає токена
@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify({
            "description": "Request does not contain an access token.",
            "error": "authorization_required",
        }),
        401,
    )


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
    balance = db.Column(db.Float, nullable=False, default=500)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    default_currency = db.Column(db.String(3), nullable=False, default='USD')
    password = db.Column(db.String(128), nullable=False)


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=True)
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


class Income(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())


# Schema for Income
class IncomeSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    amount = fields.Float()
    time = fields.DateTime()


# Створення користувача


@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    user_schema = UserSchema()

    try:
        hashed_password = pbkdf2_sha256.hash(user_data['password'])
        user = User(username=user_data['username'], password=hashed_password,
                    default_currency=user_data['default_currency'])
        db.session.add(user)
        db.session.commit()

        return jsonify(user_schema.dump(user)), 201
    except ValidationError as e:
        return jsonify({'error': 'Некоректні дані', 'messages': e.messages}), 400


# Ендпоінт для логіну
@app.route('/login', methods=['POST'])
def login_user():
    user_data = request.get_json()
    user_schema = UserSchema()

    try:
        user = User.query.filter_by(username=user_data['username']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'error': 'Неправильне ім\'я користувача або пароль'}), 401

    except ValidationError as e:
        return jsonify({'error': 'Некоректні дані', 'messages': e.messages}), 400


# Видалити користувача за ID
@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
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
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        users_data = UserSchema(many=True).dump(users)
        return jsonify(users_data)
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Створення категорії витрат
@app.route('/category', methods=['POST'])
@jwt_required()
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
@jwt_required()
def get_categories():
    try:
        categories = Category.query.all()
        categories_data = CategorySchema(many=True).dump(categories)
        return jsonify(categories_data)
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


# Видалення категорії витрат за ID
@app.route('/category/<int:category_id>', methods=['DELETE'])
@jwt_required()
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

@app.route('/record/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)

        if not expense:
            return {'error': 'Витрату не знайдено'}, 404

        db.session.delete(expense)
        db.session.commit()

        return {'message': 'Запис про витрату видалено'}, 200
    except Exception as e:
        return {'error': 'Помилка сервера', 'message': str(e)}, 500


# Отримання списку записів
@app.route('/record', methods=['GET'])
@jwt_required()
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
@app.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        data = request.json
        user_id = data.get('user_id')
        amount = data.get('amount')

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Користувача не знайдено'}), 404

        account = Account.query.filter_by(user_id=user_id).first()

        if not account:
            account = Account(user_id=user_id, balance=amount)
            db.session.add(account)
        else:
            if amount <= account.balance:
                account.balance -= amount
                expense = Expense(user_id=user_id, category_id=0, time=datetime.now(), amount=amount)
                db.session.add(expense)
                db.session.commit()
                return jsonify({'message': 'Витрату додано', 'user_id': user_id, 'amount': amount}), 201
            else:
                return jsonify({'message': 'Не вистачає коштів', 'user_id': user_id, 'amount': amount})

    except ValidationError as ve:
        return jsonify({'error': 'Помилка валідації', 'message': ve.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Помилка сервера', 'message': str(e)}), 500


@app.route('/income', methods=['POST'])
@jwt_required()
def add_income():
    try:
        data = request.json
        user_id = data.get('user_id')
        amount = data.get('amount')

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Користувача не знайдено'}), 404

        income = Income(user_id=user_id, amount=amount)

        user_account = Account.query.filter_by(user_id=user_id).first()

        if not user_account:
            user_account = Account(user_id=user_id, balance=amount)
            db.session.add(user_account)
        else:
            user_account.balance += amount

        db.session.add(income)
        db.session.commit()

        income_data = IncomeSchema().dump(income)

        return jsonify({'message': 'Дохід додано', 'income': income_data}), 201
    except ValidationError as ve:
        return jsonify({'error': 'Помилка валідації', 'message': ve.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Помилка серверу', 'message': str(e)}), 500


@app.route('/income/<int:income_id>', methods=['DELETE'])
@jwt_required()
def delete_income(income_id):
    try:
        income = Income.query.get(income_id)
        if not income:
            return jsonify({'message': 'Дохід не знайдено'}), 404

        db.session.delete(income)
        db.session.commit()

        return jsonify({'message': 'Запис про дохід видалено'}), 200
    except Exception as e:
        return jsonify({'error': 'Помилка серверу', 'message': str(e)}), 500


@app.route('/incomes/<int:user_id>', methods=['GET'])
@jwt_required()
def get_incomes(user_id):
    try:
        incomes = Income.query.filter_by(user_id=user_id).all()
        income_data = IncomeSchema(many=True).dump(incomes)
        return jsonify(income_data)
    except Exception as e:
        return jsonify({'error': 'Помилка серверу', 'message': str(e)}), 500


@app.route('/balance/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_balance(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return {'error': 'Користувача не знайдено'}, 404

        account = Account.query.filter_by(user_id=user_id).first()

        if not account:
            return {'error': 'Аккаунт не знайдено'}, 404

        account_data = AccountSchema().dump(account)

        return {'user_id': user_id, 'balance': account_data['balance']}
    except Exception as e:
        return {'error': 'Помилка серверу', 'message': str(e)}, 500


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8082, host='0.0.0.0')
