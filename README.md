# Django CRUD Project

## What is the use of this Repo

This Project is a Django CRUD Project which demonstrates the following
1. Using Django template
2. Making HTTP calls
3. Integrating Payment(Stripe)
4. Integrating Email System(Mailgun)
5. Using Basic Routing in Django
6. Using Python Decouple in Django

The project Template can be used to build bigger projects

## Prerequisites

### Install Python
Refer to https://www.python.org/downloads/ to install python

### Install Packages
pip install -r requirements.txt

## Cloning and Running the Application in local
Clone the project into local

Create mysql database named 'newarkshop'

In order to run the application Type the following command
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py run runserver
```

The Application Runs on **localhost:8000**