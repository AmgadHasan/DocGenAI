import gradio as gr
from utils.agents import TokenizersChatbot, DocGenAI
from typing import List, Tuple, Union

input_placeholder = 'Enter something here'

welcome_message = 'Thank you for reaching out to Tokenizers! My name is Picky. I am an AI assistant who can help you create your dream app with ease. Can you tell me about your app' 
#chatbot = TokenizersChatbot()
chatbot = DocGenAI()

def docgenai_chat(input: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    user_input = ' '.join(s)
    output = chatbot.generate(user_input)
    history.append((input, output))
    return history, history

block = gr.Blocks(title='DocGen.AI', css='footer {visibility: hidden}')

with block:
    gr.Markdown("""<h1><center>DocGen.AI - Create SRS documents for your apps by chatting with an AI assistant!</center></h1>""")
    chat_box = gr.Chatbot()
    text_input_box = gr.Textbox(placeholder=input_placeholder)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(docgenai_chat, inputs=[text_input_box, state], outputs=[chat_box, state])


# For user Authentication
block.launch(server_name="0.0.0.0", server_port=8000)

