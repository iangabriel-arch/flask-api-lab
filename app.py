from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Keeps track of the next id to assign so new events always get a unique id,
# even after other events have been deleted.
next_id = max(event.id for event in events) + 1


def find_event(event_id):
    """Helper to look up an event by id. Returns None if not found.
    Centralizing this logic avoids repeating the same loop/lookup in
    every route that needs to find an event."""
    return next((event for event in events if event.id == event_id), None)


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    global next_id

    # Parse the incoming JSON body. silent=True prevents Flask from
    # raising an exception if the body is missing or malformed;
    # instead get_json() returns None so we can handle it ourselves.
    data = request.get_json(silent=True)

    # Validate that a body was sent and that it includes a title
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "A 'title' field is required to create an event"}), 400

    # Create the new event using the next available id
    new_event = Event(next_id, data["title"])
    events.append(new_event)
    next_id += 1

    # 201 Created signals that a new resource was successfully created
    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    # If no event matches the given id, return a 404 with a clear message
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    data = request.get_json(silent=True)

    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "A 'title' field is required to update an event"}), 400

    # Update the event's title in place
    event.title = data["title"]

    # 200 OK signals the update was applied successfully
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    events.remove(event)

    # 200 OK with a confirmation message; 204 No Content would also be
    # valid, but a body helps confirm which event was removed.
    return jsonify({"message": f"Event with id {event_id} deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)