from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List


class Introduction(BaseModel):
    """
    Model for the introduction section of a mobile app requirements document.
    """
    app_name: str = Field(description="The name of the mobile application that is being developed.")
    purpose: str = Field(description="The reason why the mobile application is being developed, including its goals and objectives.")
    scope: str = Field(description="The boundaries and limitations of the mobile application, including what it will and will not do.")
    target_user: str = Field(description="The intended user or audience for the mobile application, including their demographics and characteristics.")

class OverAllDescription(BaseModel):
    """
    Model for the overall description section of a mobile app requirements document.
    """
    product_perspective: str = Field(description="The point of view or context in which the mobile application will be used, including the needs and preferences of the users.")
    
    product_features: str = Field(description="A list of the key features or functions that the mobile application will provide, including their importance and priority.")
    
    user_characteristics: str = Field(description="A list of the characteristics or attributes of the intended user or audience of the mobile application, including their needs, preferences, and expectations.")

class SystemFeatures(BaseModel):
    """
    Model for the system features section of a mobile app requirements document.
    """
    system_features: str = Field(description="A list of the technical features or capabilities that the mobile application will require, including the hardware and software platforms, programming languages, and third-party tools.")

class FunctionalRequirements(BaseModel):
    """
    Model for the functional requirements section of a mobile app requirements document.
    """
    functional_requirements: str = Field(description="A list of the functional requirements or specifications that the mobile application must satisfy, including the features, functions, and performance requirements.")

