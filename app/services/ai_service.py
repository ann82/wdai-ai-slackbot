import os
import time
from typing import List, Dict, Any, Optional

from app.config import (
    logger, DEFAULT_MODEL, IMAGE_MODEL, 
    IMAGE_SIZE, IMAGE_QUALITY, TTS_MODEL, TTS_VOICE, WHISPER_MODEL
)


def get_openai_response(openai_client, messages: List[Dict[str, Any]]) -> str:
    """Get a response from OpenAI with conversation history."""
    try:
        # Prepend system message
        full_messages = [{
            "role": "system", 
            "content": "You are a helpful assistant. If there are images in the conversation, describe what you see in them and answer any questions about them. If there is CSV, PDF, or tabular data, analyze it appropriately. Always provide concise, clear responses. For any creative requests like haikus, provide ONLY ONE response."
        }]
        
        # Add the other messages
        for msg in messages:
            full_messages.append(msg)
        
        # Log the messages being sent
        logger.info(f"Sending {len(full_messages)} messages to OpenAI")
        
        # Use specified model
        completion = openai_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=full_messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"


def generate_image(openai_client, prompt: str) -> Optional[str]:
    """Generate an image using DALL-E 3."""
    try:
        logger.info(f"Calling DALL-E API with prompt: {prompt}")
        response = openai_client.images.generate(
            model=IMAGE_MODEL,
            prompt=prompt,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            n=1,
        )
        image_url = response.data[0].url
        logger.info(f"Image generated successfully, URL: {image_url[:50]}...")
        return image_url
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None


def convert_text_to_speech(openai_client, text: str) -> Optional[str]:
    """Convert text to speech using OpenAI TTS."""
    try:
        response = openai_client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text
        )
        
        # Save to temporary file
        temp_file = f"/tmp/speech_{int(time.time())}.mp3"
        response.stream_to_file(temp_file)
        
        return temp_file
    except Exception as e:
        logger.error(f"Error converting text to speech: {e}")
        return None


def transcribe_audio(openai_client, audio_data: bytes, file_format: str) -> str:
    """Transcribe audio using OpenAI's Whisper model."""
    try:
        # Save audio data to temporary file
        temp_file = f"/tmp/audio_{int(time.time())}.{file_format}"
        with open(temp_file, "wb") as f:
            f.write(audio_data)
        
        # Transcribe audio
        with open(temp_file, "rb") as f:
            transcription = openai_client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=f
            )
        
        # Remove temporary file
        os.remove(temp_file)
        
        return transcription.text
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return f"Audio transcription failed: {str(e)}"


def summarize_webpage(openai_client, url: str) -> str:
    """Fetch and summarize a webpage."""
    try:
        import requests
        
        # Fetch the webpage content
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        
        # Create a summary request to OpenAI
        summary = openai_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes web content."},
                {"role": "user", "content": f"Summarize this webpage content in a concise way:\n\n{response.text[:50000]}"}
            ]
        )
        
        return summary.choices[0].message.content
    except Exception as e:
        logger.error(f"Error summarizing webpage: {e}")
        return f"Failed to summarize webpage: {str(e)}"
