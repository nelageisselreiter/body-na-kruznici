import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Body na kružnici", layout="wide")

st.title("🔵 Body na kružnici")

# --- VSTUPY ---
x0 = st.number_input("Souřadnice středu X [m]", value=0.0)
y0 = st.number_input("Souřadnice středu Y [m]", value=0.0)
r = st.number_input("Poloměr kružnice [m]", value=1.0, min_value=0.1)
n = st.slider("Počet bodů na kružnici", 1, 100, 8)
color = st.color_picker("Barva bodů", "#ff0000")

# --- VÝPOČET ---
angles = np.linspace(0, 2*np.pi, n, endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

# --- VYKRESLENÍ ---
fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.plot(x_points, y_points, "o", color=color)
circle = plt.Circle((x0, y0), r, fill=False, linestyle="--")
ax.add_patch(circle)
ax.axhline(0, color="black", linewidth=0.5)
ax.axvline(0, color="black", linewidth=0.5)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_title("Body na kružnici")
st.pyplot(fig)

# --- EXPORT DO PDF ---
st.subheader("📄 Export výsledku do PDF")

author = st.text_input("Vaše jméno", "Jan Novák")
contact = st.text_input("Kontakt (e-mail)", "jan.novak@email.cz")

if st.button("Vytvořit PDF"):
    # uložit graf do obrázku
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format="png")
    img_buf.seek(0)

    # vytvoření PDF
    pdf_buf = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Body na kružnici - Výstup", styles["Title"]))
    story.append(Spacer(1, 12))

    params = f"""
    <b>Parametry úlohy:</b><br/>
    Střed: ({x0}, {y0}) m<br/>
    Poloměr: {r} m<br/>
    Počet bodů: {n}<br/>
    Barva bodů: {color}<br/><br/>
    <b>Autor:</b> {author}<br/>
    <b>Kontakt:</b> {contact}
    """
    story.append(Paragraph(params, styles["Normal"]))
    story.append(Spacer(1, 24))

    # vložit graf do PDF
    img = Image(img_buf, width=400, height=400)
    story.append(img)

    doc.build(story)
    st.download_button(
        "📥 Stáhnout PDF",
        data=pdf_buf,
        file_name="body_na_kruznici.pdf",
        mime="application/pdf"
    )

# --- O APLIKACI ---
with st.expander("ℹ️ O aplikaci a použitých technologiích"):
    st.markdown("""
    **Autor:** Jan Novák  
    **Kontakt:** jan.novak@email.cz  

    Tato aplikace byla vytvořena v Pythonu pomocí:  
    - [Streamlit](https://streamlit.io) pro webové rozhraní  
    - [Matplotlib](https://matplotlib.org) pro grafy  
    - [ReportLab](https://www.reportlab.com) pro generování PDF  
    """)
