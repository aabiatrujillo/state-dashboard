import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium

# ---------------------------
# Page setup
# ---------------------------

st.set_page_config(page_title="Moto Initiative Map (Folium)", layout="wide")

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
# Define color mapping
# ---------------------------

color_dict = {
    "Red+": "#8B0000",     # Dark Red
    "Red": "#FF6347",      # Tomato
    "Gray": "#A9A9A9",     # Dark Gray
    "Green": "#228B22"     # Forest Green
}

def get_color(color_label):
    return color_dict.get(color_label, "#D3D3D3")  # Default: light gray

# ---------------------------
# Create Folium map
# ---------------------------

m = folium.Map(
    location=[23.6345, -102.5528],
    zoom_start=5,
    tiles="CartoDB positron"
)

# ---------------------------
# Add polygons to map
# ---------------------------

def style_function(feature):
    color = get_color(feature["properties"].get("color"))
    return {
        "fillColor": color,
        "color": "black",
        "weight": 0.8,
        "fillOpacity": 0.3,  # 🔹 More transparent
    }

tooltip = GeoJsonTooltip(
    fields=["entidad", "Status", "Legal Basis", "Reference", "Content"],
    aliases=["State", "Status", "Legal Basis", "Reference", "Content"],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        background-color: white;
        border: 1px solid black;
        border-radius: 3px;
        padding: 6px;
        font-size: 10px;
    """,
)

folium.GeoJson(
    gdf,
    name="Regulatory Status",
    style_function=style_function,
    tooltip=tooltip
).add_to(m)

# ---------------------------
# Streamlit UI
# ---------------------------

st.title("🏍️ Moto Initiative: Interactive State Map")
st.markdown("""
This interactive map shows the **regulatory status** of the Moto initiative across Mexican States.

Hover over each state to view legal and contextual details.
""")

st_folium(m, use_container_width=True, height=500)

