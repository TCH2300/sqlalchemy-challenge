##############################################
            # Import Dependencies
##############################################
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

#################################################
            # Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# view all of the classes that automap found
# Base.classes.keys() 
inspector=inspect(engine)
inspector.get_table_names()

#################################################
                # Flask Setup
#################################################
app = Flask(__name__)

#################################################
                # Routes
#################################################
# '/' (Home Page - defined endpoints)
#################################################
@app.route("/")
def home():
    print("List all available api routes.")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )
##################################################################################
# `/api/v1.0/precipitation` Convert the query results 
#  to a dict using `date` as key and `prcp` as the value. Return JSON of dict. 
##################################################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    prior_year=dt.date(2017,8,23) - dt.timedelta(days=365)
    query_last=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > prior_year).all()

### Create dict ###
#date_precip = {measurement.date: measurement.prcp}
#return jsonify(date_precip)
#come back to this part to do dict#

#########################################################################
#`/api/v1.0/stations` - Return a JSON list of stations from the dataset.
#########################################################################

@app.route("/api/v1.0/stations")
def stations():
    stations=session.query(Measurement).group_by(Measurement.station).count()
    station_count=session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()


####################################################################################
#`/api/v1.0/tobs` - Query the dates and tobs of most active station for the last year
# Return a JSON list of (TOBS) for prior year.
####################################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    obs=session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').\
    filter(Measurement.date>=prior_year).order_by(Measurement.date.desc()).all()

#####################################################################################
# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>` - 
# Return a JSON list of min temp, avg temp, and max temp for a given start or range.
#####################################################################################



if __name__ == "__main__":
    app.run(debug=True)