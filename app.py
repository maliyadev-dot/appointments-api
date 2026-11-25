from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# In-memory storage for appointments
appointments =[]
next_id = 1

# Helpers
def validate_appointment_body(data):
    # Handle missing or non-JSON body
    if not isinstance(data, dict):
        return False, {"body": "Request body must be a JSON object."}

    errors = {}

    title = data.get("title")
    start_time = data.get("start_time")

    if not isinstance(title, str) or not title.strip():
        errors["title"] = "Title is required and must be a non-empty string."

    if not isinstance(start_time, str):
        errors["start_time"] = "Start time is required and must be a string."

    if errors:
        return False, errors

    return True, {}

# API Endpoints
@app.route('/appointments', methods=['GET'])
def get_appointments():
    """
    Get all appointments
    ---
    tags:
      - Appointments
    responses:
      200:
        description: List of appointments
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  start_time:
                    type: string
                  duration:
                    type: string
                  location:
                    type: string
    """
    return jsonify(appointments), 200

@app.route('/appointments', methods=['POST'])
def create_appointment():
    """
    Create a new appointment
    ---
    tags:
      - Appointments
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Dentist"
            start_time:
              type: string
              example: "2026-11-25T10:00"
            duration:
              type: string
              example: "30m"
            location:
              type: string
              example: "Clinic"
          required:
            - title
            - start_time
    responses:
      201:
        description: Appointment created
      400:
        description: Validation error
    """
    global next_id
    data = request.get_json()

    is_valid, errors = validate_appointment_body(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    appointment = {
        "id": next_id,
        "title": data.get("title"),
        "start_time": data.get("start_time"),
        "duration": data.get("duration"),
        "location": data.get("location")
    }
    appointments.append(appointment)
    next_id += 1

    return jsonify(appointment), 201

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """
    Get a single appointment by ID
    ---
    tags:
      - Appointments
    parameters:
      - in: path
        name: appointment_id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Appointment found
      404:
        description: Appointment not found
    """
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return jsonify(appointment), 200

    return jsonify({"error": "Appointment not found"}), 404

@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.get_json()

    is_valid, errors = validate_appointment_body(data)
    if not is_valid:
        return jsonify({"errors": errors}), 400

    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointment["title"] = data.get("title")
            appointment["start_time"] = data.get("start_time")
            appointment["duration"] = data.get("duration")
            appointment["location"] = data.get("location")
            return jsonify(appointment), 200

    return jsonify({"error": "Appointment not found"}), 404

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    for index, appointment in enumerate(appointments):
        if appointment["id"] == appointment_id:
            del appointments[index]
            return "", 204

    return jsonify({"error": "Appointment not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)