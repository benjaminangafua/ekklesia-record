from flask import Blueprint, render_template, request, redirect, flash, session
from .auth import login_required
from churchAPP import db

views = Blueprint('views', __name__)

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

# Landing page
def churchName():
    row = db.execute("SELECT name FROM account WHERE account_id =?", session["user_id"])[0]["name"]
    return row

def churchId():
    row = db.execute("SELECT account_id FROM account WHERE account_id =?", session["user_id"])[0]["account_id"]
    return row
# ----------------------------------------------------------------------------Need Query --------------

# dashboard
@views.route("/dashboard")
@login_required
def home(): 
    # Query church
    church = db.execute("SELECT name FROM account")

    #Total member
    memberSum = db.execute('SELECT COUNT(*) FROM members WHERE account_id=?', churchId())[0]['COUNT(*)']
    
    #Total men
    menSum = db.execute('SELECT COUNT(*) FROM members WHERE gender LIKE "male" AND account_id=?', churchId())[0]['COUNT(*)']

    #Total women
    womenSum = db.execute('SELECT COUNT(*) FROM members WHERE gender LIKE "female" AND account_id=?', churchId())[0]['COUNT(*)']

    #Total Children
    childrenSum = db.execute('SELECT COUNT(*) FROM members WHERE account_id=?', churchId())[0]['COUNT(*)']
    
    # Department's Section
    departmentSum = db.execute('SELECT COUNT(DISTINCT(department_group)) FROM members WHERE account_id=?', churchId())[0]['COUNT(DISTINCT(department_group))']

    if len(church) > 0:

        for name in church:
            if name == church:
                
                # Birthday entry
                this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
                today = int(db.execute("SELECT strftime('%d','now');")[0]["strftime('%d','now')"])
                birth = db.execute(f"SELECT strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day' FROM WHERE account_id=?", churchId())
                
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

                newmember = db.execute("SELECT COUNT(*) FROM members WHERE join_status LIKE 'new convert' AND   WHERE account_id=?", churchId())[0]['COUNT(*)']
                male = db.execute("SELECT COUNT(*) FROM members WHERE gender LIKE 'male' AND join_status LIKE 'new convert'")[0]['COUNT(*)']
                female = db.execute("SELECT COUNT(*) FROM members  WHERE gender LIKE 'female' AND join_status LIKE 'new convert'")[0]['COUNT(*)']
                
                # Member's Section
                memberSum += newmember
                menSum+=male
                womenSum+=female

                return render_template("dashboard-index.html", 
                birth_sum_today=birth_day, birth_sum_this_month=birth_month, newmember=newmember,
                departmentSum=departmentSum, men=menSum, women=womenSum, memberSum=memberSum,church=churchName())
        
    return render_template("dashboard-index.html", departmentSum=departmentSum,  men=menSum, women=womenSum, memberSum=memberSum,church=churchName())

# Display members
@views.route("/member")
@login_required
def displayMember():
    members = db.execute("SELECT * FROM members WHERE account_id=?", churchId())
    return render_template("member.html",members=members)

# Birthday list  
@views.route("/birthday")
@login_required
def birthday():
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    
    birth_rec = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members WHERE account_id=?", churchId())
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)

# New member Form
@views.route('/add-new-member', methods=["GET", "POST"])
@login_required
def createMember():
    if request.method == "POST":

        name = request.form.get("name")
        address = request.form.get("address")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        contact = request.form.get("contact")
        department = request.form.get("department")
        mail = request.form.get("mail")
        join_status = request.form.get("join_status")
        
        find_form = dict(

        name = request.form.get("name"),
        address = request.form.get("address"),
        date_of_birth = request.form.get("date_of_birth"),
        gender = request.form.get("gender"),
        contact = request.form.get("contact"),
        department = request.form.get("department"),
        join_status = request.form.get("join_status"),
        mail = request.form.get("mail")
        )
        print(find_form)
        # Check for existing church and members
        
        if len(db.execute("SELECT * FROM account")) > 0 and len(db.execute("SELECT * FROM members  WHERE account_id=?", churchId())) > 0: 

            member_name = db.execute("SELECT name FROM members WHERE account_id=?", churchId())[0]["name"]
            # Validate member's form
            if not name:
                flash("Invalid name!", category="danger")
            elif not address:
                flash("Invalid address!", category="danger")
            elif not contact or len(contact)< 10:
                flash("Invalid contact!", category="danger")
            elif not gender:
                flash("Invalid gender!", category="danger")
            elif not date_of_birth:
                flash("Invalid date of birth!", category="danger")
            elif not department:
                flash("Invalid department!", category="danger")

            elif not join_status:
                flash("Invalid join_status!", category="danger")

            # Add member if not exist
            elif name != member_name:
                # check for a specific church before inserting

                if churchName():
                    db.execute("INSERT INTO members(name, address, department_group, gender, contact, join_status, date_of_birth, mail, account_id, joined_date) VALUES(?, ?, ?, ?, ?,?,?,?, (SELECT account_id FROM account WHERE account_id=?), date('now'))",
                            name, address, department,  gender, contact,join_status, date_of_birth, mail, churchId())
                    flash("Member created successfull!",category="success")
                    
                    return redirect("/dashboard")
                else:
                    return redirect('/login')
            # Go to members list if already exist
            elif name == member_name:
                flash("Name already exist!", category="danger")
                return redirect('/member')
        else:
            # check for a specific church before inserting
            if churchName():
                db.execute("INSERT INTO members(name, address, department_group, gender, contact, join_status, date_of_birth, mail, account_id, joined_date) VALUES(?, ?, ?, ?, ?,?,?,?, (SELECT account_id FROM account WHERE account_id=?), date('now'))",
                            name, address, department,  gender, contact,join_status, date_of_birth, mail, churchId())
                flash("Member created successfull!",category="success")
                return redirect("/dashboard")
            else:
                return redirect('/login')

    return render_template('add-new-member.html')