from flask import Flask, render_template, request, url_for, redirect
import os
from main1 import *
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    b = False
    if request.method == 'POST':
        headline = request.form.get('headline')
        if len(headline) == 0:
            return render_template('index.html', b=b)
        l = return_category(headline)
        b = True
        return render_template('index.html', b=b, l=l)

    return render_template('index.html', b=b)

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/members')
# def members():
#     return render_template('aboutme.html')

@app.route('/readme')
def readme():
    return render_template('ReadMe.html')

port = int(os.getenv('PORT', 8000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
