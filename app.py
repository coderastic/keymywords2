from flask import Flask, render_template, request
from pytrends.request import TrendReq
import os
import clipboard

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        timeframe = request.form['timeframe']
        location = request.form['location']

        # Initialize Pytrends object
        pytrends = TrendReq(hl='en-US', tz=360)

        # Build payload
        pytrends.build_payload(kw_list=[keyword], geo=location)

        # Get related topics based on the selected timeframe
        if timeframe == '24H':
            related_topics = pytrends.related_topics(timeframe='24H')
        elif timeframe == '7D':
            related_topics = pytrends.related_topics(timeframe='7d')
        elif timeframe == '30D':
            related_topics = pytrends.related_topics(timeframe='30d')
        elif timeframe == '3M':
            related_topics = pytrends.related_topics(timeframe='3m')

        # Extract popular related keywords
        popular_related_keywords = []
        for topic in related_topics['rising']['topics']:
            popular_related_keywords.append(topic['title'])

        comma_separated_keywords = ', '.join(popular_related_keywords)

        return render_template('results.html', keyword=keyword, timeframe=timeframe, location=location, popular_related_keywords=popular_related_keywords, comma_separated_keywords=comma_separated_keywords)

    return render_template('index.html')

@app.route('/copy-keywords')
def copy_keywords():
    if 'comma_separated_keywords' in request.args:
        comma_separated_keywords = request.args['comma_separated_keywords']
        clipboard.copy(comma_separated_keywords)
        return 'Keywords copied to clipboard'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
  
