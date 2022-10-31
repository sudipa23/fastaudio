#import the libraries
import uvicorn
from fastapi import FastAPI, File, UploadFile
import numpy as np
from pydub import AudioSegment
import whisper
import glob
from googletrans import Translator
from gtts import gTTS
from fastapi.staticfiles import StaticFiles
#import speech_recognition as sr
from fastapi.responses import StreamingResponse
import shutil
#create the app object
app = FastAPI()



#Index route,open automatically on http://127.0.0.1:8000
'''
video_list = glob.glob('*.3gp')
cleaned_mp4s = [files.replace("\\", "/") for files in video_list]
print(cleaned_mp4s)
filename =cleaned_mp4s[0]
'''

@app.post("/upload")
async def upload_audio(file: UploadFile):
  
  with open(f'{file.filename}',"wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  return {"file_name": file.filename}


@app.get("/audio")
async def audio_preprocess():
  video_list = glob.glob('*.3gp')
  cleaned_mp4s = [files.replace("\\", "/") for files in video_list]
  print(cleaned_mp4s)
  filename =cleaned_mp4s[0]
  
  #audio_file = open(filename, mode="rb")
  sr = 16000
  n_fft = 4096
  len_hop = n_fft / 4
  file_extension = '3gp'
  track = AudioSegment.from_file(filename, file_extension)
  audiofile_wave = filename.replace(file_extension, 'wav')
  file_handle = track.export(audiofile_wave, format='wav')
  print(audiofile_wave)
  wav_list = glob.glob('*.wav')
  cleaned_auds = [files.replace("\\", "/") for files in wav_list]
  print(cleaned_auds)
  c_filename =cleaned_auds[0]
  Converted_audio_file = open(c_filename, mode="rb")
  
  ####Speech-to-Text Trasnlation
  tiny = whisper.load_model("medium") #loading the medium whisper model by Open-AI
  result = tiny.transcribe(audiofile_wave)
  input_str = result["text"]
  print("The Converted Text ")
  print("------------------------------")
  print(input_str)

  ####Text-to-Text Translation
  translator = Translator()
  result = translator.translate(input_str, src='en', dest='hi')
  print("\n")
  print("The Translated Hindi text  ")
  print("---------------------------")
  print(result.text)
  #print(result.src)
  #print(result.dest)

  ####Text-to-Speech Translation
  mytext = result.text
  language = 'hi'
  myobj = gTTS(text=mytext, lang=language, slow=False)
  # Saving the converted audio in a wav format
  save = myobj.save("converted_hindi_audio.mp3")
  mp3_list = glob.glob('*.mp3')
  cleaned_mp3s = [files.replace("\\", "/") for files in mp3_list]
  print(cleaned_mp3s)
  ch_filename =cleaned_mp3s[0]
  Converted_hindi_audio_file = open(ch_filename, mode="rb")
  return StreamingResponse(Converted_hindi_audio_file , media_type="audio/mp3")
  #return input_str
#run the API with uvicorn
#it will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port = 8000)

 