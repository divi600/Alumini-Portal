from flask import Flask, render_template, request, redirect, session
from models import db, Student, Alumni, JobPost

app = Flask(__name__)
app.secret_key = "campusconnect"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# ---------------- STUDENT ----------------
@app.route('/student/register', methods=['GET','POST'])
def register_student():
    if request.method == 'POST':
        student = Student(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            department=request.form['department']
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/student/login')
    return render_template('register_student.html')

@app.route('/student/login', methods=['GET','POST'])
def login_student():
    if request.method == 'POST':
        user = Student.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()
        if user:
            session['student_id'] = user.id
            return redirect('/student/dashboard')
    return render_template('student_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    alumni = Alumni.query.all()
    jobs = JobPost.query.all()
    return render_template('dashboard_student.html', alumni=alumni, jobs=jobs)

@app.route('/search', methods=['POST'])
def search():
    company = request.form['company']
    role = request.form['role']
    alumni = Alumni.query.filter(
        Alumni.company.contains(company),
        Alumni.job_role.contains(role)
    ).all()
    jobs = JobPost.query.all()
    return render_template('dashboard_student.html', alumni=alumni, jobs=jobs)

# ---------------- ALUMNI ----------------
@app.route('/alumni/register', methods=['GET','POST'])
def register_alumni():
    if request.method == 'POST':
        alumni = Alumni(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            company=request.form['company'],
            job_role=request.form['job_role'],
            experience=request.form['experience']
        )
        db.session.add(alumni)
        db.session.commit()
        return redirect('/alumni/login')
    return render_template('register_alumni.html')

@app.route('/alumni/login', methods=['GET','POST'])
def login_alumni():
    if request.method == 'POST':
        user = Alumni.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()
        if user:
            session['alumni_id'] = user.id
            return redirect('/alumni/dashboard')
    return render_template('alumni_login.html')

@app.route('/alumni/dashboard')
def alumni_dashboard():
    return render_template('dashboard_alumni.html')

@app.route('/post_job', methods=['GET','POST'])
def post_job():
    if request.method == 'POST':
        post = JobPost(
            title=request.form['title'],
            description=request.form['description'],
            company=request.form['company'],
            alumni_id=session['alumni_id']
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/alumni/dashboard')
    return render_template('post_job.html')

if __name__ == '__main__':
    app.run(debug=True)
