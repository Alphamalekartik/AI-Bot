# for text-to-speech
from gtts import gTTS
# for language model
import transformers
import os
import time
# for data
import os
import datetime
import numpy as np



# BOT
class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    # Removed the speech_to_text method

    @staticmethod
    def text_to_speech(text):
        print("BOT --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')
        time.sleep(int(50 * duration))
        os.remove("res.mp3")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')


# Running the AI
if __name__ == "__main__":
    ai = ChatBot(name="bot")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True

    while ex:
        text_input = input("You: ")  # Taking user input in text form
        ## wake up
        if ai.wake_up(text_input) is True:
            res = "Hey I am AI, what can I do for you?"
        ## action time
        elif "time" in text_input:
            res = ai.action_time()
        ## respond politely
        elif any(i in text_input for i in ["thank", "thanks"]):
            res = np.random.choice(
                ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "mention not"])
        elif any(i in text_input for i in ["exit", "close"]):
            res = np.random.choice(["Tata", "Have a good day", "Bye", "Goodbye", "Hope to meet soon", "peace out!"])
            ex = False
        ## conversation
        else:
            if text_input == "ERROR":
                res = "anything else I can help you out..!"
            else:
                chat = nlp(transformers.Conversation(text_input), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ") + 6:].strip()
        ai.text_to_speech(res)

    print("----- Closing down bot -----")
