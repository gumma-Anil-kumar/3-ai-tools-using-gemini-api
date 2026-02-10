# GenAI Simple App

A Streamlit-based web application that leverages Google's Generative AI API to provide intelligent conversational features with multi-language support, speech recognition, and text-to-speech capabilities.

## Features

- **AI-Powered Chat**: Interact with Google's Generative AI model through a conversational interface
- **Multi-Language Support**: Support for 40+ languages including English, Telugu, Hindi, Spanish, French, German, and more
- **Speech Recognition**: Transcribe audio input using speech recognition technology
- **Text-to-Speech**: Convert AI responses to natural-sounding audio in multiple languages
- **Audio Processing**: Handle various audio formats with pydub
- **Model Discovery**: List and manage available AI models

## Requirements

- Python 3.7+
- Google Generative AI API key

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Google Generative AI API key:
```
GOOGLE_GENAI_API_KEY=your_api_key_here
```

## Dependencies

- **streamlit**: Web framework for the UI
- **python-dotenv**: Environment variable management
- **google-genai**: Google Generative AI API client
- **SpeechRecognition**: Speech-to-text conversion
- **pydub**: Audio processing
- **gTTS**: Google Text-to-Speech engine

## Usage

Run the application:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Features Overview

### 1. Chat Interface
- Type or speak your questions/prompts
- Get AI-generated responses in real-time
- Multi-turn conversation support

### 2. Language Selection
Supports the following languages and more:
- English, Telugu, Hindi, Spanish, French
- German, Portuguese, Russian, Italian, Dutch
- Bengali, Urdu, Arabic, Punjabi, Tamil
- Kannada, Malayalam, Marathi, Gujarati, Odia
- Nepali, Sinhala, Vietnamese, Thai, Indonesian
- Malay, Swahili, Polish, Czech, Romanian
- Hungarian, Greek, Turkish, Korean, Japanese

### 3. Audio Capabilities
- Record or upload audio for transcription
- Listen to AI responses with text-to-speech
- Automatic language detection for audio

### 4. Model Management
- View available AI models
- Select different models for different use cases

## Project Structure

```
genai_simple_app/
├── app.py                 # Main Streamlit application
├── list_models.py         # Utility to list available models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this file)
└── README.md             # This file
```

## API Configuration

The application uses Google's Generative AI API. Make sure to:
1. Generate an API key from Google AI Studio (https://aistudio.google.com)
2. Add it to your `.env` file as `GOOGLE_GENAI_API_KEY`

## Troubleshooting

### FFmpeg Warning
If you see a warning about ffmpeg/avconv, it's only needed for advanced audio processing. The app will still work for basic speech recognition and TTS.

To resolve: Install ffmpeg from https://ffmpeg.org/download.html

### API Key Issues
- Verify your API key is correctly set in the `.env` file
- Ensure the API key has proper permissions in Google Cloud Console

### Audio Issues
- Ensure your microphone has proper permissions
- For audio output, check your speaker volume and audio device settings

## Development

To list available models:
```bash
python list_models.py
```

## License

[Add your license here]

## Support

For issues or questions, please refer to:
- Streamlit Documentation: https://docs.streamlit.io
- Google Generative AI: https://ai.google.dev
- Speech Recognition Library: https://github.com/Uberi/speech_recognition
