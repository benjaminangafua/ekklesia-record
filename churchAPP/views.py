from flask import Blueprint, render_template, request, redirect, flash, session
from .auth import login_required
from churchAPP import db

views = Blueprint('views', __name__)

# Landing page
def churchName():
    row = db.execute("SELECT name FROM account WHERE id =?", session["user_id"])[0]["name"]
    return row
def anniversaryFound():
    sid =  session["user_id"]
    return sid

# landing page
@views.route("/")
def landingPage():
    # if len(db.execute("SELECT * FROM account")) != 0 and len(db.execute("SELECT * FROM members")) !=0: 
    
    #     col = int(db.execute("SELECT currChurch FROM account")[0]["currChurch"])
    #     print(col)
    #     newmember = int(db.execute("SELECT COUNT(*) FROM new_convert")[0]['COUNT(*)'])
    #     memberSum = int(db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)'])
    #     row = db.execute("SELECT * FROM account WHERE id=?", col)[0]
    #     return render_template("landing-index.html", memberSum=memberSum, newmember=newmember, row=row)
    # else:
    return render_template("index.html")

# dashboard
@views.route("/dashboard")
@login_required
def home(): 



    #Total member
    memberSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']

    #Total men
    menSum = db.execute('SELECT COUNT(*) FROM members where gender ="male"')[0]['COUNT(*)']

    #Total women
    womenSum = db.execute('SELECT COUNT(*) FROM members where gender ="female"')[0]['COUNT(*)']

    #Total Children
    childrenSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']

    # Birthday's section
    
    # Department's Section
    departmentSum = db.execute('SELECT COUNT(DISTINCT(department)) FROM members')[0]['COUNT(DISTINCT(department))']

    if len(db.execute("SELECT * FROM account")) > 0:
        # Birthday entry
        this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
        today = int(db.execute("SELECT strftime('%d','now');")[0]["strftime('%d','now')"])
        birth = db.execute(f"SELECT strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day' FROM members")
        
        # Number of birthdays today
        birth_day = 0
        for day in birth:
            if day["Day"] == today:
               birth_day= day["Day"]

        # Number of birthdays this month
        birth_month = 0
        for month in birth:
            if month["Month"] == this_month:
               birth_month = month["Month"]

 
        newmember = db.execute("SELECT COUNT(*) FROM new_convert")[0]['COUNT(*)']
        # Member's Section
        return render_template("dashboard-index.html", 
        birth_sum_today=birth_day, birth_sum_this_month=birth_month, newmember=newmember,
        departmentSum=departmentSum, memberSum=memberSum,church=churchName())
        
    return render_template("dashboard-index.html", departmentSum=departmentSum, memberSum=memberSum)

# create New member
@views.route('/add-new-member', methods=["GET", "POST"])
@login_required
def createMember():
    
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        contact = request.form.get("contact")

        relationship = request.form.get("relationship")
        department = request.form.get("department")
        role_play = request.form.get("role")
        occupation = request.form.get("occupation")
        # not require
        weddingdate = request.form.get("weddingdate")
        
        if len(db.execute("SELECT * FROM account")) != 0 and len(db.execute("SELECT * FROM members")) !=0: 

            data = db.execute("SELECT name FROM members")[0]["name"]
            # Validate member's form
            if not name:
                flash("Invalid name!", category="danger")
            elif not location:
                flash("Invalid location!", category="danger")
            elif not contact or len(contact)< 10:
                flash("Invalid contact!", category="danger")
            elif not gender:
                flash("Invalid gender!", category="danger")
            elif not date_of_birth:
                flash("Invalid date of birth!", category="danger")
            elif not relationship:
                flash("Invalid relationship!", category="danger")
            elif not department:
                flash("Invalid department!", category="danger")
            elif not role_play:
                flash("Invalid role_play!", category="danger")
            elif not occupation:
                flash("Invalid date of occupation!", category="danger")

            # Only add member if not exist
            elif name != data:
                db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, wedding_anniversary, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?, date('now') WHERE acc_id IN(SELECT id FROM account))",
                            name, location, department,  gender, contact, 
                            relationship, occupation, role_play, date_of_birth, weddingdate)
                flash("Member created successfull!",category="success")
                
                return redirect("/dashboard")
            elif name==data:
                flash("Name already exist!", category="danger")
        else:
            db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, wedding_anniversary, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?, date('now'))",
                        name, location, department,  gender, contact, relationship, occupation, role_play, date_of_birth, weddingdate)
            flash("Member created successfull!",category="success")
            return redirect("/dashboard")

    return render_template('add-new-member.html')

# Display members
@views.route("/member")
@login_required
def seeMember():
    db.execute("UPDATE account SET currChurch=:accNum", accNum=session["user_id"])

    members = db.execute("SELECT * FROM members ORDER BY id")
    return render_template("member.html",members=members)

# New convert
@views.route("/add-new-convert", methods=["GET", "POST"])
@login_required
def new_convert():
    if request.method == "POST":
        name=request.form.get("name")
        date_of_birth = request.form.get("date_of_birth")
        gender =request.form.get("gender")
        location = request.form.get("location")
        contact = request.form.get("contact")

        if len(db.execute("SELECT * FROM account")) != 0 and len(db.execute("SELECT * FROM new_convert")) !=0: 

            # Check whether new convert already exist

            data = db.execute("SELECT name FROM new_convert")[0]["name"]

            # Validate new convert's form
            if not name:
                flash("Invalid name!", category="danger")
            elif not location:
                flash("Invalid location!", category="danger")
            elif not contact or len(contact)< 10:
                flash("Invalid contact!", category="danger")
            elif not gender:
                flash("Invalid gender!", category="danger")
            elif not date_of_birth:
                flash("Invalid date of birth!", category="danger")

            elif data != name:
                db.execute("INSERT INTO new_convert(name, gender, date_of_birth, contact, location, joined_date) VALUES(?, ?, ?, ?, ?, date('now'))",
                            name, gender, date_of_birth, contact, location)
                return redirect("/convert")
            else:
                flash("Name already exist.", category="danger")
        else:
            db.execute("INSERT INTO new_convert(name, gender, date_of_birth, contact, location, joined_date) VALUES(?, ?, ?, ?, ?, date('now'))",
                            name, gender, date_of_birth, contact, location)
            return redirect("/convert")
    return render_template("add-new-convert.html")

# Convert
@views.route("/convert")
@login_required
def convert():
    convert = db.execute("SELECT * FROM new_convert ORDER BY joined_date")
    return render_template("new-convert.html", converts=convert)

# First time visitor
@views.route("/add-first-timer", methods=["GET", "POST"])
@login_required
def first_timer():
    if request.method == "POST":
        name=request.form.get("name")
        location = request.form.get("location")
        contact = request.form.get("contact")
        gender = request.form.get("gender")

        if len(db.execute("SELECT * FROM account")) != 0 and len(db.execute("SELECT * FROM first_time_visitors")) !=0: 

            data = db.execute("SELECT name FROM first_time_visitors")[0]["name"]

            # Validate first timer's form 
            if not name:
                flash("Invalid name!", category="danger")
            elif not location:
                flash("Invalid location!", category="danger")
            elif not contact or len(contact)< 10:
                flash("Invalid contact!", category="danger")
            elif not gender:
                flash("Invalid gender!", category="danger")

            # Check whether new convert already exist
            elif data != name:
                db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
                    name, contact, location, gender)

                flash("First timer successfully added!", category="danger")
                return redirect("/visitor")
            else:
                flash("Name already exist.", category="danger")
        else:
            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
                    name, contact, location, gender)
            flash("First timer successfully added!", category="danger")
            return redirect("/visitor")
    return render_template("add-first-timers.html")

# get new visitor
@views.route("/visitor")
@login_required
def visitors():
    visitors_name = db.execute("SELECT * FROM first_time_visitors ORDER BY id")
    return render_template("first-time-visitor.html", visitors_name=visitors_name)

# Birthday list
@views.route("/birthday")
@login_required
def birthday():
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)

# Contact
@views.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

# Home 
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard-index.html')

# events field
# @views.route("/events")
# def events():
#     months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
#     this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
#     birth_rec = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
#     print(f"----------->>>>>>{birth_rec}<<<<<---------------{this_month}")
#     wedding_rec = db.execute("SELECT name, strftime('%Y',wedding_anniversary) as 'Year', strftime('%m',wedding_anniversary) as 'Month', strftime('%d',wedding_anniversary) as 'Day'FROM members;")
    
#     return render_template("events.html", member=birth_rec,wedding=wedding_rec, thisMONTH=this_month, months=months)
 
# use's -profie
@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

#setting
@views.route('/settings')
@login_required
def setting():
    return render_template('settings.html')

# offering
@views.route('/offering', methods=["GET", "POST"])
@login_required
def payOffering():
    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        number = request.form.get("account")
        if len(db.execute("SELECT * FROM account")) != 0 and len(db.execute("SELECT * FROM offering")) !=0: 
            
            data = db.execute("SELECT name FROM offering")[0]["name"]

            # Validate first timer's form 
            if not name:
                flash("Invalid name!", category="danger")
            elif not amount:
                flash("Invalid amount!", category="danger")
            elif not contact or len(contact)< 10:
                flash("Invalid contact!", category="danger")
            elif not number:
                flash("Invalid number!", category="danger")

            elif data == name:
                db.execute("UPDATE offering SET member_name=:name, amount=:amount, number=number, pay_day=date('now') WHERE id >= 0",name= name, amount=amount, number=number)
                return redirect("/dashboard")
            
            db.execute("INSERT INTO offering(member_name, amount, number, pay_day) VALUES(?, ?, ?, date('now'))", name, amount, number)
            return redirect("/dashboard")
        else:
            db.execute("INSERT INTO offering(member_name, amount, number, pay_day) VALUES(?, ?, ?, date('now'))", name, amount, number)
            return redirect("/dashboard")
    return render_template("offering.html", church=churchName())

# send notification
@views.app_context_processor
def notifyUpdate():
    notify = len(db.execute("SELECT * FROM offering;"))
    return  dict(notify=notify)
    
# render notification template
@views.route("/notification")
@login_required
def notification():
    render_offering = db.execute("SELECT * FROM offering ORDER BY pay_day DESC;")
    # db.execute("DELETE FROM offering WHERE id > 0")
    return render_template("notification.html", notifying=render_offering)

def clearBNotification(notes):
    notes = 0
    return notes

def apology(message):
    return render_template("apology.html", message=message)