import math

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, UserMixin, login_required, current_user
from flask import session
from uuid import uuid4


app = Flask(__name__)
app.secret_key = '12345678'
enigma_code = "ABCD123456"


print("---------------------- start login management --------------------")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
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
users = {
    '1': User('1', 'pass'),
    '2': User('2', 'pass'),
    '3': User('3', 'pass')
}
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)
print("-------------------------  end login management  -----------------------------------")

print("-------------------------- START RouTe MapPing --------------------------------------")


print("--------------------------- BASIC UP-FRONT START ------------------------------------")
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
            flash('Log in with given password.')
            return redirect(url_for('challenges'))
        else:
            print('Invalid team number or code...')
            flash('Invalid team number or code...')
            return redirect(url_for('login'))

    return render_template('login.html')

print("-------------------------- BASIC UP-FRONT END --------------------------------------")





print("--------------------------  HOME AND MENU   --------------------------------------")
@app.route('/i5i5rsuopeyr10cov4ovuev06cb1sxchallenges')
def challenges():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/company-link')
def company_link():
    return redirect('https://linktr.ee/turingthoughts')

print("--------------------------    MENU END    --------------------------------------")



print("--------------------------   CHALLENGES   --------------------------------------")
print("                       ONE 1. ENCRYPTION CHALLENGE                              ")


@app.route('/challenge1')
def challenge1():
    return render_template('challenge1.html')

@app.route('/challenge1-validator', methods=['POST'])
def challenge1_validator():
    answer = request.form['answer'].strip().lower()
    number = enigma_code[0]
    if answer == 'well done cipher':
        return render_template('challenge1.html', number=number, result='Congratulations!')
    else:
        return render_template('challenge1.html', number=None, result='Try again!')



print("-------------------------------------------------------------------------------")
print("                        TWO 2. TECH-BASICS CHALLENGE                                 ")
@app.route('/challenge2')
def challenge2():
    return render_template('challenge2.html')
@app.route('/challenge2-validator', methods=['POST'])
def challenge2_validator():
    riddle1_answer = request.form.get('riddle1')
    riddle2_answer = request.form.get('riddle2')
    riddle3_answer = request.form.get('riddle3')
    number = enigma_code[1]

    if riddle1_answer.strip().lower() == 'javascript' and riddle2_answer.strip().lower() == 'css' and riddle3_answer.strip().lower() == 'ada lovelace':
        return render_template('challenge2.html', result=number)
    else:
        return render_template('challenge2.html', result='TRY AGAIN')



print("-------------------------------------------------------------------------------")
print("                        THREE 3. RIDDLE CHALLENGE                                 ")
@app.route('/challenge3')
def challenge3():
    return render_template('challenge3.html')
@app.route('/challenge3-validator', methods=['POST'])
def challenge3_validator():
    riddle1_answer = request.form.get('riddle1')
    riddle2_answer = request.form.get('riddle2')
    riddle3_answer = request.form.get('riddle3')
    number = enigma_code[2]

    if riddle1_answer.strip().lower() == 'friday' and riddle2_answer.strip().lower() == '25' and riddle3_answer.strip().lower() == '9 pm':
        return render_template('challenge3.html', result=number)
    else:
        return render_template('challenge3.html', result='TRY AGAIN')


print("-------------------------------------------------------------------------------")
print("                        FOUR 4. CHESS QUEEN CHALLENGE                            ")
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




print("-------------------------------------------------------------------------------")
print("                         FIVE 5. IMAGE CHALLENGE                               ")
@app.route('/challenge5')
def challenge5():
    return render_template('challenge5.html')
@app.route('/challenge5-validator', methods=['POST'])
def challenge5_validator():
    answer1 = request.form.get('q1')
    answer2 = request.form.get('q2')
    number = enigma_code[4]

    if answer1 == 'b' and answer2 == 'c':
        return render_template('challenge5.html',number=number, result='CORRECT')
    else:
        return render_template('challenge5.html',number=None, result='TRY AGAIN')



print("-------------------------------------------------------------------------------")
print("                          SIX 6. UNSCRAMBLE RAMBLE                             ")
@app.route('/challenge6')
def challenge6():
    return render_template('challenge6.html')

@app.route('/challenge6-validator', methods=['POST'])
def challenge6_validator():
    question1_answer = request.form.get('question1')
    question2_answer = request.form.get('question2')
    number = enigma_code[5]

    if question1_answer.strip().lower() == 'parachute' and question2_answer.strip().lower() == 'anniversary':
        return render_template('challenge3.html',number=number, result='SUCCESSFUL !')
    else:
        return render_template('challenge3.html',number=None,  result='TRY AGAIN')



print("-------------------------------------------------------------------------------")
print("                           SEVEN 7 . QUATER - 1                                 ")
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



print("-------------------------------------------------------------------------------")
print("                          EIGHT 8  . QUATER - 2                                 ")
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


print("-------------------------------------------------------------------------------")
print("                           NINE 9 . QUATER - 3                                 ")
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


print("-------------------------------------------------------------------------------")
print("                            TEN 10 . QUATER - 4                                 ")
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



print("-------------------------------------------------------------------------------")
print("                             CHALLENGES END                                    ")
print("-------------------------------------------------------------------------------")



print("--------------------------------  eNIGMa Validation  -----------------------------")
@app.route('/enigma-validator-render')
def enigma_validator_render():
    return render_template('enigma_validator.html')
@app.route('/enigma-validator', methods=['POST'])
def validate_enigma_code():
    global enigma_code
    code = request.json['code']
    matrix = [1 if c == enigma_code[i] else 0 for i, c in enumerate(code)]
    return jsonify(matrix)
print("---------------------------------------------------------------------------------")



print("----------------------------  end route mapping  ----------------------------------")


@app.route('/logout')
@login_required
def logout():
    current_user.logout()
    flash('Logged out successfully.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()

print("------------------------------   END OF PRGM  ----------------------------------")