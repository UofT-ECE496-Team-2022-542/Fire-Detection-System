import sqlite3
from flask import Flask, request, render_template
from datetime import datetime, timedelta

#---------- GLOBAL VARIABLES ----------
#The Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'firedetectionsystemsecretkey'
# The port this app will be run on
PORT = 5000

#---------- HELPERS ----------
# Establish a connection with the database
def get_db_connection():
    conn = sqlite3.connect('DATABASE/database.db')
    conn.row_factory = sqlite3.Row
    return conn

#---------- BACKEND ----------
#Waits for log requests from Basestation
@app.route('/log', methods=['POST'])
def log():
    #Extract data
    log_request = request.json
    drone_id = log_request['drone_id']
    time_captured = log_request['time_captured']
    lat = log_request['lat']
    lon = log_request['lon']
    prediction = log_request['prediction']
    image = log_request['image']

    #Log in Database
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO images (time_logged, drone_id, time_captured, lat, lon, prediction, image) VALUES(?, ?, ?, ?, ?, ?, ?)',
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), drone_id, time_captured, lat, lon, prediction, image)
        )
        conn.commit()
        conn.close()
        print('Image logged.')
    
    except Exception as e:
        print('COULD NOT LOG. ERROR:\n{}'.format(e))
        return("<500> Could not log image.")
    
    return("Image logged.")

#---------- FRONTEND ----------
@app.route('/')
def index():
    conn = get_db_connection()
    alerts = conn.execute(
        open('QUERIES/alerts.sql').read().format(
        # Last Hour
        # min_time=(datetime.now()-timedelta(hours = 1)).strftime('%Y-%m-%d %H:%M:%S')
        # All time
        min_time='2023-00-00 00:00:00'
        )
    ).fetchall()
    conn.close()
    return render_template('index.html', alerts=alerts)

@app.route('/query', methods=('GET', 'POST'))
def query():
    if request.method=='POST':
        drone_id = request.form['drone_id']
        min_time = request.form['min_time']
        max_time = request.form['max_time']
        min_lat = request.form['min_lat']
        max_lat = request.form['max_lat']
        min_lon = request.form['min_lon']
        max_lon = request.form['max_lon']
        prediction = request.form['prediction']

        query_str = open('QUERIES/search.sql').read()
        param_str = 'Parameters: '
        if drone_id:
            query_str += "\nAND drone_id = {}".format(drone_id)
            param_str += "drone_id='{}', ".format(drone_id)
        if min_time:
            query_str += "\nAND time_captured >= '{}'".format(min_time.replace('T', ' '))
            param_str += "min_time='{}', ".format(min_time.replace('T', ' '))
        if max_time:
            query_str += "\nAND time_captured <= '{}'".format(max_time.replace('T', ' '))
            param_str += "max_time='{}', ".format(max_time.replace('T', ' '))
        if min_lat:
            query_str += "\nAND lat >= {}".format(min_lat)
            param_str += "min_lat='{}', ".format(min_lat)
        if max_lat:
            query_str += "\nAND lat <= {}".format(max_lat)
            param_str += "max_lat='{}', ".format(max_lat)
        if min_lon:
            query_str += "\nAND lon >= {}".format(min_lon)
            param_str += "min_lon='{}', ".format(min_lon)
        if max_lon:
            query_str += "\nAND lon <= {}".format(max_lon)
            param_str += "max_lon='{}', ".format(max_lon)
        if prediction=='fire': query_str += "\nAND prediction = 'FIRE'"
        elif prediction=='no_fire': query_str += "\nAND prediction = 'NO_FIRE'"
        param_str += "prediction='{}'".format(prediction)
        query_str += "\nORDER BY time_captured DESC"

        
        conn = get_db_connection()
        results = conn.execute(query_str).fetchall()
        conn.close()

        return render_template(
            'results.html',
            results=results,
            param_str=param_str
        )

    return render_template('query.html')

#---------- MAIN ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True,)
