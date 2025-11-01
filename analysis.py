from transformers import pipeline
from PIL import Image

def analizar_imagen(image_path):
    """
    Analiza una imagen con modelos de Hugging Face:
    - Detecta objetos (personas, etc.)
    - Estima edad y género si aplica
    """

    # Detector de objetos (por ejemplo, personas)
    detector = pipeline("object-detection", model="facebook/detr-resnet-50")

    # Clasificador de edad (modelo de ejemplo)
    age_classifier = pipeline("image-classification", model="nateraw/vit-age-classifier")

    # Clasificador de género (modelo de ejemplo)
    gender_classifier = pipeline("image-classification", model="shubham-goel/age-gender-estimation")

    # Abrir imagen
    img = Image.open(image_path).convert("RGB")

    # Ejecutar detecciones
    detecciones = detector(img)

    # Comprobamos si hay persona
    hay_persona = any(d["label"].lower() == "person" for d in detecciones)

    edad = None
    genero = None

    if hay_persona:
        edad_pred = age_classifier(img)
        genero_pred = gender_classifier(img)

        if edad_pred:
            edad = edad_pred[0]["label"]
        if genero_pred:
            genero = genero_pred[0]["label"]

    resultado = {
        "hay_persona": hay_persona,
        "detecciones": detecciones,
        "edad_estimada": edad,
        "genero_estimado": genero
    }

    return resultado
