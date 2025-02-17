# Egyptian National ID Interpreter

An API that validates Egyptian National IDs and extracts useful information from them. This tool is designed for developers and services to easily integrate ID validation and data extraction functionality into their applications.


[Key Features](#key-features) •
[How To Use](#how-to-use) •
[API Endpoints](#api-endpoints)•
[Development](#development)

![Demo](./demo.gif)

## Key Features

- **National ID Validation**
    - Check whether an Egyptian National ID is valid.
    - The algorithm includes almost complete validation but lacks internal checksum validation for the last digit (due to limited online resources).
- **Data Extraction** - Extracts meaningful data from valid IDs:
    - Date of Birth (Year, Month, Day)

    - Gender (Available in both English and Arabic)

    - Governorate of Birth (or “Outside Egypt,” provided in both English and Arabic)
    - Citizen's Serial Number (a unique identifier for individuals born on the same day and in the same governorate)
- **API Features**
    - Prevent excessive API usage with customizable rate limits.
    - Use secure API keys for service-to-service communication.
    - Track API calls for monitoring and analytics.
- **Robust Development Practices**
    - Unit Tests to ensure code reliability.
    - Postman Tests to ensure expected responses from API endpoints.
    - Linting and Formatting for a clean, consistent codebase with Ruff and Pre-commit.
    - GitHub Actions for CI/CD pipelines for automated testing.
    - Swagger Documentation for self-documenting API for easy integration.

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/), and pip installed on your machine.

From your terminal:

```bash
# Clone the repository
$ git clone https://github.com/john-roufaeil/egyptian-national-id-interpreter

# Go into the repository
$ cd egyptian-national-id-interpreter

# Install dependencies
$ pip install -r requirements.txt

# Navigate to the main project directory
$ cd interpreter

# Run the application
$ python manage.py runserver
```

The API will now be available locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API Endpoints

### ```GET /```

Retrieves the API key for authorization.

Resopnse:

``` json
{
  "api_key": "<API Key>"
}
```

### ``` POST /validate-national-id/ ```

Validates the provided National ID and extracts information for valid IDs.


Request Header:

``` json
{
    "Authorization": "Api-Key <API Key>"
}
```

Request Body:

``` json
{
    "national_id": "<National ID>"
}
```

Response Body:

``` json
{
  "year": <Year of Birth>,
  "month": <Month of Birth>,
  "day": <Day of Birth>,
  "governorate": {
    "ar": <Governorate in Arabic>,
    "en": <Governorate in English>
  },
  "gender": {
    "ar": <Gender in Arabic>,
    "en": <Gender in English>
  },
  "serial_number": <Serial Number>
}
```

Error Responses:

- Invalid API Key:

``` json
{
  "error": "Invalid API key"
}
```

- Missing API Key:

``` json
{
  "error": "API key is missing."
}
```

- Invalid National ID:

``` json
{
      "error": "National ID is invalid."
}
```

## Development

### Linting and formatting

Ensure code quality and consistency using Ruff and pre-commit hooks:

``` bash
# Check for linting issues and optionally fix fixable problems
$ ruff check --fix

# Format files
$ ruff format

# Run pre-commit hooks on all files
$ pre-commit run --all-files
```

### Running Tests

Execute tests to ensure everything works as expected:

``` bash
# Navigate to the project directory
$ cd interpreter

# Run tests
$ python manage.py test
```

### Postman API Tests

- Import the provided Postman collection at the repository root to test API endpoints interactively.
- Verify the application responses for both valid and invalid inputs.
�