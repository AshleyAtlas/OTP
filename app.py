from flask import Flask, render_template_string, request, session, redirect, url_for
import random
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mastervortyx@gmail.com'
app.config['MAIL_PASSWORD'] = 'frwy ygfg vzuz mxoy'

mail = Mail(app)

email_html = '''
<!DOCTYPE html>
<html>
<head>
<title>Email Login</title>
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #f7fafc; display: flex; justify-content: center; align-items: center; height: 100vh; }
.box { background: #fff; padding: 2em 2.5em; border-radius: 10px; box-shadow: 0 4px 24px #0001; width: 330px; }
h2 { color: #3A3A3A; margin-bottom: 1.5em; }
input[type=email], input[type=text] {width: 100%; padding: 0.7em; margin-bottom: 1em; border: 1px solid #ddd; border-radius: 5px; font-size: 1em;}
input[type=submit] {width: 100%; background: #ff5722; color: #fff; border: none; padding: 0.7em; border-radius: 5px; font-size: 1.04em; cursor: pointer; transition: background 0.2s;}
input[type=submit]:hover {background: #d84315;}
.credit { margin-top: 1.5em; font-size: .95em; color: #888;}
</style>
</head>
<body>
  <form method="post" class="box" autocomplete="off">
    <h2>Sign In / Register</h2>
    <input type="email" name="email" placeholder="Email address" required>
    <input type="submit" value="Get OTP">
    <div class="credit">Made by Vortyx</div>
  </form>
</body>
</html>
'''

otp_html = '''
<!DOCTYPE html>
<html>
<head>
<title>Verify OTP</title>
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; }
.box { background: #fff; padding: 2em 2.3em; border-radius: 10px; box-shadow: 0 4px 24px #0001; width: 330px; }
h2 { color: #26235b; margin-bottom: 1.5em; }
input[type=text] {width: 100%; padding: 0.7em; margin-bottom: 1em; border: 1px solid #ddd; border-radius: 5px; font-size: 1em;}
input[type=submit] {width: 100%; background: #3f51b5; color: #fff; border: none; padding: 0.7em; border-radius: 5px; font-size: 1.02em; cursor: pointer; transition: background 0.2s;}
input[type=submit]:hover {background: #1a237e;}
.resend { margin-top: 0.7em; font-size: .96em;}
</style>
</head>
<body>
  <form method="post" class="box" autocomplete="off">
    <h2>Enter OTP sent to your email</h2>
    <input type="text" name="otp" maxlength="6" placeholder="Enter OTP" required>
    <input type="submit" value="Verify">
    <div class="resend"><a href="/">Change email?</a></div>
  </form>
</body>
</html>
'''

success_html = '''
<!DOCTYPE html>
<html>
<head>
<title>Access Granted</title>
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #e8f5e9; display: flex; justify-content: center; align-items: center; height: 100vh; }
.box { background: #fff; padding: 2em 2.3em; border-radius: 10px; box-shadow: 0 4px 24px #0002; width: 350px; text-align: center;}
h2 { color: #257800; }
p { color: #333; margin-top: 1em; }
</style>
</head>
<body>
  <div class="box">
    <h2>✅ Verified!</h2>
    <p>Your email <b>{{email}}</b> is verified.<br>Hi, you just saw my project. Hope you find it interesting!</p>
  </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['user_email'] = email
        with open("users.txt", "a") as f:
            f.write(email + "\n")
        msg = Message(subject="Your OTP Code",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email],
                      body=f"Your OTP code is {otp}")
        mail.send(msg)
        return redirect(url_for('verify_otp'))
    return render_template_string(email_html)

@app.route("/verify", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        user_otp = request.form["otp"].strip()
        if user_otp == session.get("otp"):
            email = session.get("user_email")
            return render_template_string(success_html, email=email)
        else:
            return render_template_string(otp_html + "<p style='color:red;text-align:center'>❌ Wrong OTP. Try again.</p>")
    return render_template_string(otp_html)

if __name__ == "__main__":
    app.run(debug=True)
