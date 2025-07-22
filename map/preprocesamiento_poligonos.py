import os
import geopandas as gpd

# ---------------------------
# Ruta del archivo
# ---------------------------

# Carpeta actual (donde está este script)
base_path = os.path.dirname(os.path.abspath(__file__))

# Nombre base del shapefile
shapefile_name = "dest_2010gw.shp"
shapefile_path = os.path.join(base_path, shapefile_name)

# Verificar existencia de archivos necesarios del shapefile
required_extensions = [".shp", ".shx", ".dbf"]
missing_files = [
    ext for ext in required_extensions
    if not os.path.exists(shapefile_path.replace(".shp", ext))
]

if missing_files:
    raise FileNotFoundError(f"❌ Faltan archivos del shapefile: {missing_files}")

# ---------------------------
# Carga y preprocesamiento
# ---------------------------

# Cargar shapefile
gdf = gpd.read_file(shapefile_path)

# Renombrar columnas clave
gdf = gdf.rename(columns={
    "ENTIDAD": "entidad",
    "NUM_EDO": "ent"
})

# Filtrar registros principales
gdf = gdf[gdf["RASGO_GEOG"].isna()]

# Eliminar columnas innecesarias
columnas_a_eliminar = ["AREA", "PERIMETER", "COV_", "COV_ID", "CAPITAL", "RASGO_GEOG"]
gdf = gdf.drop(columns=columnas_a_eliminar, errors="ignore")

# Asegurar formato de clave de entidad con ceros a la izquierda
gdf["ent"] = gdf["ent"].astype(str).str.zfill(2)


# Diccionario de mapeo de claves 'ent' a sus correspondientes códigos 'entidad'
ent_to_entidad = {
    '01': 'AGU', '02': 'BC', '03': 'BCS', '04': 'CAM', '05': 'COA', '06': 'COL',
    '07': 'CHP', '08': 'CHH', '09': 'CDMX', '10': 'DUR', '11': 'GUA', '12': 'GRO',
    '13': 'HID', '14': 'JAL', '15': 'MEX', '16': 'MIC', '17': 'MOR', '18': 'NAY',
    '19': 'NLE', '20': 'OAX', '21': 'PUE', '22': 'QUE', '23': 'ROO', '24': 'SLP',
    '25': 'SIN', '26': 'SON', '27': 'TAB', '28': 'TAM', '29': 'TLA', '30': 'VER',
    '31': 'YUC', '32': 'ZAC'
}

# Reemplazar los valores de la columna 'entidad' según 'ent'
gdf['entidad'] = gdf['ent'].map(ent_to_entidad)

# Disolver geometrías duplicadas (agrupar por todos los atributos excepto la geometría)
gdf = gdf.dissolve(
    by=gdf.drop(columns="geometry").apply(lambda row: tuple(row), axis=1),
    as_index=False
)

# Reproyectar a EPSG:4326 (lat/lon)
gdf = gdf.to_crs(epsg=4326)

gdf = gdf.drop(columns='index')

# ---------------------------
# Guardar archivo limpio
# ---------------------------

output_path = os.path.join(base_path, "estados_mexico_limpio.geojson")

# Eliminar cualquier columna extra de tipo geométrico (por si existiera)
geom_cols = gdf.select_dtypes(include="geometry").columns.tolist()
if len(geom_cols) > 1:
    gdf = gdf.drop(columns=[col for col in geom_cols if col != "geometry"])

# Guardar como GeoJSON
gdf.to_file(output_path, driver="GeoJSON")

print("✅ GeoDataFrame procesado correctamente.")
print(f"🗂️ Archivo guardado: {output_path}")