# IBAN Validations Service

The IBAN Validations Service is a simple API service built using Django and Django Rest Framework (DRF). It provides API endpoints for validating an International Bank Account Number (IBAN) and also fetching additional information about the IBAN like country, bank code, account number, etc.

## Features

1. Validate an IBAN
2. Fetch validation history of an IBAN
3. Fetch details from an IBAN

## Setup and Installation

The project is Dockerized for easy setup and installation. Here are the steps:

1. Ensure Docker and Docker-compose are installed on your machine.
2. Clone the repository:

```bash
git clone https://github.com/davidsilaghi24/iban-validations.git
```

3. Navigate into the directory and start the service:

cd iban-validations
docker-compose up --build

## Default User

A default user is created when the service is started. The credentials are:

username: defaultuser
password: defaultpassword

## API Documentation

Swagger API documentation is provided and can be accessed at localhost:8000/swagger.

## Testing

To run the tests, you can execute the following command:

docker-compose exec web python manage.py test

You can use the default user credentials (defaultuser/defaultpassword) to authenticate the requests.

Please refer to the Swagger API documentation for the request/response formats and other details.

## Support

If you encounter any issues or need further assistance, please raise an issue on this repository.
