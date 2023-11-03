from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allmeds.db'
db = SQLAlchemy(app)

class Meds(db.Model):

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
    meds = []
    cheapest = ''
    nomed = ''
    final_prices = []
    monthly_prices = []
    if request.method == 'POST':
        print('test')
        search = request.form['content']
        print(search)
        
        # code to search for generic name when searched brand name.
        generic_name = db.session.query(Meds).filter(or_(Meds.generic.like('%'+ search +'%'), 
                                                 Meds.brand.like('%' + search + '%'))).first()
        
        if not generic_name:
            return render_template('index.html', nomed = "Medication Does Not Exist")

        name = generic_name.generic.split(' ', 1)[0]

        meds = db.session.query(Meds).filter(Meds.generic.like('%'+ name +'%')).order_by(Meds.price - Meds.moh).all()
        meds += db.session.query(Meds).filter(Meds.brand.like('%'+ search +'%')).order_by(Meds.price - Meds.moh).all()


        for med in meds:
            try:
                final_prices.append(format(float(med.price) - float(med.moh),".2f"))
            except:
                try:
                    final_prices.append(format(float(med.price),".2f"))
                except:
                    final_prices.append('N/A')

        monthly_prices = [format(float(x) * 30, '.2f') if x != 'N/A' else 'N/A' for x in final_prices]
        
        for i in range(len(meds)):
            if monthly_prices[i] != 'N/A':
                cheapest = meds[i].brand + ' (' + meds[i].generic + ')' + ' at $' + str(monthly_prices[i])
                break
    return render_template('index.html', meds = meds, cheapest = cheapest, final_prices = final_prices, monthly_prices = monthly_prices, n = len(meds))
    
@app.route('/delete/')
def delete():
    return render_template('index.html', meds=[])

if __name__ == "__main__":
    app.run(debug = True)