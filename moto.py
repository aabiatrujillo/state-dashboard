import streamlit as st
import geopandas as gpd
import pandas as pd
import pydeck as pdk
import json

# ---------------------------
# Page setup
# ---------------------------

st.set_page_config(page_title="Moto Initiative Map (Pydeck)", layout="wide")

# ---------------------------
# Load data
# ---------------------------

@st.cache_data
def load_geojson():
    gdf = gpd.read_file("map/estados_mexico_limpio.geojson")
    gdf["ent"] = gdf["ent"].astype(str).str.zfill(2)
    gdf["entidad"] = gdf["entidad"].str.strip().str.upper()
    return gdf

@st.cache_data
def load_moto():
    df = pd.read_csv("moto.csv", dtype={"ent": str}, encoding="latin1")
    df.columns = df.columns.str.strip()
    df["ent"] = df["ent"].astype(str).str.zfill(2)
    df["entidad"] = df["entidad"].str.strip().str.upper()
    return df

gdf = load_geojson()
df = load_moto()

# ---------------------------
# Merge data
# ---------------------------

gdf = gdf.merge(df, on=["ent", "entidad"], how="left")

# ---------------------------
# Define color mapping (RGBA)
# ---------------------------

color_dict = {
    "Red+": [139, 0, 0, 120],      # Dark Red, semi-transparent
    "Red": [255, 99, 71, 120],     # Tomato, semi-transparent
    "Gray": [169, 169, 169, 120],  # Dark Gray, semi-transparent
    "Green": [34, 139, 34, 120]    # Forest Green, semi-transparent
}

# Apply fill color
gdf["fill_color"] = gdf["color"].apply(lambda c: color_dict.get(c, [211, 211, 211, 120]))

# ---------------------------
# Build GeoJSON + tooltips
# ---------------------------

geojson_data = json.loads(gdf.to_json())

for feature in geojson_data["features"]:
    props = feature["properties"]
    props["fill_color"] = color_dict.get(props.get("color"), [211, 211, 211, 120])
    
    # ✅ Ensure correct handling of AMAM field (as number or string)
    amam_raw = props.get("amam")
    amam_value = "Yes" if str(int(float(amam_raw))) == "1" else "No" if amam_raw is not None else "N/A"
    
    props["tooltip"] = f"""
        <b>{props.get('entidad')}</b><br>
        <b>AMAM:</b> {amam_value}<br>
        <b>Status:</b> {props.get('Status', 'N/A')}<br>
        <b>Legal Basis:</b> {props.get('Legal Basis', 'N/A')}<br>
        <b>Reference:</b> {props.get('Reference', 'N/A')}<br>
        <b>Content:</b> {props.get('Content', 'N/A')}
    """

# ---------------------------
# Pydeck GeoJsonLayer only
# ---------------------------

polygon_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_data,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color="properties.fill_color",
    get_line_color=[0, 0, 0],
    line_width_min_pixels=1,
    pickable=True,
)

# ---------------------------
# Viewport
# ---------------------------

view_state = pdk.ViewState(
    latitude=23.6345,
    longitude=-102.5528,
    zoom=4.5,
    pitch=0,
)

# ---------------------------
# Streamlit UI
# ---------------------------

st.title("🏍️ Moto Initiative: Interactive State Map")
st.markdown("""
This interactive map shows the *regulatory status* of the Moto initiative across Mexican States.

Hover over each state to view legal and contextual details.
""")

st.pydeck_chart(pdk.Deck(
    layers=[polygon_layer],
    initial_view_state=view_state,
    map_style="light",
    tooltip={"html": "{tooltip}", "style": {"fontSize": "11px"}}
))

# ---------------------------
# Legal note
# ---------------------------

st.markdown("""<div style='margin-top: 1em'></div>""", unsafe_allow_html=True)
st.markdown("""
#### ℹ️ Legal context note

*In Mexico, there is no state where it is legal to offer motorcycle taxi services through apps such as Uber or DiDi.*  
*These services currently operate in a national legal vacuum, as no permits have been granted anywhere in the country.*

*Furthermore, all Mexican states —except for Mexico City, Colima, Tabasco, and Veracruz— are members of the AMAM (Asociación Mexicana de Autoridades de Movilidad).*  
*AMAM has issued an official statement against app-based motorcycle ride-hailing services, emphasizing the need for national regulation:*  
👉 *[Read AMAM’s statement here](https://autoridadesdemovilidad.org/la-regulacion-nacional-de-motos-es-urgente-autoridades-estatales-y-municipales-listas-para-colaborar-con-el-gobierno-de-mexico/)*
""")
