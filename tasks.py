#all imports

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, url_for
import textile

#import os
#from werkzeug import secure_filename



#our own modules from this project

import db
import emails

# configuration

DEBUG = True
SECRET_KEY = 'i\xa5\xdb\x00\x031o\x88)\x9dMW<\xceq\x0c\xb6\xff5\xcdO%\xcch'

DEV = "Development"
PROD = "Production"

ENVIR = DEV


# thats it, now lets do our app



# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = db.connectDB()
    
@app.after_request
def after_request(response):
    g.db.commit()
    g.db.close()
    return response


# Now the application procedures.


@app.route('/', methods=['GET','POST'])
def index():
    if 'username' in session:
        return redirect(url_for('queue'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        
        debug('Before trying to login with email_id '+email_id)

        username = db.logMeIn(g.db,email_id,password)
        
        if username:
            debug('Login successful for email_id : '+email_id)
            
            user = db.getUser(g.db, username)
            
            if user:
                session['username'] = user['username']
                debug('user found and session populated with : '+user['username'])
            else:
                error = "User population failed"
                return redirect(url_for('login', error = error))
                
            return redirect(url_for('queue'))
        else:

            error = 'Login failed. Try again'
            return render_template('login.html',error = error)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    debug('logged out successfully')
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():

    if request.method <> 'POST':
        return render_template('register.html')
    else:
        debug('Registering new User : '+request.form['email_id'])
        db.createUser(g.db, request.form['email_id'], request.form['password'])
        return redirect(url_for('login'))

@app.route('/queue', methods=['GET','POST'])
def queue():
    if 'username' in session:
        users = db.getUsers(g.db)
        if request.method <> 'POST':
            debug('Getting bugList for user : '+session['username'])
            bugList = db.getBugList(g.db, session['username'])
            return render_template('queue.html', bugs = bugList, other_username = session['username'], users= users, queue_user = session['username'])
        else:
            
            if request.form['other_username'] <> 'all':
                debug('Getting bugList for user : '+request.form['other_username'])
                bugList = db.getBugList(g.db, request.form['other_username'])
                return render_template('queue.html', bugs = bugList, other_username = request.form['other_username'], users = users, queue_user = request.form['other_username'])
            else:
                debug('Getting all queues')
                #get a visible drop down of all users.
                #avallark working from here...
                #create an list of list of users
                all_queues = db.getAllQueues(g.db)
                return render_template('all_queues.html', all_queues = all_queues, users=users, other_username = "All")
    else:
        return render_template('login.html', error = 'Login first')

        

@app.route('/addBug', methods=['GET', 'POST'])
def addBug():
    if 'username' in session:
        if request.method <> 'POST':
            return render_template('createbug.html')
        else:
            debug('Creating the bug dictionary for the username : '+session['username'])
            user = db.getUser(g.db, session['username'])
            if user:
                
                user_id = user['user_id']
                
                debug('Building dictionary before creating bug for user_id : '+str(user_id))
                
                bug = dict(title = request.form['title'], customer=request.form['customer'], assigned_to_username = request.form['assigned_to_username'], description = request.form['description'], priority = request.form['priority'], status = 'OPEN', user_id = user_id)

                debug('Calling db.createBug2 for bug '+bug['title'])
                db.createBug2(g.db, bug)
                debug('Created the above bug')
                return redirect(url_for('queue'))
            else:
                return redirect(url_for('queue'))

    else:
        return render_template('login.html', error = 'Login first')

@app.route('/bug', methods=['GET', 'POST'])
def bug():
    bug_id = request.args.get('bug_id', '')
    if request.method <> 'POST':
        debug('Calling getBugHeader')
        bugh = db.getBugHeader(g.db, bug_id)
        debug('Calling getBugBody')
        bugb = db.getBugBody(g.db, bug_id)
        all_status = db.getStatuses(g.db)
        all_users = db.getUsers(g.db)
            
        return render_template('bug.html', bugh = bugh, bugb = bugb, all_status = all_status, all_users = all_users)
    
    else:
        debug('Creating dictionary of bug to update the header for '+str(bug_id))

        assigned_to_user_id = db.getUser(g.db, request.form['assigned_to_username'])['user_id']
        updating_user_id = db.getUser(g.db, session['username'])['user_id']
        
        bug = dict(title = request.form['title'], customer=request.form['customer'], updated_by_username = session['username'], assigned_to_user_id = assigned_to_user_id ,assigned_to_username = request.form['assigned_to_username'], description = request.form['description'], priority = request.form['priority'], status = request.form['status'], updating_user_id = updating_user_id, bug_id = bug_id)


        # creating list of header updates onto the body
        debug(str(bug_id))
        bugh = db.getBugHeader(g.db, bug_id)
    
        changedString = ""
        
        
        if bugh['title'] <> bug['title']:
            changedString += "** Changed Title from "+bugh['title']+" to "+ bug['title'] + "\n"

        #if bugh['description'] <> bug['description']:
        #    changedString += "** Changed Description from "+bugh['description']+" to "+ bug['description'] + "\n"

        if bugh['assigned_to_user_id'] <> bug['assigned_to_user_id']:
            to = db.getUserEmail(g.db,bug['assigned_to_user_id'])
            debug('Sending email to notify assignation to : '+to)
            emails.bugAssignNotify(bug, to)
            changedString += "** Changed Assigned from "+ bugh['assigned_to_username'] + " to "+ request.form['assigned_to_username'] + "\n"

        if bugh['description'] <> bug['description']:
            changedString += "** Changed Bug Description from " + "\n" + bugh['description'] 

        if bugh['customer'] <> bug['customer']:
            changedString += "** Changed Customer from "+bugh['customer']+" to "+ bug['customer'] + "\n"

        if bugh['status'] <> bug['status']:
            changedString += "** Changed Status from "+bugh['status']+" to "+ bug['status'] + "\n"

        if str(bugh['priority']) <> str(bug['priority']):
            changedString += "** Changed Priority from "+str(bugh['priority'])+" to "+ str(bug['priority']) + "\n"
            
        debug(changedString)    
        # Now updating the header with changes
        db.updateBugHeader(g.db, bug)

        newUpdate = changedString + "\n" + request.form['newupdate']
        bugUpdate = dict(update = newUpdate, updated_by_user_id = updating_user_id, bug_id = bug_id)

        db.insertBugUpdate(g.db, bugUpdate)
        
        return redirect(url_for('queue'))


# setup urls

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/categories')
def categories():
    pass

@app.route('/status',methods = ['GET','POST'])
def status():
    
    if request.method <> 'POST':
        status = db.getStatuses(g.db)
        return render_template('status.html', status = status)
    else:
        debug('Adding the status : ' + request.form['status'])
        db.addStatus(g.db, request.form['status'], request.form['description'])
        status = db.getStatuses(g.db)
        return render_template('status.html', status = status)
        
@app.route('/deleteStatus')
def deleteStatus():
    status = request.args.get('status', '')
    description = request.args.get('description', '')

    db.deleteStatus(g.db, status)
    return redirect(url_for('status'))


#Usual debug procedures
        
def debug(t):
    """The procedure logs all comments if the DEBUG configuration variable is set to True"""
    if DEBUG == True:
        db.m_debug(g.db, t)

@app.route('/add')
def add():
    debug(session['username'])
    return redirect(url_for('debugs'))


@app.route('/debugs')
def debugs():
    debug_log = db.getDebug(g.db)
    return render_template('debug.html', debug = debug_log)

@app.route('/flushDebug')
def flushDebug():
    debug('Entering Flush Debug')
    db.flushDebug(g.db)
    return redirect(url_for('debugs'))



# and finally lets start the program.

        
if __name__ == '__main__':
    if ENVIR <> DEV:
        app.run(host='0.0.0.0', port=4000)
    else:
        #DEBUG = False
        app.run(port=4000)

