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
    """Summarize a webpage using OpenAI's web search tool."""
    try:
        logger.info(f"Using OpenAI web search tool to summarize: {url}")
        
        # Use the web search tool to fetch and summarize content
        completion = openai_client.chat.completions.create(
            model="gpt-4o",  # Use a model that supports web search
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes web content accurately. Provide a comprehensive but concise summary of the webpage."},
                {"role": "user", "content": f"Please search for and summarize this webpage: {url}"}
            ],
            tools=[{"type": "web_search"}]  # Enable web search tool
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error using OpenAI web search: {e}")
        return f"I encountered an error when trying to summarize this webpage: {str(e)}"
