import os
from google.cloud import aiplatform
from google.generativeai import generate_text

# Ensure the API key is set using the environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("API key for Google AI Platform not set. Please set the 'GOOGLE_API_KEY' environment variable.")

os.environ['GOOGLE_API_KEY'] = api_key  # Set the API key environment variable if not already set

def detect_mood_style(text_input, more_response=False):
    model_name = "models/text-bison-001"

    prompt = f"The user said: '{text_input}'. Please identify the user's mood, suggest a suitable music style, and provide song recommendations."
    if more_response:
        prompt += " Also, provide additional song recommendations for this mood."

    try:
        response = generate_text(
            model=model_name,
            prompt=prompt,
            max_output_tokens=250 if more_response else 150  # Increase token count for more responses
        )

        # Print the raw response for debugging
        print("Raw response:", response.result)

        # Extract text from the response
        response_text = response.result

        # Parse the response to get mood, style, context, and recommendations
        mood = extract_mood_from_response(response_text)
        style = extract_style_from_response(response_text, mood)
        context = extract_context_from_response(text_input)  # Context extraction added
        recommendations = extract_recommendations_from_response(response_text)

        # Debug: print the parsed results
        print(f"Detected Mood: {mood}")
        print(f"Preferred Style: {style}")
        print(f"Context: {context}")
        print(f"Recommendations: {recommendations}")

    except Exception as e:
        print(f"Error during text generation: {e}")
        mood, style, context, recommendations = "Unknown", "Unknown", "General", ["No recommendations found."]

    return mood, style, context, recommendations

def extract_mood_from_response(text):
    """Extracts the dominant mood from the API response."""
    text = text.lower()

    mood_map = {
        # Weather-related moods
        "Rainy": ["rain", "rainy", "drizzle", "downpour", "wet", "pouring", "stormy"],
        "Sunny": ["sunny", "bright", "clear skies", "sunshine", "warm", "sunny day"],
        "Cloudy": ["cloudy", "overcast", "gray skies", "gloomy", "dull", "misty"],
        "Stormy": ["stormy", "thunder", "lightning", "tempest", "howling wind", "turbulent"],
        "Snowy": ["snowy", "snowing", "blizzard", "white out", "icy", "frosty"],
        "Foggy": ["foggy", "misty", "hazy", "thick fog", "dense fog", "murky"],
        "Windy": ["windy", "blustery", "gusty", "breezy", "whistling wind"],
        "Glorious": ["glorious day", "beautiful day", "perfect weather", "wonderful day"],
        
        # Seasonal moods
        "Spring": ["spring", "blossoming", "flowers", "renewal", "fresh"],
        "Summer": ["summer", "hot", "beach day", "vacation", "holiday"],
        "Autumn": ["autumn", "fall", "leaves", "harvest", "crisp air"],
        "Winter": ["winter", "cold", "snowy", "chilly", "frosty"],
        
        # Environmental moods
        "Urban": ["city", "urban", "busy streets", "traffic", "hustle and bustle"],
        "Rural": ["rural", "countryside", "fields", "farmland", "quiet", "serene"],
        "Beach": ["beach", "ocean", "waves", "sand", "tropical"],
        "Mountainous": ["mountain", "hiking", "climbing", "high altitude", "breathtaking views"],
        
        # Time of day moods
        "Morning": ["morning", "sunrise", "early", "dawn", "first light"],
        "Afternoon": ["afternoon", "midday", "sun high", "bright day"],
        "Evening": ["evening", "sunset", "dusk", "twilight", "getting dark"],
        "Night": ["night", "midnight", "dark", "moonlit", "quiet night"],
        
        # Emotional moods
        "Happy": ["happy", "joyful", "excited", "ecstatic", "content", "delighted", "thrilled", "elated"],
        "Sad": ["sad", "down", "depressed", "upset", "crying", "heartbroken", "unhappy", "mournful", "melancholy"],
        "Angry": ["angry", "furious", "frustrated", "irritated", "annoyed", "outraged", "enraged"],
        "Relaxed": ["relaxed", "calm", "peaceful", "serene", "tranquil", "at ease", "chilled", "contented"],
        "Romantic": ["romantic", "love", "affectionate", "in love", "passionate", "infatuated", "tender"],
        "Anxious": ["anxious", "nervous", "stressed", "worried", "tense", "on edge", "jittery", "uneasy"],
        "Lonely": ["lonely", "isolated", "alone", "solitary", "forsaken", "abandoned", "forlorn"],
        "Bored": ["bored", "indifferent", "disinterested", "apathetic", "uninterested", "weary"],
        "Confident": ["confident", "self-assured", "secure", "positive", "bold", "assertive", "empowered"],
        "Scared": ["scared", "fearful", "terrified", "afraid", "panicked", "frightened", "alarmed"],
        
        # Additional nuanced moods
        "Very Sad": ["very sad", "extremely sad", "so sad", "deeply sad"],
        "Slightly Sad": ["slightly sad", "a little sad", "kind of sad"],
        "Very Happy": ["very happy", "extremely happy", "so happy", "thrilled"],
        "Slightly Happy": ["slightly happy", "a little happy", "kind of happy"],
        
        # Neutral or Uncertain moods
        "Neutral": ["neutral", "okay", "fine", "normal", "average", "so-so"]
    }

    for mood, keywords in mood_map.items():
        if any(keyword in text for keyword in keywords):
            return mood

    return "Neutral"

def extract_style_from_response(text, mood=None):
    """Extracts the preferred music style from the API response, considering the mood."""
    text = text.lower()

    # Map moods to likely music styles
    mood_style_map = {
        "Relaxed": ["ambient", "chillwave", "acoustic folk", "smooth jazz"],
        "Happy": ["dance-pop", "synth-pop", "ska", "funk"],
        "Sad": ["indie folk", "blues", "neo-soul"],
        "Energetic": ["electro", "punk rock", "trap", "techno"],
        "Contemplative": ["post-rock", "singer-songwriter", "modern classical"],
        "Romantic": ["smooth jazz", "latin jazz", "bossa nova", "r&b"],
        # Add more mood-style mappings here
    }

    # Use mood to guide style selection
    if mood and mood in mood_style_map:
        for style in mood_style_map[mood]:
            if style in text:
                return style.capitalize()

    # Fallback to checking all styles
    styles = [
        "pop", "rock", "synth-pop", "jazz", "classical", "hip hop", "country", 
        "electronic", "metal", "r&b", "blues", "reggae", "soul", "funk", "disco", 
        "punk", "alternative", "indie", "techno", "house", 
        "trance", "dubstep", "drum and bass", "ambient", "folk", 
        "gospel", "latin", "salsa", "cumbia", "k-pop", 
        "afrobeat", "world", "new age", "opera", "soundtrack"
    ]

    for style in styles:
        if style in text:
            return style.capitalize()

    return "Unknown"

def extract_recommendations_from_response(text):
    """Extracts song recommendations from the API response."""
    recommendations = []
    start_collecting = False

    for line in text.splitlines():
        # Check if the line indicates the start of song recommendations
        if "Song recommendations:" in line:
            start_collecting = True
            continue
        
        # Skip irrelevant lines (Mood, Music style, etc.)
        if not start_collecting or any(keyword in line.lower() for keyword in ["mood", "music style"]):
            continue
        
        # Add song recommendations only
        if start_collecting and line.strip() and not line.lower().startswith("song recommendations"):
            recommendations.append(line.strip().strip("*-").strip())
    
    return recommendations if recommendations else ["No recommendations found."]

def extract_context_from_response(text):
    """Extracts the situational context from the API response."""
    text = text.lower()

    if any(word in text for word in ["working out", "exercise", "gym", "running", "lifting weights"]):
        return "Working Out"
    elif any(word in text for word in ["studying", "reading", "learning", "concentrating"]):
        return "Studying"
    elif any(word in text for word in ["relaxing", "unwinding", "chilling", "lounging"]):
        return "Relaxing"
    else:
        return "General"
