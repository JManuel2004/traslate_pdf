import streamlit as st
import fitz  # PyMuPDF
from googletrans import Translator
from fpdf import FPDF
import tempfile
import os

def extraer_texto_pdf(ruta_pdf):
    texto = ""
    doc = fitz.open(ruta_pdf)
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()
    return texto

def traducir_texto(texto, src='en', dest='es'):
    traductor = Translator()
    return traductor.translate(texto, src=src, dest=dest).text

def guardar_pdf(texto, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linea in texto.split('\n'):
        pdf.multi_cell(0, 10, linea)
    pdf.output(output_path)

# Interfaz con Streamlit
st.title("📄 Traductor de PDF Inglés → Español")

archivo_pdf = st.file_uploader("Sube tu archivo PDF en inglés", type=["pdf"])

if archivo_pdf is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(archivo_pdf.read())
        ruta_temporal = temp_pdf.name

    if st.button("Traducir PDF"):
        with st.spinner("Procesando..."):
            texto = extraer_texto_pdf(ruta_temporal)
            texto_traducido = traducir_texto(texto)
            output_path = ruta_temporal.replace(".pdf", "_traducido.pdf")
            guardar_pdf(texto_traducido, output_path)
        
        with open(output_path, "rb") as file:
            st.success("¡Traducción completa!")
            st.download_button(
                "📥 Descargar PDF traducido",
                data=file,
                file_name="pdf_traducido.pdf",
                mime="application/pdf"
            )
        
        os.remove(output_path)
    os.remove(ruta_temporal)
