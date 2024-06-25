import requests
import os


def system_prompt():
    prompt = """
You are an advanced AI model specialized in analyzing graphs and extracting hidden meanings and implications. Your task is to provide detailed insights and implications of the graph's data, focusing on the broader context and potential future impacts. Follow these guidelines:

1.Identify Key Data Points: Highlight the most critical data points or trends in the graph.
2.Explain Hidden Meanings: Provide interpretations of what these data points imply about underlying factors, societal trends, or potential future developments.
3.Contextual Analysis: Relate the graph’s data to broader contexts such as demographic trends, economic factors, or social implications.
4.Predictive Insights: Offer insights into what the data could mean for the future, considering possible changes and their impacts.

Example:
Key Data Points:
1.2020 graduation rate: 5%
2.2023 graduation rate: 5%
Hidden Meanings:
Stable graduation rates suggest that the number of schools matches the birth rate.
Predictive Insights:
If the birth rate increases, competition for school enrollment will rise, leading to more uneducated children if schools don't expand.
"""
    return prompt

def get_pengangguran():
    data = requests.get(f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/543/key/{os.getenv['BPS_API_KEY']}")
    text_result = data.text
    text_result = text_result.replace("null","None")
    json_file = eval(text_result)
    return json_file