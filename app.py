from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "MySecretKEY"



employees = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "phone": "9876543210"},
]
@app.route('/',methods=["GET","POST"])
def index():
    return render_template("index.html",employees=employees)


@app.route('/add', methods=["POST"])
def addemployee():
    new_employee = {
        "id": len(employees) + 1,
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
    }
    employees.append(new_employee)
    return redirect(url_for("index"))

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_employee(id):
    for ele in employees:
        if ele["id"] == id:
            ele["name"] = request.form.get("name")
            ele["email"] = request.form.get("email")
            ele["phone"] = request.form.get("phone")
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete_employee(id):
    for ele in employees:
        dict = ele
        if dict.get("id") == id:
            employees.remove(ele)
            break
        else:
            continue
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

