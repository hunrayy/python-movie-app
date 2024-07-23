from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, sessions
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_mail import Message, Mail
import os
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "marvel"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "henryokiyi8@gmail.com"
app.config["MAIL_PASSWORD"] = ""
app.config["MAIL_DEFAULT_SENDER"] = "henryokiyi8@gmail.com"
subject = "Test mail"
mail = Mail(app)


UPLOAD_FOLDER = "static/assets/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENTIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

mysql = MySQL(app)



@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "GET"):
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form["password"]
    email = request.form["email"]
    passhash = sha256_crypt.encrypt(password)
    print(username)
    # dbcon = mysql.connection.cursor()
    # if(dbcon):
    #     sql = f"""
    #     INSERT INTO user(username, password, email) VALUES(%s, %s, %s)"""
    #     dbcon.execute(sql, (username, passhash, email))
    #     mysql.connection.commit()
    #     return render_template("login.html")
    # return render_template("login.html")

    # send mail
    msg = Message(subject,
                  recipients=email,
                  sender=app.config['MAIL_DEFAULT_SENDER'])
    msg.body = "thanks for registering"
    mail.send(msg)
    info = "Email sent successfully"
    return jsonify(info)



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
            file = request.files['image']
            if(len(title) == 0 or len(genre) == 0 or len(description) == 0):
                return jsonify("invalid input")

            # cursor = mysql.connection.cursor()
            # if(cursor):
            #     sql = f"""
            #     INSERT INTO `movies` (`title`, `genre`, `description`) VALUES (%s, %s, %s)"""
            #     cursor.execute(sql, (title, genre, description))
            #     mysql.connection.commit()
            #     cursor.close()
            #     return render_template("adminDashboard.html", message="Movie uploaded successfully")
            # if file and file.filename:
            #     filename = secure_filename(file.filename)
            #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #     return jsonify("movie uploaded successfully")

        return render_template("upload_movie_form.html")


# get movies route
@app.route("/get-movies", methods=["GET"])
def getMovies():
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM `movies`"
            cursor.execute(sql)
            movies = cursor.fetchall()
            # Convert the result to a list of dictionaries
            movie_list = []
            for row in movies:
                movie_list.append({
                    "id": row['id'], 
                    "genre": row['genre'], 
                    "title": row['title'],  
                    "description": row['description']
                })
            return jsonify(movie_list)
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            cursor.close()



# send mail
# @app.route("/send-mail", methods=["GET"])
# def sendMail():
#         recipient = request.form['recipient']
#         sub
#         try:
#             cursor = mysql.connection.cursor()
#             sql = "SELECT * FROM `movies`"
#             cursor.execute(sql)
#             movies = cursor.fetchall()
#             # Convert the result to a list of dictionaries
#             movie_list = []
#             for row in movies:
#                 movie_list.append({
#                     "id": row['id'], 
#                     "genre": row['genre'], 
#                     "title": row['title'],  
#                     "description": row['description']
#                 })
#             return jsonify(movie_list)
#         except Exception as e:
#             return jsonify({"error": str(e)})
#         finally:
#             cursor.close()
if(__name__ == "__main__"):
    app.run(debug=True)