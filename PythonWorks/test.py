from flask import Flask,redirect,render_template,request,url_for
import sqlite3
app=Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/demo',methods=["POST","GET"])
def login():
    if request.method=="POST":
        user=request.form["id"]
        return redirect(url_for("user",usr=user))
    else:
        return render_template("demo.html")
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

"""@app.route('/view',methods=["POST","GET"])
def view():
    if request.method=="POST":
        key=request.form["id"]
        try:
            conn=sqlite3.connect('C:\\Users\\HP\\Documents\\PythonWorks\\sqlite-tools-win32-x86-3330000\\test.db')
            conn.row_factory=sqlite3.Row
            cur=conn.cursor()
            cur.execute("select * from maintain where id=?",key)
            rrr=cur.fetchall()
        except Exception as e:
            print("error: "+str(e))
        finally:
            return render_template("view.html",rows=rrr)"""
if __name__=="main":
    app.run(debug=True)