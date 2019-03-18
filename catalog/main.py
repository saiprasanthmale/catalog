from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_file import Base, College_Name, Student_Details, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///college_db.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "colleges"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
cls_ca = session.query(College_Name).all()


# login for the user
@app.route('/login')
def showLogin():
    """ It shows the login page for the user"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    """ return "The current session state is %s" % login_session['state']"""
    cls_ca = session.query(College_Name).all()
    clit = session.query(Student_Details).all()
    """ It return to login.html"""
    return render_template('login.html',
                           STATE=state, cls_ca=cls_ca, clit=clit)
    """return render_template('myhome.html', STATE=state
      cls_ca=cls_ca,clit=clit)
    """


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Validate state token """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    """ Obtain authorization code"""
    code = request.data

    try:
        """Upgrade the authorization code into a credentials object"""
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    """Check that the access token is valid."""
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    """If there was an error in the access token info, abort."""
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    """Verify that the access token is used for the intended user."""
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    """ Verify that the access token is valid for this app."""
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    """Store the access token in the session for later use."""
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    """Get user info"""
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    """see if user exists, if it doesn't make a new one"""
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# Here it shows the home


@app.route('/')
@app.route('/home')
def home():
    """ This is the home page it returns to myhome.html """
    cls_ca = session.query(College_Name).all()
    return render_template('myhome.html', cls_ca=cls_ca)

# collegeweb for admins


@app.route('/CollegeWeb')
def CollegeWeb():
    try:
        if login_session['username']:
            name = login_session['username']
            cls_ca = session.query(College_Name).all()
            bit = session.query(College_Name).all()
            clit = session.query(Student_Details).all()
            return render_template('myhome.html', cls_ca=cls_ca,
                                   bit=bit, clit=clit, uname=name)
    except:
        return redirect(url_for('showLogin'))

# It shows the details according to the id


@app.route('/CollegeWeb/<int:clid>/AllColleges')
def showColleges(clid):
    cls_ca = session.query(College_Name).all()
    bit = session.query(College_Name).filter_by(id=clid).one()
    clit = session.query(Student_Details).filter_by(college_name_id=clid).all()
    try:
        if login_session['username']:
            return render_template('showColleges.html', cls_ca=cls_ca,
                                   bit=bit, clit=clit,
                                   uname=login_session['username'])
    except:
        return render_template('showColleges.html',
                               cls_ca=cls_ca, bit=bit, clit=clit)


# we have to add college Name


@app.route('/CollegeWeb/addCollege_Name', methods=['POST', 'GET'])
def addCollege_Name():
    """ if the user has not get login the messege
    get shows below the login page will be displayed """
    if "username" not in login_session:
        flash("Please Login To Add Categories and Everything Your Own")
        return redirect(url_for("showLogin"))
    """ it returns to the addCollege_Name and display the page"""
    if request.method == 'POST':
        college_name = College_Name(name=request.form['name'],
                                    user_id=login_session['user_id'])
        session.add(college_name)
        session.commit()
        return redirect(url_for('CollegeWeb'))
    else:
        return render_template('addCollege_Name.html', cls_ca=cls_ca)

# Here we can edit College Name


@app.route('/CollegeWeb/<int:clid>/edit', methods=['POST', 'GET'])
def editCollege_Name(clid):
    """ if the user has not get login the messege
    get shows below the login page will be displayed"""
    if "username" not in login_session:
        flash("Please Login To Add Categories and Everything Your Own")
        return redirect(url_for("showLogin"))
    editCollege_Name = session.query(College_Name).filter_by(id=clid).one()
    creator = getUserInfo(editCollege_Name.user_id)
    user = getUserInfo(login_session['user_id'])
    """ If logged in user != item owner redirect them"""
    if creator.id != login_session['user_id']:
        flash("You cannot edit this collegename."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CollegeWeb'))
    if request.method == "POST":
        if request.form['name']:
            editCollege_Name.name = request.form['name']
        session.add(editCollege_Name)
        session.commit()
        flash("collegename Edited Successfully")
        return redirect(url_for('CollegeWeb'))
    else:
        """cls_ca is global variable we can them in entire application"""
        return render_template('editCollege_Name.html',
                               cl=editCollege_Name, cls_ca=cls_ca)

# Here we can delete particular College Name


@app.route('/CollegeWeb/<int:clid>/delete', methods=['POST', 'GET'])
def deleteCollege_Name(clid):
    """ if the user has not get login the messege
    get shows below the login page will be displayed"""
    if "username" not in login_session:
        flash("Please Login To Add Categories and Everything Your Own")
        return redirect(url_for("showLogin"))
    cl = session.query(College_Name).filter_by(id=clid).one()
    creator = getUserInfo(cl.user_id)
    user = getUserInfo(login_session['user_id'])
    """ If logged in user != owner redirect them"""
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this college name."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CollegeWeb'))
    if request.method == "POST":
        session.delete(cl)
        session.commit()
        flash("college name Deleted Successfully")
        return redirect(url_for('CollegeWeb'))
    else:
        return render_template('deleteCollege_Name.html', cl=cl, cls_ca=cls_ca)

# Here we can add New Student Details in Particular College


@app.route(
    '/CollegeWeb/addCollege_Name/addStudent_Details/<string:clname>/add',
    methods=['GET', 'POST'])
def addStudent_Details(clname):
    """ if the user has not get login the messege
    get shows below the login page will be displayed"""
    if "username" not in login_session:
        flash("Please Login To Add Categories and Everything Your Own")
        return redirect(url_for("showLogin"))
    bit = session.query(College_Name).filter_by(name=clname).one()
    """ See if the logged in user is not the owner"""
    creator = getUserInfo(bit.user_id)
    user = getUserInfo(login_session['user_id'])
    """ If logged in user != owner redirect them"""
    if creator.id != login_session['user_id']:
        flash("You can't add new student"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showColleges', clid=bit.id))
    if request.method == 'POST':
        stu_name = request.form['stu_name']
        stu_rnumber = request.form['stu_rnumber']
        stu_phone_number = request.form['stu_phone_number']
        stu_course = request.form['stu_course']
        stu_address = request.form['stu_address']
        slink = request.form['slink']
        studentdetails = Student_Details(stu_name=stu_name,
                                         stu_rnumber=stu_rnumber,
                                         stu_phone_number=stu_phone_number,
                                         stu_course=stu_course,
                                         stu_address=stu_address,
                                         slink=slink,
                                         college_name_id=bit.id,
                                         user_id=login_session['user_id'])
        session.add(studentdetails)
        session.commit()
        return redirect(url_for('showColleges', clid=bit.id))
    else:
        return render_template('addStudent_Details.html',
                               clname=bit.name, cls_ca=cls_ca)

# Here we can edit Student Details in the college


@app.route('/CollegeWeb/<int:clid>/<string:clename>/edit',
           methods=['GET', 'POST'])
def editStudent_Details(clid, clename):
    """ if the user has not get login the messege
    get shows below the login page will be displayed"""
    if "username" not in login_session:
        flash("Please Login To Add Categories and Everything Your Own")
        return redirect(url_for("showLogin"))
    cl = session.query(College_Name).filter_by(id=clid).one()
    studentdetails = session.query(
        Student_Details).filter_by(stu_name=clename).one()
    """ See if the logged in user is not the owner"""
    creator = getUserInfo(cl.user_id)
    user = getUserInfo(login_session['user_id'])
    """If logged in user !=  owner redirect them"""
    if creator.id != login_session['user_id']:
        flash("You can't edit this details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showColleges', clid=cl.id))
    """ POST methods"""
    if request.method == 'POST':
        studentdetails.stu_name = request.form['stu_name']
        studentdetails.stu_rnumber = request.form['stu_rnumber']
        studentdetails.stu_phone_number = request.form['stu_phone_number']
        studentdetails.stu_course = request.form['stu_course']
        studentdetails.stu_address = request.form['stu_address']
        studentdetails.slink = request.form['slink']
        session.add(studentdetails)
        session.commit()
        flash("Details Edited Successfully")
        return redirect(url_for('showColleges', clid=clid))
    else:
        return render_template('editStudent_Details.html',
                               clid=clid, studentdetails=studentdetails,
                               cls_ca=cls_ca)

# We can delete Student details in the College


@app.route('/CollegeWeb/<int:clid>/<string:clename>/delete',
           methods=['GET', 'POST'])
def deleteStudent_Details(clid, clename):
    """ if the user has not get login the messege
    get shows below the login page will be displayed"""
    if "username" not in login_session:
        flash("Please Login To Add Categories and Everything Your Own")
        return redirect(url_for("showLogin"))
    cl = session.query(College_Name).filter_by(id=clid).one()
    studentdetails = session.query(
        Student_Details).filter_by(stu_name=clename).one()
    """ See if the logged in user is not the owner"""
    creator = getUserInfo(cl.user_id)
    user = getUserInfo(login_session['user_id'])
    """ If logged in user != item owner redirect them"""
    if creator.id != login_session['user_id']:
        flash("You can't delete this details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showColleges', clid=cl.id))
    if request.method == "POST":
        session.delete(studentdetails)
        session.commit()
        flash("Deleted details Successfully")
        return redirect(url_for('showColleges', clid=clid))
    else:
        return render_template('deleteStudent_Details.html',
                               clid=clid, studentdetails=studentdetails,
                               cls_ca=cls_ca)

# USER LOGOUT


@app.route('/logout')
def logout():
    """ logout the user """
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'
                           })[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected user..'
                                            ), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Json
# It displays the all details that you have


@app.route('/CollegeWeb/JSON')
def allCollegesJSON():
    college_names = session.query(College_Name).all()
    category_dict = [c.serialize for c in college_names]
    for c in range(len(category_dict)):
        studentnames = [i.serialize for i in session.query(
            Student_Details).filter_by(
                college_name_id=category_dict[c]["id"]).all()]
        if studentnames:
            category_dict[c]["colleges"] = studentnames
    return jsonify(College_Name=category_dict)

# It shows the College name


@app.route('/CollegeWeb/college_Name/JSON')
def categoriesJSON():
    colleges = session.query(College_Name).all()
    return jsonify(college_Name=[c.serialize for c in colleges])

# It shows the Details of all students


@app.route('/CollegeWeb/colleges/JSON')
def detailsJSON():
    collegedetails = session.query(Student_Details).all()
    return jsonify(colleges=[i.serialize for i in collegedetails])

# It shows Details in the College


@app.route('/CollegeWeb/<path:collegename>/colleges/JSON')
def categorydetailsJSON(collegename):
    collegeName = session.query(College_Name).filter_by(name=collegename).one()
    colleges = session.query(
        Student_Details).filter_by(
            college_name=collegeName).all()
    return jsonify(collegeName=[i.serialize for i in colleges])

# It Shows the details that you given


@app.route('/CollegeWeb/<path:collegename>/<path:studentdetails_name>/JSON')
def DetailsJSON(collegename, studentdetails_name):
    collegeName = session.query(College_Name).filter_by(name=collegename).one()
    studentDetailsName = session.query(Student_Details).filter_by(
           stu_name=studentdetails_name, college_name=collegeName).one()
    return jsonify(studentDetailsName=[studentDetailsName.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
