import gradio as gr
import random

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
#openai.api_key = "xxxxxx"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

responses = [
  "Hello there!",
  "How can I assist you today?",
  "I'm sorry, I didn't quite understand that. Could you please rephrase your question?",
  "Interesting! Tell me more about that.",
  "I'm afraid I don't have an answer to that question at the moment.",
  "Have you tried searching for an answer online?",
  "That's a great question! Let me look that up for you.",
  "I'm sorry, but I am not programmed to provide personal information.",
  "Let's change the topic. What are your hobbies?",
  "It was nice chatting with you. Have a great day!"
]

def openai_create(prompt):

    response = random.choice(responses)

    return response



def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history


block = gr.Blocks(title='DocGen.AI', css='footer {visibility: hidden}')


with block:
    gr.Markdown("""<h1><center>DocGen.AI - Create SRS documents for your apps by chatting with an AI assistant</center></h1>
    """)
    chat_box = gr.Chatbot()
    text_input_box = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[text_input_box, state], outputs=[chat_box, state])

# For user Authentication
block.launch(server_name="0.0.0.0", server_port=8000)

