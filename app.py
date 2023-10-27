from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medications.db'
db = SQLAlchemy(app)

class Meds(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    # content = db.Column(db.String(200), nullable = False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

    din = db.Column(db.Integer, primary_key = True)
    generic = db.Column(db.String(200))
    brand = db.Column(db.String(200))
    price = db.Column(db.String(100))
    moh = db.Column(db.String(100))
    lu = db.Column(db.String(100))  

    def __repr__(self):
        return '<Meds %r>' % self.id

@app.route('/', methods=['POST','GET']) # adding methods
def index():
    meds = ''
    if request.method == 'POST':
        search = request.form['content']
        generic_name = db.session.query(Meds).filter(Meds.brand.like('%'+ search +'%')).first().generic
        if generic_name:
            meds = db.session.query(Meds).filter(Meds.generic.like('%'+ search +'%'), 
                                                 Meds.generic.like('%' + generic_name + '%')).all()
        else:
            meds = db.session.query(Meds).filter(Meds.generic.like('%'+ search +'%')).all()
    return render_template('index.html', meds = meds)
    
@app.route('/delete/')
def delete():
    return render_template('index.html', meds='')

if __name__ == "__main__":
    app.run(debug = True)