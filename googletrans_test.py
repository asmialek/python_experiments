from googletrans import Translator


jacek = Translator()
msg = 'w Londynie'
trans = jacek.translate(msg, 'en')
print(trans.text)
