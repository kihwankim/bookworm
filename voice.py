from gtts import gTTS


class voice(object):
    def __init__(self):
        self.dir_path = "./voice/"

    def store_voice(self, paragraph_list, lang='en'):
        filename = 0
        for paragraph in paragraph_list:
            data = ''
            for each_data in paragraph:
                if each_data == ' ':
                    if data == '':
                        continue
                    else:
                        data += each_data
                elif 'a' <= each_data <= 'z' or 'A' <= each_data <= 'Z' or '0' <= each_data <= '9':
                    data += each_data
            if data == '':
                continue
            filename += 1
            print(data)
            tts = gTTS(text=data)
            tts.save(self.dir_path + str(filename) + ".mp3")
            print("save all")

        return filename
