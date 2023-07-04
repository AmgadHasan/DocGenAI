"""
This module provides two functions to generate ConversationChain and LLMChain objects for a conversation with a client and generating an SRS document respectively.

Functions:
- get_conversation_chain(chat_model): Returns a ConversationChain object for a conversation with a client to gather app details.
- get_srs_chain(instruct_model): Returns an LLMChain object for generating an SRS document based on the app details.

"""

from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from utils.templates import get_conversation_prompt, get_srs_prompt

def get_conversation_chain(chat_model):
    """
    Returns a ConversationChain object for a conversation with a client to gather app details.

    Args:
    chat_model (str): The language model to use for generating responses.

    Returns:
    ConversationChain: A ConversationChain object representing the conversation chain.
    """
    conversation_prompt = get_conversation_prompt()
    conversation_chain = ConversationChain(
        llm=chat_model,
        verbose=True,
        memory=ConversationBufferMemory(),
        prompt=conversation_prompt)
    return conversation_chain

def get_srs_chain(text_model):
    """
    Returns an LLMChain object for generating an SRS document based on the app details.

    Args:
    instruct_model (str): The language model to use for generating the SRS document.

    Returns:
    LLMChain: An LLMChain object representing the SRS chain.
    """
    srs_prompt = get_srs_prompt()
    srs_chain = LLMChain(llm=text_model, prompt=srs_prompt)
    return srs_chain

