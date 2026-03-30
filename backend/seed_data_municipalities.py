import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Muestra representativa de municipios colombianos (70 municipios clave)
COLOMBIA_MUNICIPALITIES = [
    # Antioquia
    {"name": "Medellín", "dept": "Antioquia", "coords": [6.2442, -75.5812]},
    {"name": "Envigado", "dept": "Antioquia", "coords": [6.1726, -75.5832]},
    {"name": "Itagüí", "dept": "Antioquia", "coords": [6.1848, -75.5993]},
    {"name": "Bello", "dept": "Antioquia", "coords": [6.3369, -75.5631]},
    {"name": "Rionegro", "dept": "Antioquia", "coords": [6.1552, -75.3736]},
    {"name": "Apartadó", "dept": "Antioquia", "coords": [7.8814, -76.6268]},
    {"name": "Turbo", "dept": "Antioquia", "coords": [8.0926, -76.7276]},
    {"name": "Necoclí", "dept": "Antioquia", "coords": [8.4273, -76.7891]},
    {"name": "Caucasia", "dept": "Antioquia", "coords": [7.9868, -75.1938]},
    {"name": "Segovia", "dept": "Antioquia", "coords": [7.0791, -74.6978]},
    
    # Bogotá D.C.
    {"name": "Bogotá D.C.", "dept": "Bogotá D.C.", "coords": [4.7110, -74.0721]},
    
    # Valle del Cauca
    {"name": "Cali", "dept": "Valle del Cauca", "coords": [3.4372, -76.5225]},
    {"name": "Palmira", "dept": "Valle del Cauca", "coords": [3.5394, -76.3036]},
    {"name": "Buenaventura", "dept": "Valle del Cauca", "coords": [3.8801, -77.0318]},
    {"name": "Tuluá", "dept": "Valle del Cauca", "coords": [4.0865, -76.1954]},
    {"name": "Jamundí", "dept": "Valle del Cauca", "coords": [3.2636, -76.5394]},
    
    # Nariño
    {"name": "Pasto", "dept": "Nariño", "coords": [1.2136, -77.2811]},
    {"name": "Tumaco", "dept": "Nariño", "coords": [1.7991, -78.7994]},
    {"name": "Ipiales", "dept": "Nariño", "coords": [0.8274, -77.6419]},
    {"name": "Samaniego", "dept": "Nariño", "coords": [1.3403, -77.5833]},
    {"name": "Barbacoas", "dept": "Nariño", "coords": [1.6733, -78.1419]},
    {"name": "El Charco", "dept": "Nariño", "coords": [2.4811, -78.1103]},
    
    # Cauca
    {"name": "Popayán", "dept": "Cauca", "coords": [2.4419, -76.6063]},
    {"name": "Santander de Quilichao", "dept": "Cauca", "coords": [3.0104, -76.4899]},
    {"name": "Puerto Tejada", "dept": "Cauca", "coords": [3.2313, -76.4169]},
    {"name": "Patía", "dept": "Cauca", "coords": [2.0707, -77.1059]},
    {"name": "Argelia", "dept": "Cauca", "coords": [2.2803, -77.0086]},
    {"name": "Corinto", "dept": "Cauca", "coords": [3.1734, -76.2647]},
    
    # Norte de Santander
    {"name": "Cúcuta", "dept": "Norte de Santander", "coords": [7.8939, -72.5078]},
    {"name": "Ocaña", "dept": "Norte de Santander", "coords": [8.2404, -73.3542]},
    {"name": "Tibú", "dept": "Norte de Santander", "coords": [8.6389, -72.7289]},
    {"name": "El Tarra", "dept": "Norte de Santander", "coords": [8.5736, -73.0578]},
    {"name": "Sardinata", "dept": "Norte de Santander", "coords": [8.0678, -72.8178]},
    
    # Putumayo
    {"name": "Mocoa", "dept": "Putumayo", "coords": [1.1479, -76.6439]},
    {"name": "Puerto Asís", "dept": "Putumayo", "coords": [0.5085, -76.4989]},
    {"name": "Valle del Guamuez", "dept": "Putumayo", "coords": [0.6578, -76.9225]},
    {"name": "Orito", "dept": "Putumayo", "coords": [0.6631, -76.8919]},
    {"name": "San Miguel", "dept": "Putumayo", "coords": [0.2828, -76.8869]},
    
    # Caquetá
    {"name": "Florencia", "dept": "Caquetá", "coords": [1.6144, -75.6062]},
    {"name": "San Vicente del Caguán", "dept": "Caquetá", "coords": [2.1153, -74.7631]},
    {"name": "Cartagena del Chairá", "dept": "Caquetá", "coords": [1.3367, -74.8336]},
    {"name": "Solano", "dept": "Caquetá", "coords": [0.7203, -75.2564]},
    
    # Chocó
    {"name": "Quibdó", "dept": "Chocó", "coords": [5.6936, -76.6611]},
    {"name": "Istmina", "dept": "Chocó", "coords": [5.1593, -76.6847]},
    {"name": "Alto Baudó", "dept": "Chocó", "coords": [5.6472, -76.9992]},
    {"name": "Medio Baudó", "dept": "Chocó", "coords": [5.1186, -76.8644]},
    
    # Meta
    {"name": "Villavicencio", "dept": "Meta", "coords": [4.1420, -73.6266]},
    {"name": "Acacías", "dept": "Meta", "coords": [3.9878, -73.7610]},
    {"name": "La Macarena", "dept": "Meta", "coords": [2.1843, -73.7850]},
    {"name": "Mapiripán", "dept": "Meta", "coords": [2.8903, -72.1364]},
    
    # Bolívar
    {"name": "Cartagena", "dept": "Bolívar", "coords": [10.3910, -75.4794]},
    {"name": "Magangué", "dept": "Bolívar", "coords": [9.2414, -74.7536]},
    {"name": "El Carmen de Bolívar", "dept": "Bolívar", "coords": [9.7172, -75.1208]},
    {"name": "Simití", "dept": "Bolívar", "coords": [8.0075, -73.9644]},
    
    # Córdoba
    {"name": "Montería", "dept": "Córdoba", "coords": [8.7479, -75.8814]},
    {"name": "Tierralta", "dept": "Córdoba", "coords": [8.1731, -76.0603]},
    {"name": "Valencia", "dept": "Córdoba", "coords": [8.2389, -76.1389]},
    
    # Guaviare
    {"name": "San José del Guaviare", "dept": "Guaviare", "coords": [2.5656, -72.6372]},
    {"name": "Calamar", "dept": "Guaviare", "coords": [1.9575, -72.2608]},
    
    # Arauca
    {"name": "Arauca", "dept": "Arauca", "coords": [7.0869, -70.7575]},
    {"name": "Saravena", "dept": "Arauca", "coords": [6.9525, -71.8756]},
    {"name": "Tame", "dept": "Arauca", "coords": [6.4600, -71.7347]},
    
    # Atlántico
    {"name": "Barranquilla", "dept": "Atlántico", "coords": [10.9639, -74.7964]},
    {"name": "Soledad", "dept": "Atlántico", "coords": [10.9172, -74.7694]},
    
    # Santander
    {"name": "Bucaramanga", "dept": "Santander", "coords": [7.1193, -73.1227]},
    {"name": "Barrancabermeja", "dept": "Santander", "coords": [7.0653, -73.8539]}
]

# Datos mock por municipio - basados en riesgo conocido
MUNICIPALITY_DATA = {
    "coca": {
        # Alto riesgo
        "Tumaco": 25000, "Puerto Asís": 18000, "Valle del Guamuez": 16000,
        "Orito": 14000, "San Miguel": 12000, "Tibú": 15000, "El Tarra": 13000,
        "Sardinata": 11000, "El Charco": 14000, "Barbacoas": 12000,
        "San Vicente del Caguán": 16000, "Cartagena del Chairá": 14000,
        "Solano": 10000, "La Macarena": 12000, "Mapiripán": 10000,
        "Calamar": 8000, "San José del Guaviare": 9000, "Apartadó": 7000,
        "Turbo": 6000, "Samaniego": 8000, "Patía": 7000, "Argelia": 6000,
        # Medio riesgo
        "Tierralta": 5000, "Valencia": 4000, "Alto Baudó": 4500,
        "Medio Baudó": 4000, "Simití": 3500, "Caucasia": 3000,
        "Segovia": 2500, "Necoclí": 2000
    },
    "violence": {
        # Alto riesgo
        "Tumaco": 450, "Tibú": 380, "Buenaventura": 520, "Cali": 890,
        "Cúcuta": 420, "Medellín": 680, "Bogotá D.C.": 1200, "Cartagena": 380,
        "Barranquilla": 420, "Quibdó": 290, "San José del Guaviare": 180,
        "Puerto Asís": 280, "Popayán": 320, "Pasto": 380, "Saravena": 240,
        "Barrancabermeja": 310, "Caucasia": 260, "Apartadó": 290,
        "El Carmen de Bolívar": 180, "Tierralta": 220, "Florencia": 240,
        # Medio riesgo
        "Bucaramanga": 180, "Villavicencio": 220, "Montería": 240,
        "Palmira": 160, "Soledad": 140, "Bello": 180
    },
    "armed_groups": {
        # Alto riesgo
        "Tumaco": 45, "Tibú": 38, "El Tarra": 32, "Samaniego": 28,
        "Barbacoas": 26, "El Charco": 25, "Puerto Asís": 35, "Valle del Guamuez": 33,
        "Orito": 30, "San Miguel": 28, "Buenaventura": 38, "Patía": 32,
        "Argelia": 28, "San Vicente del Caguán": 35, "Cartagena del Chairá": 32,
        "La Macarena": 30, "Mapiripán": 28, "Calamar": 26, "San José del Guaviare": 28,
        "Alto Baudó": 25, "Medio Baudó": 24, "Quibdó": 26, "Tierralta": 28,
        "Valencia": 25, "Saravena": 30, "Tame": 26, "Arauca": 28,
        # Medio riesgo
        "Apartadó": 20, "Turbo": 18, "Caucasia": 16, "Segovia": 15
    },
    "murders": {
        # Alto riesgo
        "Cali": 1850, "Medellín": 1520, "Bogotá D.C.": 1890, "Cúcuta": 680,
        "Barranquilla": 720, "Cartagena": 580, "Buenaventura": 420,
        "Tumaco": 380, "Palmira": 280, "Bucaramanga": 380, "Villavicencio": 320,
        "Montería": 340, "Quibdó": 220, "Popayán": 280, "Pasto": 320,
        "Florencia": 180, "Apartadó": 160, "Caucasia": 140, "Barrancabermeja": 220,
        # Medio-bajo riesgo
        "Bello": 120, "Itagüí": 100, "Envigado": 80, "Soledad": 110,
        "Tibú": 120, "Puerto Asís": 110, "Tierralta": 90
    },
    "poverty": {
        # Alto riesgo
        "Tumaco": 72.3, "El Charco": 68.5, "Barbacoas": 65.8, "Alto Baudó": 78.2,
        "Medio Baudó": 74.5, "Quibdó": 58.9, "Tibú": 62.4, "El Tarra": 60.3,
        "San José del Guaviare": 56.8, "Calamar": 54.2, "Puerto Asís": 58.3,
        "Valle del Guamuez": 56.7, "San Miguel": 54.9, "San Vicente del Caguán": 52.8,
        "Cartagena del Chairá": 51.3, "La Macarena": 49.8, "Mapiripán": 48.2,
        "Patía": 55.6, "Argelia": 53.2, "Samaniego": 50.8, "Magangué": 48.9,
        "El Carmen de Bolívar": 46.7, "Tierralta": 48.3, "Valencia": 46.1,
        # Medio riesgo
        "Buenaventura": 44.5, "Apartadó": 42.8, "Turbo": 41.2, "Caucasia": 39.6,
        "Quibdó": 45.3, "Popayán": 38.2, "Florencia": 37.8, "Pasto": 36.4,
        # Bajo riesgo
        "Bogotá D.C.": 18.5, "Medellín": 22.3, "Cali": 24.6, "Barranquilla": 26.8,
        "Bucaramanga": 19.7, "Cartagena": 28.4
    }
}

def create_circle_polygon(lat, lon, radius_km=8):
    """Create a circular polygon around a point - smaller for municipalities"""
    import math
    points = 16
    coords = []
    
    for i in range(points + 1):
        angle = (i * 2 * math.pi) / points
        dx = radius_km * math.cos(angle) / 111.0
        dy = radius_km * math.sin(angle) / (111.0 * math.cos(lat * math.pi / 180))
        coords.append([lon + dy, lat + dx])
    
    return coords

async def seed_database():
    print("Starting municipalities database seed...")
    
    await db.geo_data.delete_many({})
    await db.layer_stats.delete_many({})
    
    for layer_type, layer_values in MUNICIPALITY_DATA.items():
        features = []
        
        for municipality in COLOMBIA_MUNICIPALITIES:
            muni_name = municipality["name"]
            value = layer_values.get(muni_name, 0)
            
            lat, lon = municipality["coords"]
            polygon_coords = create_circle_polygon(lat, lon, radius_km=8)
            
            feature = {
                "type": "Feature",
                "properties": {
                    "name": muni_name,
                    "department": municipality["dept"],
                    "value": value,
                    "layer": layer_type
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]
                }
            }
            features.append(feature)
        
        geojson_data = {
            "layer_type": layer_type,
            "type": "FeatureCollection",
            "features": features
        }
        
        await db.geo_data.insert_one(geojson_data)
        
        values = [v for v in layer_values.values() if v > 0]
        if values:
            stats = {
                "layer_name": layer_type,
                "total_value": sum(values),
                "avg_value": sum(values) / len(values),
                "max_value": max(values),
                "affected_regions": len(values)
            }
            await db.layer_stats.insert_one(stats)
        
        print(f"✓ Seeded {layer_type} layer with {len(features)} municipalities ({len(values)} with data)")
    
    print(f"\n✓ Database seeding completed! {len(COLOMBIA_MUNICIPALITIES)} municipalities loaded")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
