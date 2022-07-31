import imp
from flask import Blueprint, render_template, request, redirect, flash, session
from flask_mail import Mail, Message
from sqlalchemy import null
from .auth import login_required
from churchAPP import db
views = Blueprint('views', __name__)

# --------------------------------------------------------------------------- Builder ---------------------------------------
mail = Mail()
# landing page
@views.route("/", methods=["GET", "POST"])
def landingPage():
    if request.method == "POST":
        name = request.form.get("name")
        tel = request.form.get("tel")
        message = request.form.get("message")
        email = request.form.get("email")

        msg = Message('Thanks For Reaching Us!', sender = f'benjaminarkutl2017@gmail.com', recipients = [f'{email}'])
        msg.body = f"""Hi {name}, Thanks for reaching us we will get back to you shortly.""" 
        mail.send(msg) 
        # DELETE FROM table WHERE search_condition ORDER BY criteria LIMIT row_count OFFSET offset;
        db.execute("INSERT INTO visitorRemark(name, tel, email, message, date) VALUES(?, ?, ?, ?, date('now'))", name, tel, email, message)
        print(db.execute("select * from visitorRemark"))
        return redirect("/")
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
# ----------------------------------------------------------------------------Need Query ------------------------

# dashboard
@views.route("/dashboard")
@login_required
def home(): 
    # Query church
    church = db.execute("SELECT * FROM members WHERE account_id=?", churchId())

    if len(church) > 0:
        #Total member
        memberSum = len(db.execute('SELECT name FROM members WHERE account_id=?', churchId()))
        
        #Total men
        menSum = len(db.execute('SELECT * FROM members WHERE gender LIKE "male" AND account_id=?', churchId()))

        #Total women
        womenSum = len(db.execute('SELECT name FROM members WHERE gender LIKE "female" AND account_id=?', churchId()))

        #Total Children
        children = db.execute(f"SELECT strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day' FROM members WHERE account_id=?", churchId())
        
        # Department's Section
        departmentSum = db.execute('SELECT COUNT(DISTINCT(department_group)) FROM members WHERE account_id=?', churchId())[0]['COUNT(DISTINCT(department_group))']
        
        # Birthday entry
        currentDate =  db.execute("SELECT  strftime('%Y','now') as 'ThisYear', strftime('%m','now') as 'Month', strftime('%d','now') as 'Day'")[0]
        this_year = currentDate["ThisYear"]
        this_month = currentDate["Month"]
        today = currentDate["Day"]
        birth = db.execute(f"SELECT strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day' FROM members WHERE account_id=?", churchId())                       

        # New Member

        # countConvert = db.execute("SELECT strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day' FROM members WHERE join_status = 'New Convert' AND account_id=?", churchId())[0]
        # convertYear=getYear(this_year, countConvert["Year"], memberSum), convertMonth=getMonth(this_month, countConvert["Month"], memberSum),
        birth_sum_today=getADay(today, birth, memberSum)
        
        data = [
                ('Jan',  898),
                ('Feb', 732),
                ('Mar', 653),
                ('Apr', 212),
                ('May', 334),
                ('Jun', 993),
                ('Jul', 234),
                ('Aug', 887),
                ('Sept', 653),
                ('Oct', 567),
                ('Nov', 498),
                ('Dec', 1993),
            ]

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        return render_template("dashboard-index.html", 
        birth_sum_today=getADay(today, birth, memberSum), birth_sum_this_month=0, label=labels, value=values,
        departmentSum=departmentSum, men=menSum, women=womenSum, memberSum=memberSum,church=churchName())
    else:
        return redirect("/add-new-member")
def getYear(This_year, Db_Year,total_member ):
    year = 0    
    if int(Db_Year) == This_year:
        year = total_member
        return year
    else:
        return year

def getMonth(This_Month, Db_Month,total_member):
    birth_month = 0
    if int(This_Month) == int(Db_Month):
        birth_month = total_member
        return birth_month
    else:
        return birth_month

def getADay(today, Db_Day, total_member):
    birth_day = 0
    
    for day in Db_Day:
        if int(day["Day"]) == int(today):
            
            birth_day= int(total_member)

            return birth_day
        else:
            return birth_day

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
        baptized = request.form.get("baptize")
        
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
                    db.execute("INSERT INTO members(name, address, department_group, gender, contact, join_status, date_of_birth, mail, account_id, joined_date) VALUES(?, ?, ?, ?,?,?,?,?, (SELECT account_id FROM account WHERE account_id=?), date('now'))",
                            name, address, department,  gender, contact,join_status, date_of_birth, mail, churchId())
                    flash("Member created successful!",category="success")
                    
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
                db.execute("INSERT INTO members(name, address, department_group, gender, contact, join_status, date_of_birth, mail, account_id, joined_date) VALUES(?, ?, ?, ?,?,?,?, ?, (SELECT account_id FROM account WHERE account_id=?), date('now'))",
                            name, address, department,  gender, contact,join_status, date_of_birth, mail, churchId())
                flash("Member created successful!",category="success")
                return redirect("/dashboard")
            else:
                return redirect('/login')

    return render_template('add-new-member.html')
    