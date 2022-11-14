import streamlit as st
import whisper
import pandas as pd
from audiorecorder import audiorecorder

def VoiceToText():
    quran=["اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ", "لا تَأْخُذُهُ سِنَةٌ وَلا نَومٌ","لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ",
           "مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ", "يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ",
           "وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ", "وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ",
           "وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِي"]
    qr_output=["الله لا إله إلا هو الحي القيوم", "لا تأخذه سنة ولا نوم", "له ما في السماوات وما في الأرض",
               "من ذا الذي يشفع عنده إلا بإذنه", "يعلم ما بين أيديهم وما خلفهم",
               "ولا يحيطون بشيء من علمه إلا بما شاء", "وسع كرسيه السماوات والأرض",
               "ولا يئوده حفظهما وهو العلي العظيم"]

    audiopath='myfile.mp3'
    model = whisper.load_model("medium")
    audio = whisper.load_audio(audiopath)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)
    #Transcription
    result = model.transcribe(audiopath)['text']
    re = set(result.split())
    ct = []
    for line in qr_output:
      line = set(line.split())
      ct.append(len(re & line))
    quran1=[]
    for i in ct:
      if i >= 3:
        quran1.append(quran[ct.index(i)])
    st.write(ct)
    #Translation of Arabic transcription to English
    options = dict(language='ar',beam_size=5,best_of=5)
    translate_options = dict(task="translate",**options)
    translation = model.transcribe(audiopath,**translate_options)['text']
    if lang == 'en':
        lang = 'English'
    elif lang == 'ar':
        lang = 'Arabic'
    lang = "The detected language is: "+lang
    st.write(lang)
    arabic = "Audio transcription: \n"+result
    st.write(arabic)
    eng = "Translation: \n"+translation
    st.write(eng)
    qr = "Quran lines: \n"+" ".join(quran1)
    st.write(qr)


def ServiceChoice():
    task = st.selectbox("Menu", ["Select Your choice", "Record your Voice", "Upload a audio file"])

    if task == "Select Your choice":
        st.write(" ")

    elif task == "Record your Voice":
        st.subheader("Record your voice")
        audio_bytes = audiorecorder("Click to record", "Recording...")
        if len(audio_bytes) > 0:
            st.audio(audio_bytes, format="audio/wav")
        with open('myfile.mp3', 'wb') as f:
            f.write(audio_bytes)
        if st.button('Submit'):
            VoiceToText()

    elif task == "Upload a audio file":
        st.subheader("Upload a file here")
        uploaded_file = st.file_uploader("Upload file", type=['.mp3'])
        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            with open('myfile.mp3', mode='bw') as f:
                f.write(audio_bytes)
        if st.button('Submit'):
            VoiceToText()

st.markdown(
         f"""
         <style>
         .stApp {{
             background-image:url("https://t4.ftcdn.net/jpg/03/46/02/03/360_F_346020347_7NZjfUbEdwP3N83wfzrHpufirqmLv20t.jpg");
             background-repeat: no-repeat; 
             background-size:1400px 1200px
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.header("Welcome to my App")
menu = ["Home", "Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")

elif choice == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.checkbox("Login"):
        table = pd.read_csv("login.csv")
        for ind in table.index:
            if table['uname'][ind] == username:
                if password == table['pass'][ind]:
                    st.sidebar.success("Login Successful")
                    ServiceChoice()
                else:
                    st.sidebar.warning("Try again")

if choice == "Sign Up":
    st.subheader("Create a new account")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    if st.button("Submit"):
        table = pd.read_csv("login.csv")
        table1 = pd.DataFrame({'uname': [username], 'pass': [password]})
        table = table.append(table1,ignore_index=True)
        table.to_csv("login.csv", index=False)
        st.success("Account created successfully")
