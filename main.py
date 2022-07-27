from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import nltk
from summa import summarizer
import re
from punctuator import Punctuator
import random, string

app = Flask(__name__)
nltk.download('punkt')

def summarizeTranscript(link):
    link = str.replace(link, "https://", '')
    if "youtu.be" in link:
        video_id = link.split("youtu.be/")[1]
    else:
        link = str.replace(link, "www.youtube.com/watch?v=", '')
        video_id = link.split("&ab_channel=")[0]
    print("Summarizing...\n\n")
    script = YouTubeTranscriptApi.get_transcript(video_id, ['en', 'iw'])
    f_script = TextFormatter().format_transcript(script)
    fin_script = re.sub('\n', ' ', f_script) # replaces all new lines with spaces
    p = Punctuator('model.pcl')
    b = get_summary(p.punctuate(fin_script))
    print(b)
    return b

def get_summary(words):
    return summarizer.summarize(words)

@app.route('/', methods=['GET', 'POST'])
def base_page():
    if request.method == "POST":
        text_in = request.form.get("input")
        text_out = summarizeTranscript(text_in)
        return render_template('index.html',output = text_out)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(
        port = random.randint(2000,9000)
    )

