from googletrans import Translator


class translator(object):
    def __init__(self):
        self.translator = Translator()

    def translate(self, paragraph_list, mode='ko'):
        """
        translate en to ko or ko to en
        :param paragraph_list: list of string
        :param mode: ko or en
        :return:
        """
        translated_string = self.translator.translate(paragraph_list, dest=mode)
        for item in translated_string:
            print(item.origin, '->', item.text)
        return translated_string


if __name__ == '__main__':
    trans = translator()
    strings_en = ['I like a book', 'You look very familiar', "I'm afraid I've got to go now"]
    strings_ko = ['나는 가짜 나사이 보는 중 입니다.', '나는 앞으로의 미래가 기대된다.', '내일은 학교 가는 날이다.']
    trans.translate(strings_ko, 'en')
