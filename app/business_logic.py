import json
from mock_data import products


def get_available_products() -> list:
    try:
        return [product["name"] for product in products]
    except Exception as e:
        return []


def get_product_info(product_name: str) -> dict | str:
    for product in products:
        if product["name"] == product_name:
            return {
                "description": product["description"],
                "price": product["price"],
            }

    return f"Product with name: {product_name} not found!"


def check_stock(product_name: str) -> int | str:
    for product in products:
        if product["name"] == product_name:
            return product["stock"]

    return f"Product with name: {product_name} not found!"


def function_controller(id: str, name: str, parameters: str) -> str:
    """
    This function is in charge of calling the corresponding function
    chosen by the assistant and returning its corresponding response.
    """
    response = {
        "tool_call_id": id,
        "output": f"Function with name: '{name}' not found!",
    }

    try:
        parameters = json.loads(parameters)

        if name == "get_available_products":
            response["output"] = json.dumps({
                "available_products": get_available_products(),
            })
        elif name == "get_product_info":
            if not parameters.get("product_name"):
                raise Exception("Parameter 'product_name' not found!")

            response["output"] = json.dumps({
                "product_info": get_product_info(parameters["product_name"]),
            })
        elif name == "check_stock":
            if not parameters.get("product_name"):
                raise Exception("Parameter 'product_name' not found!")

            response["output"] = json.dumps({
                "product_stock": check_stock(parameters["product_name"]),
            })

        return response
    except json.JSONDecodeError as e:
        print(f"ERROR (function_controller): {e}")
        return f"Invalid parameters format: {parameters}"
    except Exception as e:
        print(f"ERROR (function_controller): {e}")
        return "An error occurred at the time of the function call"