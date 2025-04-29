
import streamlit as st
import easyocr
import pandas as pd
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(page_title="Delivery Challan OCR", layout="centered")
st.title("📦 Delivery Challan to CSV Converter")

uploaded_file = st.file_uploader("Upload an image of the delivery challan", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        image.save(tmp_file.name)
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(tmp_file.name, detail=0)

    st.subheader("🧾 Extracted Text")
    st.write(result)

    df = pd.DataFrame(result, columns=["Extracted Text"])
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "challan_output.csv", "text/csv")
