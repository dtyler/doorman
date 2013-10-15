from flask import Flask
import flask
import yaml
import json
import urllib2
from boto.dynamodb2.table import Table
import boto.dynamodb2
import xml.etree.cElementTree as etree
app = Flask(__name__)

configMap = []


@app.route('/')
def hello_world():
    raw_data = fetch_current_config()
    keycode_arr = [ x.get('keycode') for x in raw_data ]
    finalMap = {
        'action_map' : keycode_arr
    }
    return flask.render_template('home.html', data=finalMap)

@app.route('/static/<path:filename>')
def get_statics(filename):
    return flask.url_for('static', filename=filename)

@app.route('/codeinfo/<int:keycode>')
def return_entry_info(keycode):
    raw_data = fetch_current_config()
    for entry in raw_data:
        if entry.get('keycode') != None:
            return flask.render_template('code_div.html', data=entry)

def fetch_current_config(table=None):
    if table == None:
        print "Connecting to aws"
        conn = boto.dynamodb2.connect_to_region(configMap['aws_region'])
        table = Table(u'doorman_keycodes', connection=conn)
    entryMap = []
    for item in table.scan():
        entryMap.append( {
                'keycode' : int(item['keycode'].to_integral_value()),
                'action' : item['action'],
                'name' : item.get('name')
                })
    print entryMap
    return entryMap
    
if __name__ == '__main__':
    configMap = yaml.load(open('config.yaml', 'r'))
    app.run(host='0.0.0.0', debug=True)
