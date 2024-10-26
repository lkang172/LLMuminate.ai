import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

'''client = anthropic.Anthropic(
    api_key = os.getenv("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model = "claude-3-5-sonnet-20241022",
    max_tokens = 1000,
    temperature = 0,
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You will be given an AI-generated response. Your task is to extract relevant keywords from this response that can be used to search for scholarly articles and fact-check the information provided.\n\nHere is the AI-generated response:\n<ai_response>\n{ai_response}\n</ai_response>\n\nTo complete this task, follow these steps:\n\n1. Carefully read and analyze the AI-generated response.\n2. Identify the main claims, statements, or pieces of information that would benefit from fact-checking.\n3. For each identified claim or statement, select keywords that best represent the core concepts or ideas.\n4. Choose keywords that are specific enough to yield relevant search results but not so narrow that they might miss important scholarly articles.\n5. Avoid common words or phrases that are too general to be useful in a targeted search.\n6. Extract a few keywords or short phrases from the response.\n\nPresent your output in the following format:\n[First keyword or short phrase],[Second keyword or short phrase],[Third keyword or short phrase]... [Last keyword or short phrase]\n\n\nHere's an example of what your output might look like (don't include anything other than the keywords):\n\nClimate change impacts,Coral reef bleaching,Ocean acidification,Marine ecosystem disruption,Global warming and sea levels"
                }
            ]
        }
    ]
)

keywords = message.content'''