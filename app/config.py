import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Optional environment variables with defaults
MAX_THREAD_HISTORY = int(os.environ.get("MAX_THREAD_HISTORY", "10"))
ALLOWED_CHANNEL = os.environ.get("ALLOWED_CHANNEL")

# Log configuration
logger.info(f"Bot configured to work only in channel: {ALLOWED_CHANNEL}")

# Constants for the application
DEFAULT_MODEL = "gpt-4o"  # This model supports web search capability
IMAGE_MODEL = "dall-e-3"
TTS_MODEL = "tts-1"
WHISPER_MODEL = "whisper-1"
TTS_VOICE = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
IMAGE_SIZE = "1024x1024"
IMAGE_QUALITY = "standard"
MAX_CACHE_SIZE = 100
CACHE_EXPIRY_SECONDS = 60
