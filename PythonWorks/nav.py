from flask import Flask,redirect,render_template,request,url_for
nav = Flask(__name__)
@nav.route('/')
def index():
    var="sakthi"
    return render_template("loginpage_2.html",v=var)

@nav.route('/allow/<v>',methods=["POST","GET"])
def view(v):
    return ("Hello "+str(v))

if __name__=="main":
    nav.run(debug=True)
         