# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)


# Save references to each table
Measurement  = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def main_page():
    return (
        f"Welcome to the Home Page!<br>"
        f"To navigate thru the routes, copy and paste the links below to the end of the web address<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )


# Query through the precipitation analysis
@app.route("/api/v1.0/precipitation")
def precip():
    previous_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).\
                order_by(Measurement.date).all()
    
    results_dict = dict(results)
    session.close()
    return jsonify(results_dict)

# Query through the stations analysis

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    
    stations_dict = dict(stations)
    session.close()
    return jsonify(stations_dict)

# Query through the tobs analysis

@app.route("/api/v1.0/tobs")
def tobs():
    max_temp = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()
    
    tobs_dict = dict(max_temp)
    session.close()
    return jsonify(tobs_dict)

# Query through the start

@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    
    total_tobs = []

    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        total_tobs.append(tobs_dict)

    return jsonify(total_tobs)

# Query through the start to end

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                           func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                           filter(Measurement.date <= end).all()
    session.close()

    total_tobs = []
    
    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        total_tobs.append(tobs_dict)

    return jsonify(total_tobs)

if __name__ == '__main__':
    app.run(debug=True)








