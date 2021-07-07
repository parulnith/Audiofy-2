import os
import re
import shutil
import requests
import bs4
from gtts import gTTS
from pathlib import Path
from transformers import pipeline

import warnings

warnings.filterwarnings("ignore")


class MediumArticle:
    def __init__(self, article_URL):
        response = requests.get(article_URL)
        soup = bs4.BeautifulSoup(response.text, features="html.parser")
        paragraphs = soup.find_all(["li", "p", "strong", "em"])
        self.description = soup.find(["h1", "title"]).get_text()
        self.title = self.description.split("|")[0]
        self.author = self.description.split("|")[1]

        txt_list = []
        tag_list = []

        for p in paragraphs:
            if p.href:
                pass
            else:
                if len(p.get_text()) > 100:
                    tag_list.append(p.name)
                    txt_list.append(p.get_text())
                    self.text_file = "".join(txt_list).replace(".", ", ")

    def get_audio(self, accent, tld):
        text = self.text_file
        speech = gTTS(text=str(text), lang=accent, tld=tld)
        speech.save("audio.mp3")
        return str(Path("audio.mp3"))

    def get_summary(self):
        text = self.text_file
        summarizer = pipeline("summarization")
        summarized = summarizer(text[:2000], min_length=75, max_length=300)
        return summarized[0]["summary_text"]


languages_dict = {
    "English (Australia)": ["en", "com.au"],
    "English (United Kingdom)": ["en", "co.uk"],
    "English (United States)": ["en", "com"],
    "English (Canada)": ["en", "ca"],
    "English (India)": ["en", "co.in"],
    "English (Ireland)": ["en", "ie"],
    "English (South Africa)": ["en", "co.za"],
    "French (Canada)": ["fr", "ca"],
    "French (France)": ["fr", "fr"],
    "Mandarin (China Mainland)": ["zh-CN", "com"],
    "Mandarin (Taiwan)": ["zh-TW", "com"],
    "Portuguese (Brazil)": ["pt", "com.br"],
    "Portuguese (Portugal)": ["pt", "pt"],
    "Spanish (Mexico)": ["es", "com.mx"],
    "Spanish (Spain)": ["es", "es"],
}
