from flask import render_template, request, jsonify, redirect
import json
import os
from database import get_loc, app, db
import help
from random import randrange


def file_init():
    dir = os.listdir('json_data/London/listing')
    loc_dic = {}
    loc_dic['london'] = {}
    loc_dic['sydney'] = {}
    loc_dic['sanfrancisco'] = {}
    for li in dir:
        f = open(os.path.join('json_data/London/listing', li), 'r')
        sts = json.load(f)
        t = li.split('.')[0]
        loc_dic['london'][t] = sts
    dir = os.listdir('json_data/SanFrancisco/listing')
    for li in dir:
        f = open(os.path.join('json_data/SanFrancisco/listing', li), 'r')
        sts = json.load(f)
        t = li.split('.')[0]
        loc_dic['sanfrancisco'][t] = sts
    dir = os.listdir('json_data/Sydney/listing')
    for li in dir:
        f = open(os.path.join('json_data/Sydney/listing', li), 'r')
        sts = json.load(f)
        t = li.split('.')[0]
        loc_dic['sydney'][t] = sts
    return loc_dic


def loct_init():
    root = os.listdir('json_data')
    loc_dt = {}
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


# Normalize data
def Normalize(data):
    mx = max(data)
    mn = min(data)
    if mx == mn:
        return data
    else:
        return [(float(i) - mn)/(mx-mn) for i in data]


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


def ret_loc(plus, city, time):
    if plus == 'both':
        return loc_dt[city][time]
    elif plus == 'plus':
        li = loc_dt[city][time]
        result = []
        for listings in li:
            if listings['plus'] == 1:
                result.append(listings)
        return result
    else:
        li = loc_dt[city][time]
        result = []
        for listings in li:
            if listings['plus'] == 0:
                result.append(listings)
        return result


@app.route('/plus', methods={'GET', 'POST'})
def get_plus():
    print("Getting info...")
    stat = {}
    loc = []
    time = '2018-10'
    city = 'london'
    plus = 'both'
    #default graph list
    if request.method == 'GET':
        stat = loc_dic['london']['2018-10']
        loc = get_loc('london', 'both', '2018-10')
    elif request.method == 'POST':
        city = request.form['city']
        time = request.form['time']
        plus = request.form['plus']
        print(city, time, plus)
        stat = loc_dic[city][time]
        loc = get_loc(city, plus, time)
        print(len(loc))
    tf = True
    pc = 0
    if time != "2018-10":
        tf = False
    else:
        pc = int((1.0*stat["Plus Number"]/stat["Total Listings"])*10000)/100
    #get an graph list according to the query
    dirs = os.listdir('json_data/' + city + '/listing/')
    dirs.sort()
    time_sequence = []
    total_listings = []
    for dir in dirs:
        time_sequence.append(dir[:-4])
        f = open('json_data/' + city + '/listing/' + dir, 'r',
                 encoding='utf-8')
        trend_data = json.load(f)
        f.close()
        total_listings.append(trend_data['Total Listings'])
    print("rendering")
    gp = [('Number-of-listings', time_sequence, total_listings)]
    return render_template('dataview.html', stat=stat, t=time, city=city, plus=plus, loc_dat=loc, graph=gp,
                           flag=tf, pc=pc)


@app.route('/dataComp')
def index():
    return render_template('index.html')


@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    # if request.method == 'POST':
    time = request.values.get('time', '')
    feature = request.values.get('name', '')

    root_path = 'json_data/'
    fp_london = open(root_path + 'London/comparison/' + time + '.json', 'r',
                     encoding='utf-8')
    data_london = json.load(fp_london)
    fp_sanfrancisco = open(root_path + 'SanFrancisco/comparison/' + time + '.json',
                           'r', encoding='utf-8')
    data_sanfrancisco = json.load(fp_sanfrancisco)
    fp_sydney = open(root_path + 'Sydney/comparison/' + time + '.json', 'r',
                     encoding='utf-8')
    data_sydney = json.load(fp_sydney)
    fp_review = open('json_data/review_json.json', 'r', encoding='utf-8')
    data_review = json.load(fp_review)

    data_return = {}
    if feature == "Roomtype":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['Entire Room %'] = [data_london['Entire Room %'], data_sanfrancisco['Entire Room %'],
                                        data_sydney['Entire Room %']]
        data_return['Private Room %'] = [data_london['Private Room %'], data_sanfrancisco['Private Room %'],
                                         data_sydney['Private Room %']]
        data_return['Shared Room %'] = [data_london['Shared Room %'], data_sanfrancisco['Shared Room %'],
                                        data_sydney['Shared Room %']]
    elif feature == "TotalListings":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['Total Listings'] = [data_london['Total Listings'], data_sanfrancisco['Total Listings'],
                                         data_sydney['Total Listings']]
    elif feature == "MinPrice":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['MinPrice'] = [data_london['Min Price'], data_sanfrancisco['Min Price'],
                                   data_sydney['Min Price']]
    elif feature == "MaxPrice":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['MaxPrice'] = [data_london['Max Price'], data_sanfrancisco['Max Price'],
                                   data_sydney['Max Price']]
    elif feature == "AveragePrice":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['AveragePrice'] = [data_london['Average Price'], data_sanfrancisco['Average Price'],
                                       data_sydney['Average Price']]
    elif feature == "MedianPrice":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['MedianPrice'] = [data_london['Median Price'], data_sanfrancisco['Median Price'],
                                      data_sydney['Median Price']]
    elif feature == "TotalHost":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['Total Host #'] = [data_london['Total Host #'], data_sanfrancisco['Total Host #'],
                                       data_sydney['Total Host #']]
    elif feature == "MultipleHost":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['Multiple Host %'] = [data_london['Multiple Host %'], data_sanfrancisco['Multiple Host %'],
                                          data_sydney['Multiple Host %']]
    elif feature == "ReviewSentiment":
        data_return['Feature'] = feature
        data_return['Time'] = time
        data_return['Positive'] = [data_review[0]['pos%'], data_review[1]['pos%'], data_review[2]['pos%']]
        data_return['Negative'] = [data_review[0]['neg%'], data_review[1]['neg%'], data_review[2]['neg%']]
        data_return['Neutral'] = [data_review[0]['neu%'], data_review[1]['neu%'], data_review[2]['neu%']]

    return jsonify(data_return)


@app.route('/about', methods={'GET'})
def about():
    return render_template('about.html')


@app.route('/', methods={'GET', 'POST'})
def homepage():
    return redirect('/plus')


@app.route('/dataTrend', methods={'GET', 'POST'})
def Trend():
    return render_template('trend.html')


@app.route('/get_loc', methods={'GET', 'POST'})
def ret_location():
    city = request.form['city']
    time = request.form['time']
    plus = request.form['plus']
    stat = loc_dic[city][time]
    loc = get_loc(city, plus, time)
    dirs = os.listdir('json_data/' + city + '/listing/')
    dirs.sort()
    time_sequence = []
    total_listings = []
    for dir in dirs:
        time_sequence.append(dir[:-4])
        f = open('json_data/' + city + '/listing/' + dir, 'r',
                 encoding='utf-8')
        trend_data = json.load(f)
        f.close()
        total_listings.append(trend_data['Total Listings'])
    gp = [('Number-of-listings', time_sequence, total_listings)]
    tf = True
    pc = 0
    if time != "2018-10":
        tf = False
    else:
        pc = int((1.0 * stat["Plus Number"] / stat["Total Listings"]) * 10000) / 100
    content = render_template('panel.html', flag=tf, pc=pc, stat=stat)
    data = {'stat': stat, 'loc': loc, 'graph': gp[0], 'flag': tf, 'pc': pc, 'ct': content}
    return jsonify(data)


@app.route('/trend', methods=['GET', 'POST'])
def trend():
    # if request.method == 'POST':
    feature = request.values.get('name', '')
    time_axis = help.get_time_axis()
    london_list = []
    sanfrancisco_list = []
    sydney_list = []
    for time in time_axis:
        root_path = 'json_data/'
        fp_london = open(root_path + 'London/comparison/' + time + '.json', 'r',
                         encoding='utf-8')
        data_london = json.load(fp_london)
        fp_sanfrancisco = open(root_path + 'SanFrancisco/comparison/' + time + '.json',
                               'r', encoding='utf-8')
        data_sanfrancisco = json.load(fp_sanfrancisco)
        fp_sydney = open(root_path + 'Sydney/comparison/' + time + '.json', 'r',
                         encoding='utf-8')
        data_sydney = json.load(fp_sydney)
        fp_review = open('json_data/review_json.json', 'r', encoding='utf-8')
        data_review = json.load(fp_review)

        data_return = {}
        if feature == "Entire_Room":
            london_list.append(data_london['Entire Room #']/data_london['Total Listings'])
            sanfrancisco_list.append(data_sanfrancisco['Entire Room #']/data_sanfrancisco['Total Listings'])
            sydney_list.append(data_sydney['Entire Room #']/data_sydney['Total Listings'])
        elif feature == "Private_Room":
                london_list.append(data_london['Private Room #']/data_london['Total Listings'])
                sanfrancisco_list.append(data_sanfrancisco['Private Room #']/data_sanfrancisco['Total Listings'])
                sydney_list.append(data_sydney['Private Room #']/data_sydney['Total Listings'])
        elif feature == "Shared_Room":
            london_list.append(data_london['Shared Room #']/data_london['Total Listings'])
            sanfrancisco_list.append(data_sanfrancisco['Shared Room #']/data_sanfrancisco['Total Listings'])
            sydney_list.append(data_sydney['Shared Room #']/data_sydney['Total Listings'])
        elif feature == "TotalListings":
            london_list.append(data_london['Total Listings'])
            sanfrancisco_list.append(data_sanfrancisco['Total Listings'])
            sydney_list.append(data_sydney['Total Listings'])
        elif feature == "MinPrice":
            london_list.append(data_london['Min Price'])
            sanfrancisco_list.append(data_sanfrancisco['Min Price'])
            sydney_list.append(data_sydney['Min Price'])
        elif feature == "MaxPrice":
            london_list.append(data_london['Max Price'])
            sanfrancisco_list.append(data_sanfrancisco['Max Price'])
            sydney_list.append(data_sydney['Max Price'])
        elif feature == "AveragePrice":
            london_list.append(data_london['Average Price'])
            sanfrancisco_list.append(data_sanfrancisco['Average Price'])
            sydney_list.append(data_sydney['Average Price'])
        elif feature == "MedianPrice":
            london_list.append(data_london['Median Price'])
            sanfrancisco_list.append(data_sanfrancisco['Median Price'])
            sydney_list.append(data_sydney['Median Price'])
        elif feature == "TotalHost":
            london_list.append(data_london['Total Host #'])
            sanfrancisco_list.append(data_sanfrancisco['Total Host #'])
            sydney_list.append(data_sydney['Total Host #'])
        elif feature == "MultipleHost":
            london_list.append(data_london['Multiple Host #']/data_london['Total Host #'])
            sanfrancisco_list.append(data_sanfrancisco['Multiple Host #']/data_sanfrancisco['Total Host #'])
            sydney_list.append(data_sydney['Multiple Host #']/data_sydney['Total Host #'])
        elif feature == "Positive":
            london_list.append(data_review[0]['pos%'])
            sanfrancisco_list.append(data_review[1]['pos%'])
            sydney_list.append(data_review[2]['pos%'])
        elif feature == "Negative":
            london_list.append(data_review[0]['neg%'])
            sanfrancisco_list.append(data_review[1]['neg%'])
            sydney_list.append(data_review[2]['neg%'])
        elif feature == "Neutral":
            london_list.append(data_review[0]['neu%'])
            sanfrancisco_list.append(data_review[1]['neu%'])
            sydney_list.append(data_review[2]['neu%'])
    result = {}
    if feature == 'TotalListings' or feature == "TotalHost":
        result['time'] = time_axis
        result['London'] = Normalize(london_list)
        result['SanFrancisco'] = Normalize(sanfrancisco_list)
        result['Sydney'] = Normalize(sydney_list)
    else:
        result['time'] = time_axis
        result['London'] = london_list
        result['SanFrancisco'] = sanfrancisco_list
        result['Sydney'] = sydney_list
    return jsonify(result)


if __name__ == '__main__':
    loc_dic = file_init()
    #loc_dt = loct_init()
    app.run()
