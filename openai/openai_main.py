import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def main():
    """
    Simple CLI Chat Application using OpenAI API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please add it to your .env file.")
        return

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return

    print("Welcome to the OpenAI Chat App!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("-" * 50)

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})

            # Call OpenAI API
            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="gpt-3.5-turbo",
                )
            except Exception as e:
                print(f"Error communicating with OpenAI: {e}")
                continue

            assistant_response = chat_completion.choices[0].message.content
            print(f"AI: {assistant_response}")

            messages.append({"role": "assistant", "content": assistant_response})

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break


if __name__ == "__main__":
    main()
