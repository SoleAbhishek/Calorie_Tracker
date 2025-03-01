from groq import Groq
from dotenv import load_dotenv
import base64
import json
import sys
from flask import jsonify

load_dotenv()
api_key1 = "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"  
client = Groq(api_key=api_key1)

# from groq import Groq

def get_calories_from_image(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """You are a professional AI calorie detector. Identify food item is in this image? Identify the food's dimensions in volume and determine the number of calories in it. Use the following JSON format:

{
    "reasoning": "reasoning for the total calories",
    "food_items": [
        {
            "name": "food item name", (note: if there are multiple food items then display them by seperating with commas(,), this is very important)
            "calories": "calories in the food item"
        }
    ],
    "total": "total calories in the meal" (eg: if the answer is "150 calories" then the value in total should be only "150" not "150 calories")
}"""
                    },
                    {
                        "type": "text",
                        "text": "How many calories are in this meal?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            },
        ],
    )
    
    response_message = response.choices[0].message
    content = response_message.content

    return json.loads(content)  # Convert JSON string to dictionary

if __name__ == "__main__":
    image_path = sys.argv[1]
    calories = get_calories_from_image(image_path)

    # Ensure it prints correctly
    print(json.dumps(calories, indent=4))  # Print full JSON
    print(f"Total Calories: {calories.get('total', 'N/A')}")  # Print total calories safely



# api_key1="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"
# client = Groq(api_key=api_key1)
# def get_calories_from_image(image_path):
#     with open(image_path, "rb") as image:
#         base64_image = base64.b64encode(image.read()).decode("utf-8")

#     response = client.chat.completions.create(
#         model="llama-3.2-90b-vision-preview",
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You are a dietitian. A user sends you an image of a meal and you tell them how many calories are in it. Use the following JSON format:

# {
#     "reasoning": "reasoning for the total calories",
#     "food_items": [
#         {
#             "name": "food item name",
#             "calories": "calories in the food item"
#         }
#     ],
#     "total": "total calories in the meal"
# }"""
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": "How many calories is in this meal?"
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     }
#                 ]
#             },
#         ],
#     )

#     response_message = response.choices[0].message
#     content = response_message.content

#     return json.loads(content)
