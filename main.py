from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
import base64
import json
import sys

from calorie_counter import get_calories_from_image

load_dotenv()


if __name__ == "__main__":
    image_path = sys.argv[1]
    calories = get_calories_from_image(image_path)
    print(json.dumps(calories, indent=4))