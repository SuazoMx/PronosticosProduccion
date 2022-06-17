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
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Seleccione:")
pozo = st.sidebar.multiselect(
    "Pozo:",
    options=df["NPD_WELL_BORE_CODE"].unique(),
    default=df["NPD_WELL_BORE_CODE"].unique()
)

#customer_type = st.sidebar.multiselect(
#    "Select the Customer Type:",
#    options=df["Customer_type"].unique(),
#    default=df["Customer_type"].unique(),
#)

#gender = st.sidebar.multiselect(
#    "Select the Gender:",
#    options=df["Gender"].unique(),
#    default=df["Gender"].unique()
#)

df_selection = df.query("NPD_WELL_BORE_CODE == @pozo")

# ---- MAINPAGE ----
st.title(":bar_chart: Producción de Aceite")
st.markdown("##")

# TOP KPI's
#total_sales = int(df_selection["Total"].sum())
#average_rating = round(df_selection["Rating"].mean(), 1)
#star_rating = ":star:" * int(round(average_rating, 0))
#average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

#left_column, middle_column, right_column = st.columns(3)
#with left_column:
#    st.subheader("Ventas Totales:")
#    st.subheader(f"US $ {total_sales:,}")
#with middle_column:
#    st.subheader("Average Rating:")
#    st.subheader(f"{average_rating} {star_rating}")
#with right_column:
#    st.subheader("Average Sales Per Transaction:")
#    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["NPD_WELL_BORE_CODE"]).sum()[["BORE_OIL_VOL"]].sort_values(by="BORE_OIL_VOL")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x=sales_by_product_line.index,
    y="BORE_OIL_VOL",
    orientation="h",
    title="<b>Producción de Aceite por pozo</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
#sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
#fig_hourly_sales = px.bar(
#    sales_by_hour,
#    x=sales_by_hour.index,
#    y="Total",
#    title="<b>Sales by hour</b>",
#    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#    template="plotly_white",
#)
#fig_hourly_sales.update_layout(
#    xaxis=dict(tickmode="linear"),
#    plot_bgcolor="rgba(0,0,0,0)",
#    yaxis=(dict(showgrid=False)),
#)


left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
