"""
Swagger template
"""

template = {
    "swagger": "2.0",
    "info": {
        "title": "Fast-Food-Fast",
        "description": 'Fast-Food-Fast is a food delivery service app for a restaurant.',
    },
    "definition": {
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
                "status": {
                    "type": "string"
                }
            }
        },

    },
}
