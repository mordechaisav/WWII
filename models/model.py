from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import db
Base = declarative_base()


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(100), unique=True, nullable=False)
    def to_dict(self):
        return {"country_id": self.country_id, "country_name": self.country_name}



class City(db.Model):
    __tablename__ = 'cities'

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(100), unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.country_id'))
    country = relationship("Country", backref="cities" , lazy= True)
    def to_dict(self):
        return {"city_id": self.city_id, "city_name": self.city_name, "country": self.country.to_dict() if self.country else None}



class Location(db.Model):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))

    # Relationship to city
    city = relationship("City", backref="locations", lazy=True)
    def to_dict(self):
        return {"location_id": self.location_id,
                "city": self.city.to_dict() if self.city else None,
                "latitude": self.latitude,
                "longitude": self.longitude}




class Target(db.Model):
    __tablename__ = 'targets'

    target_id = Column(Integer, primary_key=True)
    target_type = Column(String(100))
    target_industry = Column(String(255))
    target_priority = Column(String(5))
    location_id = Column(Integer, ForeignKey('locations.location_id'))

    # Relationship to location
    location = relationship("Location", backref="targets", lazy=True)
    def to_dict(self):
        return {"target_id": self.target_id,
                "target_type": self.target_type,
                "target_industry": self.target_industry,
                "target_priority": self.target_priority,
                "location": self.location.to_dict() if self.location else None}



class Mission(db.Model):
    __tablename__ = 'missions'

    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    theater_of_operations = Column(String(100))
    country = Column(String(100))
    air_force = Column(String(100))
    unit_id = Column(String(100))
    aircraft_series = Column(String(100))
    callsign = Column(String(100))
    mission_type = Column(String(100))
    takeoff_base = Column(String(255))
    takeoff_location = Column(String(255))
    takeoff_latitude = Column(String(15))
    takeoff_longitude = Column(Numeric(10, 6))
    target_id = Column(Integer, ForeignKey('targets.target_id'))
    altitude_hundreds_of_feet = Column(Numeric(7, 2))
    airborne_aircraft = Column(Numeric(4, 1))
    attacking_aircraft = Column(Integer)
    bombing_aircraft = Column(Integer)
    aircraft_returned = Column(Integer)
    aircraft_failed = Column(Integer)
    aircraft_damaged = Column(Integer)
    aircraft_lost = Column(Integer)
    high_explosives = Column(String(255))
    high_explosives_type = Column(String(255))
    high_explosives_weight_pounds = Column(String(25))
    high_explosives_weight_tons = Column(Numeric(10, 2))
    incendiary_devices = Column(String(255))
    incendiary_devices_type = Column(String(255))
    incendiary_devices_weight_pounds = Column(Numeric(10, 2))
    incendiary_devices_weight_tons = Column(Numeric(10, 2))
    fragmentation_devices = Column(String(255))
    fragmentation_devices_type = Column(String(255))
    fragmentation_devices_weight_pounds = Column(Numeric(10, 2))
    fragmentation_devices_weight_tons = Column(Numeric(10, 2))
    total_weight_pounds = Column(Numeric(10, 2))
    total_weight_tons = Column(Numeric(10, 2))
    time_over_target = Column(String(8))
    bomb_damage_assessment = Column(String(255))
    source_id = Column(String(100))

    # Relationship to target
    target = relationship("Target", backref="missions", lazy=True)

    def to_dict(self):
        return {
            "mission_id": self.mission_id,
            "mission_date": self.mission_date,
            "theater_of_operations": self.theater_of_operations,
            "country": self.country,
            "air_force": self.air_force,
            "unit_id": self.unit_id,
            "aircraft_series": self.aircraft_series,
            "callsign": self.callsign,
            "mission_type": self.mission_type,
            "takeoff_base": self.takeoff_base,
            "takeoff_location": self.takeoff_location,
            "takeoff_latitude": self.takeoff_latitude,
            "takeoff_longitude": self.takeoff_longitude,
            "target_id": self.target.to_dict() if self.target else None
            ,
            "altitude_hundreds_of_feet": self.altitude_hundreds_of_feet,
            "airborne_aircraft": self.airborne_aircraft,
            "attacking_aircraft": self.attacking_aircraft,
            "bombing_aircraft": self.bombing_aircraft,
            "aircraft_returned": self.aircraft_returned,
            "aircraft_failed": self.aircraft_failed,
            "aircraft_damaged": self.aircraft_damaged,
            "aircraft_lost": self.aircraft_lost,
            "high_explosives": self.high_explosives,
            "high_explosives_type": self.high_explosives_type,
            "high_explosives_weight_pounds": self.high_explosives_weight_pounds,
            "high_explosives_weight_tons": self.high_explosives_weight_tons,
            "incendiary_devices": self.incendiary_devices,
            "incendiary_devices_type": self.incendiary_devices_type,
            "incendiary_devices_weight_pounds": self.incendiary_devices_weight_pounds,
            "incendiary_devices_weight_tons": self.incendiary_devices_weight_tons,
            "fragmentation_devices": self.fragmentation_devices,
            "fragmentation_devices_type": self.fragmentation_devices_type,
            "fragmentation_devices_weight_pounds": self.fragmentation_devices_weight_pounds,
            "fragmentation_devices_weight_tons": self.fragmentation_devices_weight_tons,
            "total_weight_pounds": self.total_weight_pounds,
            "total_weight_tons": self.total_weight_tons,
            "time_over_target": self.time_over_target,
            "bomb_damage_assessment": self.bomb_damage_assessment,
            "source_id": self.source_id
        }


