import gradio as gr
from utils.agents import TokenizersChatbot
from typing import List, Tuple, Union

prompt = 'Thank you for reaching out to Tokenizers! How can we help you?'
chatbot = TokenizersChatbot()

def docgenai_chat(input: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]],input]:
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    user_input = ' '.join(s)
    output = chatbot.generate(user_input)
    history.append((input, output))
    #clear textbox
    input=" "

    return history, history, input




def clear_state():

      print(f"before : {chatbot.conversation_chain.memory.buffer}")
      chatbot.conversation_chain.memory.clear()
      print(f"after : {chatbot.conversation_chain.memory.buffer}")
      history=[]
      return history


block = gr.Blocks(title='DocGen.AI', css='.gradio-container {background-image: linear-gradient(-45deg,#B4C5F8,#ADDEFF,#F9DEDC, #FCD9E8); border-radius:10px; },   footer {visibility: hidden} ')

with block:
    gr.Markdown("""<h1><center>DocGen.AI - Create SRS documents for your apps by chatting with an AI assistant</center></h1>
    """)
    chat_box = gr.Chatbot()
    with gr.Row():
       with gr.Column(scale=0.85):
          text_input_box = gr.Textbox(placeholder=prompt)
          state = gr.State()

       with gr.Column(scale=0.15):
          submit = gr.Button("Send 📤", variant="secondary")
          # print(text_input_box, state)
          submit.click(docgenai_chat, inputs=[text_input_box, state], outputs=[chat_box, state,text_input_box])
          text_input_box.submit(docgenai_chat, inputs=[text_input_box, state], outputs=[chat_box, state,text_input_box])
          # print(chat_box, state,text_input_box)

    clear = gr.ClearButton([text_input_box,chat_box,state],value="Restart Chat 🔃",variant="danger")
    clear.click(clear_state,outputs=[state])
# For user Authentication
block.launch(server_port=8000,debug=True)

