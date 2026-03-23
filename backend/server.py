from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


class GeoJSONFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: str = "Feature"
    properties: Dict[str, Any]
    geometry: Dict[str, Any]

class GeoJSONCollection(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

class LayerStats(BaseModel):
    model_config = ConfigDict(extra="ignore")
    layer_name: str
    total_value: float
    avg_value: float
    max_value: float
    affected_regions: int


@api_router.get("/")
async def root():
    return {"message": "Colombia Narco Impact Map API"}

@api_router.get("/layers/{layer_type}", response_model=GeoJSONCollection)
async def get_layer_data(layer_type: str):
    """
    Get GeoJSON data for a specific layer
    layer_type: coca, violence, armed_groups, murders, poverty
    """
    data = await db.geo_data.find_one({"layer_type": layer_type}, {"_id": 0})
    if not data:
        return {"type": "FeatureCollection", "features": []}
    return data

@api_router.get("/stats", response_model=List[LayerStats])
async def get_all_stats():
    """
    Get statistics for all layers
    """
    stats = await db.layer_stats.find({}, {"_id": 0}).to_list(100)
    return stats

@api_router.get("/stats/{layer_type}", response_model=LayerStats)
async def get_layer_stats(layer_type: str):
    """
    Get statistics for a specific layer
    """
    stats = await db.layer_stats.find_one({"layer_name": layer_type}, {"_id": 0})
    return stats

@api_router.get("/region/{region_name}")
async def get_region_data(region_name: str):
    """
    Get all layer data for a specific region (departamento)
    """
    region_data = {}
    layers = ["coca", "violence", "armed_groups", "murders", "poverty"]
    
    for layer in layers:
        data = await db.geo_data.find_one(
            {"layer_type": layer},
            {"_id": 0}
        )
        if data:
            for feature in data.get("features", []):
                if feature["properties"].get("name") == region_name:
                    region_data[layer] = feature["properties"].get("value", 0)
                    break
    
    return {
        "region": region_name,
        "data": region_data
    }


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()