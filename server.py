import time
from flask import Flask
import flask
import yaml
import json
import urllib2
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
import boto.dynamodb2
import xml.etree.cElementTree as etree
app = Flask(__name__)

table = None
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

@app.route('/delete/<int:keycode_param>')
def delete_entry(keycode_param):
    try:
        item = table.get_item( keycode=keycode_param )
        item.delete()
    except e:
        print e
        raise e

@app.route('/add/<int:keycode_param>')
def add_entry(keycode_param):
    params = request.args
    try:
        item = Item(table, data= {
            'keycode': keycode_param,
            'action' : params['action']
            'name' : params['name']
        })
    except KeyError as e:
        # better error?
        raise e
    item.save()

def fetch_current_config():
    global table
    if table == None:
        print "Connecting to dynamodb"
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
    fetch_current_config()
    app.run(host='0.0.0.0', debug=True)
