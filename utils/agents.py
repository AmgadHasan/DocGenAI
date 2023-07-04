import utils.chains as chains	# has get_conversation_chain, get_srs_chain
import utils.api as api	# To authenticate and get models from API
from utils.templates import ROUTE_TEMPLATE


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
