import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("API_KEY", ""))

def create_assistant(
    instructions: str,
    name: str,
    model: str,
    tools: list | None = None
) -> dict:
    try:
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name=name,
            model=model,
            tools=tools,
        )

        return {"status": "success", "assistant_info": assistant.dict()}
    except Exception as e:
        print(f"ERROR (create_assistant): {e}")
        return {"status": "fail", "assistant_info": None}

def create_thread() -> dict:
    try:
        thread = client.beta.threads.create()

        return {"status": "success", "thread_info": thread.dict()}
    except Exception as e:
        print(f"ERROR (create_thread): {e}")
        return {"status": "fail", "thread_info": None}

def create_query_message(thread_id: str, role: str, content: str) -> dict:
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content,
        )

        return {"status": "success", "message_info": message.dict()}
    except Exception as e:
        print(f"ERROR (create_query_message): {e}")
        return {"status": "fail", "message_info": None}

def get_response(
    assistant_id: str,
    thread_id: str,
    run_id: str = "",
    tool_outputs: list | None = None
) -> dict:
    try:
        if run_id and tool_outputs:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs
            )
        else:
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id,
            )

        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )

            time.sleep(0.5)

        run = run.dict()

        if run["required_action"]:
            required_action = run["required_action"]["submit_tool_outputs"]["tool_calls"]
            function_id = required_action[0]["id"]
            function_name = required_action[0]["function"]["name"]
            function_parameters = required_action[0]["function"]["arguments"]

            return {
                "status": "success",
                "run": {"id": run["id"]},
                "function": {
                    "id": function_id,
                    "name": function_name,
                    "parameters": function_parameters,
                },
            }
        else:
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            messages = messages.dict()
            assistant_message = messages["data"][0]["content"][0]["text"]["value"]

            return {"status": "success", "assistant_message": assistant_message}
    except Exception as e:
        print(f"ERROR (get_response): {e}")
        return {"status": "fail", "assistant_message": "", "function": {}}