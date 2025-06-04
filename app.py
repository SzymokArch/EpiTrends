import json
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Float, String
import xml.etree.ElementTree as ET
from flask import Response
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Prosta baza użytkowników
users = {
    "admin": "password123",
    "user": "testpass"
}


Base = declarative_base()

class DailyData(Base):
    __tablename__ = "daily_data"
    date = Column(Date, primary_key=True)
    covid_deaths = Column(Float)
    vaccinations = Column(Float)
    daily_vaccinations = Column(Float)
    wig20 = Column(Float)
    government_support = Column(Float)

class Event(Base):
    __tablename__ = "events"
    date = Column(Date, primary_key=True)
    event = Column(String)
    description = Column(String)

engine = create_engine("sqlite:///covid_data.db")
Session = sessionmaker(bind=engine)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    session = Session()
    records = session.query(DailyData).order_by(DailyData.date).all()
    session.close()
    # serializacja daty do stringa
    data = [
        {
            "date": r.date.strftime("%Y-%m-%d"),
            "covid_deaths": r.covid_deaths,
            "vaccinations": r.vaccinations,
            "daily_vaccinations": r.daily_vaccinations,
            "wig20": r.wig20,
            "government_support": r.government_support
        }
        for r in records
    ]
    return jsonify(data)

@app.route("/api/data.json")
def export_json():
    session = Session()
    records = session.query(DailyData).order_by(DailyData.date).all()
    session.close()

    data = [
        {
            "date": r.date.strftime("%Y-%m-%d"),
            "covid_deaths": r.covid_deaths,
            "vaccinations": r.vaccinations,
            "daily_vaccinations": r.daily_vaccinations,
            "wig20": r.wig20,
            "government_support": r.government_support
        }
        for r in records
    ]
    return jsonify(data)

@app.route("/api/data.xml")
def export_xml():
    session = Session()
    records = session.query(DailyData).order_by(DailyData.date).all()
    session.close()

    root = ET.Element("data")

    for r in records:
        item = ET.SubElement(root, "record")
        ET.SubElement(item, "date").text = r.date.strftime("%Y-%m-%d")
        ET.SubElement(item, "covid_deaths").text = str(r.covid_deaths or "")
        ET.SubElement(item, "vaccinations").text = str(r.vaccinations or "")
        ET.SubElement(item, "daily_vaccinations").text = str(r.daily_vaccinations or "")
        ET.SubElement(item, "wig20").text = str(r.wig20 or "")
        ET.SubElement(item, "government_support").text = str(r.government_support or "")

    xml_data = ET.tostring(root, encoding='utf-8', method='xml')
    return Response(xml_data, mimetype='application/xml')

@app.route("/api/events")
def api_events():
    try:
        with open("wydarzenia_2019_2023.json", "r", encoding="utf-8") as f:
            events = json.load(f)
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Brak nazwy użytkownika lub hasła"}), 400

    if users.get(username) != password:
        return jsonify({"msg": "Niepoprawny login lub hasło"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
