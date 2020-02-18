# Flask Flash Cards

A simple Python API for keeping track of collections of flash cards.
Flash cards are organized by collection, and collections are organized by subject.

The API provides a simple, JWT-based membership system using a username/password combination.

## API

### POST - /register

- { string:username, string:password}

### POST - /login

- { string:username, string:password}

### DELETE - /delete

- { int:user_id}

### /collections

- GET - retrieves all card collections
- POST {string:subject} - Add a new collection

### /collections/<int:col_id>

- GET - retrieves a single card collection
- PUT {string:new_subject} - update the collection name
- DELETE - cascade delete a single collection

### /collections/<int:col_id/>cards>

- POST - adds a flash card to the given collection

### /collections/<int:col_id>/cards/<int:card_id>

- GET - retrieves a single flash card
- PUT {string:question, string:answer, string:hint, bool:learned} update a flash card
- DELETE delete a card from the collection
