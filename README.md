# best-taxi-service
![Logo of the project](https://raw.githubusercontent.com/vulpemventures/liquid.taxi/master/src/images/taxi-social.jpg)


> Taxi-service!

Web-site for manage local taxi-service with cars, drivers and manufacturers!

## Check it out!

[taxi project deployed to render.com](https://best-taxi-service.onrender.com/)

## Installing / Getting started

Python3 must be already installed.

Clone the [repository](https://github.com/AriohBelskij/best-taxi-service) and run the commands:

```shell
cd taxi-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

After cloning the repository, you need to go to the root of the project, create and activate the virtual environment, and install the elements necessary for the project. And then start the server.

You can use this to add data to db:
```shell
python manage.py loaddata taxi_service_db_data.json
```
and use this login and password to test staff Features:
* username - admin.user
* password - 1qazcde3

## Features

What's all the feature and whistles this project can perform?
* Authentication functionality for Driver/User.
* Like and comment system
* Managing cars, driver & cars directly from website interface.
* Preaty users profile with avatars

![img.png](img.png)