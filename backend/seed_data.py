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

# Coordinates for Colombian departments (approximate centers)
COLOMBIA_DEPARTMENTS = [
    {"name": "Antioquia", "coords": [6.25, -75.56]},
    {"name": "Atlántico", "coords": [10.96, -74.79]},
    {"name": "Bolívar", "coords": [9.30, -74.76]},
    {"name": "Boyacá", "coords": [5.45, -73.36]},
    {"name": "Caldas", "coords": [5.07, -75.51]},
    {"name": "Caquetá", "coords": [1.86, -75.25]},
    {"name": "Cauca", "coords": [2.44, -76.61]},
    {"name": "Cesar", "coords": [9.32, -73.65]},
    {"name": "Chocó", "coords": [5.69, -76.66]},
    {"name": "Córdoba", "coords": [8.75, -75.88]},
    {"name": "Cundinamarca", "coords": [5.03, -74.03]},
    {"name": "Guainía", "coords": [2.58, -69.00]},
    {"name": "Guaviare", "coords": [2.56, -72.64]},
    {"name": "Huila", "coords": [2.54, -75.53]},
    {"name": "La Guajira", "coords": [11.35, -72.52]},
    {"name": "Magdalena", "coords": [10.41, -74.41]},
    {"name": "Meta", "coords": [3.30, -73.24]},
    {"name": "Nariño", "coords": [1.21, -77.28]},
    {"name": "Norte de Santander", "coords": [7.94, -72.90]},
    {"name": "Putumayo", "coords": [0.49, -76.35]},
    {"name": "Quindío", "coords": [4.46, -75.67]},
    {"name": "Risaralda", "coords": [5.31, -75.99]},
    {"name": "Santander", "coords": [7.00, -73.13]},
    {"name": "Sucre", "coords": [9.15, -75.12]},
    {"name": "Tolima", "coords": [4.09, -75.15]},
    {"name": "Valle del Cauca", "coords": [3.88, -76.60]},
    {"name": "Vaupés", "coords": [0.85, -70.81]},
    {"name": "Vichada", "coords": [4.42, -69.28]},
    {"name": "Arauca", "coords": [7.08, -70.76]},
    {"name": "Casanare", "coords": [5.76, -71.57]},
    {"name": "Amazonas", "coords": [-1.44, -71.93]},
    {"name": "Bogotá D.C.", "coords": [4.71, -74.07]}
]

# Mock data based on known patterns (higher values in conflict zones)
LAYER_DATA = {
    "coca": {
        "Nariño": 45000,
        "Putumayo": 42000,
        "Cauca": 38000,
        "Norte de Santander": 35000,
        "Caquetá": 33000,
        "Bolívar": 28000,
        "Guaviare": 26000,
        "Meta": 24000,
        "Antioquia": 22000,
        "Chocó": 18000,
        "Córdoba": 15000,
        "Valle del Cauca": 12000,
        "Arauca": 10000,
        "Vichada": 8000
    },
    "violence": {
        "Cauca": 850,
        "Nariño": 780,
        "Norte de Santander": 720,
        "Antioquia": 680,
        "Chocó": 620,
        "Valle del Cauca": 590,
        "Caquetá": 540,
        "Putumayo": 510,
        "Arauca": 480,
        "Bolívar": 450,
        "Córdoba": 420,
        "Cesar": 380,
        "Magdalena": 360,
        "Meta": 340
    },
    "armed_groups": {
        "Cauca": 95,
        "Nariño": 88,
        "Chocó": 82,
        "Norte de Santander": 78,
        "Arauca": 72,
        "Caquetá": 68,
        "Putumayo": 65,
        "Antioquia": 60,
        "Bolívar": 55,
        "Valle del Cauca": 52,
        "Córdoba": 48,
        "Guaviare": 45,
        "Meta": 42,
        "Vichada": 38
    },
    "murders": {
        "Valle del Cauca": 2850,
        "Antioquia": 2620,
        "Bogotá D.C.": 1890,
        "Cauca": 1650,
        "Nariño": 1540,
        "Norte de Santander": 1420,
        "Atlántico": 1280,
        "Bolívar": 1150,
        "Córdoba": 980,
        "Cesar": 920,
        "Magdalena": 870,
        "Santander": 810,
        "Cundinamarca": 760,
        "Caquetá": 680
    },
    "poverty": {
        "Chocó": 68.5,
        "La Guajira": 65.2,
        "Vaupés": 62.8,
        "Vichada": 60.4,
        "Cauca": 58.3,
        "Guainía": 56.7,
        "Amazonas": 54.2,
        "Nariño": 52.8,
        "Córdoba": 51.3,
        "Magdalena": 49.5,
        "Sucre": 48.7,
        "Cesar": 46.2,
        "Caquetá": 45.8,
        "Bolívar": 44.3,
        "Norte de Santander": 42.1
    }
}

def create_circle_polygon(lat, lon, radius_km=50):
    """Create a circular polygon around a point"""
    import math
    points = 32
    coords = []
    
    for i in range(points + 1):
        angle = (i * 2 * math.pi) / points
        dx = radius_km * math.cos(angle) / 111.0
        dy = radius_km * math.sin(angle) / (111.0 * math.cos(lat * math.pi / 180))
        coords.append([lon + dy, lat + dx])
    
    return coords

async def seed_database():
    print("Starting database seed...")
    
    await db.geo_data.delete_many({})
    await db.layer_stats.delete_many({})
    
    for layer_type, layer_values in LAYER_DATA.items():
        features = []
        
        for dept in COLOMBIA_DEPARTMENTS:
            dept_name = dept["name"]
            value = layer_values.get(dept_name, 0)
            
            lat, lon = dept["coords"]
            polygon_coords = create_circle_polygon(lat, lon, radius_km=40)
            
            feature = {
                "type": "Feature",
                "properties": {
                    "name": dept_name,
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
        
        values = list(layer_values.values())
        if values:
            stats = {
                "layer_name": layer_type,
                "total_value": sum(values),
                "avg_value": sum(values) / len(values),
                "max_value": max(values),
                "affected_regions": len(values)
            }
            await db.layer_stats.insert_one(stats)
        
        print(f"✓ Seeded {layer_type} layer with {len(features)} features")
    
    print("\n✓ Database seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())