#import the libraries
import uvicorn
from fastapi import FastAPI, File, UploadFile
import numpy as np
from pydub import AudioSegment
import glob
from googletrans import Translator
from gtts import gTTS
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from fastapi.responses import StreamingResponse
import shutil
from fastapi.middleware.cors import CORSMiddleware

#create the app object
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#Index route,open automatically on http://127.0.0.1:8000
'''
video_list = glob.glob('*.3gp')
cleaned_mp4s = [files.replace("\\", "/") for files in video_list]
print(cleaned_mp4s)
filename =cleaned_mp4s[0]
'''

@app.post("/upload")
async def upload_audio(file: UploadFile):
  print("\n======================== Upload the Audio File=============================\n")
  with open(f'{file.filename}',"wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  print("\n======================== Audio File has Uploaded=============================\n")
  print("the audio file name is : ",file.filename)
  return {"file_name": file.filename}


@app.get("/audio")
async def audio_preprocess():
  print("\n======================== Audio Analysis has startred=============================\n")
  video_list = glob.glob('*.3gp')
  cleaned_mp4s = [files.replace("\\", "/") for files in video_list]
  print("cleaned_mp4s:",cleaned_mp4s)
  filename =cleaned_mp4s[0]
  
  file_extension = '3gp'
  print("\n======================== 1. Converting the Audio to WAV format=============================\n")
  track = AudioSegment.from_file(filename, file_extension)
  audiofile_wave = filename.replace(file_extension, 'wav')
  file_handle = track.export(audiofile_wave, format='wav')
  print("audiofile_wave:", audiofile_wave)
  wav_list = glob.glob('*.wav')
  cleaned_auds = [files.replace("\\", "/") for files in wav_list]
  print("cleaned_auds:",cleaned_auds)
  c_filename =cleaned_auds[0]
  Converted_audio_file = open(c_filename, mode="rb")
  
  ####Speech-to-Text Trasnlation
  print("\n======================== 2. Converting Speech to Text=============================\n")
  recognizer = sr.Recognizer()
  aud_file = sr.AudioFile(Converted_audio_file )
  with aud_file as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.50)
    audio = recognizer.record(source)
    input_str = recognizer.recognize_google(audio)
  print(input_str)
  '''
  tiny = whisper.load_model("medium") #loading the medium whisper model by Open-AI
  result = tiny.transcribe(audiofile_wave)
  input_str = result["text"]
  print("The Converted Text ")
  print("------------------------------")
  print(input_str)
  '''
  ####Text-to-Text Translation
  print("\n======================== 3. Initiating Text To Text Translation =============================\n")
  translator = Translator()
  result = translator.translate(input_str, src='en', dest='hi')
  print("\n")
  print("The Translated Hindi text  ")
  print("---------------------------")
  print(result.text)
  #print(result.src)
  #print(result.dest)

  ####Text-to-Speech Translation
  print("\n======================== 4. converting Text To Speech Translation =============================\n")
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
  
#run the API with uvicorn
#it will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port = 8000)

 