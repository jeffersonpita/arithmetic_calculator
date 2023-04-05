# Arithmetic Calculator REST API

Implement a Web platform to provide a simple calculator functionality (addition, subtraction, multiplication, division, square root, and a random string generation) where each functionality will have a separate cost per request.
User’s will have a starting credit/balance. Each request will be deducted from the user’s balance. If the user’s balance isn’t enough to cover the request cost, the request shall be denied.
This Web application and its UI application should be live (on any platform of your choice). They should be ready to be configured and used locally for any other developer (having all instructions written for this purpose).

Here is the django backend of this application

# Installation

```
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

You may go to http://localhost:8000/admin/api/user/1/change/ to change the user balance before testing.
