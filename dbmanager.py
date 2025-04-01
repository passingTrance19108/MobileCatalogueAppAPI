from flask_sqlalchemy import SQLAlchemy
from phoneValidator import (
    validate_serial_number,
    validate_imei,
    validate_model,
    validate_brand,
    validate_network_technologies,
    validate_number_of_cameras,
    validate_number_of_cores,
    validate_weight,
    validate_battery_capacity,
    validate_cost,
)

db = SQLAlchemy()

class MobilePhone(db.Model):
    __tablename__ = 'mobile_phones'
    
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(11), unique=True, nullable=False)
    imei = db.Column(db.String(15), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    network_technologies = db.Column(db.String(100), nullable=False)
    number_of_cameras = db.Column(db.Integer, nullable=False)
    number_of_cores = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    battery_capacity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    
    def __init__(self, serial_number: str, imei: str, model: str, brand: str,
                 network_technologies: list, number_of_cameras: int, number_of_cores: int,
                 weight: int, battery_capacity: int, cost: float):
        self.serial_number = validate_serial_number(serial_number)
        self.imei = validate_imei(imei)
        self.model = validate_model(model)
        self.brand = validate_brand(brand)
        self.network_technologies = validate_network_technologies(network_technologies)
        self.number_of_cameras = validate_number_of_cameras(number_of_cameras)
        self.number_of_cores = validate_number_of_cores(number_of_cores)
        self.weight = validate_weight(weight)
        self.battery_capacity = validate_battery_capacity(battery_capacity)
        self.cost = validate_cost(cost)
        
    def __repr__(self):
        return (f"MobilePhone(serial_number='{self.serial_number}', imei='{self.imei}', "
                f"model='{self.model}', brand='{self.brand}', "
                f"network_technologies='{self.network_technologies}', "
                f"number_of_cameras={self.number_of_cameras}, number_of_cores={self.number_of_cores}, "
                f"weight={self.weight}, battery_capacity={self.battery_capacity}, cost={self.cost})")
    
    def to_dict(self):
        return {
            "id": self.id,
            "serial_number": self.serial_number,
            "imei": self.imei,
            "model": self.model,
            "brand": self.brand,
            "network_technologies": self.network_technologies.split(","),  # Convert back to list.
            "number_of_cameras": self.number_of_cameras,
            "number_of_cores": self.number_of_cores,
            "weight": self.weight,
            "battery_capacity": self.battery_capacity,
            "cost": self.cost
        }
