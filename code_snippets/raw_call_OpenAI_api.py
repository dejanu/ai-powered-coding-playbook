#!/usr/bin/env python3

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.5", # model selection : gpt-5.5 gpt-5.4 gpt-5.4-mini
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)