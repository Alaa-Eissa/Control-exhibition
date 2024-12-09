from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# إعدادات الاتصال بقاعدة البيانات
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # اسم المستخدم
app.config['MYSQL_PASSWORD'] = 'Natigaa@2022'  # كلمة المرور
app.config['MYSQL_DB'] = 'Votingsystem'  # اسم قاعدة البيانات

mysql = MySQL(app)

# الصفحة الرئيسية
@app.route('/')
def index():
    # جلب المشاريع من قاعدة البيانات
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM votes')
    projects = cur.fetchall()
    cur.close()
    return render_template('index.html', projects=projects)

# تسجيل التصويت
@app.route('/vote', methods=['POST'])
def vote():
    project_id = request.form['project_id']
    
    # تحديث عدد التصويتات في قاعدة البيانات
    cur = mysql.connection.cursor()
    cur.execute("UPDATE votes SET votecount = votecount + 1 WHERE project_id = %s", (project_id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
