from flask import Flask, json, jsonify
import datetime as datetime
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func

##create the database connection

engine = create_engine ("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
#the instruction to suppress the check for the same thread is ok because we are only reading, not writing

# Create our session (link) from Python to the DB
session = Session(engine)
#discover what's in the database

Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#Bring in Flask

app = Flask(__name__)

#define the routes

@app.route("/api/v1.0/stations")
def weatherstation():
   # """Return a list of weatherstations and counts"""
   ##COME BACK HERE AND FILTER THIS QUERY BY DATE########
   ## WE ONLY NEED A YEAR OF RESULTS########
    results = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()

    # Convert the query results to a list of stations inside Dicitonary
    all_stations=[]
    for row in results:
        station_dict = {}
        station_dict["station"] = row[0]
        station_dict["count"] = row[1]
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
   # """Return a list of observed precip"""
    results = session.query(Measurement.date, (Measurement.prcp)).\
                order_by((Measurement.date).desc()).all()

     # Convert the query results to a Dictionary using date as the key and prcp as the value.
    all_precipitation=[]
    for precip in results:
        precip_dict = {}
        precip_dict["date"] = precip.date
        precip_dict["prcp"] = precip.prcp
        all_precipitation.append(precip_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/tobs")
def alltobs():
   # """Return a list of observed temperatures"""
    results = session.query(Measurement.date, (Measurement.tobs)).\
                order_by((Measurement.date).desc()).all()

     # Convert the query results to a Dictionary using date as the key and prcp as the value.
    all_temps=[]
    for temp in results:
        tobs_dict = {}
        tobs_dict["date"] = temp.date
        tobs_dict["prcp"] = temp.tobs
        all_temps.append(tobs_dict)

    return jsonify(all_temps)



@app.route("/api/v1.0/<start_date>")


def calc_temps_start(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX"""
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    calc_tobs=[]
    for row in results:
        calc_tobs_dict = {}
        calc_tobs_dict["TMIN"] = row[0]
        calc_tobs_dict["TAVG"] = row[1]
        calc_tobs_dict["TMAX"] = row[2]
        calc_tobs.append(calc_tobs_dict)

    return jsonify(calc_tobs)


@app.route("/api/v1.0/<start_date><end_date>")


def calc_temps_start_end(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX"""
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all().filter(Measurement.date <= end_date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    calc_tobs=[]
    for row in results:
        calc_tobs_dict = {}
        calc_tobs_dict["TMIN"] = row[0]
        calc_tobs_dict["TAVG"] = row[1]
        calc_tobs_dict["TMAX"] = row[2]
        calc_tobs.append(calc_tobs_dict)

    return jsonify(calc_tobs)

#define the default route

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Historical Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date>"
        f"/api/v1.0/start_date-end_date<br/>"   )

if __name__ == '__main__':
    app.run(debug=True)





