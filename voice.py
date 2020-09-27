from gtts import gTTS


class voice(object):
    def __init__(self):
        self.dir_path = "./voice/"

    def store_voice(self, paragraph_list, lang='en'):
        filename = 0
        for paragraph in paragraph_list:
            filename += 1
            tts = gTTS(text=paragraph, lang=lang)
            tts.save(self.dir_path + str(filename) + ".mp3")

        return filename
