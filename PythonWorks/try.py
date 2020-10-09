from flask import Flask,redirect,render_template,url_for,request
import sqlite3
app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def login():
  return render_template("indexpage.html")

@app.route("/nextform",methods=["POST","GET"])
def nextform():
  if request.method == 'POST':
    return render_template("index.html")

@app.route("/listform",methods=["POST","GET"])
def listform():
  if request.method == 'POST':
    return render_template("entry.html")

@app.route("/det",methods=["POST","GET"])
def save():
   msg="msg"
   if request.method == "POST":
     nam=request.form["name"]
     pas=request.form["pass"]
     lin=request.form["link"]
     do=request.form["dom"]
     n=str(nam).lower()
     l=str(lin).lower()
     d=str(do).lower()
     with sqlite3.connect("C:\\Users\\HP\\Documents\\PythonWorks\\data.db") as con:
       msg="connected"
       try:
        cur=con.cursor()
        msg="good"
        cur.execute("INSERT INTO login VALUES('"+d+"', '"+n+"', '"+pas+"', '"+l+"')")
        con.commit(
        )
        msg="added successfully"
       except:
        con.rollback()
       finally:
        return render_template("index.html")
        con.close()

@app.route('/view',methods=["POST","GET"])
def view():
    if request.method == "POST":
        value=request.form["id"]
        key=str(value).lower()
        try:
            conn=sqlite3.connect('C:\\Users\\HP\\Documents\\PythonWorks\\data.db')
            with conn:
                conn.row_factory = sqlite3.Row
                cur=conn.cursor()
                cur.execute('''select * from login where domain=? OR name=? OR weblink=?''',(key,key,key))
                rrr=cur.fetchall()
        except Exception as e:
            print("error: "+str(e))

        finally:
            return render_template("finish.html",rows = rrr)

if __name__ == "main":
 app.run(debug=True)
