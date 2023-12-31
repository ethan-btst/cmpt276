import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask
from flask import *
from chat_request import text_request
import openai
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key' #needed for sessions

UPLOAD_FOLDER = 'upload folder/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1000 * 1000
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'

url = os.environ.get("DATABASE_URL")  # gets db variable 

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, password TEXT, openai_key TEXT);"
)
INSERT_USER = "INSERT INTO users (name, password, openai_key) VALUES (%s, %s, %s);"
USERS = (
    """SELECT * FROM users;"""
)

INVALID_MODELS = []
file = open("invalid models.txt",'r')
lines = file.readlines()
for line in lines:
    INVALID_MODELS.append(line.strip('\n'))
file.close()

Session(app)

@app.post("/api/users")
def create_users():
    connection = psycopg2.connect(url)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
    
    connection.close()
    return {"users table created."}, 201
@app.post("/api/users")
def insert_users(username, password):
    connection = psycopg2.connect(url)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER, (username,password, ''))
    
    connection.close()
    return {"message": f"USER {username} created."}, 201

# Use to update something in the database
# Uses user id in case name needs to be changed
@app.post("/app/users")
def update_user_info(data,data_type,user_id):
    connection = psycopg2.connect(url)
    with connection:
        with connection.cursor() as cursor:

            # Special username case to check for unique user names
            if data_type == 'name':
                status = ''
                cursor.execute("SELECT name FROM users")
                allUsers = cursor.fetchall()

                for i in allUsers:
                    if data == i[0]:
                        status = 'Username taken'
                    
                if data != '' and status == '':
                    cursor.execute("UPDATE users SET %s = '%s' where id = %s;" % (data_type,data,user_id))
                    session['username'] = data
                    status = 'Username changed'

                elif data == '':
                    status = 'Please insert something'

            # General case for password, api keys ...
            else:
                if data == '':
                    status = 'Insert a ' + data_type

                else:
                    cursor.execute("UPDATE users SET %s = '%s' where id = %s;" % (data_type,data,user_id))
                    if (data_type == 'openai_key'):
                        session['openai_key'] = data
                    status = data_type + ' changed to' + data

    connection.close()
    return status

# Gets something about a user from the database
# Could use name, or id to specify which user to get
@app.get("/api/users")
def get_user_info(data,identifier,identity):
    connection = psycopg2.connect(url)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT %s FROM users WHERE %s = '%s';" % (data,identifier,identity))
            info = cursor.fetchone()[0]
    
    connection.close()
    return info


@app.get("/api/users")
def get_users_all():
    connection = psycopg2.connect(url)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(USERS)
            users = cursor.fetchall()
    
    connection.close()
    return users

# 404 Not found page error
@app.errorhandler(404)
def notfound(e):
    return render_template("404.html")

# Homepage, redirects to login page
@app.route('/')
def index():
    create_users()
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle the login form submission
        username = request.form['username']
        password = request.form['password']
        error_message = ''
        if len(username) < 1 or len(password) < 1: # Still tested in case of post sneaky post requests (outside of the html form)
            error_message ='tries to sign up with empty field' 
        users = get_users_all()
        for u in users:
            # print(u[1])
            if (username == u[1]):
                error_message = 'username has been used'

        if len(error_message) > 0:
            print('caught error')
            return render_template('signup.html', error_message=error_message)

        insert_users(username, password)
        # Redirect to a new page on successful login
        session['username'] = username
        session['openai_key'] = '' 
        session['type'] = 'text'
        return redirect(url_for('chat'))

    return render_template('signup.html')

# Logout portion
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session: 
        print('logged in user trying to login') 
        return redirect(url_for('chat'))

    if request.method == 'POST':
        # Handle the login form submission
        username = request.form['username']
        password = request.form['password']

        users = get_users_all()
        print(users)
        error_message = ''
        if len(username) < 1 or len(password) < 1: # Still tested in case of post sneaky post requests (outside of the html form)
            error_message ='tries to login with no usernmae' 

        users = get_users_all()
        isUser = False
        passwordKey = ''

        for u in users:

            if (username == u[1]):
                isUser = True
                passwordKey = u[2]


        if (not isUser):
            error_message='user does not exist'
        elif (password != passwordKey):
            error_message='incorrect password'

        if (len(error_message) > 0):
            return render_template('login.html', error_message=error_message)

        # Add relevent user data to session
        session['username'] = username
        session['openai_key'] = get_user_info('openai_key','name',username)
        session['user_id'] = get_user_info('id','name',username)

        # Redirect to a new page on successful login
        if (username == 'admin'): # Admin Edgecase
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

# Settings page
@app.route("/settings",methods=('GET','POST'))
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        # Move back to chat
        if "chat" in request.form:
            return redirect(url_for('chat'))   

        # Change data
        else:
            change_data = request.form['change']
            change_type = request.form['type']
            status = update_user_info(change_data,change_type,session['user_id'])
            return render_template('settings.html',status = status)
        

    return render_template('settings.html')


# Add buttons here to the list
file_buttons = ["audio file","pdf file","plain text"]
buttons = ["text","youtube","article"] + file_buttons

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

            # Upload file
            file = request.files["file"]
            
            if 'test submit' in request.form:
                test_toggle = True
            else:
                test_toggle = False

            session["type"] = request.form["type"]
            
            session["current_response"] = text_request(
                request.form["user input"],
                request.form["chatbox"],
                session['type'],
                session['openai_key'],
                file,
                test_toggle,
                request.form["user model"]
            )

        else:
            session["current_response"] = ""
        return redirect(request.path)
    try:
        models = openai.OpenAI(api_key=session['openai_key']).models.list()
        models = [model.id for model in models if model.id not in INVALID_MODELS]
    except:
        models = 'Not valid'
    # Display result to page
    if request.method == "GET":
        return render_template("chat.html",
        result=session['current_response'],
        userResponse=session['username'],
        buttons=buttons,
        file_buttons = file_buttons,
        type=session['type'],
        models = models
        )

    return render_template(
        "chat.html",
         userResponse=session['username'],
         buttons=buttons,
         type=session['type'],
         models = models,
         file_buttons = file_buttons
         )