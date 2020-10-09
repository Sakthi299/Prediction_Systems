
from flask import Flask,render_template,request,redirect,url_for,session
from flask_pymongo import PyMongo
from cryptography.fernet import Fernet
key=Fernet.generate_key()
salt=key.decode('utf8')

try:
  app=Flask(__name__)
  app.config['MONGO_URI']="mongodb://localhost:27017/manager"
  mongo=PyMongo(app)

  @app.route("/",methods=["POST","GET"])
  def log():
    return render_template("loginpage_2.html")
  @app.route("/signup",methods=["POST","GET"])
  def signup():
    return render_template("register_2.html")
  @app.route("/returnlist/<v>",methods=["POST","GET"])
  def returnlist(v):
    return render_template("second_2.html",v=v)
  @app.route("/register",methods=["POST","GET"])
  def reg():
    message=''
    if request.method =='POST':
      u=request.form['id']
      pw=request.form['pwd']
      rpw=request.form['repwd']
      ur=str(u).lower()
      obj=pw.encode()
      instance=salt.encode()
      crypter=Fernet(instance)
      bush=crypter.encrypt(obj)
      k=str(bush,'utf8')
      users=mongo.db.register.find({})
      for x in users:
        usr=x['username']
        if usr == ur:
          message="Username already exists"
          return render_template("register_2.html",msg=message)
      if pw != rpw:
        message="Password doesn't match"
        return render_template("register_2.html",msg=message)
      else:
        users=mongo.db.register.insert({"username":ur,"password":k,"salt":salt})
        return render_template("loginpage_2.html") 
  
  @app.route("/allow",methods=["POST","GET"])
  def allow():
    message=''
    flag=0
    if request.method == "POST":
      u=request.form["id"]
      pas=request.form["key"]
      name=str(u).lower()
      users=mongo.db.register.find({})
      for x in users:
        n=x['username']
        if n == name:
          flag=1
      if(flag==0):
        message="Invalid Username"  
        return render_template("loginpage_2.html",msg=message) 
      user=mongo.db.register.find({"username":name})
      for x in user:
        pwd=x['password']
        sss=x['salt']
        s=pwd.encode()
        instance=sss.encode()
        crypter=Fernet(instance)
        decryptpw=crypter.decrypt(s)
        returned=decryptpw.decode('utf8')
        if returned == pas:
          return render_template("second_2.html",v=u)
        else:
          message="Invalid Password"  
          return render_template("loginpage_2.html",msg=message) 

  @app.route("/save/<v>",methods=["POST","GET"])
  def insert(v):
    if request.method == "POST":
      w=request.form["web"]
      u=request.form["user"]
      d=request.form["dom"]
      k=request.form["key"]
      pr=str(v).lower()
      web=str(w).lower()
      user=str(u).lower()
      domain=str(d).lower()
      instance=salt.encode()
      crypter=Fernet(instance)
      obj=k.encode()
      pw=crypter.encrypt(obj)
      k=str(pw,'utf8')
      users=mongo.db.wallet.insert({"profile":pr,"name":user,"passkey":k,"domain":domain,"web":web,"salt":salt})
      return render_template("second_2.html",v=v)
  
  @app.route("/insert/<v>",methods=["POST","GET"])
  def join(v):
    return render_template("insert_2.html",v=v)

  @app.route("/got/<v>",methods=["POST","GET"])
  def got(v):
    if request.method == "POST":
      message=""
      p=request.form["id"]
      pas=str(p).lower()
      man=str(v).lower()
      users=mongo.db.wallet.find({ "$or": [{"profile":man,"domain":pas},{"profile":man,"name":pas},{"profile":man,"web":pas}]})
      if(users.count() <= 0):
        return render_template("view_2.html",msg="No Records Found !!!",user=" ",keyvalue=" ",link=" ",v=v)
      for x in users:
        usr=x['name']
        loc=x['web'] 
        d=x['domain']
        ping=x['passkey']
        hhh=x['salt']
      s=ping.encode()
      instance=hhh.encode()
      crypter=Fernet(instance)
      decryptpw=crypter.decrypt(s)
      returned=decryptpw.decode('utf8')
      return render_template("view_2.html",user=usr,keyvalue=returned,link=loc,v=v)

except Exception as e:
  print(e)

if __name__ == "main":
 app.run(debug=True)