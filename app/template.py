"""
Swagger template
"""

template = {
    "swagger": "2.0",
    "info": {
        "title": "Fast-Food-Fast",
        "description": 'Fast-Food-Fast is a food delivery service app for a restaurant.'
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "definition": {
        "UserSignup": {
            "type": "object",
            "in": "body",
            "properties": {
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "confirm_password": {
                    "type": "string"
                }
            }
        },
        "UserLogin": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            }
        },
        "Orders": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "quantity": {
                    "type": "string"
                },
                "price": {
                    "type": "string"
                },
                "created_by": {
                    "type": "string"
                }
            }
        },
    },
}
