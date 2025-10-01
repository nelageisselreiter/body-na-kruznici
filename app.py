import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Body na kružnici", page_icon="🔵")

st.title("🔵 Body na kružnici")
st.write("Zadejte parametry a aplikace vykreslí body na kružnici.")

x_center = st.number_input("X souřadnice středu (m)", value=0.0)
y_center = st.number_input("Y souřadnice středu (m)", value=0.0)
radius = st.number_input("Poloměr kružnice (m)", value=5.0, min_value=0.1)
points = st.number_input("Počet bodů", value=6, min_value=1, step=1)
color = st.color_picker("Barva bodů", "#ff0000")

angles = np.linspace(0, 2 * np.pi, int(points), endpoint=False)
x_points = x_center + radius * np.cos(angles)
y_points = y_center + radius * np.sin(angles)

fig, ax = plt.subplots()
ax.scatter(x_points, y_points, c=color, label="Body")
circle = plt.Circle((x_center, y_center), radius, color="gray", fill=False)
ax.add_artist(circle)

ax.axhline(0, color="black", linewidth=0.5)
ax.axvline(0, color="black", linewidth=0.5)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_aspect("equal", adjustable="box")
ax.legend()

st.pyplot(fig)

if st.button("📄 Exportovat do PDF"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    text = c.beginText(50, 800)
    text.setFont("Helvetica", 12)
    text.textLine("Body na kružnici - parametry úlohy:")
    text.textLine(f"Střed: ({x_center}, {y_center}) m")
    text.textLine(f"Poloměr: {radius} m")
    text.textLine(f"Počet bodů: {points}")
    text.textLine(f"Barva: {color}")
    text.textLine("")
    text.textLine("Autor: Jan Novák")
    text.textLine("Kontakt: jan.novak@email.cz")
    c.drawText(text)
    c.showPage()
    c.save()
    st.download_button(
        label="⬇️ Stáhnout PDF",
        data=buffer.getvalue(),
        file_name="body_na_kruznici.pdf",
        mime="application/pdf",
    )

if st.checkbox("ℹ️ Informace o aplikaci"):
    st.info("Tato aplikace byla vytvořena v Pythonu pomocí knihoven Streamlit, NumPy, Matplotlib a ReportLab.")
