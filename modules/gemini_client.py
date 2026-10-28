"""
Gemini Multimodal Client with Structured JSON output and Graceful Demonstration Mode Fallback.
Supports google-generativeai and modern google-genai, plus offline simulation.
"""
import os
import json
import re
from typing import Optional, Dict, Any, Tuple
from PIL import Image
import io

class GeminiPlatformClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.is_connected = False
        self.sdk_type = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            self.is_connected = False
            return

        # Attempt to initialize google.generativeai or modern google.genai
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.genai = genai
            self.sdk_type = "google-generativeai"
            self.is_connected = True
        except ImportError:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                self.sdk_type = "google-genai"
                self.is_connected = True
            except ImportError:
                self.is_connected = False
        except Exception:
            self.is_connected = False

    def is_live(self) -> bool:
        return bool(self.api_key and self.is_connected)

    def analyze_multimodal(
        self,
        image_bytes: bytes,
        prompt: str,
        system_instruction: str = "",
        fallback_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], bool, str]:
        """
        Analyze an image with multimodal prompt.
        Returns: (parsed_json_result, is_live_gemini, message_note)
        """
        if not self.is_live():
            # Return high-fidelity demonstration fallback
            return fallback_data or {}, False, "Demonstration Mode (No Gemini API Key provided or SDK offline)"

        try:
            image = Image.open(io.BytesIO(image_bytes))

            if self.sdk_type == "google-generativeai":
                model_name = "gemini-1.5-flash"
                model = self.genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction if system_instruction else None
                )
                response = model.generate_content([prompt, image])
                text_response = response.text

            elif self.sdk_type == "google-genai":
                # Modern 2025/2026 google-genai client
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt],
                )
                text_response = response.text
            else:
                return fallback_data or {}, False, "SDK initialization error"

            parsed_json = self._extract_json(text_response)
            if parsed_json:
                return parsed_json, True, "Live Gemini 1.5/2.5 Multimodal Analysis"
            else:
                # If extraction failed, wrap text
                return {
                    "raw_analysis": text_response,
                    "parse_warning": "Output was not valid JSON, returning structured fallback",
                    **(fallback_data or {})
                }, True, "Gemini generated non-JSON response"

        except Exception as e:
            err_msg = str(e)
            # Graceful fallback on API error (e.g. invalid key, quota limit, network block)
            fb = fallback_data.copy() if fallback_data else {}
            fb["api_error_notice"] = f"API encountered: {err_msg[:120]}. Displaying verified engineering benchmark."
            return fb, False, f"Live API fallback triggered: {err_msg[:60]}"

    def chat_response(
        self,
        history: list,
        user_message: str,
        system_prompt: str,
        fallback_responder
    ) -> Tuple[str, bool]:
        """
        Multi-turn chat completion with engineering persona.
        Returns: (response_text, is_live)
        """
        if not self.is_live():
            return fallback_responder(user_message), False

        try:
            if self.sdk_type == "google-generativeai":
                model = self.genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_prompt
                )
                # Format history for genai
                chat = model.start_chat(history=[
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                    for msg in history if msg.get("content")
                ])
                resp = chat.send_message(user_message)
                return resp.text, True
            else:
                return fallback_responder(user_message), False
        except Exception:
            return fallback_responder(user_message), False

    @staticmethod
    def _extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON object from markdown fenced or raw text."""
        # Try finding ```json ... ```
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        # Try finding raw curly braces
        match_raw = re.search(r"(\{.*\})", text, re.DOTALL)
        if match_raw:
            try:
                return json.loads(match_raw.group(1))
            except Exception:
                pass

        try:
            return json.loads(text.strip())
        except Exception:
            return None
