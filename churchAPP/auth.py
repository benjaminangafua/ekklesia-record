from flask import render_template, g, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import functools  
import re
from . import db

from flask import Blueprint

# string = dict(newTxt = "PYTHON new STUff")
# print(string["newTxt"].lower())


auth = Blueprint("auth", __name__)

# auth.secret_key = "hello"
# auth.permanent_session_lifetime = timedelta(minutes=5)
@auth.route('/register', methods=["GET", "POST"])
def registerAccount():
    # Create church account
    if request.method == "POST":
        
        register = dict(
        fullname = request.form.get("full_name"),
        email = request.form.get("email"),
        password =generate_password_hash(request.form.get("password"), "sha256"),
        phone = msisdn_sanitizer(request.form.get("phone"), "+231"),
        confirm_password = request.form.get("confirm_password"),
        address = request.form.get("address"),
        admin_name = (request.form.get("admin_name")).lower()
        )
        
        if len(db.execute("SELECT * FROM account")) > 0:
            data = db.execute("SELECT name FROM account WHERE name=?", register["fullname"])

            if not register["fullname"]:
                flash("Invalid name!", category="danger")

            elif len(register["fullname"]) < 2:
                flash("Full name must be more than 2 characters!", category="danger")

            elif request.form.get("password") != register["confirm_password"]:
                flash("Password not confirm!", category="danger")
            
            # Add account if not exist

            elif data != register["fullname"]:  
                db.execute("INSERT INTO account(name, mail, password, phone, admin_name, address, joined_date) VALUES(?, ?, ?, ?, ?, ?, date('now'))", register["fullname"], register["email"], register["password"], register["phone"], register["admin_name"], register["address"])
                flash("Church system successful created!", category="success")
                return redirect("/") 
            else:
                flash("Church already exist!", category="danger")
                return render_template("register.html")  
        else:
            db.execute("INSERT INTO account(name, mail, password, phone, admin_name, address, joined_date) VALUES(?, ?, ?, ?, ?, ?, date('now'))", register["fullname"], register["email"], register["password"], register["phone"], register["admin_name"], register["address"])
            flash("Church system successful created!", category="success")
            return redirect("/")
    
    return render_template("register.html")     
  
# Sign in
@auth.route("/login", methods=["GET", "POST"])
def loginAccount():
    if request.method == "POST":
        session.permanent=True
        log = dict(
        admin_name = (request.form.get("admin_name")).lower(),
        password =request.form.get("password")
        )
        if len(db.execute("SELECT * FROM account")) > 0:
            if [name for name in db.execute("SELECT * FROM account") if name['admin_name'] == log["admin_name"]]:
                user = [name for name in db.execute("SELECT * FROM account") if name['admin_name'] == 'blessing'][0]
                if check_password_hash(user["password"], log["password"]):

                    flash("Login was successful", category="success")
                    session["user_id"] = user["account_id"]
                    return redirect("/dashboard")
                
            else:
                flash("Invalid Username or Password!", category="danger")
                return redirect("/login")
        else:
            return redirect("/register")
        
    return render_template('login.html')

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            'SELECT * FROM account WHERE account_id = ?', (user_id,)
        )[0]

# Log in required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/login")
        return view(**kwargs)
    return wrapped_view

# Log out
@auth.route("/logout")
@login_required
def logout(): 
    session.pop("user_id",None)
    return redirect("/login")

def msisdn_sanitizer(msisdn, phone_code, leading_zero=False, plus=True) :

    #  append the phone to the msisdn
    msisdn = msisdn.strip()
    msisdn = msisdn.replace('+', '')
    
    pattern = re.compile("[^0-9]")
    msisdn = pattern.sub("", msisdn)

    phone_code = phone_code.replace('+', '')

    pattern = re.compile(r"^("+phone_code+")+")
    msisdn = pattern.sub(phone_code, msisdn)

    regex = "^" + phone_code
    if re.match(regex, msisdn):
        msisdn = msisdn[len(phone_code):]

    if leading_zero is False:
        pattern = re.compile("^0+")
        msisdn = pattern.sub("", msisdn)

    msisdn = phone_code + msisdn
    if plus:
        msisdn = "+" + msisdn
    if not msisdn:
        flash("Invalid Number!", category="danger")
        return redirect(request.url)
    else:
        return msisdn

# Use cases
# Key thing taken care of

#     take care of leading zeros in from of numbers
#     remove excess leading zeros
#     remove invalid character
#     remove white spaces
#     remove repeating phone code

# print(msisdn_sanitizer("+2348030000000", "+234")) # +2348030000000
# print(msisdn_sanitizer("+2348030000000", "+234")) # +2348030000000
# print(msisdn_sanitizer("08030000000", "+234")) # +2348030000000
# print(msisdn_sanitizer("8030000000", "+234")) # +2348030000000
# print(msisdn_sanitizer("+234803000#!*()%,^&0000", "+234")) # +2348030000000
# print(msisdn_sanitizer("+234803000ben0000", "+234")) # +2348030000000
# print(msisdn_sanitizer("+234000000080 3000 00 00","+234")) # +2348030000000
# print(msisdn_sanitizer("+234234234234 80 3000 00 00","+234")) # +2348030000000

