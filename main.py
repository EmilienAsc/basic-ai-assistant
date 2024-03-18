from google_speech import Speech
from openai import OpenAI
import speech_recognition as sr

lang = "en"

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

while True :
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("I listen")
            audio = recognizer.listen(source, timeout=3)
            text = recognizer.recognize_google(audio, language="en-EN") # Adapt to your language
            print("You said: ", text)
    except:
        print("erreur")
    completion = client.chat.completions.create(
    model="local-model", # this field is currently unused
    messages=[
        {"role": "system", "content": "Just answer the question, and don't hesitate to reopen the conversation in a relevant way."},
        {"role": "user", "content": text}
    ],
    temperature=0.7,
    )

    print(completion.choices[0].message.content)
    speech = Speech(completion.choices[0].message.content, lang)
    sox_effects = ("speed", "1.1")
    speech.play(sox_effects)
