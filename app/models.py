from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime, date, time

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password_hash = user_data['password']

    @staticmethod
    def get_by_email(db, email):
        user_data = db.users.find_one({'email': email})
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_id(db, user_id):
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None

    @staticmethod
    def create(db, username, email, password):
        password_hash = generate_password_hash(password)
        user_id = db.users.insert_one({
            'username': username,
            'email': email,
            'password': password_hash
        }).inserted_id
        return User.get_by_id(db, user_id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task:
    @staticmethod
    def create(db, user_id, title, description, category, due_date):
        if isinstance(due_date, date):  # ✅ use 'date' directly
            due_date = datetime.combine(due_date, time.min)

        task = {
            'user_id': ObjectId(user_id),
            'title': title,
            'description': description,
            'category': category,
            'due_date': due_date,
            'completed': False,
            'created_at': datetime.utcnow()
        }
        db.tasks.insert_one(task)

    @staticmethod
    def get_by_user(db, user_id):
        return list(db.tasks.find({'user_id': ObjectId(user_id)}))

    @staticmethod
    def get_by_id(db, task_id):
        return db.tasks.find_one({'_id': ObjectId(task_id)})

    @staticmethod
    def update(db, task_id, updates):
        if 'due_date' in updates and isinstance(updates['due_date'], date):
            updates['due_date'] = datetime.combine(updates['due_date'], time.min)

        db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': updates})

    @staticmethod
    def delete(db, task_id):
        db.tasks.delete_one({'_id': ObjectId(task_id)})

    @staticmethod
    def toggle_complete(db, task_id):
        task = db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            db.tasks.update_one(
                {'_id': ObjectId(task_id)},
                {'$set': {'completed': not task['completed']}}
            )