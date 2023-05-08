import math
from random import random

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import session
from uuid import uuid4


# create Flask app and configure session
app = Flask(__name__)
app.secret_key = '12345678'

# create LoginManager instance
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


enigma_code = "ABCD123456"

class User(UserMixin):
    def __init__(self, team_number, code):
        self.team_number = team_number
        self.code = code
        self.session_id = None

    def get_id(self):
        return str(self.team_number)

    def __repr__(self):
        return f'<User {self.team_number}>'

    def login(self):
        self.session_id = str(uuid4())
        session['user_id'] = self.get_id()
        session['session_id'] = self.session_id

    def logout(self):
        self.session_id = None
        session.pop('user_id', None)
        session.pop('session_id', None)

# define user credentials
users = {
    '1': User('1', 'pass'),
    '2': User('2', 'pass'),
    '3': User('3', 'pass')
}

# define user_loader function
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


# define wait route
@app.route('/')
def wait():
    seconds_to_wait = 1 # replace with desired number of seconds to wait
    return render_template('wait.html', seconds=seconds_to_wait)

# define login route and function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("_______  ENTER POST CAPTURE  ______")
        team_number = request.form['team_number']
        print(team_number)
        code = request.form['code']
        print(code)

        # validate user credentials
        user = users.get(team_number)

        if user is not None and user.code == code:
            print("--- USER VALID IN DATABASE ---")
            # check if user is already logged in
            if user.session_id and session.get('session_id') != user.session_id:
                print('DOUBLE DEVICE LOGIN -- ATTEMPT')
                flash('Another device is already logged in with this account.')
                return redirect(url_for('login'))

            # login the user
            user.login()
            print("LOG-IN Successful")
            flash('Logged in successfully.')
            return redirect(url_for('challenges'))
        else:
            print('Invalid team number or code...')
            flash('Invalid team number or code...')
            return redirect(url_for('login'))

    return render_template('login.html')


# define challenges route and function
@app.route('/challenges')
def challenges():
    return render_template('home.html')


# define routes for challenges
@app.route('/challenge1')
def challenge1():
    return render_template('challenge1.html')

@app.route('/challenge1-validator', methods=['POST'])
def challenge1_validator():
    answer = request.form['answer']
    number = enigma_code[0]
    if answer == 'Narnia is coming':
        return render_template('challenge1.html', number=number, result='Congratulations!')
    else:
        return render_template('challenge1.html', number=None, result='Try again!')





@app.route('/challenge2')
def challenge2():
    return render_template('challenge2.html')

@app.route('/challenge2-validator', methods=['POST'])
def challenge2_validator():
    riddle1_answer = request.form.get('riddle1')
    riddle2_answer = request.form.get('riddle2')
    riddle3_answer = request.form.get('riddle3')
    number = enigma_code[1]

    if riddle1_answer.lower() == 'javascript' and riddle2_answer.lower() == 'css' and riddle3_answer.lower() == 'ada lovelace':
        return render_template('challenge2.html', result=number)
    else:
        return render_template('challenge2.html', result='TRY AGAIN')



@app.route('/challenge3')
def challenge3():
    return render_template('challenge3.html')


@app.route('/challenge3-validator', methods=['POST'])
def challenge3_validator(number, answer1, answer2, answer3):
    correct_answers = {
        'Python': 'A popular high-level programming language known for its simplicity and ease of use',
        'JavaScript': 'A client-side scripting language used for creating interactive web pages',
        'HTML': 'A markup language used for creating web pages and web applications',
        'CSS': 'A style sheet language used for describing the presentation of a document written in HTML',
        'Java': 'A popular object-oriented programming language used for creating desktop and mobile applications'
    }

    if len(set([answer1, answer2, answer3])) != 3:
        return 'Please select three different options.'

    if all([correct_answers[answer1] == answer2, correct_answers[answer2] == answer3]):
        return f'Congratulations! The number is {number}.'
    else:
        return 'Sorry, your answers are incorrect. Please try again.'


@app.route('/challenge4')
def challenge4():
    return render_template('challenge4.html')

@app.route('/challenge4-validator', methods=['POST'])
def challenge4_validator():
    chessboard = [[0] * 8 for _ in range(8)]
    for position in request.form.getlist('chessboard[]'):
        row, col = map(int, position.split(','))
        chessboard[row][col] = 1
    if is_valid_chessboard(chessboard):
        number = enigma_code[3]
        return str(number)
    else:
        return '', 400

def is_valid_chessboard(chessboard):
    for row in range(8):
        queens_in_row = sum(chessboard[row])
        if queens_in_row > 1:
            return False
        elif queens_in_row == 1:
            col = chessboard[row].index(1)
            for i in range(col-1, -1, -1): # check left side of the row
                if chessboard[row][i] == 1:
                    return False
            for i in range(col+1, 8): # check right side of the row
                if chessboard[row][i] == 1:
                    return False
            for col in range(8):
                queens_in_col = sum([chessboard[row][col] for row in range(8)])
                if queens_in_col > 1:
                    return False
                elif queens_in_col == 1:
                    row = [chessboard[row][col] for row in range(8)].index(1)
                    for i in range(row - 1, -1, -1):  # check above the column
                        if chessboard[i][col] == 1:
                            return False
                    for i in range(row + 1, 8):  # check below the column
                        if chessboard[i][col] == 1:
                            return False

            for row in range(8):
                for col in range(8):
                    if chessboard[row][col] == 1:
                        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):  # check top-left diagonal
                            if chessboard[i][j] == 1:
                                return False
                        for i, j in zip(range(row - 1, -1, -1), range(col + 1, 8)):  # check top-right diagonal
                            if chessboard[i][j] == 1:
                                return False
                        for i, j in zip(range(row + 1, 8), range(col - 1, -1, -1)):  # check bottom-left diagonal
                            if chessboard[i][j] == 1:
                                return False
                        for i, j in zip(range(row + 1, 8), range(col + 1, 8)):  # check bottom-right diagonal
                            if chessboard[i][j] == 1:
                                return False

            return True
def calculate_number(chessboard):
    columns = [chessboard[row].index(1) for row in range(8)]
    return sum([columns[i] * (10 ** (7-i)) for i in range(8)])

@app.route('/challenge5')
def challenge5():
    return render_template('challenge5.html')

@app.route('/challenge6')
def challenge6():
    return render_template('challenge6.html')

answer = None
@app.route('/challenge7')
def challenge7():
    global answer
    # Generate 4 random numbers between 1 and 10
    A, B, C, D = [7,6,7,6]
    # Compute the answer based on the formula
    answer = int(math.sqrt(A - B) + math.pow(C, 3) - math.pow(C - D, 2) + 2)
    print(answer)
    return render_template('challenge7.html', number=None)

@app.route('/challenge7-validator', methods=['POST'])
def challenge7_validator():
    global answer
    print("-- ENTER VALIDATOR --")
    num = request.form['number']
    print(num)
    num = int(num)
    number = enigma_code[6]
    print(number)
    if answer == num:
        print("ENTER IF")
        return render_template('challenge7.html', number=number, result='Congratulations!')
    else:
        print("ENTER ELSE")
        return render_template('challenge7.html', number=None, result='Try again!')


@app.route('/challenge8')
def challenge8():
    global answer
    A, B, C, D = [7,6,7,6]
    answer = int(math.sqrt(A - B) + math.pow(C, 3) - math.pow(C - D, 2) + 2)
    print(answer)
    return render_template('challenge8.html', number=None)

@app.route('/challenge8-validator', methods=['POST'])
def challenge8_validator():
    global answer
    print("-- ENTER VALIDATOR --")
    num = request.form['number']
    print(num)
    num = int(num)
    number = enigma_code[7]
    print(number)
    if answer == num:
        print("ENTER IF")
        return render_template('challenge8.html', number=number, result='Congratulations!')
    else:
        print("ENTER ELSE")
        return render_template('challenge8.html', number=None, result='Try again!')


@app.route('/challenge9')
def challenge9():
    global answer
    A, B, C, D = [7,6,7,6]
    answer = int(math.sqrt(A - B) + math.pow(C, 3) - math.pow(C - D, 2) + 2)
    print(answer)
    return render_template('challenge9.html', number=None)

@app.route('/challenge9-validator', methods=['POST'])
def challenge9_validator():
    global answer
    print("-- ENTER VALIDATOR --")
    num = request.form['number']
    print(num)
    num = int(num)
    number = enigma_code[8]
    print(number)
    if answer == num:
        print("ENTER IF")
        return render_template('challenge9.html', number=number, result='Congratulations!')
    else:
        print("ENTER ELSE")
        return render_template('challenge9.html', number=None, result='Try again!')



@app.route('/challenge10')
def challenge10():
    global answer
    A, B, C, D = [7,6,7,6]
    answer = int(math.sqrt(A - B) + math.pow(C, 3) - math.pow(C - D, 2) + 2)
    print(answer)
    return render_template('challenge10.html', number=None)

@app.route('/challenge10-validator', methods=['POST'])
def challenge10_validator():
    global answer
    print("-- ENTER VALIDATOR --")
    num = request.form['number']
    print(num)
    num = int(num)
    number = enigma_code[9]
    print(number)
    if answer == num:
        print("ENTER IF")
        return render_template('challenge10.html', number=number, result='Congratulations!')
    else:
        print("ENTER ELSE")
        return render_template('challenge10.html', number=None, result='Try again!')


@app.route('/enigma-validator-render')
def enigma_validator_render():
    return render_template('enigma_validator.html')
@app.route('/enigma-validator', methods=['POST'])
def validate_enigma_code():
    global enigma_code
    code = request.json['code']
    matrix = [1 if c == enigma_code[i] else 0 for i, c in enumerate(code)]
    return jsonify(matrix)

# define logout route and function
@app.route('/logout')
@login_required
def logout():
    current_user.logout()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# run Flask app
if __name__ == '__main__':
    app.run()
