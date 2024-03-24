from google_speech import Speech
from openai import OpenAI
import speech_recognition as sr
import speech_recognition as sr
import sys

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

history = [
    {"role": "system", "content": "Just answer the question, and don't hesitate to reopen the conversation in a relevant way."}
]

lang="en"

# Read the text
def text_to_audio(text):
    speech = Speech(text, lang)
    sox_effects = ("speed", "1.1")
    speech.play(sox_effects)


def text_in_parentheses(text):
    start = text.find('(')
    end = text.find(')')
    return text[start + 1:end]


def listen_and_transcribe():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening in class ...")
            audio = recognizer.listen(source, timeout=2) # you can increase the speed by reducing timeout
            text = recognizer.recognize_google(audio, language="en-EN")
            print("You said :", text)
            if "stop" in text:
                sys.exit("🛑 Stop AI")
            return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        text = ""
        return text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        text = ""
        return text


def ai_to_speech(completion):
    short_content = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            short_content += chunk.choices[0].delta.content
            new_message["content"] += chunk.choices[0].delta.content

            # a way to increase the speed 
            if "." in chunk.choices[0].delta.content or "!" in chunk.choices[0].delta.content or "?" in chunk.choices[0].delta.content :
                text_to_audio(short_content)
                short_content = ""
    history.append(new_message)


text_to_audio("Hi there !")


while True:
    user_input = listen_and_transcribe()
    history.append({"role": "user", "content": user_input})

    new_message = {"role": "assistant", "content": ""}
    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.8,
        stream=True,
    )
    ai_to_speech(completion)
