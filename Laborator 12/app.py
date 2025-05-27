from flask import Flask, request, redirect, jsonify
import random

app = Flask(__name__)

sensors = [
    {
        'name': 'sensor1',
        'read': lambda: round(random.uniform(20.0, 25.0), 2),
        'unit': 'C'
    },
    {
        'name': 'sensor2',
        'read': lambda: round(random.uniform(20.0, 25.0), 2),
        'unit': 'C'
    },
    {
        'name': 'sensor3',
        'read': lambda: round(random.uniform(20.0, 25.0), 2),
        'unit': 'C'
    }
]

config_files = {}


def add_sensor_links(sensor):
    config = config_files.get(sensor['name'])
    if config:
        sensor['unit'] = config['unit']

    value = sensor['read']()
    if sensor['unit'] == 'F':
        value = value + 32
    elif sensor['unit'] == 'K':
        value = value + 273

    return {
        'name': sensor['name'],
        'value': value,
        'unit': sensor['unit'],
        '_links': {
            'self': f'/sensors/{sensor["name"]}',
            'update-config': {
                'href': f'/sensors/{sensor["name"]}',
                'method': 'PUT'
            },
            'create-config': {
                'href': f'/sensors/{sensor["name"]}',
                'method': 'POST'
            },
            'parent': {
                'href': '/sensors',
                'method': 'GET'
            }
        }
    }



def add_sensors_links(sensors):
    return {
        'Sensors': [add_sensor_links(sensor) for sensor in sensors],
        '_links': {
            'self': {
                'href': '/sensors',
                'method': 'GET'
            }
        }
    }


@app.route("/sensors", methods=['GET'])
def getAllSensors():
    return jsonify(add_sensors_links(sensors)), 200

@app.route("/sensors/<name>", methods=['GET'])
def getSingleSensor(name):
    for sensor in sensors:
        if sensor['name'] == name:
            return jsonify({'File': add_sensor_links(sensor)}), 200
    
    return jsonify({'error': 'Sensor not found'}), 404


@app.route("/sensors/<name>", methods=['POST'])
def createSensorConfig(name):
    sensor_found = None
    for sensor in sensors:
        if sensor['name'] == name:
            sensor_found = sensor
            break

    if not sensor_found:
        return jsonify({'error': 'Sensor not found'}), 404

    if name in config_files:
        return jsonify({
            'error': 'Configuration already exists for this sensor',
        }), 409

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing configuration data'}), 400

    config_files[name] = data

    return jsonify({
        'message': f'Configuration created for {name}',
        'config': config_files[name],
        '_links': add_sensor_links(sensor_found)['_links']
    }), 201


@app.route("/sensors/<name>", methods=['PUT'])
def updateSensorConfig(name):
    data = request.get_json()
    if not data or 'unit' not in data:
        return jsonify({'error': 'Missing unit in request body'}), 400

    if name not in config_files:
        return jsonify({'error': f'Config file for sensor {name} does not exist'}), 409

    unit = data['unit']
    if unit not in ['C', 'F', 'K']:
        return jsonify({'error': 'Invalid unit. Must be C, F, or K'}), 400

    config_files[name]['unit'] = unit
    return '', 204


@app.route("/")
def main():
    return redirect('/sensors')
