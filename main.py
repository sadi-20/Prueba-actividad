import streamlit as st
from analysis import analizar_imagen
from firebase_admin import firestore, storage
import firebase_admin
from firebase_admin import credentials
import uuid

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred, {
        "storageBucket": "<TU_BUCKET>.appspot.com"
    })

db = firestore.client()
bucket = storage.bucket()

st.title("Detector de imágenes con Hugging Face + Firebase")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Guardar temporalmente
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    # Analizar con Hugging Face
    resultado = analizar_imagen("temp.jpg")
    st.json(resultado)

    # Subir imagen a Firebase Storage
    file_id = str(uuid.uuid4())
    blob = bucket.blob(f"imagenes/{file_id}.jpg")
    blob.upload_from_filename("temp.jpg")
    url = blob.public_url

    # Guardar datos en Firestore
    doc = {
        "id": file_id,
        "resultado": resultado,
        "imagen_url": url
    }
    db.collection("imagenes").document(file_id).set(doc)
    st.success("Guardado en Firebase")
    st.image(url, caption="Imagen subida")
