from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

# create Flask app and configure session
app = Flask(__name__)
app.secret_key = '12345678'

# create LoginManager instance
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create User model
class User(UserMixin):
    def __init__(self, team_number, code):
        self.team_number = team_number
        self.code = code

    def get_id(self):
        return str(self.team_number)

    def __repr__(self):
        return f'<User {self.team_number}>'

# define user credentials
users = {
    '1': User('1', 'pass'),
    '2': User('2', 'pass')
}

# define user_loader function
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


# define wait route
@app.route('/')
def wait():
    seconds_to_wait = 5 # replace with desired number of seconds to wait
    return render_template('wait.html', seconds=seconds_to_wait)

# define login route and function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        team_number = request.form['team_number']
        code = request.form['code']

        # validate user credentials
        user = users.get(team_number)
        if user is not None and user.code == code:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('challenges'))
        else:
            flash('Invalid team number or code.')
            return redirect(url_for('login'))

    return render_template('login.html')

# define challenges route and function
@app.route('/challenges')
@login_required
def challenges():
    return render_template('home.html')


# define routes for challenges
@app.route('/challenge1')
def challenge1():
    return render_template('challenge1.html')

@app.route('/challenge2')
def challenge2():
    return render_template('challenge2.html')

@app.route('/challenge3')
def challenge3():
    return render_template('challenge3.html')

@app.route('/challenge4')
def challenge4():
    return render_template('challenge4.html')

@app.route('/challenge5')
def challenge5():
    return render_template('challenge5.html')

@app.route('/challenge6')
def challenge6():
    return render_template('challenge6.html')

@app.route('/challenge7')
def challenge7():
    return render_template('challenge7.html')

@app.route('/challenge8')
def challenge8():
    return render_template('challenge8.html')

@app.route('/challenge9')
def challenge9():
    return render_template('challenge9.html')

@app.route('/challenge10')
def challenge10():
    return render_template('challenge10.html')

# define logout route and function
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# run Flask app
if __name__ == '__main__':
    app.run()
