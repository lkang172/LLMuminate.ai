import anthropic
import os
from dotenv import load_dotenv
from Backend.scraper import search_articles

def extract_q(keywords, original_prompt):
    load_dotenv()

    scholarly_articles, sources = search_articles(keywords)

    client = anthropic.Anthropic(
        api_key = os.getenv("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You are tasked with fact-checking an AI-generated response by finding relevant quotes from scholarly articles. Your goal is to provide a list of quotes that are directly related to the information in the original prompt. Follow these instructions carefully:\n\n1. First, you will be presented with the original prompt:\n{original_prompt}\n\n2. Next, you will be given a set of scholarly articles from WebMD:\n{scholarly_articles}\n\n3. Analyze the original prompt and identify the key claims, facts, or pieces of information that need to be fact-checked.\n\n4. Carefully read through the scholarly articles and look for quotes that directly relate to the key points identified in step 3. Focus on finding quotes that either support, contradict, or provide additional context to the information in the original prompt.\n\n5. For each relevant quote you find, format it as follows:\n\"[Exact quote from the article]\" - [Author(s) last name(s)], [Year of publication]\n\n6. When selecting quotes, prioritize the following:\n   a. Quotes that directly address claims made in the original prompt\n   b. Quotes from more recent publications, when available\n   c. Quotes from peer-reviewed sources, if that information is provided\n\n7. Avoid including quotes that are not directly relevant to the original prompt, even if they seem interesting or related to the general topic.\n\n8. If you find multiple quotes related to the same topic or claim, group them together under a relevant subheading.\n\n9. After compiling the list of quotes, provide a brief summary of your findings.\nAfter all of the above, cite/output all of the sources: {sources}.\n\n10. Present your final output in the following JSON format (don't include anything else):\n{{\n  \"fact_checks\": [\n    {{\n      \"llm_claim\": \"Exact quote of claim from the AI response\",\n      \"check\": \"Your analysis or fact-checking summary of the claim\",\n      \"backup\": {{\n        \"quote\": \"Exact quote from the article that supports or contradicts the claim - Author(s) last name(s), Year of publication\",\n        \"link\": \"Link to the corresponding article or source\"\n      }}\n    }},\n    {{\n      \"llm_claim\": \"Another exact quote of key claim from the AI response\",\n      \"check\": \"Your analysis or fact-checking summary of the claim\",\n      \"backup\": {{\n        \"quote\": \"Exact quote from the article that supports or contradicts the claim - Author(s) last name(s), Year of publication\",\n        \"link\": \"Link to the corresponding article or source\"\n      }}\n    }}\n  ],\n  \"similarity_assessment\": {{\n    \"reasoning\": \"Your detailed reasoning for the similarity assessment between the AI response and scholarly articles.\",\n    \"similarity_score\": 85,  // Example similarity score\n  }}\n}}\n\nRemember, your primary goal is to provide accurate and relevant quotes that can be used to fact-check the information in the original prompt. Be thorough in your search but selective in your choice of quotes."
                    }
                ]
            }
        ]
    )

    return message.content[0].text


'''"text": f"You are tasked with fact-checking an AI-generated response by finding relevant quotes from scholarly articles. Your goal is to provide a list of quotes that are directly related to the information in the original prompt. Follow these instructions carefully:\n\n1. First, you will be presented with the original prompt:\n<original_prompt>\n{original_prompt}\n</original_prompt>\n\n2. Next, you will be given a set of scholarly articles from PubMed:\n<scholarly_articles>\n{scholarly_articles}\n</scholarly_articles>\n\n3. Analyze the original prompt and identify the key claims, facts, or pieces of information that need to be fact-checked.\n\n4. Carefully read through the scholarly articles and look for quotes that directly relate to the key points identified in step 3. Focus on finding quotes that either support, contradict, or provide additional context to the information in the original prompt.\n\n5. For each relevant quote you find, format it as follows:\n<quote>\n\"[Exact quote from the article]\" - [Author(s) last name(s)], [Year of publication]\n</quote>\n\n6. When selecting quotes, prioritize the following:\n   a. Quotes that directly address claims made in the original prompt\n   b. Quotes from more recent publications, when available\n   c. Quotes from peer-reviewed sources, if that information is provided\n\n7. Avoid including quotes that are not directly relevant to the original prompt, even if they seem interesting or related to the general topic.\n\n8. If you find multiple quotes related to the same topic or claim, group them together under a relevant subheading.\n\n9. After compiling the list of quotes, provide a brief summary of your findings. Include this summary within <summary> tags.\n\n10. Present your final output in the following format:\n<fact_check>\n<quotes>\n[List of formatted quotes, grouped by topic if necessary]\n</quotes>\n<summary>\n[Brief summary of findings]\n</summary>\n</fact_check>\nAfter all of the above, cite/output all of the sources: {sources}.\n\nRemember, your primary goal is to provide accurate and relevant quotes that can be used to fact-check the information in the original prompt. Be thorough in your search but selective in your choice of quotes."'''