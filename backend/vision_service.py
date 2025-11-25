import os
import base64
from groq import Groq
from typing import Dict, Optional
import logging
logger = logging.getLogger(__name__)
class VisionService:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("Groq API key is required for vision capabilities.")
        self.client = Groq(api_key=api_key)
        self.vision_model = "llama-3.2-90b-text-preview"
    def analyze_image(
        self,
        image_data: str,
        user_prompt: str = None,
        analysis_type: str = "general"
    ) -> Dict:
        try:
            helpful_messages = {
            }
            message = helpful_messages.get(analysis_type, helpful_messages["general"])
            if user_prompt:
                message += f"\n\nYour question: {user_prompt}\n\nCould you provide more details so I can help better?"
            return {
                "success": True,
                "analysis": message,
                "analysis_type": analysis_type,
                "model": "fallback"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": "I encountered an error. Please try describing the image instead!"
            }
    def _get_analysis_prompt(self, analysis_type: str) -> str:
        prompts = {
        }
        return prompts.get(analysis_type, prompts["general"])
    def detect_image_type(self, user_message: str) -> str:
        message_lower = user_message.lower()
        if any(word in message_lower for word in ['code', 'program', 'script', 'function', 'syntax', 'debug']):
            return "code"
        if any(word in message_lower for word in ['diagram', 'flowchart', 'chart', 'graph', 'flow', 'architecture']):
            return "diagram"
        if any(word in message_lower for word in ['math', 'equation', 'formula', 'calculate', 'solve']):
            return "math"
        if any(word in message_lower for word in ['technical', 'system', 'network', 'infrastructure', 'design']):
            return "technical"
        if any(word in message_lower for word in ['document', 'text', 'read', 'extract', 'transcribe']):
            return "document"
        return "general"
    def analyze_with_context(
        self,
        image_data: str,
        user_message: str,
        conversation_history: list = None
    ) -> str:
        analysis_type = self.detect_image_type(user_message)
        result = self.analyze_image(
            image_data=image_data,
            user_prompt=user_message,
            analysis_type=analysis_type
        )
        if result["success"]:
            return result["analysis"]
        else:
            return result["analysis"]
    def compare_images(
        self,
        image1_data: str,
        image2_data: str,
        comparison_prompt: str = None
    ) -> str:
        return "Image comparison feature coming soon!"
def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def is_valid_image_format(filename: str) -> bool:
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)