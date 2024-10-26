import anthropic
import os
from dotenv import load_dotenv
from scraper import search_articles
from extract_keywords import keywords

load_dotenv()

scholarly_articles = search_articles(keywords)

'''original_prompt = Here are some effective ways to help manage and alleviate flu symptoms:

1. **Rest:** Ensure you get plenty of sleep and rest to help your body recover.

2. **Stay Hydrated:** Drink plenty of fluids like water, herbal teas, and broths to stay hydrated and help thin mucus.

3. **Over-the-Counter Medications:** Use pain relievers (like acetaminophen or ibuprofen) to reduce fever and relieve body aches. Decongestants and antihistamines can help with nasal congestion.

4. **Warm Salt Water Gargle:** Gargling with warm salt water can soothe a sore throat.

5. **Steam Inhalation:** Inhaling steam from a hot shower or a bowl of hot water can help relieve congestion.

6. **Humidifier:** Using a humidifier in your room can add moisture to the air, helping ease breathing and congestion.

7. **Nutrition:** Eat light, nutritious meals. Foods rich in vitamins (like fruits and vegetables) can help support your immune system.

8. **Honey and Lemon:** Mixing honey and lemon in warm water can soothe a sore throat and help with cough.

9. **Avoid Irritants:** Stay away from smoke, strong odors, and other irritants that can worsen your symptoms.

10. **Consult a Doctor:** If symptoms are severe or persist, consult a healthcare professional. They may prescribe antiviral medications if appropriate.

Make sure to listen to your body and take care of yourself. If you have any underlying health conditions or concerns, it’s best to reach out to a healthcare provider.'''

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
                    "text": f"You are tasked with fact-checking an AI-generated response by finding relevant quotes from scholarly articles. Your goal is to provide a list of quotes that are directly related to the information in the original prompt. Follow these instructions carefully:\n\n1. First, you will be presented with the original prompt:\n<original_prompt>\n{original_prompt}\n</original_prompt>\n\n2. Next, you will be given a set of scholarly articles from PubMed:\n<scholarly_articles>\n{scholarly_articles}\n</scholarly_articles>\n\n3. Analyze the original prompt and identify the key claims, facts, or pieces of information that need to be fact-checked.\n\n4. Carefully read through the scholarly articles and look for quotes that directly relate to the key points identified in step 3. Focus on finding quotes that either support, contradict, or provide additional context to the information in the original prompt.\n\n5. For each relevant quote you find, format it as follows:\n<quote>\n\"[Exact quote from the article]\" - [Author(s) last name(s)], [Year of publication]\n</quote>\n\n6. When selecting quotes, prioritize the following:\n   a. Quotes that directly address claims made in the original prompt\n   b. Quotes from more recent publications, when available\n   c. Quotes from peer-reviewed sources, if that information is provided\n\n7. Avoid including quotes that are not directly relevant to the original prompt, even if they seem interesting or related to the general topic.\n\n8. If you find multiple quotes related to the same topic or claim, group them together under a relevant subheading.\n\n9. After compiling the list of quotes, provide a brief summary of your findings. Include this summary within <summary> tags.\n\n10. Present your final output in the following format:\n<fact_check>\n<quotes>\n[List of formatted quotes, grouped by topic if necessary]\n</quotes>\n<summary>\n[Brief summary of findings]\n</summary>\n</fact_check>\n\nRemember, your primary goal is to provide accurate and relevant quotes that can be used to fact-check the information in the original prompt. Be thorough in your search but selective in your choice of quotes."
                }
            ]
        }
    ]
)
print(message.content)