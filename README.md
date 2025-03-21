# Talk to an LLM in Slack (Slackbot template from WDAI)

A Slack bot that uses OpenAI's GPT-4o model to respond to messages, analyze images, process CSV data, and extract information from PDFs.  Originally created for the purposes of enabling more AI experiments in-channel for our Women Defining AI micro-learning program participants, this repo is a templatized version of our Slackbot implementation that is open so that others can build their own AI Slackbot

## 🚀 Getting Started (For Beginners)

If you're new to coding or GitHub, this section will help you get started:

1. **Fork this template**: Click the "Use this template" button at the top of this GitHub page to create your own copy of this repository.

2. **Get your API credentials**: 
   - Create a [Slack App](https://api.slack.com/apps) (Instructions in the "Create a Slack App" section below)
   - Get an [OpenAI API key](https://platform.openai.com/api-keys)

3. **Deploy your bot**: This template is set up for easy deployment on [Railway](https://railway.app/), a hosting platform that doesn't require technical expertise.

4. **Test and enjoy**: Once deployed, invite your bot to a Slack channel and start interacting with it!

Need more detailed instructions? Follow the step-by-step guides in the sections below.

## Features
This template relies on OpenAI APIs for LLM capabiltiies, but you can continue to expand on these capabilities by integrating other LLM and providers for various features.
- **AI-Powered Conversations**: Responds to messages using OpenAI's GPT-4o model
- **Conversation Memory**: Maintains context by tracking conversation history in threads
- **Multi-Modal Capabilities**:
  - **Image Analysis**: Describes and answers questions about images
  - **Image Generation**: Creates custom images using DALL-E 3 based on text prompts
  - **CSV Processing**: Analyzes tabular data shared in CSV format
  - **PDF Extraction**: Extracts and summarizes content from PDF documents
  - **Text File Handling**: Processes plain text files

## Setup and Deployment

### Prerequisites

- **Slack Workspace with Admin privileges**: You need admin access to a Slack workspace to create and install a bot. You can create a free Slack team for testing purposes if needed.
- **OpenAI API Key**: Create an account at [OpenAI](https://platform.openai.com/) and generate an API key
- **Railway account**: Sign up at [Railway](https://railway.app/) for deploying your bot (free tier available)
- **GitHub account**: Required to fork this template and connect with Railway

### Environment Variables

Environment variables are settings that need to be configured for your bot to work. You'll set these up in Railway during deployment:

- `SLACK_BOT_TOKEN`: Your Slack Bot User OAuth Token (you'll get this when creating your Slack App)
- `SLACK_SIGNING_SECRET`: Your Slack App Signing Secret (also provided when creating your Slack App)
- `OPENAI_API_KEY`: Your OpenAI API Key
- `MAX_THREAD_HISTORY` (optional): Maximum number of messages to retrieve from a thread (default: 10)
- `ALLOWED_CHANNEL` (optional): Channel ID where the bot is allowed to respond (if not set, bot works in all channels)
- `LOG_DIR` (optional): Directory where logs will be stored (default: `logs`)
- `LOG_LEVEL` (optional): Minimum log level to record (default: `INFO`)
- `RATE_LIMIT_ENABLED` (optional): Enable or disable rate limiting (default: `true`)
- `USER_RATE_LIMIT_WINDOW` (optional): Time window in seconds for user rate limiting (default: `60`)
- `USER_RATE_LIMIT_MAX` (optional): Maximum number of requests per user in the window (default: `10`)
- `TEAM_RATE_LIMIT_WINDOW` (optional): Time window in seconds for team rate limiting (default: `60`)
- `TEAM_RATE_LIMIT_MAX` (optional): Maximum number of requests per team in the window (default: `100`)

### ⚠️ Security Warning

**IMPORTANT**: Never commit your actual `.env` file or any file containing real API keys, tokens, or secrets to your repository. Only commit the `.env.example` file with placeholder values.

- **API Tokens**: If you accidentally expose your API tokens, immediately rotate them (create new ones and invalidate the old ones) in the respective dashboards.
- **Environment Variables**: Always use environment variables for sensitive information, especially in production.
- **Git Practices**: Make sure `.env` is included in your `.gitignore` file to prevent accidental commits.

### 🔒 Enhanced Security Features

#### PII Redaction in Logs

This bot includes an advanced logging system that automatically redacts personally identifiable information (PII) from log files, including:

- Email addresses
- IP addresses
- Phone numbers
- Social Security Numbers
- Credit card numbers
- API keys and tokens

This prevents sensitive information from being exposed in log files while still providing useful debugging information. All logs are stored in the `logs/bot_activity.log` file by default.

To configure logging behavior, you can set the following environment variables:
- `LOG_DIR`: Directory where logs will be stored (default: `logs`)
- `LOG_LEVEL`: Minimum log level to record (default: `INFO`)

#### Rate Limiting

The bot implements rate limiting to prevent abuse and ensure fair usage across users and teams. Rate limiting works on two levels:

- **User-level**: Limits how many requests each individual user can make in a time window
- **Team-level**: Limits the total requests across all users in a team/workspace

When a user exceeds their rate limit, they'll receive a polite message indicating when they can try again. This protects the bot from unintentional flooding and ensures a responsive experience for all users.

Rate limiting can be customized using these environment variables:
- `RATE_LIMIT_ENABLED`: Enable or disable rate limiting (default: `true`)
- `USER_RATE_LIMIT_WINDOW`: Time window in seconds for user rate limiting (default: `60`)
- `USER_RATE_LIMIT_MAX`: Maximum number of requests per user in the window (default: `10`)
- `TEAM_RATE_LIMIT_WINDOW`: Time window in seconds for team rate limiting (default: `60`)
- `TEAM_RATE_LIMIT_MAX`: Maximum number of requests per team in the window (default: `100`)

The bot also includes an automatic cleanup process to prevent memory growth from stored rate limit data.

### Installation

#### 1. **Create a Slack App**:
   - Go to [api.slack.com/apps](https://api.slack.com/apps) and click "Create New App"
   - Choose "From scratch" and give your app a name and select your workspace
   - In the left sidebar, under "Features", click on "OAuth & Permissions"
   - Scroll down to "Scopes" and add the following Bot Token Scopes:
     - `app_mentions:read` - For reading when your bot is mentioned
     - `channels:history` - For viewing messages in public channels where the bot is added
     - `chat:write` - For sending messages as the bot
     - `files:read` - For viewing files shared with the bot
     - `files:write` - For uploading generated images to Slack
   - Scroll up and click "Install to Workspace"
   - After installation, you'll see a "Bot User OAuth Token" - copy this for later (this is your `SLACK_BOT_TOKEN`)
   - In the left sidebar, go to "Basic Information" and scroll down to "App Credentials"
   - Copy the "Signing Secret" for later (this is your `SLACK_SIGNING_SECRET`)

#### 2. **Deploy the Bot**:
   - Use this repository as a template by clicking the "Use this template" button
   - Name your new repository and create it
   - Sign up or log in to [Railway](https://railway.app/)
   - From the Railway dashboard, click "New Project" and select "Deploy from GitHub repo"
   - Connect your GitHub account if prompted and select your repository
   - Click "Deploy Now"
   - Once the deployment is initiated, click on "Variables" in the left sidebar
   - Add the environment variables mentioned above, particularly:
     - `SLACK_BOT_TOKEN`: The Bot User OAuth Token you copied
     - `SLACK_SIGNING_SECRET`: The Signing Secret you copied
     - `OPENAI_API_KEY`: Your OpenAI API key

#### 3. **Configure Slack Event Subscriptions**:
   - After Railway deploys your bot, it will provide a URL (find it in the "Settings" tab)
   - Go back to your Slack App configuration
   - In the left sidebar, click on "Event Subscriptions" and toggle "Enable Events" to On
   - Enter your Request URL: `https://your-railway-app-url.railway.app/slack/events`
   - Under "Subscribe to bot events", click "Add Bot User Event" and add:
     - `message.channels`
     - `app_mention`
   - Click "Save Changes" at the bottom
   - In the left sidebar, click on "App Home" and check "Allow users to send Slash commands and messages from the messages tab"

## Deployment on Railway

### Setting Up Railway

1. Create a [Railway](https://railway.app/) account if you don't have one.
2. Create a new project from your GitHub repository.
3. Set up the required environment variables:
   - In the Railway dashboard, go to your project
   - Click on the "Variables" tab
   - Add all the environment variables from your `.env.example` file:
     - `SLACK_BOT_TOKEN`
     - `SLACK_SIGNING_SECRET`
     - `OPENAI_API_KEY`
     - `MAX_THREAD_HISTORY` (optional)
     - `ALLOWED_CHANNEL` (optional)
     - `LOG_DIR` (optional)
     - `LOG_LEVEL` (optional)
     - `RATE_LIMIT_ENABLED` (optional)
     - `USER_RATE_LIMIT_WINDOW` (optional)
     - `USER_RATE_LIMIT_MAX` (optional)
     - `TEAM_RATE_LIMIT_WINDOW` (optional)
     - `TEAM_RATE_LIMIT_MAX` (optional)
     - `PORT` (Railway will set this automatically, but you can override it)
4. Deploy your application:
   - Railway will automatically deploy your application when you push to your repository
   - You can also manually deploy from the Railway dashboard by clicking "Deploy" button

### Network Access Requirements

For certain features to work properly, your deployment environment needs:

- **File Storage**: For processing image generation results, the bot needs temporary file storage access.

If you're experiencing issues with these features, check your deployment platform's documentation about file system access.

### Slack Configuration for Deployed Bot

1. After deployment, Railway will provide you with a URL for your application
   - Find this under the "Settings" tab in your Railway project
   - Copy the URL (it will look like `https://your-app-name.railway.app`)
2. Copy this URL and go to your Slack App's settings at [api.slack.com/apps](https://api.slack.com/apps)
3. Select your app and then under "Event Subscriptions", enable events and set the Request URL to:
   ```
   https://your-railway-app-url.railway.app/slack/events
   ```
4. Save changes and verify the URL (Slack will check if your application is responding correctly)

### Testing Your Deployment

1. Invite your bot to a channel in your Slack workspace:
   - In Slack, go to the channel where you want to add the bot
   - Type `/invite @YourBotName`
2. Mention the bot with a message:
   - Type `@YourBotName Hello!` and send the message
3. If the bot doesn't respond, check Railway logs:
   - Go to your Railway dashboard
   - Click on your project
   - Click on "Logs" in the left sidebar
   - Look for any error messages that might explain the issue

## Usage

### Basic Interaction

Mention the bot with `@Bot Name` in any channel it's invited to, or send it a direct message.

### Image Analysis

Attach an image to your message to have the bot analyze it:
```
@Bot Name What's in this image?
[image attachment]
```

### Image Generation

Ask the bot to create images with DALL-E 3:
```
@Bot Name generate an image of a cat riding a bicycle
```
or
```
@Bot Name create a funny meme about programming
```

### CSV Analysis

Attach a CSV file to have the bot analyze the data:
```
@Bot Name analyze this data please
[CSV attachment]
```

### PDF Processing

Share a PDF document for content extraction and summarization:
```
@Bot Name extract the key points from this document
[PDF attachment]
```

### Thread Conversations

The bot maintains context in threads, so you can have a continuous conversation by replying in a thread.

## Development

### Technology Stack

- **FastAPI**: Web framework
- **Slack SDK**: For Slack API integration
- **OpenAI API**: For AI capabilities
- **DALL-E 3**: For image generation
- **Railway**: Deployment platform

### Local Development

If you want to run the bot on your local machine for testing or development:

1. Clone the repository to your computer:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:
   ```
   # Install uv if you don't have it yet
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies using uv
   uv pip install -e .
   ```

3. Set up environment variables:
   - Create a file named `.env` in the root directory
   - Copy the contents from `.env.example` into `.env`
   - Fill in your actual API keys and tokens

4. Run the application:
   ```
   uvicorn app:app --reload
   ```

5. To test with Slack, you'll need to expose your local server to the internet:
   - Install [ngrok](https://ngrok.com/) (a tool to create a tunnel to your local server)
   - Run ngrok: `ngrok http 8000`
   - Use the ngrok URL (looks like `https://something.ngrok.io`) in your Slack App's Event Subscriptions URL

### Automated Quality Checks

This project includes automatic code quality and security checks that run whenever new code is submitted. These checks:

- Ensure the code follows standard formatting rules
- Scan for potential security issues
- Verify all dependencies are safe to use

This means you can be confident that the bot maintains high quality and security standards without needing to run technical tests yourself. This is enabled using Github actions. See python-checks.yml for more details.

### Dependencies

Dependencies are managed using `pyproject.toml` and `uv.lock`. The project uses [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver. It requires Python 3.13+ and includes the following main packages:

```
fastapi
openai
pillow
pydantic
python-multipart
requests
slack-sdk
uvicorn
```

To add new dependencies, update the `pyproject.toml` file and run `uv pip install -e .` to regenerate the lock file.

## Troubleshooting

### Common Issues

1. **Bot doesn't respond in Slack**
   - Check if your bot is invited to the channel
   - Verify that your Railway application is running (check Railway dashboard)
   - Check the Railway logs for errors
   - Make sure your Event Subscriptions URL is verified in Slack

2. **Image generation or file processing doesn't work**
   - Check if you have proper API keys set up
   - Verify that the bot has the correct permissions in Slack

3. **Deployment fails on Railway**
   - Check that all required environment variables are set
   - Look at the deployment logs for specific error messages

### Getting Help

If you're experiencing issues not covered here:
- Check the Railway documentation: [docs.railway.app](https://docs.railway.app/)
- Visit the Slack API documentation: [api.slack.com](https://api.slack.com/)
- Check OpenAI's documentation: [platform.openai.com/docs](https://platform.openai.com/docs)

## Limitations

- The bot can process files up to 25MB (Slack file size limit)
- PDF analysis quality depends on the document's formatting and clarity
- CSV parsing works best with well-formatted data
- The bot may have slower response times when processing large files
- Image generation follows OpenAI's content policy and may reject certain prompts

## License

MIT