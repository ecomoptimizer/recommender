import sys
from pathlib import Path

# Get the current script's directory
script_dir = Path(__file__).resolve().parent

# Get the project's root directory by going up one level
project_root = script_dir.parent

# Add the project's root directory to sys.path
sys.path.append(str(project_root))

import streamlit as st
from langchain.llms import openai
from langchain.chat_models import chatopenai
from langchain.prompts import prompttemplate
from langchain.chains import llmchain
from langchain.output_parsers import pydanticoutputparser
from langchain.schema import humanmessage

from dotenv import dotenv_values

from prompts.prompt import get_prompt
from src.output import campaign
from src.utils import get_brand_tone_and_voice, format_json_to_multiline_string

# config = dotenv_values(".env")

# openai_api_key = config["openai_api_key"]

def generate_emails(inputs, api_key):
    try:
        tone_and_voice = get_brand_tone_and_voice(inputs.tone_and_voice.tone_and_voice_from_website, api_key)
        inputs.tone_and_voice.tone_and_voice_from_website = tone_and_voice
    except AttributeError:
        print("Error")

    string_inputs = format_json_to_multiline_string(inputs)

    with open("prompts/p2.prompt", "r") as f:
        template = f.read()

    parser = pydanticoutputparser(pydantic_object=campaign)

    prompt = prompttemplate(
        template=template,
        input_variables=["inputs"],
        partial_variables={"output_format": parser.get_format_instructions()}
    )

    if api_key == "openai":
        llm = openai(openai_api_key=api_key, max_tokens=3000, presence_penalty=1)
    elif api_key == "gemini-pro":
        llm = openai(openai_api_key=api_key, max_tokens=3000, presence_penalty=1)

    chat = chatopenai(openai_api_key=api_key, max_tokens=3000)

    formatted_input = prompt.format(inputs=string_inputs)
    # print("-"*30)
    # print("formatted input:")
    # print(formatted_input)
    # print("-"*30)

    response = llm(formatted_input)
    parsed_output = parser.parse(response)
    return parsed_output
