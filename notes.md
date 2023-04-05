

### SOP to create an API:
1. Create a db schema in models directory
2. Create a user input schema for the APIs in schemas.py
3. Create the APIs to take inside the input and perform operation on it in resource directory
4. Connect the blueprints from resource directory to 'func: create_app' in app.py
5. Create endpoints on Postman or Insomnia for API testing