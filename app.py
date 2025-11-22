import streamlit as st
st.set_page_config(
    page_title='InmoData 360',
    page_icon='documentos/Favicon BDI.png',
    layout='wide'
)

import pandas as pd
import plotly.express as px
import os
# import itertools
# from collections import OrderedDict
color_palette = px.colors.qualitative.Set3

# Cargar el archivo Excel
excel_path = os.path.join('documentos', 'FActNOTARIADOnacionalidades.xlsx')
df = pd.read_excel(excel_path)

# Sidebar: selector de municipio
logo_path = os.path.join('documentos', 'Logo BDI white.png')
st.sidebar.image(logo_path, use_container_width=True)
st.sidebar.markdown(
    '<h2 style="text-align: center; color: #3741c1; font-size: 1.6em;">InmoData 360</h2>',
    unsafe_allow_html=True
)
st.sidebar.markdown('---')

municipios = df['municipio'].dropna().unique()
municipio_sel = st.sidebar.selectbox('Selecciona un municipio', sorted(municipios))

# Filtrar por municipio
df_filtrado = df[df['municipio'] == municipio_sel].copy()

# Crear un único color_map para todas las nacionalidades presentes en el municipio filtrado
import itertools
from collections import OrderedDict
color_palette = px.colors.qualitative.Set3
unique_nacionalidades = list(OrderedDict.fromkeys(df_filtrado['nacionalidad'].dropna()))
color_cycle = itertools.cycle(color_palette)
color_map = {nac: next(color_cycle) for nac in unique_nacionalidades}

# Mostrar el título con estilos personalizados
st.markdown(
    '<h1 style="text-align: center; color: white;">Compraventas por Nacionalidades en <span style="color: #3741c1;">Alicante</span></h1>',
    unsafe_allow_html=True
)

# Sección de KPIs con 5 columnas
cols = st.columns(5)
def kpi_box(col, label, value):
    col.markdown(f"""
        <div style='background-color:#0e1117; border-radius:18px; padding:16px; box-shadow:0 4px 16px 0 rgba(30,33,39,0.18); text-align:center; margin-bottom:8px; border:1px solid #23272f;'>
            <span style='font-size:15px; color:#fff;'>{label}</span><br>
            <span style='font-size:22px; font-weight:bold; color:#fff;'>{value}</span>
        </div>
    """, unsafe_allow_html=True)

# KPI 1: Municipio seleccionado
kpi_box(cols[0], 'Municipio', municipio_sel)

# KPI 2 y 3: Nacionalidades de residentes número 1 y 2 en el municipio
nac_residentes = []
if 'residentes' in df_filtrado.columns:
    residentes_mun = df_filtrado.groupby('nacionalidad')['residentes'].sum().reset_index()
    residentes_mun = residentes_mun.sort_values('residentes', ascending=False)
    residentes_mun_no_otros = residentes_mun[residentes_mun['nacionalidad'] != 'Otros']
    nac_residentes = residentes_mun_no_otros['nacionalidad'].tolist()
if len(nac_residentes) > 0:
    kpi_box(cols[1], 'Residentes Nº1', nac_residentes[0])
else:
    kpi_box(cols[1], 'Residentes Nº1', '-')
if len(nac_residentes) > 1:
    kpi_box(cols[2], 'Residentes Nº2', nac_residentes[1])
else:
    kpi_box(cols[2], 'Residentes Nº2', '-')

# KPI 4 y 5: Nacionalidades de no residentes número 1 y 2 en el municipio
nac_nores = []
if 'no_residentes' in df_filtrado.columns:
    nores_mun = df_filtrado.groupby('nacionalidad')['no_residentes'].sum().reset_index()
    nores_mun = nores_mun.sort_values('no_residentes', ascending=False)
    nores_mun_no_otros = nores_mun[nores_mun['nacionalidad'] != 'Otros']
    nac_nores = nores_mun_no_otros['nacionalidad'].tolist()
if len(nac_nores) > 0:
    kpi_box(cols[3], 'No Residentes Nº1', nac_nores[0])
else:
    kpi_box(cols[3], 'No Residentes Nº1', '-')
if len(nac_nores) > 1:
    kpi_box(cols[4], 'No Residentes Nº2', nac_nores[1])
else:
    kpi_box(cols[4], 'No Residentes Nº2', '-')

# Eliminar columnas de identificador y fecha si existen
cols_to_hide = [c for c in df_filtrado.columns if 'id' in c.lower() or 'fecha' in c.lower()]
cols_to_show = [c for c in df_filtrado.columns if c not in cols_to_hide]

# Calcular porcentajes para las cantidades
if 'total' in df_filtrado.columns:
    total_sum = df_filtrado['total'].sum()
    df_filtrado['total_%'] = (df_filtrado['total'] / total_sum * 100).map('{:.2f}%'.format)
    cols_to_show = [c for c in cols_to_show if c != 'total']
if 'residentes' in df_filtrado.columns:
    res_sum = df_filtrado['residentes'].sum()
    df_filtrado['residentes_%'] = (df_filtrado['residentes'] / res_sum * 100).map('{:.2f}%'.format)
if 'no_residentes' in df_filtrado.columns:
    nores_sum = df_filtrado['no_residentes'].sum()
    df_filtrado['no_residentes_%'] = (df_filtrado['no_residentes'] / nores_sum * 100).map('{:.2f}%'.format)

st.write(f'Datos para el municipio: {municipio_sel}')
cols_final = [c for c in cols_to_show if c != 'total']
# Forzar municipio y nacionalidad como primeras columnas si existen
ordered = []
if 'provincia' in df_filtrado.columns:
    ordered.append('provincia')
if 'municipio' in df_filtrado.columns:
    ordered.append('municipio')
if 'nacionalidad' in df_filtrado.columns:
    ordered.append('nacionalidad')
for c in cols_final:
    if c not in ordered:
        ordered.append(c)
if 'residentes_%' in df_filtrado.columns:
    ordered.append('residentes_%')
if 'no_residentes_%' in df_filtrado.columns:
    ordered.append('no_residentes_%')
if 'total_%' in ordered:
    ordered.remove('total_%')
st.dataframe(df_filtrado[ordered])


# Botones para elegir el tipo de porcentaje
st.markdown('### Gráfico de barras por porcentaje')
col_btn1, col_btn2 = st.columns(2)
show_residentes = col_btn1.button('Porcentaje Residentes', key='btn_res')
show_nores = col_btn2.button('Porcentaje No Residentes', key='btn_nores')

bar_df = df_filtrado.copy()
bar_title = ''
bar_y = ''
bar_text = None
bar_color = None

# Crear un diccionario de colores fijo para cada país SOLO para los presentes en el gráfico
if show_residentes and 'residentes_%' in bar_df.columns:
    bar_df = bar_df.sort_values('residentes_%', ascending=False)
    bar_title = f'Residentes por Nacionalidad en {municipio_sel} (%)'
    bar_y = 'residentes_%'
    bar_text = bar_df['residentes_%']
    bar_color = 'residentes_%'
elif show_nores and 'no_residentes_%' in bar_df.columns:
    bar_df = bar_df.sort_values('no_residentes_%', ascending=False)
    bar_title = f'No Residentes por Nacionalidad en {municipio_sel} (%)'
    bar_y = 'no_residentes_%'
    bar_text = bar_df['no_residentes_%']
    bar_color = 'no_residentes_%'

if bar_y:
    bar_df = bar_df.sort_values(bar_y, ascending=False)
    nacionalidad_order = bar_df['nacionalidad'].tolist()
    fig = px.bar(
        bar_df,
        x='nacionalidad',
        y=bar_y,
        title=bar_title,
        text=bar_text,
        color='nacionalidad',
        color_discrete_map=color_map,
        category_orders={'nacionalidad': nacionalidad_order}
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
col1, col2 = st.columns(2)
# Donut de no residentes filtrado

if 'no_residentes' in df_filtrado.columns:
    donut_nores = df_filtrado.groupby('nacionalidad')['no_residentes'].sum().reset_index()
    donut_nores = donut_nores.sort_values('no_residentes', ascending=False)
    nacionalidad_order_nores = donut_nores['nacionalidad'].tolist()
    fig_nores = px.pie(
        donut_nores,
        names='nacionalidad',
        values='no_residentes',
        hole=0.5,
        title='No Residentes por Nacionalidad',
        category_orders={'nacionalidad': nacionalidad_order_nores},
        color_discrete_map=color_map
    )
    fig_nores.update_traces(
        sort=False,
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='%{label}<br>%{percent:.2%} del total<extra></extra>'
    )
    col1.plotly_chart(fig_nores, use_container_width=True)
else:
    col1.info('No hay datos de no residentes.')

# Donut de residentes filtrado

if 'residentes' in df_filtrado.columns:
    donut_res = df_filtrado.groupby('nacionalidad')['residentes'].sum().reset_index()
    donut_res = donut_res.sort_values('residentes', ascending=False)
    nacionalidad_order_res = donut_res['nacionalidad'].tolist()
    fig_res = px.pie(
        donut_res,
        names='nacionalidad',
        values='residentes',
        hole=0.5,
        title='Residentes por Nacionalidad',
        category_orders={'nacionalidad': nacionalidad_order_res},
        color_discrete_map=color_map
    )
    fig_res.update_traces(
        sort=False,
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='%{label}<br>%{percent:.2%} del total<extra></extra>'
    )
    col2.plotly_chart(fig_res, use_container_width=True)
else:
    col2.info('No hay datos de residentes.')

## Sección de dos columnas para las tablas de nacionalidades (justo después de los KPIs)
col_a, col_b = st.columns(2)

# Tabla de nacionalidades de residentes en el municipio seleccionado
if 'residentes' in df_filtrado.columns:
    residentes_mun = df_filtrado.groupby('nacionalidad')['residentes'].sum().reset_index()
    total_mun_res = residentes_mun['residentes'].sum()
    residentes_mun['porcentaje'] = (residentes_mun['residentes'] / total_mun_res * 100).map('{:.2f}%'.format)
    residentes_mun = residentes_mun.sort_values('residentes', ascending=False).reset_index(drop=True)
    residentes_mun.index = residentes_mun.index + 1
    residentes_mun_no_otros = residentes_mun[residentes_mun['nacionalidad'] != 'Otros']
    if not residentes_mun_no_otros.empty:
        max_row = residentes_mun_no_otros.iloc[0]
    else:
        max_row = residentes_mun.iloc[0]
    col_a.markdown('<div style="padding-right:30px">', unsafe_allow_html=True)
    col_a.write(f'Nacionalidades de residentes en {municipio_sel} (ordenadas de mayor a menor)')
    table_html = '<table style="width:100%"><tr><th>#</th><th>Nacionalidad</th><th>Porcentaje</th></tr>'
    for idx, row in residentes_mun.iterrows():
        if row['nacionalidad'] == max_row['nacionalidad']:
            table_html += f'<tr style="background-color:#2ecc71;color:#000;font-weight:bold"><td>{idx}</td><td>{row["nacionalidad"]}</td><td>{row["porcentaje"]}</td></tr>'
        else:
            table_html += f'<tr><td>{idx}</td><td>{row["nacionalidad"]}</td><td>{row["porcentaje"]}</td></tr>'
    table_html += '</table>'
    col_a.markdown(table_html, unsafe_allow_html=True)
    col_a.markdown('</div>', unsafe_allow_html=True)

# Tabla de nacionalidades de no residentes en el municipio seleccionado
if 'no_residentes' in df_filtrado.columns:
    nores_mun = df_filtrado.groupby('nacionalidad')['no_residentes'].sum().reset_index()
    total_mun_nores = nores_mun['no_residentes'].sum()
    nores_mun['porcentaje'] = (nores_mun['no_residentes'] / total_mun_nores * 100).map('{:.2f}%'.format)
    nores_mun = nores_mun.sort_values('no_residentes', ascending=False).reset_index(drop=True)
    nores_mun.index = nores_mun.index + 1
    nores_mun_no_otros = nores_mun[nores_mun['nacionalidad'] != 'Otros']
    if not nores_mun_no_otros.empty:
        max_row_nores = nores_mun_no_otros.iloc[0]
    else:
        max_row_nores = nores_mun.iloc[0]
    col_b.markdown('<div style="padding-left:30px">', unsafe_allow_html=True)
    col_b.write(f'Nacionalidades de no residentes en {municipio_sel} (ordenadas de mayor a menor)')
    table_html_nores = '<table style="width:100%"><tr><th>#</th><th>Nacionalidad</th><th>Porcentaje</th></tr>'
    for idx, row in nores_mun.iterrows():
        if row['nacionalidad'] == max_row_nores['nacionalidad']:
            table_html_nores += f'<tr style="background-color:#2ecc71;color:#000;font-weight:bold"><td>{idx}</td><td>{row["nacionalidad"]}</td><td>{row["porcentaje"]}</td></tr>'
        else:
            table_html_nores += f'<tr><td>{idx}</td><td>{row["nacionalidad"]}</td><td>{row["porcentaje"]}</td></tr>'
    table_html_nores += '</table>'
    col_b.markdown(table_html_nores, unsafe_allow_html=True)
    col_b.markdown('</div>', unsafe_allow_html=True)

# Gráficos de barras y donut ya no se repiten aquí
