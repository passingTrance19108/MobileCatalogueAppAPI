from flask import Flask, jsonify, request
from dbmanager import db, MobilePhone
from sqlalchemy.exc import IntegrityError
from read_config import get_database_uri

import configparser

# config = configparser.ConfigParser()
# config.read('config.properties')
database_uri = get_database_uri()
# Example: sqlite:///app.db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Welcome to the Phone API!"

# Endpoint to add a new phone record
@app.route('/add_phone', methods=['POST'])
def add_phone():
    data = request.get_json()
    try:
        phone = MobilePhone(
            serial_number=data['serial_number'],
            imei=data['imei'],
            model=data['model'],
            brand=data['brand'],
            network_technologies=data['network_technologies'],
            number_of_cameras=data['number_of_cameras'],
            number_of_cores=data['number_of_cores'],
            weight=data['weight'],
            battery_capacity=data['battery_capacity'],
            cost=data['cost']
        )
        db.session.add(phone)
        db.session.commit()
        return jsonify(phone.to_dict()), 201
    except KeyError as e:
        db.session.rollback()
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except IntegrityError as e:
        db.session.rollback()  # Roll back the failed transaction.
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        # Check for specific constraint violations.
        if "mobile_phones.serial_number" in error_message:
            friendly_message = "A phone with this serial number already exists."
        elif "mobile_phones.imei" in error_message:
            friendly_message = "A phone with this IMEI already exists."
        
        return jsonify({"error": friendly_message}), 400
    except Exception as e:
        # logging the error can be helpful for debugging.
        app.logger.error(f"Error adding phone: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
        


# Endpoint to retrieve all phone records
@app.route('/phones', methods=['GET'])
@app.route('/phone/', methods=['GET'])
def get_phones():
    phones = MobilePhone.query.all()
    return jsonify([phone.to_dict() for phone in phones]), 200

# Helper function for type conversion
def convert_field_value(field, value):
    conversion_funcs = {
        'number_of_cameras': int,
        'number_of_cores': int,
        'weight': int,
        'battery_capacity': int,
        'cost': float
    }
    if field in conversion_funcs:
        return conversion_funcs[field](value)
    return value

# Endpoint to update a phone record
@app.route('/update_phone/<string:serial_number>', methods=['PUT'])
def update_phone(serial_number):
    data = request.get_json()
    phone = MobilePhone.query.filter_by(serial_number=serial_number).first_or_404()
    try:
        restricted_fields = ['serial_number', 'imei', 'model', 'brand']
        for field, value in data.items():
            if field in restricted_fields:
                return jsonify({"error": f"Updating '{field}' is not allowed."}), 400
            if field in MobilePhone.__table__.columns.keys():
                if field == 'network_technologies':
                    setattr(phone, field, ",".join(value))
                else:
                    try:
                        setattr(phone, field, convert_field_value(field, value))
                    except ValueError:
                        return jsonify({"error": f"Invalid type for field {field}. Expected {convert_field_value.__annotations__.get(field, 'appropriate type')}."}), 400
            else:
                return jsonify({"error": f"Invalid field: {field}"}), 400
            
        db.session.commit()
        return jsonify(phone.to_dict()), 200
    except Exception as e:
        app.logger.error(f"Error updating phone: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Endpoint to delete a phone record
@app.route('/delete_phone/<string:serial_number>', methods=['DELETE'])
def delete_phone(serial_number):
    phone = MobilePhone.query.filter_by(serial_number=serial_number).first_or_404()
    db.session.delete(phone)
    db.session.commit()
    return jsonify({"message": "Phone deleted successfully"}), 200

# Endpoint to retrieve a specific phone record
@app.route('/phone/<string:serial_number>', methods=['GET'])
def get_phone(serial_number):
    phone = MobilePhone.query.filter_by(serial_number=serial_number).first_or_404()
    return jsonify(phone.to_dict()), 200

# Endpoint to retrieve phones by a specific field and value
@app.route('/phones/<string:field>/<string:value>', methods=['GET'])
def get_phones_by_field(field, value):
    if field not in MobilePhone.__table__.columns.keys():
        return jsonify({"error": "Invalid field"}), 400

    try:
        converted_value = convert_field_value(field, value)
    except ValueError:
        return jsonify({"error": f"Invalid type for field {field}. Expected {convert_field_value.__annotations__.get(field, 'appropriate type')}."}), 400

    if field == 'network_technologies':
        search_value = f"%{value}%"
        phones = MobilePhone.query.filter(MobilePhone.network_technologies.like(search_value)) \
                                  .order_by(MobilePhone.brand, MobilePhone.model, MobilePhone.cost).all()
    else:
        phones = MobilePhone.query.filter(getattr(MobilePhone, field) == converted_value) \
                                  .order_by(MobilePhone.brand, MobilePhone.model, MobilePhone.cost).all()

    return jsonify([phone.to_dict() for phone in phones]), 200


if __name__ == '__main__':
    app.run(debug=True)
