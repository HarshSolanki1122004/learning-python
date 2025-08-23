from flask import Flask,request,render_template,redirect,url_for,flash

app = Flask(__name__)
app.secret_key = "superSecretKey"

@app.route("/logout")
def logout():
    return render_template("thankyou.html",username="",message="")

@app.route("/",methods=["POST","GET"])
def home():
    return render_template("feedback.html")

@app.route("/feedback",methods=["POST","GET"])
def feedback():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")
        if not username or not message:
            flash("Username Or Message cannot be blank")
            return redirect(url_for("feedback"))
        return render_template("thankyou.html",username=username,message=message)
    else:
        return render_template("feedback.html")
