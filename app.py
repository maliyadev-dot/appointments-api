from flask import Flask, jsonify, request

app = Flask(__name__)

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
    return jsonify(appointments), 200

@app.route('/appointments', methods=['POST'])
def create_appointment():
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