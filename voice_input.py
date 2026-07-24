# Transcribes the voice
import os
import streamlit as st
from groq import Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
def transcribe_audio(audio_bytes):
    try:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes, "audio/wav"),
            model="whisper-large-v3-turbo",
            language="en",
            response_format="text")
        return transcription.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"
def map_to_never_rarely_often(text):
    text = text.lower().strip()
    never_score  = 0
    rarely_score = 0
    often_score  = 0
    never_keywords = ["never", "not at all", "doesn't", "does not",
        "not really", "hardly ever", "not once", "zero",
        "nothing", "nope", "nah"]
    rarely_keywords = ["rarely", "sometimes", "occasionally", "not much",
        "once in a while", "every now and then", "not often",
        "few times", "here and there", "not always",
        "but sometimes", "but yeah sometimes", "sometimes but",
        "every now and then", "not frequently"]
    often_keywords = ["often", "always", "frequently",
        "a lot", "most of the time", "usually",
        "constantly", "all the time", "regularly",
        "every time", "mostly", "definitely",
        "absolutely"]
    for word in never_keywords:
        if word in text:
            never_score += 2 if len(word.split()) > 1 else 1
    for word in rarely_keywords:
        if word in text:
            rarely_score += 2 if len(word.split()) > 1 else 1
    for word in often_keywords:
        if word in text:
            often_score += 2 if len(word.split()) > 1 else 1
    print(f"Scores → never:{never_score} rarely:{rarely_score} often:{often_score}")
    scores = {"never"  : never_score,"rarely" : rarely_score,"often"  : often_score}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None
    return best

def map_to_yes_no(text):
    text = text.lower().strip()
    yes_score = 0
    no_score  = 0
    yes_keywords = ["yes", "yep", "yup", "sure","absolutely", "definitely", "of course","we are", "we do", "i do", "we're", "iam"]
    no_keywords = ["no", "nope", "nah", "not really","we're not", "we don't", "we are not","aren't", "are not", "i don't", "negative","not friends", "don't follow", "doesn't follow","we aren't"]
    for word in yes_keywords:
        if word in text:
            yes_score += 2 if len(word.split()) > 1 else 1
    for word in no_keywords:
        if word in text:
            no_score += 2 if len(word.split()) > 1 else 1
    print(f"Yes/No scores → yes:{yes_score} no:{no_score}")
    if no_score > yes_score:
        return 0
    elif yes_score > no_score:
        return 1
    else:
        return None  
def map_to_slider(text, max_val=5):
    text = text.lower().strip()
    number_map = {"zero"  : 0, "none"  : 0, "nothing": 0,"one"   : 1, "two"   : 2, "three"  : 3,"four"  : 4, "five"  : 5,}
    for i in range(max_val + 1):
        if str(i) in text:
            return i
    for word, val in number_map.items():
        if word in text:
            return val
    if any(w in text for w in ["very high", "maximum", "a lot", "fully"]):
        return 5
    if any(w in text for w in ["high", "quite", "mostly"]):
        return 4
    if any(w in text for w in ["medium", "moderate", "average", "middle"]):
        return 3
    if any(w in text for w in ["low", "little", "slight"]):
        return 2
    if any(w in text for w in ["very low", "barely", "almost never"]):
        return 1
    if any(w in text for w in ["never", "zero", "none", "nothing"]):
        return 0
    return None 
def map_transcription_to_answer(transcription, dtype, rule, labels):
    if dtype == str:
        return map_to_never_rarely_often(transcription)
    elif dtype == int and rule == [0, 1]:
        return map_to_yes_no(transcription)
    elif dtype == int and labels:
        return map_to_slider(transcription, max_val=max(labels.keys()))
    elif dtype == int:
        return map_to_slider(transcription)
    return None