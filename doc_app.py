import os

from flasgger import Swagger

from app import create_app

app = create_app('production')
swagger = Swagger(app)


# Orders
@app.route('v1/orders', methods=["POST"])
def create_order():
    """
    endpoint for adding a new order.
    ---
    parameters:
    - name: name
      required: true
      in: formData
      type: string
    - name: quantity
      required: true
      in: formData
      type: integer
    - name: price
      required: true
      in: formData
      type: float
    - name: status
      required: false
      in: formData
      type: string
    """


@app.route('v1/orders', methods=["GET"])
def get_all_orders():
    """
    endpoint for fetching all orders.
    ---
    parameters:
    :return:
    """


@app.route("/v1/orders/<int:orders_id>", methods=["GET"])
def get_particular_order():
    """endpoint for fetching a particular order.
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
    """


@app.route('/v1/orders/<int:order_id>', methods=["PUT"])
def update_order():
    """ endpoint for updating an existing order.
    ---
    parameters:
    - name: name
      required: true
      in: formData
      type: string
    - name: quantity
      required: true
      in: formData
      type: integer
    - name: price
      required: true
      in: formData
      type: float
    - name: status
      required: false
      in: formData
      type: string
    """


@app.route('/v1/orders/<int:order_id>', methods=["DELETE"])
def delete_ride():
    """ endpoint for deleting an existing ride.
    ---
    parameters:
      - name: ride_id
        in: path
        type: integer
        required: true
    """


@app.route('/')
def hello_world():
    """test that flask app is running"""
    return "To view the docs visit: https://masha-fast-food.herokuapp.com/apidocs"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
