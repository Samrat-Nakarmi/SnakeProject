import speech_recognition as sr
import keyboard

def voice():
    r = sr.Recognizer()

    print("What do you want?")

    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''

        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)

        except sr.UnknownValueError:
            print("Sorry I didn't get that")

        except sr.RequestError:
            print("Sorry I'm dumb")

    return voice_data

# def respond(voice_data):
#     if 'up' in voice_data:
#         keyboard.press_and_release('up')
#     if 'down' in voice_data:
#         keyboard.press_and_release('down')
#     if 'left' in voice_data:
#         keyboard.press_and_release('left')
#     if 'right' in voice_data:
#         keyboard.press_and_release('space')

voice_data = voice()
# respond(voice_data)