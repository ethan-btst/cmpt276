import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask
from flask import *
from chat_request import text_request

app = Flask(__name__)
app.secret_key = 'your_secret_key' #needed for sessions


UPLOAD_FOLDER = 'upload folder/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

url = os.environ.get("DATABASE_URL")  # gets db variable 
connection = psycopg2.connect(url)

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, password TEXT);"
)
INSERT_USER = "INSERT INTO users (name, password) VALUES (%s, %s);"
USERS = (
    """SELECT * FROM users;"""
)
GET_USER_ID = "SELECT id FROM users WHERE name = '%s';"
CHANGE_USER_DATA = "UPDATE users SET %s = '%s' where id = %s;"
@app.post("/api/users")
def create_users(username, password):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER, (username,password))
    return {"message": f"USER {username} created."}, 201

@app.post("/app/users")
def update_info(data,data_type):
    current_user = session['username']
    print(current_user)
    with connection:
        with connection.cursor() as cursor:

            cursor.execute(GET_USER_ID % (session['username']))
            user_id = cursor.fetchone()[0]

            # Special username case to check for unique user names
            if data_type == 'name':
                cursor.execute("SELECT name FROM users")
                allUsers = cursor.fetchone()

                for i in allUsers:
                    if data == i[0]:
                        return 'Username taken'
                    
                if data == '':
                    return 'Insert a username'

                else:
                    cursor.execute(CHANGE_USER_DATA % (data_type,data,user_id))
                    session['username'] = data
                    return 'Username changed'

            # General case
            else:
                if data == '':
                    return 'Insert a ' + data_type

                else:
                    cursor.execute(CHANGE_USER_DATA % (data_type,data,user_id))
                    return data_type + ' changed'
    



@app.get("/api/users")
def get_users_all():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(USERS)
            users = cursor.fetchall()
    return users

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

        create_users(username, password)
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

        # Redirect to a new page on successful login
        session['username'] = username

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
    if request.method == 'POST':

        # Move back to chat
        if "chat" in request.form:
            return redirect(url_for('chat'))   

        # Change data
        else:
            change_data = request.form['change']
            change_type = request.form['type']
            status = update_info(change_data,change_type)
            return render_template('settings.html',status = status)
        

    return render_template('settings.html')


# Add buttons here to the list
buttons = ["text","youtube","article","test submit"]

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
            if file.filename != '':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))

            
            user_in = request.form["chatbox"]
            session["type"] = request.form["type"]
            api_key = request.form["api_key"]
            session["current_response"] = text_request(
                user_in,
                session['type'],
                api_key,
                file.filename
            )

        else:
            session["current_response"] = ""
        return redirect(request.path)

    # Display result to page
    if request.method == "GET":
        return render_template("chat.html",result=session['current_response'],userResponse=session['username'],buttons=buttons,type=session['type'])

    return render_template("chat.html", userResponse=session['username'],buttons=buttons,type=session['type'])