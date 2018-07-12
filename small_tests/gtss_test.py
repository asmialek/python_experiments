from gtts import gTTS

tts = gTTS('Cześć świecie', lang='pl')
tts.save('gtts_save.mp3')