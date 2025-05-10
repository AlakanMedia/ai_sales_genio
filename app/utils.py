game_store_instruction = "You are a helpful and knowledgeable virtual assistant for a video game console store. You provide detailed, accurate, and friendly information about products available in the store."


get_available_products_func = {
    "type": "function",
    "function": {
        "name": "get_available_products",
        "description": "Returns a list with the names of all available products.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


get_product_info_func = {
    "type": "function",
    "function": {
        "name": "get_product_info",
        "description": "Find the description and price of a product by its name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product."
                },
            },
            "required": ["product_name"]
        }
    }
}


check_stock_func = {
    "type": "function",
    "function": {
        "name": "check_stock",
        "description": "Searches the available stock of the product requested by the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product."
                },
            },
            "required": ["product_name"]
        }
    }
}