class Token:

    def __init__(self):
        self.token = ''

    def get_token(self, name_file):
        """ Получаю TOKEN из файла token_app.txt """
        with open(name_file, "r", encoding="utf-8") as f:
            self.token = f.readline()
            return self.token


