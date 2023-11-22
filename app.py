import os
from SearchCode.searchContent import *

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def query_records():
    complex = request.args.get('complex')
    if complex:
        return("MEN AT WORK")
        #return(search(paragraph(includes(complex)),visual=True,capture=True))
    else:
        return("please enter a term")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
   app.run()
