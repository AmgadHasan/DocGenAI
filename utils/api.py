import logging
import os
from typing import Optional, List, Dict
import google.auth
import vertexai
from langchain.llms import VertexAI, LlamaCpp
from langchain.chat_models import ChatVertexAI

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

