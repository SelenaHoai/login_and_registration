from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models.model_user import User



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome')
def welcome_user():
    context = {
        'all_users': User.get_all_users()
    }

    if 'uuid' in session:
        get_user = User.get_one_user({'id':session['uuid']})
        context['user'] = get_user
    print(context)
    return render_template('dashboard.html', **context)


@app.route('/logout')
def logout():
    # del session['uuid']
    return redirect('/')


@app.route('/login', methods=['post'])
def login():
    # validate that the form is good
    is_valid = User.validator_login(request.form)

    if not is_valid:
        return redirect('/')

    return redirect('/welcome')


@app.route('/register', methods=['post'])
def register():

    # validate user
    is_valid = User.validator(request.form)

    if not is_valid:
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        **request.form,
        'password': pw_hash
    }

    id = User.register_user(data)
    session['uuid'] = id

    return redirect('/welcome')


# @app.route('/')
# def user_show(id):
#     context = {
#         'user': User.get_one({'id': id})
#     }
#     return render_template('index.html', **context)