from flask import Blueprint, render_template, request, redirect, flash, session
from .auth import login_required
from churchAPP import db

views = Blueprint('views', __name__)

# Landing page
def churchName():
    row = db.execute("SELECT name FROM account WHERE id =?", session["user_id"])[0]["name"]
    return row

# ---------------------------------------------------------------Need Query --------------

# dashboard
@views.route("/dashboard")
@login_required
def home(): 
    # Query church
    church = db.execute("SELECT name FROM account")

    #Total member
    memberSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']
    
    #Total men
    menSum = db.execute('SELECT COUNT(*) FROM members where gender ="male"')[0]['COUNT(*)']

    #Total women
    womenSum = db.execute('SELECT COUNT(*) FROM members where gender ="female"')[0]['COUNT(*)']

    #Total Children
    childrenSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']
    
    # Department's Section
    departmentSum = db.execute('SELECT COUNT(DISTINCT(department)) FROM members')[0]['COUNT(DISTINCT(department))']

    if len(church) > 0:
        # print(churchName())

        for name in church:
            if name == church:
                print(church)
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
                male = db.execute("SELECT COUNT(*) FROM new_convert where gender like 'male'")[0]['COUNT(*)']
                female = db.execute("SELECT COUNT(*) FROM new_convert where gender like 'female'")[0]['COUNT(*)']
                
                # Member's Section
                memberSum += newmember
                menSum+=male
                womenSum+=female
                # print(memberSum)

                return render_template("dashboard-index.html", 
                birth_sum_today=birth_day, birth_sum_this_month=birth_month, newmember=newmember,
                departmentSum=departmentSum, men=menSum, women=womenSum, memberSum=memberSum,church=churchName())
        
    return render_template("dashboard-index.html", departmentSum=departmentSum,  men=menSum, women=womenSum, memberSum=memberSum,church=churchName())

# Display members
@views.route("/member")
@login_required
def displayMember():
    db.execute("UPDATE account SET currChurch=:accNum", accNum=session["user_id"])

    members = db.execute("SELECT * FROM members ORDER BY id")
    newmember = db.execute("SELECT * FROM new_convert  ORDER BY id")

    return render_template("member.html",members=members, newMember=newmember)

# Convert
@views.route("/convert")
@login_required
def convert():
    convert = db.execute("SELECT * FROM new_convert ORDER BY joined_date")
    return render_template("new-convert.html", converts=convert)

# Birthday list  
@views.route("/birthday")
@login_required
def birthday():
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    
    birth_rec = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)

# Display visitor 
@views.route("/visitor")
@login_required
def visitors():
    visitors_name = db.execute("SELECT * FROM first_time_visitors ORDER BY id")
    return render_template("first-time-visitor.html", visitors_name=visitors_name)


# New member Form
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

# First time visitor Form
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

# Admin profie
@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

#setting
@views.route('/settings')
@login_required
def setting():
    return render_template('settings.html')


# ------------------------------------------------------------------------------ Builder ---------------------------------------

# landing page
@views.route("/")
def landingPage():
    return render_template("index.html")

# Contact form
@views.route('/contact')
@login_required
def contact():
    return render_template('contact.html')
