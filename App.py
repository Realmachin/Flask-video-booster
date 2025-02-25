from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Free platforms to post videos
PLATFORMS = {
    "Reddit": "https://www.reddit.com/submit?url={url}",
    "Quora": "https://www.quora.com/submit?url={url}",
    "Medium": "https://medium.com/new-story",
    "LinkedIn": "https://www.linkedin.com/shareArticle?url={url}",
    "Twitter": "https://twitter.com/intent/tweet?url={url}",
    "Facebook Groups": "https://www.facebook.com/groups/",
    "Niche Forums": "https://www.google.com/search?q={keywords}+forum"
}

def extract_keywords(video_url):
    """Extracts video ID from the URL (for now, simulating keyword extraction)."""
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", video_url)
    if video_id_match:
        video_id = video_id_match.group(1)
        return f"video_{video_id} keywords"
    return "general keywords"

@app.route("/", methods=["GET", "POST"])
def index():
    suggestions = {}
    if request.method == "POST":
        video_url = request.form.get("video_url")
        keywords = extract_keywords(video_url)
        suggestions = {platform: url.format(url=video_url, keywords=keywords) for platform, url in PLATFORMS.items()}
    
    return """
    <html>
    <head>
        <title>Video Sharing Suggestion Tool</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            input { width: 60%; padding: 10px; margin: 10px; }
            button { padding: 10px 20px; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
        </style>
    </head>
    <body>
        <h2>Enter Your YouTube Video Link</h2>
        <form method="post">
            <input type="text" name="video_url" placeholder="Paste your YouTube link here..." required>
            <br>
            <button type="submit">Get Suggestions</button>
        </form>
        <h3>Suggested Platforms:</h3>
        <ul>
            """ + "".join(f'<li><a href="{link}" target="_blank">{platform}</a></li>' for platform, link in suggestions.items()) + """
        </ul>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
