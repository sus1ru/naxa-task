# naxa-task
A simple REST API django application to manage interns in an organization.


### Features

* Class based views for User management supporting CRUD operations.
* Attendance and Task app implemented using Viewsets also supporting CRUD operations.
* API visualization and automatic documentation done with drf-yasg and swagger-ui.
* Intern can mark a task assigned to them completed.
* Token based authentication for valid API calls.
* Followed test driven development approach just for the suffering (bit off more than i could chew).


## Requirements

* Docker
* Django>=3.2.4,<3.3
* djangorestframework>=3.12.4,<3.13
* psycopg2>=2.8.6,<2.9
* drf-yasg==1.21.4


# Installation

Install docker on your machine and follow these steps:


Clone the repository
```
git clone https://github.com/sus1ru/naxa-task.git
```

Initialize the project and Install all the requirements

```
cd naxa-task/
docker-compose build
```

Create database tables
```
docker-compose run --rm app sh -c "python manage.py makemigrations"
```

Create an admin
```
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

Run django server
```
docker-compose up
```

## Usage
Then, open the django admin page in browser, should be ```localhost:8000/admin/``` and login to the application with the admin credentials. To test the api use the swagger url ```localhost:8000/swagger/```.