from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql://postgres:postgres@localhost:5434/register'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models


@app.route("/home")
def hello():
    return render_template('home.html', title="Home")

@app.route("/register/")
def signup():
    return render_template('register.html', title="REGISTER", information="Use the form displayed to register")


@app.route("/process-register/", methods=['POST'])
def register():
    # Let's get the request object and extract the parameters sent into local variables.
    firstname = request.form['firstname']
    surname = request.form['surname']
    dateofbirth = request.form['dateofbirth']
    residentialaddress= request.form['residentialadress']
    nationality= request.form['nationality']
    nationalidentificationnumber = request.form['nationalidentificationnumber']
    # let's write to the database
    try:
        user = models.User(firstname=firstname, surname=surname, dateofbirth=dateofbirth, residentialaddress=residentialaddress, nationality=nationality, nationalidentificationnumber=nationalidentificationnumber)
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        # Error caught, prepare error information for return
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('register.html', title="REGISTER", information=information)

    # If we have gotten to this point, it means that database write has been successful. Let us compose success info

    # Let us prepare success feedback information

    information = 'MTN user by name {} {} successfully added. The register name is the firstname {}.'.format(firstname, surname)

@app.route("/login/")
def login():
    #Save off in session where we should go after login process. Session survives across requests.
    #Where to go is passed as parameter named next along with the request to /login/ URL.
    session['next_url'] = request.args.get('next', '/') #get the next or use default '/' URL after login
    return render_template('login.html', title="SIGN IN", information="Enter login details")

@app.route("/process-login/", methods=['POST'])
def process_login():
    # Get the request object and the parameters sent.
    email = request.form['email']
    password = request.form['password']

    # call our custom defined function to authenticate user
    if (authenticateUser(email, password)):
        session['username'] = email
        session['userroles'] = 'admin' #just hardcoding for the sake of illustration. This should be read from database.
        return redirect(session['next_url'])
    else:
        error = 'Invalid user or password'
        return render_template('login.html', title="SIGN IN", information=error)

def authenticateUser(email, password):
    # First check to see if the user with the email can be found
    user = models.User.query.filter_by(nationalidentificationnumber=nationalidentificationnumber).first()

    # Notice below that we are using the check_password() function defined in the User class
    # to check password correctness.
    if user and user.check_password(password): # return True only if both are True.
        return True
    else:
        return False

def logged_in():
    if 'username' not in session:
        return False
    else:
        return True

@app.route("/no-anonymity-here/")
def no_anonymity_here():
    if not logged_in():
        return redirect(url_for('login', next='/no-anonymity-here/'))

        # username in session, continue
    return '''
    You have successfully entered a non-anonymous zone. You are logged in as {}.
    <a href="/">Click here to go to the Home page</a>
    '''.format(session['username'])

@app.route("/logout/")
def logout():

    session.pop('username', None) # remove the item with key called username from the session
    session.pop('userroles', None) # remove the item with key called userroles from the session
    return redirect(url_for('home'))

    firstname = request.form['firstname']
    surname = request.form['surname']
    dateofbirth = request.form['dateofbirth']
    residentialaddress= request.form['residentialadress']
    nationality= request.form['nationality']
    nationalidentificationnumber = request.form['nationalidentificationnumber']
    # let's write to the database

    # let's update the database
    try:
        # Get the existing data from database as object
        product = models.User.query.filter_by(id=id).first()
        # Update the fields
        product.firstname = firstname
        product.surname = surname
        product.dateofbirth = dateofbirth
        product.residentialaddress = residentialaddress
        product.nationality = nationality
        product.nationalidentificationnumber = nationalidentificationnumber
        models.db.session.commit()

    except Exception as e:
        error = 'Could not update product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Update not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Update successful", css="success"))


# Flask can also help up handle errors e.g. 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found.html'), 404


@app.route("/")
def home():
    return '''My name is Peace Obasi-Kalu. This is my CA2 work.
 My GitHub URL is https://github.com/PeaceObasi'''
    # In the return statement above, Use your own name and GitHub URL

if __name__ == "__main__":
    app.run(port=5005)
