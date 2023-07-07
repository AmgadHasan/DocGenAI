import logging
import utils.chains as chains	# has get_conversation_chain, get_srs_chain
import utils.api as api	# To authenticate and get models from API
from utils.templates import ROUTE_TEMPLATE
import os
OUTPUT_DIR = 'generated_output'
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
            # IMPORTANT: Only use one model to save resources
            # This WizardCoder model is 4 bit quantized and requires 16 GB of RAM to run efficiently
            models_info = {'text_model': {'model_name':'WizardCoder-15B-1.0.ggmlv3.q4_0.bin'}}
            models = api.get_llamacpp_models(models_info)
        
        # Need to modify routing logic to use this
        #loaded_chains = {'introduction_chain': chains.get_introduction_chain(models['text_model']),
        #            'overall_description_chain': chains.get_overall_description_chain(models['text_model'])}
        loaded_chains = [chains.get_introduction_chain(models['text_model']), chains.get_overall_description_chain(models['text_model'])]
        return loaded_chains

    def generate(self, input_text):
        #logging.debug("chains:", self.chains)
        active_chain = self.chains[self.active_chain_index]
        output = active_chain.chain_run(input_text)
        logging.debug("output", output)
        
        if active_chain.condition:
            logging.debug('chain.condition')
            self.active_chain_index += 1
            if self.active_chain_index == len(self.chains):
                app_name = self.chains[0].parsed_text.app_name
                with open(f"{OUTPUT_DIR}/{app_name}.txt", "w") as file:
                    # Write output of chain 0 and then new line and then chain 1 to the file
                    file.write(self.chains[0].raw_text + "\n" + self.chains[1].raw_text)
                return "Finished"
            
            active_chain = self.chains[self.active_chain_index]
            logging.debug("In chain:", active_chain.section_name)
            output = self.initialize_chain(active_chain)
            logging.debug('init', output)
            
            return output
      	              
        if active_chain.use_custom_prompt:
            logging.debug('active_chain.use_custom_prompt')
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
        #logging.debug(response_type)
        if response_type == 'description': # If model has enough information about the app, generate srs.
            return True
        elif response_type == 'question':  # If model outputs questions about the app, route back to user.
            return False
        else:
            pass  # Maybe raise error?

    def generate(self, input):
        #response = self.conversation_chain.predict(input=input)
        output = self.conversation_chain.predict(input=input)
        
        if self.ready_to_generate_document(response):
            document = self.srs_chain.predict(app_description = output)
            response = output + '\n' + document
        else:
            response = output
        
        return response

