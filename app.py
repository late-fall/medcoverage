from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

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
    cheapest = ''
    if request.method == 'POST':
        search = request.form['content']
        generic_name = db.session.query(Meds).filter(or_(Meds.generic.like('%'+ search +'%'), 
                                                 Meds.brand.like('%' + search + '%'))).first()
        name = generic_name.generic.split(' ', 1)[0]
        print(name)
        meds = db.session.query(Meds).filter(Meds.generic.like('%'+ name +'%')).order_by(Meds.price - Meds.moh).all()
        final_prices = []
        for med in meds:
            try:
                final_prices.append(format(float(med.price) - float(med.moh),".2f"))
            except:
                final_prices.append('n/a')
        print(final_prices)
        monthly_prices = [format(float(x) * 30, '.2f') if x != 'n/a' else 'n/a' for x in final_prices]
        cheapest = 'Cheapest option is ' + meds[0].brand
    return render_template('index.html', meds = meds, cheapest = cheapest, unit_prices = final_prices, monthly_prices = monthly_prices, n = len(meds))
    
@app.route('/delete/')
def delete():
    return render_template('index.html', meds='')

if __name__ == "__main__":
    app.run(debug = True)