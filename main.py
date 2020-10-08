# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your cosdasdas
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import  SQLAlchemy

from cloudipsp import Api,Checkout

app = Flask(__name__)
#we use data base "shop.db"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#create table in data base
class Item(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title= db.Column(db.String(100),nullable = False)
    price = db.Column(db.Integer,nullable=False)
    isActive = db.Column(db.Boolean,default=True)
    #show data with __repr__
    def __repr__(self):
        return {self.title}

#main page
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all() #get all elements from data base
    return render_template('index.html',data=items)

#page buy
@app.route('/buy/<int:id>')
def buy_page(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) +"00"
    }
    url = checkout.url(data).get('checkout_url')
    return  redirect(url)

@app.route('/create',methods =['POST','GET'])
def create():
    if request.method == "POST":
        title=request.form['title']
        price=request.form['price']
        item = Item(title=title,price=price)
        try:
            db.session.add(item)
            db.session.commit()
            #return redirect('/index.html')
        except:
            pass


    else:
        return  render_template('create.html')

    #if request.method == "POST":
        #title = request.form['title'] #get from title
        #price = request.form['price'] # get price
        #item = Item(title=title,price=price) #put it into Item variable
        #save in data base
        #try:
            #db.session.add(item)
            #db.session.commit()
            #return render_template('create.html')
    #else:
        #return render_template('create.html')



#information about shop

@app.route('/about')
def about():
    return  render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)
