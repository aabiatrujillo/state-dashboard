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
        "description": """
<b style='font-size:16px;'>🚺 Espacio reservado para highlights de GA (I1):</b><br><br>
<ul>
<li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
<li>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</li>
<li>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.</li>
</ul>
"""
    },
    "Initiative 2: DiDigitalízate": {
        "code": "i2",
        "color": "#FFA500",
        "description": """
<b style='font-size:16px;'>💻 Espacio reservado para highlights de GA (I2):</b><br><br>
<ul>
<li>Duis aute irure dolor in reprehenderit in voluptate velit esse.</li>
<li>Cillum dolore eu fugiat nulla pariatur.</li>
<li>Excepteur sint occaecat cupidatat non proident.</li>
</ul>
"""
    },
    "Initiative 3: EVs": {
        "code": "i3",
        "color": "#228B22",
        "description": """
<b style='font-size:16px;'>🔋 Espacio reservado para highlights de GA (I3):</b><br><br>
<ul>
<li>Sunt in culpa qui officia deserunt mollit anim id est laborum.</li>
<li>Nunc sed blandit libero volutpat sed cras ornare arcu.</li>
<li>Vel facilisis volutpat est velit egestas dui id ornare arcu.</li>
</ul>
"""
    },
    "Initiative 4: C5": {
        "code": "i4",
        "color": "#1E90FF",
        "description": """
<b style='font-size:16px;'>🎥 Espacio reservado para highlights de GA (I4):</b><br><br>
<ul>
<li>Mattis ullamcorper velit sed ullamcorper morbi tincidunt ornare.</li>
<li>Fermentum et sollicitudin ac orci phasellus egestas tellus rutrum.</li>
<li>Scelerisque eu ultrices vitae auctor eu augue.</li>
</ul>
"""
    },
    "Initiative 5: Trip Donation": {
        "code": "i5",
        "color": "#FF69B4",
        "description": """
<b style='font-size:16px;'>🎁 Espacio reservado para highlights de GA (I5):</b><br><br>
<ul>
<li>Integer feugiat scelerisque varius morbi.</li>
<li>Massa tempor nec feugiat nisl pretium fusce id velit.</li>
<li>Pellentesque pulvinar pellentesque habitant morbi tristique senectus.</li>
</ul>
"""
    },
    "Initiative 6: Business Chambers": {
        "code": "i6",
        "color": "#8B4513",
        "description": """
<b style='font-size:16px;'>🏛️ Espacio reservado para highlights de GA (I6):</b><br><br>
<ul>
<li>At elementum eu facilisis sed odio morbi quis.</li>
<li>Sit amet nulla facilisi morbi tempus iaculis urna id volutpat.</li>
<li>Faucibus pulvinar elementum integer enim neque.</li>
</ul>
"""
    },
    "Initiative 7: PTP Taxi": {
        "code": "i7",
        "color": "#FFD300",
        "description": """
<b style='font-size:16px;'>🚖 Espacio reservado para highlights de GA (I7):</b><br><br>
<ul>
<li>Justo eget magna fermentum iaculis eu non diam phasellus.</li>
<li>Est ultricies integer quis auctor elit sed vulputate.</li>
<li>Lacus sed turpis tincidunt id aliquet risus feugiat.</li>
</ul>
"""
    },
    "Initiative 8: Moto": {
        "code": "i8",
        "color": "#800020",
        "description": """
<b style='font-size:16px;'>🏍️ Espacio reservado para highlights de GA (I8):</b><br><br>
<ul>
<li>Vulputate enim nulla aliquet porttitor lacus luctus accumsan.</li>
<li>Vitae congue eu consequat ac felis donec et odio.</li>
<li>Aenean vel elit scelerisque mauris pellentesque pulvinar.</li>
</ul>
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
H1 2025 saw GA MX driving 8 high-impact initiatives across state governments — here’s what we achieved.
(A dummy dataset is used for demonstration purposes).
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
    st.subheader("📍 Results")
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
