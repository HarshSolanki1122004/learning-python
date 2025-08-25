import os.path
from flask import Flask,render_template,request,redirect,url_for,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "MySecretKEY"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/crud_operations_flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOADS_FOLDER = os.path.join(os.getcwd(),"uploads")
os.makedirs(UPLOADS_FOLDER,exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f"<Employee {self.name}>"


@app.route('/',methods=["GET","POST"])
def index():
    employees = Employee.query.all()
    return render_template("index.html",employees=employees)


@app.route('/add', methods=["POST"])
def addemployee():
    new_employee = Employee(
        name=request.form.get("name"),
        email=request.form.get("email"),
        phone=request.form.get("phone")
    )
    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>",methods=["POST"])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    employee.name = request.form.get("name")
    employee.email = request.form.get("email")
    employee.phone = request.form.get("phone")
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>",methods=["POST"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for("index"))


def allowed_file(filename):
    if "." in filename:
        list = filename.rsplit('.',1)
        lower = list[1].lower()
        if lower in ALLOWED_EXTENSIONS:
            return True
    return False

@app.route("/upload",methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/download/<filename>', methods=["GET"])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)



