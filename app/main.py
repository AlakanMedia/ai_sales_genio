from business_logic import function_controller
from assistant import create_assistant, create_thread, create_query_message, get_response
from utils import game_store_instruction, get_available_products_func, get_product_info_func, check_stock_func


def start_conversation(assistant_id: str, thread_id: str) -> None:
    """
    Function that handles user interactions, 
    tool calls and assistant responses in a loop.
    """
    function_interaction = False

    while True:
        if function_interaction:
            run_id = user_query.pop("run_id")
            response = get_response(
                assistant_id,
                thread_id,
                run_id=run_id,
                tool_outputs=[user_query],
            )
        else:
            user_query = input("user: ")

            if user_query == "exit":
                return

            response = create_query_message(thread_id, "user", user_query)

            if response["status"] != "success":
                return

            response = get_response(assistant_id, thread_id)

        if response["status"] != "success":
            return

        if response.get("assistant_message"):
            print(f"assistant: {response["assistant_message"]}")
            function_interaction = False
        elif response.get("function") and response.get("run"):
            user_query = function_controller(
                response["function"]["id"],
                response["function"]["name"],
                response["function"]["parameters"],
            )
            user_query["run_id"] = response["run"]["id"]
            function_interaction = True


def main():
    """
    Main function that is responsible for creating the assistant and
    creating the thread of the conversation. If everything goes well, 
    the conversation loop is started.
    """
    response = create_assistant(
        instructions=game_store_instruction,
        model="gpt-4o",
        name="GameStoreBot",
        tools=[get_available_products_func, get_product_info_func, check_stock_func],
    )

    if response["status"] != "success":
        return

    assistant = response["assistant_info"]
    assistant_id = assistant["id"]

    response = create_thread()

    if response["status"] != "success":
        return

    thread = response["thread_info"]
    thread_id = thread["id"]

    start_conversation(assistant_id, thread_id)


if __name__ == "__main__":
    main()