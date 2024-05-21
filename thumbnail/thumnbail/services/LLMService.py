import requests
from thumnbail.utils.generate_random_name import generate_random_name
from thumnbail.parser.PromptParser import prompt_parser, PromptParser
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")


class LLMService:
    def __init__(self):
        self.models = ["nerijs/pixelportraits192-XL-v1.0", "blink7630/caricature-xl",
                       "lora-library/B-LoRA-cartoon_line", "artificialguybr/TshirtDesignRedmond-V2"]
        self.negative_prompts = "blurry, out of focus, text, watermark, low quality, unrealistic anatomy, extra limbs, missing limbs, noise, deformed"

    def generate_image(self, message):
        API_TOKEN = "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"
        API_URL = "https://api-inference.huggingface.co/models/nerijs/pixelportraits192-XL-v1.0"
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

        prompt = self.__generate_prompt(message)[0]

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.ok:
                return response.content
            return None

        image_bytes = query({
            "inputs": prompt,
        })
        if not image_bytes:
            return "erro"
        name = generate_random_name()
        with open(f"{name}.png", "wb") as f:
            f.write(image_bytes)
        return name

    def __generate_prompt(self, message):
        model = GoogleGenerativeAI(
            model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        prompt = PromptTemplate(
            template="""You are an expert prompt engineer.
            I will give you a prompt which is intended for generating thumbnails or tshirt design. Give me an array of 4 prompt for feeding it into a stable diffusion image generation model.
            Give me in the output in the json format- prompts:[]
            If you do not know the value of an attribute asked to extract.return null for the attribute's value.
            input - {message}
            """,
            input_variables=["message"],
        )

        chain = prompt | model | prompt_parser
        ans: PromptParser = chain.invoke({"message": message})
        return ans.prompts if ans else []
