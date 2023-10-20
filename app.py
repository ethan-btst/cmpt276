from flask import Flask
from flask import *
from chat_request import text_request
app = Flask(__name__)
app.secret_key = 'your_secret_key' #needed for sessions

# 404 Not found page error
@app.errorhandler(404)
def notfound(e):
    return render_template("404.html")

# Homepage, redirects to login page
@app.route('/')
def index():
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle the login form submission
        username = request.form['username']
        password = request.form['password']
        # todo Perform validation here
        error_message = ''
        if len(username) < 1 or len(password) < 1:
            error_message ='tries to sign up with empty field' 

            #need to check if exists in db

        if len(error_message) > 0:
            return render_template('login.html', error_message=error_message)

        # Redirect to a new page on successful login
        session['username'] = username
        return redirect(url_for('chat'))

    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session: 
        print('logged in user trying to login') 
        return redirect(url_for('chat'))

    if request.method == 'POST':
        # Handle the login form submission
        username = request.form['username']
        # todo Perform authentication and validation here
        error_message = ''
        if len(username) < 1:
            error_message ='tries to login with no usernmae' 
            #need to check if exists in db

        if len(error_message) > 0:
            return render_template('login.html', error_message=error_message)
        # Redirect to a new page on successful login
        session['username'] = username
        if (username == 'admin'):
            return redirect(url_for('admin'))
        return redirect(url_for('chat'))

    # Render the login page for GET requests
    return render_template('login.html')

# Admin page
@app.route('/admin')
def admin():
    if 'username' not in session: #debugging. prevents keyerror
        print('user tries admin accessing dashboard without login') 
        return redirect(url_for('login'))

    if not session['username'] == 'admin':
        print('regular user trying to access admin dashboard')
        return redirect(url_for('index'))

    return render_template('admin.html')

# Add buttons here to the list
buttons = ["text","youtube","article"]


# Page for chat
@app.route('/chat',methods=("GET","POST"))
def chat():

    if 'username' not in session: #debugging. prevents keyerror
        print('user tries accessing regular dashboard without login') 
        return redirect(url_for('login'))

    # Set a default empty response
    if 'current_response' not in session:
        session["current_response"] = '' 

    if "type" not in session:
        session["type"] = 'text'

    print('accessing dashboard for user named: ' + session['username'])
    # Processes chat request
    if request.method == "POST":
        session["type"] = request.form["type"]
        if request.form["submit"] == "Submit":
            user_in = request.form["chatbox"]
            session["type"] = request.form["type"]
            api_key = request.form["api_key"]
            session["current_response"] = text_request(user_in,session['type'],api_key)
        
        else:
            session["current_response"] = ""
        return redirect(request.path)

    # Display result to page
    if request.method == "GET":
        return render_template("chat.html",result=session['current_response'],userResponse=session['username'],buttons=buttons,type=session['type'])

    return render_template("chat.html", userResponse=session['username'],buttons=buttons,type=session['type'])