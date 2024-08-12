from flask import Flask, render_template, request, jsonify
import mood_style  # Import your mood detection module
import audio_analysis

app = Flask(__name__)

# Music database setup
music_db_path = "/Users/aniketsoni/Aniket/GeminiApi/music_mood_app/music_db/"
music_database = audio_analysis.analyze_music_database(music_db_path)  # Populate with audio features

# Example playlist model: A simple dictionary-based model for generating playlists
mood_to_playlist = {
    "happy": ["Song A", "Song B", "Song C"],
    "sad": ["Song D", "Song E", "Song F"],
    "calm": ["Song G", "Song H", "Song I"],
    "energetic": ["Song J", "Song K", "Song L"],
}

def generate_playlist(mood):
    return mood_to_playlist.get(mood, ["Default Song 1", "Default Song 2"])

# Example sentiment analysis function
def analyze_sentiment(text_input):
    # Placeholder for actual sentiment analysis logic
    if "happy" in text_input:
        return "positive"
    elif "sad" in text_input:
        return "negative"
    else:
        return "neutral"

@app.route("/", methods=["GET", "POST"])
def index():
    print("Index route accessed")
    mood = None
    style = None
    context = None
    recommendations = None
    text_input = None

    if request.method == "POST":
        try:
            text_input = request.form["text_input"]
            more_response = request.form.get("more_response") == "true"  # Check if the "More" button was pressed
            print(f"Received input: {text_input}, More Response: {more_response}")
            mood, style, context, recommendations = mood_style.detect_mood_style(text_input, more_response=more_response)
            print(f"Detected mood: {mood}, style: {style}, context: {context}")
            print(f"Recommendations: {recommendations}")
        except Exception as e:
            print(f"Error: {e}")

    return render_template("index.html", mood=mood, style=style, context=context, recommendations=recommendations, text_input=text_input)

@app.route('/generate_playlist', methods=['POST'])
def generate_playlist_route():
    mood = request.json.get('mood')
    playlist = generate_playlist(mood)  # Generate playlist based on mood
    return jsonify({"playlist": playlist})

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_route():
    text_input = request.json.get('text_input')
    sentiment = analyze_sentiment(text_input)  # Analyze the sentiment of the input
    return jsonify({"sentiment": sentiment})

@app.errorhandler(404)
def page_not_found(e):
    # Custom 404 page
    return render_template('404.html'), 404

if __name__ == "__main__":
    print("Starting main Flask app...")
    app.run(debug=True)
