#############################
# api.py #
#############################
import logging
import os
from typing import Optional, List, Dict
import google.auth
import vertexai
from langchain.llms import VertexAI, LlamaCpp
from langchain.chat_models import ChatVertexAI

# def get_chat_model(platform: str, model_name: str|Dict[str, str], max_output_tokens: int|List[int] = [128, 1024]):
#     if platform == 'VertexAI':
#         logging.debug('Initializing Vertex AI ...')
#         credentials, project_id = google.auth.default() # Save credentials json file in 'GOOGLE_APPLICATION_CREDENTIALS' env variable
#         vertexai.init(project=project_id, credentials=credentials)
#         chat_model = ChatVertexAI(model_name='chat-bison', max_output_tokens=128)
#         text_model = VertexAI(model_name='text-bison', max_output_tokens=1024)
    
#     elif platform == 'llama.cpp':
#         logging.debug('Initializing llama.cpp ...')
#         model_dir = os.environ.get('LLAMACPP_MODLES_DIRECTORY')
#         text_model = LlamaCpp(model_path=model_path,max_output_tokens=128)
#         chat_model = LlamaCpp(model_path=model_path,max_output_tokens=1024)
    
#     logging.debug(f"Loaded chat model: {chat_model}\t text_model: {text_model}.")
#     return {chat_model, text_model}

def get_vertexai_models(models_info: str|Dict[str, str], credentials_file_path: str|None = None):
    logging.debug('Authenticating GCP ...')
    credentials, project_id = google.auth.default() # Save credentials json file in 'GOOGLE_APPLICATION_CREDENTIALS' env variable
    logging.debug('Initializing VertexAI ...')
    vertexai.init(project=project_id, credentials=credentials)
    
    models = {}
    for model_type, model_info in models_info.items():
        if model_type in ['chat_model', 'chat']:
            models[model_type] = ChatVertexAI(**model_info)
            logging.debug(f"Loaded chat model: {models[model_type]}")
        
        elif model_type in ['text_model', 'text']:
            models[model_type]  = VertexAI(**model_info)
            logging.debug(f"Loaded text model: {models[model_type]}")
    
    return models
    
def get_llamacpp_models(models_info: str|Dict[str, str], models_dir: str|None = None):
    logging.debug('Initializing llama.cpp ...')
    
    if models_dir is None:
        logging.debug("No model directory specified; defaulting to LLAMACPP_MODLES_DIRECTORY")
        models_dir = os.environ.get('LLAMACPP_MODLES_DIRECTORY')
        logging.debug(f"Models Directory: {models_dir}")
    
    models = {}
    # # if len(models_info) == 1:
    # #     model_name = models_info.pop('model_name')
    # #     model = LlamaCpp(model_path=os.path.join(models_dir, model_name), **models_info)
    # #     logging.debug(f"Loaded model: {model_name}")
    
    # else:
    #logging.debug(f"Loading model: {models_info.values()}")
    for model_type, model_info in models_info.items():
        logging.debug(f"Entered model loading loop")
        model_name = model_info.pop('model_name')
        logging.debug(f"Loading model: {model_name}")
        models[model_type]  = LlamaCpp(model_path=os.path.join(models_dir, model_name), **models_info)
        logging.debug(f"Successfully loaded model: {model_name}")

    return models

#############################
# agents.py #
#############################
import logging
import utils.chains as chains	# has get_conversation_chain, get_srs_chain
import utils.api as api	# To authenticate and get models from API
from utils.templates import ROUTE_TEMPLATE

class DocGenAI :
    def __init__(self, platform='VertexAI'):
        self.platform = platform
        self.chains = self._load_chains()
        self.active_chain_index = 0
        
    def __repr__(self):
        return f"""ChainLinker(chains={self.chains})"""

    def __str__(self):
        return self.__repr__()

    def initialize_chain(self, chain):
        if self.active_chain_index == 1:
            output = chain.chain_run("Ask me a questions about the description of the app.")
        
        return output

    def _load_chains(self):
        if self.platform == 'VertexAI':
            models_info = {'chat_model': {'model_name': 'chat-bison'},
                            'text_model': {'model_name': 'text-bison'}}
            models = api.get_vertexai_models(models_info)
        
        elif self.platform == 'llama.cpp':
            models_info = {'chat_model': {'model_name':'WizardCoder-15B-1.0.ggmlv3.q4_0.bin'},
                            'text_model': {'model_name':'WizardCoder-15B-1.0.ggmlv3.q4_0.bin'}}
            models = api.get_llamacpp_models(models_info)
        
        chains = {'introduction_chain': chains.get_introduction_chain(models['text_model']),
                    'overall_description_chain': chains.get_overall_description_chain(models['text_model'])}
        
        return chains

    def generate(self, input_text):
        #print("chains:", self.chains)
        active_chain = self.chains[self.active_chain_index]
        output = active_chain.chain_run(input_text)
        print("output", output)
      
        if active_chain.condition:
            print('chain.condition')
            self.active_chain_index += 1
            if self.active_chain_index == len(self.chains):            
                return "Finished"
            active_chain = self.chains[self.active_chain_index]
            print("In chain:", active_chain.section_name)
            output = self.initialize_chain(active_chain)
            print('init', output)
            
            return output
      	              
        if active_chain.use_custom_prompt:
            print('active_chain.use_custom_prompt')
            parsed_texts = [chain.parsed_text for chain in self.chains[:self.active_chain_index]]
            active_chain.format_custom_prompt(parsed_texts)
            active_chain.use_custom_prompt = False

        return output


class TokenizersChatbot():
    def __init__(self, platform='VertexAI'):
        self.platform = platform
        self.chat_model, self.text_model = api.get_chat_text_models(platform=self.platform)
        self.conversation_chain = chains.get_conversation_chain(chat_model=self.chat_model)
        self.srs_chain = chains.get_srs_chain(self.text_model)

    def ready_to_generate_document(self, model_output):
        # If model outputs app description, generate document using srs_chain
        response_type = self.text_model(ROUTE_TEMPLATE.format(model_output))
        #print(response_type)
        if response_type == 'description': # If model has enough information about the app, generate srs.
            return True
        elif response_type == 'question':  # If model outputs questions about the app, route back to user.
            return False
        else:
            pass  # Maybe raise error?

    def generate(self, input):
        response = self.conversation_chain.predict(input=input)
        
        if self.ready_to_generate_document(response):
            document = self.srs_chain.predict(app_description = response)
            output = response + '\n' + document
        else:
            output = response
        
        return output

#############################
# app.py #
#############################
import logging
from typing import List, Tuple, Union
import argparse

import gradio as gr
from utils.agents import TokenizersChatbot, DocGenAI

logging.basicConfig(level=logging.DEBUG)

input_placeholder = 'Enter something here'

welcome_message = 'Thank you for reaching out to Tokenizers! My name is Picky. I am an AI assistant who can help you create your dream app with ease. Can you tell me about your app' 
#chatbot = TokenizersChatbot()
chatbot = DocGenAI(platform='llama.cpp')

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

# Launch Gradio interface
block.launch(server_name=args.server_name, server_port=args.server_port)
