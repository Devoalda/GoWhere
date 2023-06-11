import random, os

from flask import Flask, render_template

import SG_Shopping_Malls.SG_Shopping_Malls as sm

app = Flask(__name__)
sm = sm.Shopping_Mall()
try:
    sm.import_file('SG_Shopping_Malls/dataset.json')
except FileNotFoundError:
    # Try full path with os module
    sm.import_file(os.path.join(os.path.dirname(__file__), 'SG_Shopping_Malls/dataset.json'))

regions = sm.headers


@app.route('/')
def index():
    title = 'Go Where?'
    mall_dict = sm.get_random_mall(num_malls=random.randint(3, 7))
    region, malls = list(mall_dict.keys())[0], list(mall_dict.values())[0]

    return render_template('base.html', title=title, region=region, malls=malls, regions=regions)


@app.route('/<region>')
def getMalls(region):
    # Capitalize first letter of each word
    region = region.split()
    region = [word.capitalize() for word in region]
    region = ' '.join(region)

    title = region

    if region == 'South':
        mall_dict = sm.get_random_mall(num_malls=random.randint(1, 3), region=region)
    else:
        mall_dict = sm.get_random_mall(num_malls=random.randint(3, 7), region=region)
    region, malls = list(mall_dict.keys())[0], list(mall_dict.values())[0]

    return render_template('base.html', title=title, region=region, malls=malls, regions=regions)


@app.route('/<region>/<num_malls>')
def getMallsByRegionNum(region, num_malls):
    region = region.split()
    region = [word.capitalize() for word in region]
    region = ' '.join(region)

    title = region
    num_malls = int(num_malls)

    mall_dict = sm.get_random_mall(num_malls=num_malls, region=region)
    region, malls = list(mall_dict.keys())[0], list(mall_dict.values())[0]

    return render_template('base.html', title=title, region=region, malls=malls, regions=regions)


@app.route('/search')
def search(query):
    # 404 Error Handling
    return render_template('404.html'), 404


# 404 Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
