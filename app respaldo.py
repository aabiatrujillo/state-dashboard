import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import io

# ---------------------------
# Initial setup
# ---------------------------

st.set_page_config(page_title="State-Level Initiative Dashboard", layout="wide")

# Optional styling for better visuals
st.markdown("""
    <style>
        ul { padding-left: 20px; }
        li { margin-bottom: 4px; font-size: 15px; }
        b { font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_geojson_mexico():
    return gpd.read_file("map/estados_mexico_limpio.geojson")

@st.cache_data
def load_data():
    df = pd.read_csv("datos.csv", dtype={"ent": str})
    df.columns = df.columns.str.strip()
    return df

# ---------------------------
# Initiative dictionary
# ---------------------------

initiatives = {
    "Initiative 1: Women Experts & Gender Guide": {
        "code": "i1",
        "color": "#800080",
        "description": """#### 🚺 Women Experts & Gender Guide

> DiDi sets an example in launching the first mobility guide with a gender perspective by a digital platform in Mexico, opening new opportunities for engagement with stakeholders such as Women’s Ministries and the Secretary of Government.

**📊 Key figures:**
- 1 Federal Guide + 3 State Guides finalized MTY, GDL, QROO + 3 in the making CDMX, MOR, EDOMEX  
- 14 new different stakeholders engaged
"""
    },
    "Initiative 2: DiDigitalízate": {
        "code": "i2",
        "color": "#FFA500",
        "description": """#### 💻 DiDigitalízate

> DiDigitalízate is a free, eight-week online training program offered by DiDi Food, consisting of a quick, 20 hour training for Small and Medium Businesses to support the business and boosting our Advocacy with Local stakeholders.

**📊 Key figures:**
- 8 modules covering topics such as digital marketing, sustainable business models, business diagnostics, sanitation best practices, and hospitality sales skills, among others  
- 8 key partners: COPARMEX, CANIRAC, CONCANACO, NAFIN, Universidad Anáhuac, Ulinea and local governments  
- 3297 Restaurants engaged so far  
- 14 States engaged by 2025  
- 1 Senate forum with legislators and chamber presidents to talk about digital tools for SMEs
"""
    },
    "Initiative 3: EVs": {
        "code": "i3",
        "color": "#228B22",
        "description": """#### 🔋 EVs

> DiDi's initiatives in the EV sector position us as a key Sustainability leader in Mexico, with a unique innovation agenda to discuss with government officials from Federal & Local levels.

**📊 Key figures:**
- 2 Federal authorities reached: Ing. Mauricio Montesinos, Head of Office of the Director of Basic Electrical Supply, & Ing. Víctor Arellano, Senior Manager at Programa de Ahorro de Energía del Sector Eléctrico (PAESE), both middle-level public servants at CFE  
- 1 State with a fixed innovation project: Nuevo León (in negotiations to exchange mobility fund for vehicle acquisition)
"""
    },
    "Initiative 4: C5": {
        "code": "i4",
        "color": "#1E90FF",
        "description": """#### 🎥 C5

> By providing access to trip data (vehicle plates, model, color, cellphone numbers, names of DRV + PAX, and locations) and connecting to emergency networks like C5/Emergency Portals, DiDi aids authorities in responding more quickly to incidents and monitoring high-risk areas in real-time.

**📊 Key figures:**
- Announced in: AGS, SON, JAL, NL, BCS  
- 4 WIP (CDMX, COAH, MOR, EDOMEX)  
- 4 Events in H1
"""
    },
    "Initiative 5: Trip Donation": {
        "code": "i5",
        "color": "#FF69B4",
        "description": """#### 🎁 Trip Donation

> DiDi demonstrates its commitment to cooperating with public authorities and law enforcement by enabling Trips donations to women in vulnerable situations to safely access justice centers and support services at no cost, facilitating city-level partnerships.

**📊 Key figures:**
- 6 City-level partnerships  
- 4000 (NL, CUU, BC, ZAC) Total trips donated  
- 6 WIPs
"""
    },
    "Initiative 6: Business Chambers": {
        "code": "i6",
        "color": "#8B4513",
        "description": """#### 🏛️ Business Chambers

> Chambers advocate for fair and clear regulations, assisting DiDi in navigating local laws to avoid operational disruptions while enhancing its reputation as a relevant ally within the private sector.

**📊 Key figures:**
- 42 Partnerships achieved in states  
- 8 Events, Webinars and Chamber Forums: ABAUSTUR, COPARMEX International SME Fair, ANPEC collaboration
"""
    },
    "Initiative 7: PTP Taxi": {
        "code": "i7",
        "color": "#FFD300",
        "description": """#### 🚖 PTP Taxi

> New launches, and PTP Taxi is helping create a win-win scenario with mobility authorities by providing technology and a safer, more accessible alternative to the traditional public transportation system.

**📊 Key figures:**
- 3 Mkts Launch with GA support  
- 1 Governor-level event in Querétaro  
- 10+ Taxi leaders engaged
"""
    },
    "Initiative 8: Moto": {
        "code": "i8",
        "color": "#800020",
        "description": """#### 🏍️ Moto

> As one of the most controversial transport alternatives, our goal is to position moto hailing as an inclusive and accessible transportation option, particularly in underserved areas, and shield the product ahead of strong regulatory prohibitions.

**📊 Key figures:**
- 5 markets launched so far  
- 8 Rumbo Seguro’s events in CDMX and EDOMEX  
- 1,500 couriers and drivers engaged  
- 198 Moto GR + 5 Grasstops - CDMX  
- 60 Moto GR - GDL + 2 Grasstops - GDL
"""
    },
    "Initiative 9: Grassroots": {
        "code": "i9",
        "color": "#FFA500",
        "description": """#### 🧱 Grassroots

> Bottom-up movements legitimizing social impact of digital platforms in the country, that contribute to support Federal + local regulations, Taxi, Launches, and business initiatives, while building trust among communities.

**📊 Key figures:**
- 40 communities engaged  
- 16/32 States with allied communities  
- +1400 Total GR engaged MX
"""
    }
}



# ---------------------------
# Load data
# ---------------------------

gdf = load_geojson_mexico()
df = load_data()

# ---------------------------
# Main interface
# ---------------------------

st.title("📈 State-Level Initiative Dashboard")
st.markdown("""
#### H1 2025 saw GA MX driving 8 high-impact initiatives across state governments — here’s what we achieved.
""")

initiative_name = st.selectbox("Select an initiative:", list(initiatives.keys()))
initiative_code = initiatives[initiative_name]["code"]
color_base = initiatives[initiative_name]["color"]

# ---------------------------
# Initial validation
# ---------------------------

for col in ["ent", "entidad", initiative_code]:
    if col not in df.columns:
        st.error(f"❌ Column '{col}' is missing in datos.csv.")
        st.write("Available columns in df:", df.columns.tolist())
        st.stop()

# ---------------------------
# Normalize keys
# ---------------------------

gdf["ent"] = gdf["ent"].astype(str).str.zfill(2)
df["ent"] = df["ent"].astype(str).str.zfill(2)

gdf["entidad"] = gdf["entidad"].str.strip().str.upper()
df["entidad"] = df["entidad"].str.strip().str.upper()

# ---------------------------
# Key match check
# ---------------------------

claves_gdf = set(zip(gdf["ent"], gdf["entidad"]))
claves_df = set(zip(df["ent"], df["entidad"]))
missing = claves_gdf - claves_df

if missing:
    st.warning("⚠️ Some (ent, entidad) combinations in gdf are missing in df:")
    st.write(missing)

# ---------------------------
# Merge
# ---------------------------

gdf = gdf.drop(columns=[c for c in ["valor", initiative_code] if c in gdf.columns], errors="ignore")
gdf = gdf.merge(df[["ent", "entidad", initiative_code]], on=["ent", "entidad"], how="left")

if len(gdf) != 32:
    st.error(f"🚨 The merge result does not contain 32 rows (current: {len(gdf)}).")
    st.stop()

gdf["valor"] = gdf[initiative_code]

# ---------------------------
# Visualization
# ---------------------------

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📍 Highlights")
    st.markdown(initiatives[initiative_name]["description"], unsafe_allow_html=True)

with col2:
    st.subheader("🌍 Geographic Coverage")

    plt.rcParams['lines.antialiased'] = True
    plt.rcParams['patch.antialiased'] = True

    custom_cmap = LinearSegmentedColormap.from_list(
        initiative_name,
        colors=["#ffffff", color_base]
    )

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    gdf.plot(
        column="valor",
        cmap=custom_cmap,
        linewidth=0.5,
        edgecolor="gray",
        vmin=0, vmax=1,
        legend=False,
        missing_kwds={"color": "lightgrey", "label": "No data"},
        ax=ax
    ) 

    text_effect = path_effects.withStroke(linewidth=2, foreground="white")
    drawn_labels = []
    for _, row in gdf.iterrows():
        if (
            pd.notna(row.get("entidad")) and
            pd.notna(row.get("valor")) and
            row.geometry and
            not row.geometry.is_empty
        ):
            centroid = row.geometry.centroid
            if row.geometry.contains(centroid):
                too_close = False
                for x_prev, y_prev in drawn_labels:
                    dist = ((centroid.x - x_prev)**2 + (centroid.y - y_prev)**2)**0.5
                    if dist < 1.0:
                        too_close = True
                        break
                if not too_close:
                    ax.text(
                        centroid.x, centroid.y,
                        row["entidad"],
                        fontsize=7,
                        ha="center",
                        color="black",
                        path_effects=[text_effect]
                    )
                    drawn_labels.append((centroid.x, centroid.y))

    ax.axis("off")
    ax.set_xlim(gdf.total_bounds[[0, 2]])
    ax.set_ylim(gdf.total_bounds[[1, 3]])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, transparent=True)
    st.image(buf, use_container_width=False)
