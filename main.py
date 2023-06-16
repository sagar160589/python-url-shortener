import redis, random, datetime, pandas as pd
from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from forms import URLForm
from models import db, Mapping, URLRange, URLDetails

app = Flask(__name__)
short_url_prefix = "http://127.0.0.1:5000/"

with app.app_context():
    app.config['SECRET_KEY'] = 'Youarethesecretkey23456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    db.init_app(app)
    db.create_all()
    Bootstrap(app)
    url_range_id = []
    #Get mapping codes
    mapping_codes = Mapping.query.all()
    for row in mapping_codes:
        number = row.mapping_number
        alphabet = row.mapping_character
        if not r.exists(number):
            r.set(number,alphabet)

    #Get ranges
    url_ranges = URLRange.query.filter_by(id=URLRange.id).all()
    for range_id in url_ranges:
        url_range_id.append(range_id.id)

#Save short urls
def save_short_url(org_url, binary_code):
    print(f"Org url: {org_url} and binary code: {binary_code}, {len(binary_code)}")
    group_length = 6
    groups = [binary_code[i:i+group_length] for i in range(0, len(binary_code), group_length)]
    code_list = []
    code_list_details = [Mapping.query.filter_by(mapping_number=group).first() for group in groups]
    for code in code_list_details:
        code_list.append(code.mapping_character)

    final_code_list = ''.join(code_list)
    url_details = URLDetails(short_code=final_code_list, original_url=org_url, no_of_clicks=0,date=datetime.date.today().strftime("%Y-%m-%d"))
    db.session.add(url_details)
    db.session.commit()
    return f"{short_url_prefix}{final_code_list}"


#Convert the number to binary
def convert_binary(number):
    #Convert the umber to binary
    binary_code = bin(int(number))[2:]
    count_pad = 1
    while len(binary_code) % 6 != 0:
        binary_code = str(binary_code.zfill(len(binary_code) + count_pad))
    return binary_code

#Save short urls in file
def save_short_url_in_file(org_url, short_url):
    data = {
        'Original-URL': [org_url],
        'Short-URL': [short_url]
    }

    # Make data frame of above data
    df = pd.DataFrame(data)
    # append data frame to CSV file
    df.to_csv('short_url.csv', mode='a', index=False, header=False)

#App route for creating short urls
@app.route("/create-short-url", methods=['GET','POST'])
def get_url():
    url_form = URLForm()
    #Code to get orginal url from UI
    if url_form.validate_on_submit():
        org_url = url_form.url.data
        org_url_list = URLDetails.query.all()
        for org in org_url_list:
            if org.original_url == org_url:
                flash('Short URL already exists for your business URL...')
                return render_template("add.html", short_url=f"{short_url_prefix}{org.short_code}", short_url_form=url_form)
        url_range = random.choice(url_range_id)
        range_details = URLRange.query.filter_by(id=url_range).first()
        if range_details.current_number <= range_details.end_range:
            binary_code = convert_binary(range_details.current_number)
            range_details.current_number = range_details.current_number + 1
            db.session.commit()
            if len(binary_code) > 0:
                short_url = save_short_url(org_url, binary_code)
                save_short_url_in_file(org_url, short_url)
                return render_template("add.html", short_url=short_url, short_url_form=url_form)
    return render_template("add.html", short_url_form=url_form)

#App route to redirect from short url to original url
@app.route("/<short_url_code>")
def get_original_url(short_url_code):
    org_url_details = URLDetails.query.filter_by(short_code=short_url_code).first()
    if org_url_details:
        org_url_details.no_of_clicks = org_url_details.no_of_clicks + 1
        db.session.commit()
        return redirect(org_url_details.original_url)
    else:
        return render_template("index.html", message="Original URL not found")

if __name__ == '__main__':
    app.run(debug=True)

