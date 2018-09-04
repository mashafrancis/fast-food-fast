"""API Schema definitions"""

Order_Schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "quantity": {"type": "string"},
        "price": {"type": "number"},
    }
}
