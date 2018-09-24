[![Build Status](https://travis-ci.org/mashafrancis/fast-food-fast.svg?)](https://travis-ci.org/mashafrancis/fast-food-fast)
[![Coverage Status](https://coveralls.io/repos/github/mashafrancis/fast-food-fast/badge.svg?branch=ch-api-authentication-160479327)](https://coveralls.io/github/mashafrancis/fast-food-fast?branch=ch-api-authentication-160479327)
[![Maintainability](https://api.codeclimate.com/v1/badges/fbf800046792d80d7b57/maintainability)](https://codeclimate.com/github/mashafrancis/fast-food-fast/maintainability)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# Fast-Food-Fast
Fast-Food-Fast is a food delivery service app for a restaurant.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.7
* Virtualenv

### Features
* Users can create accounts and sign in
* Users can view available food items
* Users can order a specific food item
* Admin can view all orders
* Admin can view a specific food order
* Admin can update the order status

### Technologies Used
**Flask** For API implementation

**PyJWT** For securing endpoints

**Pytest** For documentation

**SwaggerUI** For API documentation

### Installation
1. To clone this repo run ``https://github.com/mashafrancis/fast-food-fast/tree/master`` from your local terminal
2. `git checkout develop` to use the develop branch
3. Cd into the fast-food-fast Folder
4. Create a virtual environment `python3 -m venv venv`
5. Activate the virtual environment `source venv/bin/activate`
6. Install requirements `pip install -r requirements.txt` This should install all dependancies including flask
7. Create a `.env` file in the root folder
8. Copy the contents of `.env.sample` into `.env`
9. In the terminal run `source .env` to export the settings
10. Now Run the app `python run.py`

### Usage
The API implements a CRUD interface for the orders using GET, POST, PUT, PATCH and DELETE HTTP methods. The API has 
an auth route for registration and login.

### Available Endpoints
| Method             | Endpoint                                       | Functionality
|:------------------:|:----------------------------------------------:|:--------------------------------------:|
 POST                | /api/v1/auth/signup                            | Register a new account
 POST                | /api/v1/auth/login                             | Login into application
 GET                 | /api/v1/users                                  | Get all users
 GET                 | /api/v1/users/<user_id>                        | Get a single user by user_id
 GET                 | /api/v1/orders                                 | Get a list of all available orders
 GET                 | /api/v1/orders/<order_id>                      | Get order with specified order_id
 POST                | /api/v1/orders                                 | Create a new order
 DELETE              | /api/v1/orders                                 | Delete all orders
 PUT                 | /api/v1/orders/<order_id>                      | Update order with specified order_id
 DELETE              | /api/v1/orders/<order_id>                      | Delete order with specified order_id
 PATCH               | /api/v1/orders/<order_id>                      | Update the status of a specific order
 GET                 | /api/v1/category                               | Get a specific food category
 POST                | /api/v1/category                               | Add a food category
 DELETE              | /api/v2/category                               | Delete all categories

The endpoints can be tested using Postman
**Note** After login or signup, an access token is returned that needs to be passed in the header of all the other requests.

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

### Users (For Authentication)
"user_registration": 
      
      "username": "tester",
      "email": "test@gmail.com",
      "password": "test1234",
      "confirm_password": "test1234"
 
    
"user_login": 

      "email": "test@gmail.com",
      "password": "test1234"
    
    

"order": 

      "order_id": 1,
      "name": "Burger",
      "quantity": 4,
      "price": 1000,
      "created_by": "Test"

"category": 

      "category_id": 1,
      "name": "Drinks",
      "description": "Get your drinks!"



## Version
Most recent version: version 1

### Documentation
[Heroku](https://masha-fast-food.herokuapp.com/api/v1/docs/)

### Frontend
[Github Pages](https://mashafrancis.github.io/fast-food-fast/)

## Author
* [Francis Masha](https://github.com/mashafrancis)

