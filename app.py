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

- *DiDi sets an example* by launching the first mobility guide with a gender perspective by a digital platform, opening new opportunities for engagement with stakeholders such as Women’s Ministries and the Secretary of Government.

- *By proactively addressing gender-inclusive mobility*, DiDi differentiates itself from competitors and attracts socially conscious users and partners in Mexico's growing market.

- *Addressing gender-specific risks in mobility*, such as harassment and unsafe routes, helps build greater trust among female passengers and drivers.

- In Mexico, many women face insecurity while commuting. *A gender-focused guide demonstrates that DiDi is attentive to local concerns and is actively working to close gender-based mobility gaps.*

- *Promoting equitable access to safe and reliable transportation* reflects DiDi's commitment to diversity, equity, and social responsibility, which is vital for maintaining a positive reputation and fostering passengers' trust.
"""
    },
    "Initiative 2: DiDigitalízate": {
        "code": "i2",
        "color": "#FFA500",
        "description": """#### 💻 DiDigitalízate

- *DiDigitalízate is a free, eight-week online training program* offered by DiDi Food in partnership with COPARMEX, CANIRAC, CONCANACO, NAFIN, Universidad Anáhuac, Ulinea and local governments, that consists of eight modules covering topics such as digital marketing, sustainable business models, business diagnostics, sanitation best practices, and hospitality sales skills, among others.

- *The goal of this program is to address the high closure rates among Mexican restaurants* by equipping restaurateurs with practical tools to improve their visibility and increase their revenue, especially for those who are new to delivery services.

- *Key highlights of the program include:*
    - *Contributing to social and economic development in Mexico*
    - *Enhancing DiDi's influence* within the Secretary of Economy and the Secretary of Tourism
    - *Launching in two major markets* (Jalisco and Nuevo León) by 2025
    - *Expanding to 14 states* by 2025
"""
    },
    "Initiative 3: EVs": {
        "code": "i3",
        "color": "#228B22",
        "description": """#### 🔋 EVs

- *Promoting electric vehicles (EVs) opens new markets* for Chinese EV manufacturers, such as BYD, in line with China's strategy for global exports and clean technology.

- *DiDi's initiatives in the EV sector position the company as a sustainability leader* in Mexico, gaining favor with eco-conscious users and government officials.

- *Encouraging the use of EVs fosters closer economic ties between China and Mexico*, with potential investments in EV infrastructure and supply chains.

- *By prioritizing electrification*, DiDi can differentiate itself from competitors like Uber by offering cleaner, technologically advanced ride options that align with urban mobility goals.

- *Getting ahead in electrification* also allows DiDi to comply more effectively with current and future environmental policies in major Mexican cities.
"""
    },
    "Initiative 4: C5": {
        "code": "i4",
        "color": "#1E90FF",
        "description": """#### 🎥 C5

- *It is important to demonstrate our commitment to safety conditions* by working closely with governors and C5 authorities.

- *We aim to mitigate safety issues* through various safety initiatives.

- *By providing access to trip data and connecting to emergency networks like C5/Emergency Portals*, DiDi aids authorities in responding more quickly to incidents and monitoring high-risk areas in real-time. This enhances overall security for rides and allows for the sharing of critical information such as vehicle plates, model, color, cellphone numbers, names, and locations.

- *Contributing ride information to local authorities showcases DiDi’s dedication to transparency and collaboration.* This facilitates smoother regulatory approvals and helps DiDi gain official recognition.
"""
    },
    "Initiative 5: Trip Donation": {
        "code": "i5",
        "color": "#FF69B4",
        "description": """#### 🎁 Trip Donation

- *DiDi demonstrates its commitment to cooperating with public authorities and law enforcement*, fostering regulatory trust, and facilitating compliance in city-level partnerships and initiatives focused on safer travel.

- *It positions DiDi as a dedicated ally* in combating gender-based violence through tangible, high-impact actions.

- *The company enables women in vulnerable situations to safely access justice centers and support services at no cost.*

- *DiDi transforms mobility into a tool* for gaining access to protection, legal support, and dignity.

- *Additionally, it builds trust with government stakeholders* by providing timely and meaningful collaboration that goes beyond commercial interests.
"""
    },
    "Initiative 6: Business Chambers": {
        "code": "i6",
        "color": "#8B4513",
        "description": """#### 🏛️ Business Chambers

- *Chambers advocate for fair and clear regulations*, assisting DiDi in navigating local laws to avoid operational disruptions while enhancing its reputation as a supportive ally of the private sector.

- *They act as a third-party validator*, connecting DiDi with local businesses, governments, and service providers, which fosters strategic alliances and promotes smoother operations.

- *This approach positions DiDi as a key player in digital transformation* and facilitates the dissemination of the company's initiatives through chamber forums, such as ABAUSTUR and the COPARMEX International SME Fair.
"""
    },
    "Initiative 7: PTP Taxi": {
        "code": "i7",
        "color": "#FFD300",
        "description": """#### 🚖 PTP Taxi

- *Create a win-win scenario with mobility authorities* by providing a safe, accessible, and technology-driven alternative to the traditional public transportation system.

- *Promote digital inclusion for taxi operators*, enhance service reliability, and contribute to safer, traceable mobility. Expand our GR community.

- *Engage with high-level stakeholders*, such as the governor of Querétaro, by launching this initiative with them.
"""
    },
    "Initiative 8: Moto": {
        "code": "i8",
        "color": "#800020",
        "description": """#### 🏍️ Moto

- *Position moto hailing as a safe and professional mobility option.*

- *Strengthen grassroots support* to protect moto hailing services from restrictive policies.

- *Create visibility and influence with key decision-makers* by mobilizing motorcycle users, drivers, and allies at the local level.

- *Reframe motorcycles as an inclusive and accessible transportation option*, particularly in underserved areas.

- *Align with national road safety goals* by training over 1,200 motorcycle drivers and couriers in partnership with ANASEVI.
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
