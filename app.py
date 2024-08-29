import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import base64

# Función para convertir imagen a base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Función para generar el PDF y guardarlo en un archivo temporal
def generar_pdf(tabla_gramatica, tabla_vocabulario, tabla_cct, file_path, logo_path):
    pdf = FPDF()
    pdf.add_page()

    # Añadir el logo en la parte superior
    pdf.image(logo_path, x=10, y=8, w=40)  # Ajusta x, y y w según sea necesario
    
    # Título principal
    pdf.set_font("Arial", size=12)
    pdf.set_y(30)  # Ajustar la posición del título para que no se sobreponga al logo
    pdf.cell(200, 10, txt="Resultados por zona - INEIIY 2024", ln=True, align="C")
    pdf.ln(10)

    # Añadir tablas de frecuencias con porcentaje
    pdf.set_font("Arial", size=10)
    
    pdf.cell(100, 10, txt="Tabla de Frecuencias: Gramática", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="Nivel", border=1)
    pdf.cell(40, 10, txt="Estudiantes", border=1)
    pdf.cell(40, 10, txt="Porcentaje", border=1)
    pdf.ln()
    for i in range(len(tabla_gramatica)):
        pdf.cell(80, 10, txt=f"{tabla_gramatica.iloc[i]['Nivel']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_gramatica.iloc[i]['Estudiantes']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_gramatica.iloc[i]['Porcentaje']}", border=1)
        pdf.ln()
    pdf.ln(10)

    pdf.cell(100, 10, txt="Tabla de Frecuencias: Vocabulario", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="Nivel", border=1)
    pdf.cell(40, 10, txt="Estudiantes", border=1)
    pdf.cell(40, 10, txt="Porcentaje", border=1)
    pdf.ln()
    for i in range(len(tabla_vocabulario)):
        pdf.cell(80, 10, txt=f"{tabla_vocabulario.iloc[i]['Nivel']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_vocabulario.iloc[i]['Estudiantes']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_vocabulario.iloc[i]['Porcentaje']}", border=1)
        pdf.ln()
    
    pdf.ln(10)
    
    # Tabla de CCT
    pdf.cell(100, 10, txt="Frecuencia por CCT", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="CCT", border=1)
    pdf.cell(40, 10, txt="Frecuencia", border=1)
    pdf.ln()
    for i in range(len(tabla_cct)):
        pdf.cell(80, 10, txt=f"{tabla_cct.iloc[i]['CCT']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_cct.iloc[i]['Frecuencia']}", border=1)
        pdf.ln()
    
    # Añadir la leyenda al final de la página
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 10, txt="La información proporcionada en esta página es suministrada por el Centro de Evaluación Educativa del Estado de Yucatán con fines exclusivamente informativos", align='C')

    # Guardar el PDF en un archivo temporal
    pdf.output(file_path)

# Cargar datos desde la ruta especificada
df = pd.read_csv('Resultados.csv')

# Configuración de la página
st.set_page_config(page_title="Resultados por zona - INEIIY 2024", layout="wide")

# Convertir la imagen del logo a base64 (opcional)
logo_path = "logo.png"

# Mostrar el logo arriba del título en la parte superior de la página
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="data:image/png;base64,{image_to_base64(logo_path)}" width="235" height="56" style="margin-bottom: 10px;">
        <h1>Resultados por zona - INEIIY 2024</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Filtro por Zona
zona_options = sorted(df['Zona'].unique())  # Obtener opciones únicas de Zona y ordenarlas de menor a mayor
zona_selected = st.selectbox("Selecciona la Zona:", zona_options)

# Filtrar DataFrame según el valor de Zona seleccionado
df_filtered = df[df['Zona'] == zona_selected]

if not df_filtered.empty:
    # Filtrar valores no nulos para gráficos
    df_gramatica = df_filtered[df_filtered['Gramática'].notna()]
    df_vocabulario = df_filtered[df_filtered['Vocabulario'].notna()]

    # Contar la frecuencia de estudiantes
    freq_gramatica = df_gramatica['Gramática'].count()
    freq_vocabulario = df_vocabulario['Vocabulario'].count()

    # Lista de categorías en orden deseado
    categorias_ordenadas = ['Pre A1', 'A1', 'A2', 'Superior a A2']

    # Definir colores gradientes para los gráficos de sectores
    colores_gramatica = {
        'Pre A1': '#a2c9a0',  # Verde más claro
        'A1': '#7aab7e',
        'A2': '#4a8d54',
        'Superior a A2': '#2d5b30'  # Verde más oscuro
    }

    colores_vocabulario = {
        'Pre A1': '#f9f3a6',  # Amarillo más claro
        'A1': '#f3e46b',
        'A2': '#f1d236',
        'Superior a A2': '#f0b30f'  # Amarillo más oscuro
    }

    # Gráfico de sectores para Gramática con gradiente verde militar
    fig_gramatica = px.pie(df_gramatica, names='Gramática', 
                           category_orders={'Gramática': categorias_ordenadas},
                           color='Gramática',
                           color_discrete_map=colores_gramatica)
    fig_gramatica.update_layout(
        title={
            'text': f"Gramática<br><span style='font-size:12px'>Frecuencia: {freq_gramatica} estudiantes",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=120)
    )

    # Gráfico de sectores para Vocabulario con gradiente amarillo mostaza
    fig_vocabulario = px.pie(df_vocabulario, names='Vocabulario', 
                             category_orders={'Vocabulario': categorias_ordenadas},
                             color='Vocabulario',
                             color_discrete_map=colores_vocabulario)
    fig_vocabulario.update_layout(
        title={
            'text': f"Vocabulario<br><span style='font-size:12px'>Frecuencia: {freq_vocabulario} estudiantes",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=120)
    )

    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)

    # Mostrar gráfico de Gramática y Vocabulario
    with col1:
        st.plotly_chart(fig_gramatica, use_container_width=True)

    with col2:
        st.plotly_chart(fig_vocabulario, use_container_width=True)

    # Contar la frecuencia y calcular el porcentaje de cada nivel para Gramática y Vocabulario
    tabla_gramatica = df_gramatica['Gramática'].value_counts().reindex(categorias_ordenadas, fill_value=0).reset_index()
    tabla_gramatica.columns = ['Nivel', 'Estudiantes']
    tabla_gramatica['Porcentaje'] = (tabla_gramatica['Estudiantes'] / freq_gramatica * 100).round(2).astype(str) + '%'
    
    tabla_vocabulario = df_vocabulario['Vocabulario'].value_counts().reindex(categorias_ordenadas, fill_value=0).reset_index()
    tabla_vocabulario.columns = ['Nivel', 'Estudiantes']
    tabla_vocabulario['Porcentaje'] = (tabla_vocabulario['Estudiantes'] / freq_vocabulario * 100).round(2).astype(str) + '%'

    # Contar la frecuencia de cada CCT
    tabla_cct = df_filtered['CCT'].value_counts().reset_index()
    tabla_cct.columns = ['CCT', 'Frecuencia']

    # Mostrar tablas de frecuencias
    st.write("**Tabla de Frecuencias: Gramática**")
    st.write(tabla_gramatica)

    st.write("**Tabla de Frecuencias: Vocabulario**")
    st.write(tabla_vocabulario)

    st.write("**Frecuencia por CCT**")
    st.write(tabla_cct)

    # Crear botón de descarga de PDF
    st.write("\n\n**Descargar resultados en PDF**")
    file_path = "resultados_por_zona.pdf"  # Nombre temporal del archivo
    generar_pdf(tabla_gramatica, tabla_vocabulario, tabla_cct, file_path, logo_path)
    
    # Leer el archivo PDF generado y permitir la descarga
    with open(file_path, "rb") as file:
        pdf_data = file.read()
    
    st.download_button(
        label="Descargar PDF",
        data=pdf_data,
        file_name=f"resultados_zona_{zona_selected}.pdf",
        mime="application/pdf"
    )
    
    # Eliminar el archivo PDF temporal después de su uso
    os.remove(file_path)
else:
    st.write("No hay datos disponibles para la Zona seleccionada.")
