
from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# تسجيل الدخول
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = {'id': user[0], 'username': user[1], 'role': user[3]}
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="بيانات الدخول غير صحيحة")
    return render_template('login.html')

# لوحة التحكم حسب الدور
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    role = session['user']['role']
    if role == 'admin':
        return render_template('admin.html')
    elif role == 'delegate':
        return render_template('delegate.html', username=session['user']['username'])
    elif role == 'director':
        return render_template('director.html')
    return "صلاحية غير معروفة"

# تسجيل خروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# عرض جميع المشاريع
@app.route('/view_all_projects')
def view_all_projects():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    projects = c.fetchall()
    conn.close()
    return render_template('all_projects.html', projects=projects)

# روابط تحميل PDF
@app.route('/download_admin_pdf')
def download_admin_pdf():
    return send_file('admin_summary_report_clean.pdf', as_attachment=True)

@app.route('/download_father_pdf')
def download_father_pdf():
    return send_file('father_summary_report_clean.pdf', as_attachment=True)

@app.route('/download_delegate_pdf')
def download_delegate_pdf():
    return send_file('delegate_summary_report_clean.pdf', as_attachment=True)

@app.route('/download_previous_projects_pdf')
def download_previous_projects_pdf():
    return send_file('previous_projects_report_clean.pdf', as_attachment=True)

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

