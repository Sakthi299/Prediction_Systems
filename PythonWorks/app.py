
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
    return render_template("srp_home.html")
  @app.route("/signup",methods=["POST","GET"])
  def signup():
    return render_template("srp_register.html")
  @app.route("/returnlist/<v>",methods=["POST","GET"])
  def returnlist(v):
    return render_template("srp_home.html",v=v)
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
          return render_template("srp_register.html",msg=message)
      if pw != rpw:
        message="Password doesn't match"
        return render_template("srp_register.html",msg=message)
      else:
        users=mongo.db.register.insert({"username":ur,"password":k,"salt":salt})
        return render_template("srp_home.html") 
  
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
        return render_template("srp_home.html",msg=message) 
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
          return render_template("srp_query.html",v=u)
        else:
          message="Invalid Password"  
          return render_template("srp_home.html",msg=message) 

  @app.route("/got/<v>",methods=["POST","GET"])
  def got(v):
    if request.method == "POST":
      message=""
      p=request.form["user"]
      q=request.form["dom"]
      pas=str(p)
      h=int(pas)+3
      high=str(h)
      l=int(pas)-3
      low=str(l)
      caste=str(q).upper()
      if(caste == "OC"):
        ocuser=mongo.db.cutoffs.find({"$and" : [{"OC":{"$lte":high}},{"OC":{"$gte":low}}]})
      if(ocuser.count() <= 0):
        return render_template("view_2.html",msg="No Records Found !!!",user=" ",keyvalue=" ",link=" ",v=v)

      return render_template("view_2.html",user=ocuser)

except Exception as e:
  print(e)

if __name__ == "main":
 app.run(debug=True)