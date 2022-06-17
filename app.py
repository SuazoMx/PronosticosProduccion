import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Pronósticos de producción de aceite y gas", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="final_data.xlsx",
        engine="openpyxl",
        sheet_name="final_data",
        skiprows=0,
        usecols="B:L",
        nrows=7879,
    )
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Seleccione:")
pozo = st.sidebar.multiselect(
    "Pozo:",
    options=df["NPD_WELL_BORE_CODE"].unique(),
    default=df["NPD_WELL_BORE_CODE"].unique()
)

df_selection = df.query("NPD_WELL_BORE_CODE == @pozo")

# ---- MAINPAGE ----
st.title(":bar_chart: Producción de Gas y Aceite por pozo")
st.markdown("##")
st.markdown("""---""")

# ACEITE POR POZO[BAR CHART DERECHA]
aceite_by_pozo = (
    df_selection.groupby(by=["NPD_WELL_BORE_CODE"]).sum()[["BORE_OIL_VOL"]].sort_values(by="BORE_OIL_VOL")
)
fig_aceite_pozo = px.bar(
    aceite_by_pozo,
    x="BORE_OIL_VOL",
    y=aceite_by_pozo.index,
    orientation="h",
    title="<b>Producción de Aceite</b>",
    color_discrete_sequence=["#0083B8"] * len(aceite_by_pozo),
    template="plotly_white",
)
fig_aceite_pozo.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)

# GAS POR POZO [BAR CHART IZQUIERDA]
gas_por_pozo = (
    df_selection.groupby(by=["NPD_WELL_BORE_CODE"]).sum()[["BORE_GAS_VOL"]].sort_values(by="BORE_GAS_VOL")
)
fig_gas_pozo = px.bar(
    gas_por_pozo,
    x="BORE_GAS_VOL",
    y=gas_por_pozo.index,
    title="<b>Producción de gas</b>",
    color_discrete_sequence=["#0083B8"] * len(gas_por_pozo),
    template="plotly_white",
)
fig_gas_pozo.update_layout(
    #xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_gas_pozo, use_container_width=True)
right_column.plotly_chart(fig_aceite_pozo, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
