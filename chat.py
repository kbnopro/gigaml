import glob
from ai_sdk import generate_chat, stream_chat

context = []

context.append(
    """"
        The following text is the data you are given, and this is the only knowledge you have.
        Those are data of companies, each seperated by "\n--------------------\n". The name of company is one of the main heading at the top. 
        The retail equity research is the company name. One of the other heading is the industry of the company. 
    """
)

for file_name in glob.glob("./processed_data/*.txt"):
    print(f"Loading file: {file_name}")

    with open(file_name, "r") as f:
        if f.readline().strip() == "":
            print(f"File {file_name} is empty, skipping.")
            continue
        context.append("\n".join(f.readlines()))
        context.append("\n--------------------\n")

context.append(
    "This is the end of data",
)

messages = []

while True:
    inp = input("Enter the question: ")
    if len(inp) == 0:
        continue
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": inp,
                }
            ],
        }
    )
    # with stream_chat(messages, "\n".join(context)) as stream:
    #     response = ""
    #     for chunk in stream.text_stream:
    #         print(chunk, end="", flush=True)
    #         response += chunk
    #     print(stream.response.headers)
    # print("\n\n")

    response = generate_chat(messages, "\n".join(context))

    print("\n\n")
    print(response.content[0].text)
    print("\n\n")

    messages.append(
        {
            "role": "assistant",
            "content": [{"type": "text", "text": response.content[0].text}],
        }
    )
