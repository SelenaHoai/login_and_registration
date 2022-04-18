from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import model_user

from flask_app import DATABASE, bcrypt

from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # @property
    # def fullname(self):
    #     return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @classmethod
    def register_user(cls, data: dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id


    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        user_result = connectToMySQL(DATABASE).query_db(query, data)
        if user_result:
            one_user = (cls(user_result[0]))
            return one_user
        return False


    @classmethod
    def get_one_by_email(cls, data:dict) -> object:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            user_actual = cls(result[0])
            return user_actual
        return False


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        users_result = connectToMySQL(DATABASE).query_db(query)
        all_users = []
        for user in users_result:
            all_users.append(user)
        return all_users


    @staticmethod
    def validator(form_data:dict):
            is_valid = True

            if len(form_data['first_name']) <= 0:
                # session['first_name'] = "first_name is required!"
                flash("First name is required!", 'err_first_name')
                is_valid = False

            if len(form_data['last_name']) <= 0:
                # session['last_name'] = "last_name is required!"
                flash("Last name is required!", 'err_last_name')
                is_valid = False

            if len(form_data['email']) <= 0:
                # session['email'] = "email is required!"
                flash("Email is required!", 'err_email')
                is_valid = False
            elif not EMAIL_REGEX.match(form_data['email']): 
                flash("Invalid email address!", 'err_email')
                is_valid = False

            if len(form_data['password']) < 8:
                # session['password'] = "password is required!"
                flash("Password must be at least 8 characters long!", 'err_password')
                is_valid = False
            if len(form_data['password_confirmation']) < 8:
                # session['password'] = "password is required!"
                flash("Password must be at least 8 characters long!", 'err_password_confirmation')
                is_valid = False
            if (form_data['password'] != form_data['password_confirmation']):
                flash("Passwords must be the same!", 'err_password_confirmation')
                is_valid = False
            return is_valid


    @staticmethod
    def validator_login(form_data:dict):
            is_valid = True

            if len(form_data['email']) <= 0:
                # session['email'] = "email is required!"
                flash("Email is required!", 'err_email_login')
                is_valid = False
            elif not EMAIL_REGEX.match(form_data['email']): 
                flash("Invalid email address!", 'err_email_login')
                is_valid = False

            if len(form_data['password']) < 8:
                # session['password'] = "password is required!"
                flash("Password must be at least 8 characters long!", 'err_password_login')
                is_valid = False
            else:
                potential_user = User.get_one_by_email({'email': form_data['email']})
                print(potential_user)
                if not bcrypt.check_password_hash(potential_user.password, form_data['password']):
                    flash("Invalid Credentials!", 'err_password_login')
                    is_valid = False
                else:
                    session['uuid'] = potential_user.id

            return is_valid


# save || create
# get_all
# get_one
# update_one
# delete_one