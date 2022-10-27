#import the libraries
from importlib.metadata import files
import uvicorn
from fastapi import FastAPI, File, UploadFile
import numpy as np
from pydub import AudioSegment
import whisper
import glob
from googletrans import Translator
from gtts import gTTS
from fastapi.staticfiles import StaticFiles
import os
#import speech_recognition as sr
from fastapi.responses import StreamingResponse
import shutil
#create the app object
app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload-file/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"file_name": uploaded_file.filename}
#update file structure
x = 'files'

@app.get("/audio")
async def audio_preprocess():
  print("\n=============================== AUDIO ANALYSIS IS GOING ON ==========================================\n")
  video_list = glob.glob(x+'/*.3gp')
  cleaned_mp4s = [files.replace("\\", "/") for files in video_list]
  print(cleaned_mp4s)
  filename =cleaned_mp4s[0]
  
  sr = 16000
  n_fft = 4096
  len_hop = n_fft / 4
  file_extension = '3gp'
  track = AudioSegment.from_file(filename, file_extension)
  audiofile_wave = filename.replace(file_extension, 'wav')
  file_handle = track.export(audiofile_wave, format='wav')
  print("\naudiofile_wave:",audiofile_wave)
  '''
  wav_list = glob.glob(x+'/*.wav')
  cleaned_auds = [files.replace("\\", "/") for files in wav_list]
  print(cleaned_auds)
  c_filename =cleaned_auds[0]
  Converted_audio_file = open(c_filename, mode="rb")
  '''
  ####Speech-to-Text Trasnlation
  tiny = whisper.load_model("medium") #loading the medium whisper model by Open-AI
  print("\n speech to text transcribing is ongoing...\n")
  result = tiny.transcribe(audiofile_wave)
  input_str = result["text"]
  print("\n")
  print("The Converted Text is: ")
  print("------------------------------")
  print(input_str)

  ####Text-to-Text Translation
  translator = Translator()
  result = translator.translate(input_str, src='en', dest='hi')
  print("\n")
  print("The Translated Hindi text is: ")
  print("---------------------------")
  print(result.text)
  #print(result.src)
  #print(result.dest)

  ####Text-to-Speech Translation
  print("\n")
  print("The converted text to speech translation is going on...\n")
  mytext = result.text
  language = 'hi'
  myobj = gTTS(text=mytext, lang=language, slow=False)
  # Saving the converted audio in a wav format
  save = myobj.save("files/converted_hindi_audio.mp3")
  mp3_list = glob.glob(x+'/*.mp3')
  cleaned_mp3s = [files.replace("\\", "/") for files in mp3_list]
  print(cleaned_mp3s)
  ch_filename =cleaned_mp3s[0]
  Converted_hindi_audio_file = open(ch_filename, mode="rb")
  print("\n=============================== AUDIO ANALYSING HAS FINISHED ==========================================\n")
  return StreamingResponse(Converted_hindi_audio_file , media_type="audio/mp3")
  #return input_str
#run the API with uvicorn
#it will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port = 8000)

