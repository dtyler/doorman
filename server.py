from flask import Flask
import flask
import urllib2
import yaml
from boto.dynamodb2.table import Table
import boto.dynamodb2
import xml.etree.cElementTree as etree
app = Flask(__name__)

configMap = []


@app.route('/')
def hello_world():
    raw_data = fetch_current_config()
    
    data = { 'key_codes' : raw_data.keys(),
             'action_map': raw_data
           }
    return flask.render_template('home.html', data=data)

@app.route('/static/<path:filename>')
def get_statics(filename):
    return flask.url_for('static', filename=filename)

def fetch_current_config(table=None):
    if table == None:
        conn = boto.dynamodb2.connect_to_region(configMap['aws_region'])
        table = Table(u'doorman_keycodes', connection=conn)
    entryMap = dict()
    for item in table.scan():
        entryMap[item.get('keycode')] = item.get('action')
    return entryMap
    
if __name__ == '__main__':
    configMap = yaml.load(open('config.yaml', 'r'))
    app.run(host='0.0.0.0', debug=True)
