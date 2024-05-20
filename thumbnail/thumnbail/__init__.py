from flask import Flask
from .db import create_db
from .services.LLMService import LLMService
import random
def create_app():
    create_db()
    app = Flask(__name__)
    @app.get("/")
    def home():
        message = random.choices([
            "youtube video content creator",
            "how to make 2lakh per month",
            "dbms educator"
        ])
        service = LLMService()
        prompts = service.generate_prompt(message)
        return {"status":prompts}
    return app