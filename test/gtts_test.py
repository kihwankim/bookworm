from gtts import gTTS


class voice(object):
    def __init__(self):
        self.dir_path = "./"

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


test_voice = voice()
test_text = ["""ing a home-business owner presents numerous challenges. Along 

uty 19 Be ometing the product or service, entrepreneurs also have to orgar

sattcut oo vartive aspects of the company. There are many products thal ¢

ra easiness owners streamfine their Projects. Oftentimes these products ar

be net sometimes unnecessary. A amast cine owner is continually tok

oe mine administrative costs and maximize profits, Here are three optis
‘rey prove useful
"""]

test_voice.store_voice(test_text)
