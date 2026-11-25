from flask import Flask, jsonify, request

app = Flask(__name__)

appointments =[]
next_id = 1

@app.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify(appointments), 200

@app.route('/appointments', methods=['POST'])
def create_appointment():
    global next_id
    data = request.get_json()

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