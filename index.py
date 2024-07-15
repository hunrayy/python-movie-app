from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, sessions
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "marvel"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)



@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "GET"):
        return render_template("register.html")
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    passhash = sha256_crypt.encrypt(password)
    dbcon = mysql.connection.cursor()
    if(dbcon):
        sql = f"""
        INSERT INTO user(username, password, email) VALUES(%s, %s, %s)"""
        dbcon.execute(sql, (username, passhash, email))
        mysql.connection.commit()
        return render_template("login.html")
    return render_template("login.html")


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        email = request.form["email"]
        password = request.form["password"]
        print(email)
        cursor = mysql.connection.cursor()
        if(cursor):
            # return("success")
            sql = f"""
            SELECT * FROM user WHERE email = %s"""
            result = cursor.execute(sql, (email,))
            feedback = cursor.fetchone()
            if(feedback):
                email = feedback["email"]
                passwordDb = feedback["password"]
                if(sha256_crypt.verify(password, passwordDb)):
                    return redirect(url_for('adminDashboard'))
                
    return(render_template("login.html"))
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if(request.method == "POST"):
#         email = request.form["email"]
#         password = request.form["password"]
#         cursor = mysql.connection.cursor()
#         if(cursor):
#             # return("success")
#             sql = f"""
#             SELECT * FROM user WHERE email = %s"""
#             result = cursor.execute(sql, (email,))
#             feedback = cursor.fetchone()
#             if(feedback):
#                 email = feedback["email"]
#                 passwordDb = feedback["password"]
#                 if(sha256_crypt.verify(password, passwordDb)):
#                     return(render_template("dashboard.html", email=email))
#                 # return(jsonify(feedback["email"]))
#             # cursor.connection.commit()
#             # cursor.close()
#             # return("hello")
#             # return(jsonify(result))
#         return(render_template("sign.html"))


@app.route("/adminDashboard", methods=["GET"])
def adminDashboard():
    return render_template("adminDashboard.html")


@app.route("/uploadMovie", methods=["GET", "POST"])
def uploadMovie():
        if(request.method == "POST"):
            title = request.form["title"]
            genre = request.form["genre"]
            description = request.form["description"]
            cursor = mysql.connection.cursor()
            if(cursor):
                sql = f"""
                INSERT INTO `movies` (`title`, `genre`, `description`) VALUES (%s, %s, %s)"""
                cursor.execute(sql, (title, genre, description))
                mysql.connection.commit()
                cursor.close()
                return render_template("upload_movie_form.html", message="Movie uploaded successfully")
        return render_template("upload_movie_form.html")
                
if(__name__ == "__main__"):
    app.run(debug=True)