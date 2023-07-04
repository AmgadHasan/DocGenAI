"""
This module provides two functions to generate PromptTemplate objects for conversation and software requirements specification (SRS) documents.

Functions:
- get_conversation_prompt(): Returns a PromptTemplate object for a conversation with a client to gather app details.
- get_srs_prompt(): Returns a PromptTemplate object for generating an SRS document based on the app details.

"""

from langchain.prompts import PromptTemplate

CONVERSATION_TEMPLATE = """You are a friendly, client-respecting and helpful customer service working for Tokenizers, a software company that develops mobile apps for its clients. Your job is to generate an extremely detailed and specific description of the app the client wants to build which will be later used to generate a software requirements specification (SRS) docuemnt. You engage in a back-and-forth conversation with the client by asking them one and only one question at a time based on their previous replies if there are previous replies. You don't mention any of this at all unless asked about it directly. Make sure to ask them only one question! And keep the questions short, simple and goal oriented. Only ask them one question at a time! You will cut to the point and ask them the first question immediately.

Current conversation:
{history}
Human: {input}
AI:"""


SRS_TEMPLATE = """You are an experienced product manager that can generate a software requirements specification document (SRS) given a detailed description of the app. The document will be formated in markdown and will have bullet points.

Here's the app description:
{app_description}"""


ROUTE_TEMPLATE = """Does the agent have enough description of the app to generate a software requirements specification (SRS) document or they need to ask the user more questions? Respond with <description> for the former or <question> for the latter.

Response:
{}
"""

def get_conversation_prompt():
    """
    Returns a PromptTemplate object for a conversation with a client to gather app details.

    Returns:
    PromptTemplate: A PromptTemplate object representing the conversation prompt.
    """
    conversation_prompt = PromptTemplate(
        input_variables=['history', 'input'],
        template=CONVERSATION_TEMPLATE,
        template_format='f-string',
        validate_template=True,
        output_parser=None,
        partial_variables={},
    )
    return conversation_prompt

def get_srs_prompt():
    """
    Returns a PromptTemplate object for generating an SRS document based on the app details.

    Returns:
    PromptTemplate: A PromptTemplate object representing the SRS prompt.
    """
    srs_prompt = PromptTemplate(
        template=SRS_TEMPLATE,
        input_variables=["app_description"]
    )
    return srs_prompt
