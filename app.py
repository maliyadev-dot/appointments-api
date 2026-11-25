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

if __name__ == '__main__':
    app.run(debug=True)