from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)

# connfig db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        

        if request.form['submit_button']=='first_sub':
            headings = ("Project","Employee", "Date", "Hours")

            userDetails = request.form
            project = userDetails['project']
            employee = userDetails['employee']
            date = userDetails['date']
            hours = userDetails['hours']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(project, employee, date, hours)VALUES(%s, %s, %s, %s)",
                    (project, employee, date, hours))
            mysql.connection.commit()
            cur.close()
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT * FROM users")
            if resultValue > 0:
                userDetails = cur.fetchall()
            return render_template('users.html', headings=headings,userDetails=userDetails)
        elif request.form['submit_button']=='second_sub':
            c_box = request.form.getlist('mycheck')

            if "0" in c_box:
                headings = ("Project","Employee", "Date", "Hours")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                user_val = cur.execute("SELECT * FROM users")
                if user_val > 0:
                    check_value = cur.fetchall()
                else:
                    return "<h1>Please add Valid data..</h1>"
                return render_template('agg.html', headings=headings,check_value=check_value)




            if '1' in c_box:
                headings = ("Project","Employee")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                agg_project = cur.execute("SELECT project, sum(hours) from users GROUP by project")
                if agg_project > 0:
                    check_value = cur.fetchall()
                else:
                    return "<h1>Please add Valid data..</h1>"
                return render_template('agg.html', headings=headings,check_value=check_value)
            if '2' in c_box:
                headings = ("Project","Employee","Hours")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                agg_Pro_employee= cur.execute("SELECT project, Employee, sum(hours) from users GROUP by project, Employee ORDER by Project desc")
                if agg_Pro_employee > 0:
                    check_value = cur.fetchall()
                else:
                    return "<h1>Please add Valid data..</h1>"
                       
                return render_template('agg.html', headings=headings,check_value=check_value)
            if '3' in c_box:
                headings = ("Employee","Project","Hours")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                agg_employee = cur.execute("SELECT Employee, Project, sum(hours) from users GROUP by Employee, Project ORDER by Employee desc , sum(hours) desc")
                if agg_employee > 0:
                    check_value = cur.fetchall()
                else:
                    return "<h1>Please add Valid data..</h1>"
                return render_template('agg.html', headings=headings,check_value=check_value)
            


    return render_template('index.html')


    
        

if __name__ == '__main__':
    app.run(debug=True)
