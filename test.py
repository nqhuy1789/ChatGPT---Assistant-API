import os
import openai as client

OPENAI_API_KEY = "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"
THREAD_ID = "thread_fNwAKS1n6V8aQZ7f2AXvHgs5"
ASSISTANT_ID = "asst_eWMoILrLvCwfGpCEdxuaxUDI"

client.api_key = OPENAI_API_KEY

# my_assistant = client.beta.assistants.retrieve("asst_eWMoILrLvCwfGpCEdxuaxUDI")

# my_thread = client.beta.threads.create()
# print(my_thread.id)

# # Step 4: Add a Message to a Thread
# my_thread_message = client.beta.threads.messages.create(
#   thread_id=THREAD_ID,
#   role="user",
#   content='Hướng dẫn giảng bài "CHỊ SẼ GỌI EM BẰNG TÊN" trong chương trình ngữ văn lớp 6?',
# )

# # Step 5: Run the Assistant
# my_run = client.beta.threads.runs.create(
#   thread_id=THREAD_ID,
#   assistant_id=ASSISTANT_ID,
# )

# # Step 6: Periodically retrieve the Run to check on its status to see if it has moved to completed
# while my_run.status in ["queued", "in_progress"]:
#     keep_retrieving_run = client.beta.threads.runs.retrieve(
#         thread_id=THREAD_ID,
#         run_id=my_run.id
#     )
#     print(f"Run status: {keep_retrieving_run.status}")

#     if keep_retrieving_run.status == "completed":
#         print("\n")

#         # Step 7: Retrieve the Messages added by the Assistant to the Thread
#         all_messages = client.beta.threads.messages.list(
#             thread_id=THREAD_ID
#         )

#         print("------------------------------------------------------------ \n")

#         print(f"User: {my_thread_message.content[0].text.value}")
#         print(f"Assistant: {all_messages.data[0].content[0].text.value}")

#         break
#     elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
#         pass
#     else:
#         print(f"Run status: {keep_retrieving_run.status}")
#         break

all_messages = client.beta.threads.messages.list(
    thread_id=THREAD_ID, order="asc"
)

for message in all_messages: 
    # print(message.role + ": " + message.content[0].text.value)
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')
        # Gather citations based on annotation attributes
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
            # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    message_content.value += '\n' + '\n'.join(citations)
    print(message_content.value)