# Event Management API

A simple RESTful API built with Flask for managing events. Data is stored
in memory (a Python list of `Event` objects) to simulate a database, so
the data resets each time the server restarts.

## Running the server

```bash
pip install flask
python app.py
```

The server runs at `http://localhost:5000`.

## Routes

### `POST /events`
Creates a new event.

**Request body**
```json
{ "title": "Hackathon" }
```

**Response — `201 Created`**
```json
{ "id": 3, "title": "Hackathon" }
```

**Error — `400 Bad Request`** (missing or empty `title`)
```json
{ "error": "A 'title' field is required to create an event" }
```

---

### `PATCH /events/<id>`
Updates the title of an existing event.

**Request**: `PATCH /events/1`
```json
{ "title": "Hackathon 2025" }
```

**Response — `200 OK`**
```json
{ "id": 1, "title": "Hackathon 2025" }
```

**Error — `404 Not Found`** (no event with that id)
```json
{ "error": "Event with id 1 not found" }
```

---

### `DELETE /events/<id>`
Removes an event from the list.

**Request**: `DELETE /events/2`

**Response — `200 OK`**
```json
{ "message": "Event with id 2 deleted" }
```

**Error — `404 Not Found`** (no event with that id)
```json
{ "error": "Event with id 2 not found" }
```

## Notes

- All responses are formatted as JSON using `jsonify()`.
- Route paths use plural nouns (`/events`) to follow REST conventions.
- A shared `find_event()` helper avoids duplicating the id-lookup logic
  across the PATCH and DELETE routes.
- Validation ensures a `title` is present before creating or updating an
  event, returning a `400` with a clear error message if it's missing.