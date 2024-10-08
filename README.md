# Music Mood App

## Overview
Music Mood App is a web-based application developed for the [Gemini API Developer Competition](https://ai.google.dev/competition). The app detects the user's mood and suggests a suitable music style along with song recommendations. It leverages various Google services, including the Google Gemini API, for text generation and mood analysis.

## Features
- **Mood Detection**: Detects the user's mood based on text input.
- **Music Style Recommendation**: Suggests music styles suitable for the detected mood.
- **Song Recommendations**: Provides song recommendations based on the mood and music style.
- **Voice Interaction**: Users can interact with the app using voice commands.
- **Theme Selection**: Choose from multiple visual themes.

## Technologies Used
- **Google Gemini API**: For mood detection and generating text-based responses.
- **Google Cloud**: For integrating various AI and machine learning services.
- **Librosa**: For analyzing and modifying audio files.
- **Flask**: As the backend framework to handle requests and render HTML templates.

## Text-to-Speech Feature

The app includes a Text-to-Speech feature that allows users to listen to the recommended songs. This feature is implemented using the browser's built-in `SpeechSynthesis` API, which is part of the Web Speech API. The voices available for synthesis depend on the browser and operating system, and may include Google voices on certain platforms.

## Setup Instructions

### 1. Clone the Repository
   ```bash
   git clone https://github.com/aniketsoni1/music-mood-app.git
   cd music-mood-app
   ```

### 2\. Create a Virtual Environment 
```bash 
 `python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate`
```

### 3\. Install Dependencies
```bash 
 `pip install -r requirements.txt`
 ```

### 4\. Set Up Google API Keys 
* Ensure you have your Google API keys set up in your environment variables: 
```bash
`export GOOGLE_API_KEY='your-google-api-key'`
```

### 5\. Run the Application
```bash 
 `python app.py`
 ```

Screenshots
-----------
### Home Page
<img width="1510" alt="Screenshot 2024-08-12 at 1 30 36 PM" src="https://github.com/user-attachments/assets/b8451fa0-737a-421d-9029-64b19075b8ab">

### Response Page
<img width="1510" alt="Screenshot 2024-08-12 at 1 32 53 PM" src="https://github.com/user-attachments/assets/c9c69af6-ed43-492e-aa9b-11ba063bf85f">

