import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import json
from flask import Flask
from sqlalchemy import DECIMAL
from random import randrange


app = Flask(__name__, template_folder='template')
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@localhost/AirbnbPlus"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def loct_init():
    root = os.listdir('json_data')
    loc_dt = {}
    c = 1
    for city in root:
        try:
            loc_dir = os.listdir('json_data/' + city + '/location')
        except NotADirectoryError:
            continue
        loc_dt[city.lower()] = {}
        for fl in loc_dir:
            f = open(os.path.join('json_data', city, 'location', fl), 'r', encoding='utf-8')
            js = json.load(f)
            f.close()
            loc_dt[city.lower()][fl.split('.')[0]] = js
    return loc_dt


class Listing(db.Model):
    __tablename__ = "listings"
    cid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.Text)
    price = db.Column(db.String(10))
    city = db.Column(db.String(30))
    time = db.Column(db.String(15))
    plus = db.Column(db.Integer)
    style = db.Column(db.Integer)
    roomtype = db.Column(db.Integer)
    lat = db.Column(DECIMAL(16, 13))
    lng = db.Column(DECIMAL(16, 13))


def randomSelect(loc):
    result = []
    for p in loc:
        if p["plus"] == 1:
            t = randrange(0, 10)
            if t < 3:
                result.append(p)
        if p["plus"] == 0:
            t = randrange(0, 20)
            if t == 0:
                result.append(p)
    return result


def update():
    root = os.listdir('json_data')
    c = 1
    for city in root:
        try:
            loc_dir = os.listdir('json_data/' + city + '/location')
        except NotADirectoryError:
            continue
        for time in loc_dir:
            f = open(os.path.join('json_data', city, 'location', time), 'r', encoding='utf-8')
            js = json.load(f)
            f.close()
            t = time.split('.')[0]
            for p in js:
                listing = Listing(
                                  cid=c,
                                  id=int(p["id"]),
                                  name=p["name"],
                                  price=p["price"],
                                  city=city,
                                  time=t,
                                  style=p["style"],
                                  plus=p["plus"],
                                  roomtype=p["roomtype"],
                                  lat=p["lnglat"][0],
                                  lng=p["lnglat"][1]
                                  )
                db.session.add(listing)
                c += 1
            db.session.commit()
            print(city, time)
        print(city, 'finished')
    print('end')
    db.session.commit()


def get_loc(ct, plus, time):
    result = []
    if plus == 'both':
        lsts = Listing.query.filter(and_(Listing.city == ct, Listing.time == time)).all()
    elif plus == 'plus':
        lsts = Listing.query.filter(and_(Listing.city == ct, Listing.time == time, Listing.plus == 1)).all()
    else:
        lsts = Listing.query.filter(and_(Listing.city == ct, Listing.time == time, Listing.plus == 0)).all()
    for l in lsts:
        dic = {}
        dic["id"] = l.id
        dic["name"] = l.name
        dic["price"] = l.price
        dic['lnglat'] = [float(l.lat), float(l.lng)]
        dic['plus'] = l.plus
        dic['style'] = l.style
        dic['roomtype'] = l.roomtype
        result.append(dic)
    result = randomSelect(result)
    return result


if __name__ == '__main__':
    loc_dt = loct_init()
    c = 1
    for city in loc_dt.keys():
        for t in loc_dt[city].keys():
            ct = loc_dt[city][t]
            for p in ct:
                listing = Listing(cid=c,
                                  id=int(p["id"]),
                                  name=p["name"],
                                  price=p["price"],
                                  city=city,
                                  time=t,
                                  style=p["style"],
                                  plus=p["plus"],
                                  roomtype=p["roomtype"],
                                  lat=p["lnglat"][0],
                                  lng=p["lnglat"][1]
                                  )
                db.session.add(listing)
                c += 1
    print('end', c)
    db.session.commit()





