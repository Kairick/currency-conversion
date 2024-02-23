Task: Develop an API for currency conversion using FastAPI, SQLAlchemy. The API should provide the ability to obtain current currency rates and convert between them.

Subtasks:
  1. Receive current exchange rates:
Create a model to store information about the currency (name, code, rate).
Implement a function that will request current exchange rates from an external API (for example, https://exchangeratesapi.io/) and save them in the database.
Implement a function that will return the date and time of the last update of courses in the database.

  2. Conversion between currencies:
Implement a function that will accept two currencies (source and target) and the amount to convert. The function should return the conversion result based on current exchange rates from the database.

  3. Creating and setting up an API:
Use FastAPI to create an API with three endpoints:
Update exchange rates in the database to current rates.
Displaying the date and time of the last update of courses in the database.
Conversion between currencies.
The database session and endpoints must be asynchronous.
The project should be launched with one command after cloning the repository, preferably via "docker-compose -f docker-compose.yml up --build -d".
PostgreSQL must also run in a container.

4. Applying Migrations with Predefined Data:
Include a migration script that initializes the database with predefined currency data, including names, codes, and initial exchange rates.
Ensure that these migrations are automatically applied when setting up the project, either during the initial setup or during container initialization.
Document the migration process and provide instructions for running migrations when setting up the project.

Notes:
Once development is complete, provide instructions for installing and running the project, as well as examples of using the API.
Please note that the number of requests to the API specified in the description is limited. You must leave at least 2 requests for verification using the preset API key. An external API with current currencies is not important. If you find another service, the requirements are the same - the ability to update exchange rates at least 2 times.
Push project to github
Set up a CI script that will do the following:
Check the syntax of your code for errors (for example, using pylint or flake8 for Python).
Run automated tests for your application (if any).
Generate a report on code coverage by tests (if possible).

How to run the project:
1. Clone the repository
2. Create a .env file in the root directory with the following content:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=currency
POSTGRES_HOST=db
POSTGRES_PORT=5432
API_KEY=your_api_key
APY_URL=https://api.currencyapi.com/v3/
```
3. Run the command "docker-compose -f docker-compose.yml up --build -d"
4. The API will be available at http://0.0.0.0:8000