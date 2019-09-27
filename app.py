# Import Dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Python code
engine = create_engine("sqlite:///Instructions/Resources/hawaii.sqlite")
### Reflect an Existing Database Into a New Model
Base = automap_base()
### Reflect the Tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create an app
app = Flask(__name__)

# Home Route
@app.route("/")
def index():
    return(
            f"<p>Home Page</p>"
            f"<p>Last 12 Months of Precipitation Data -- /api/v1.0/precipitation</p>"
            f"<p>List of Stations -- /api/v1.0/stations</p>"
            f"<p>Last 12 Months of Temperature Observations -- /api/v1.0/tobs</p>"
            f"<p>Temperature for Select Date -- /api/v1.0/<start></p>"
            f"<p>Temperature for Date Ranges -- /api/v1.0/<start>/<end></p>"
         )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    session.close()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)
    

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    stations = session.query(Station.station, Station.name).all()
    session.close()

    station = []
    for id, name in stations:
        station_dict = {}
        station_dict["id"] = id
        station_dict["name"] = name
        station.append(station_dict)
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    session.close()

    temp_list = []
    for date, temp in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = temp
        temp_list.append(temp_dict)
    return jsonify(temp_list)

    

@app.route("/api/v1.0/<start>")
def startday(start):
    session = Session(engine)
    start = dt.datetime.strptime(start, "%Y-%m-%d")  
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    print(results)
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def dateranges(start, end):
    session = Session(engine)
    start = dt.datetime.strptime(start, "%Y-%m-%d")  
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    print(results)
    return jsonify(results)
    
#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)