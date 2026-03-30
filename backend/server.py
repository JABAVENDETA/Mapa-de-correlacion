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

class CorrelationAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    hotspots: List[Dict[str, Any]]
    correlations: Dict[str, float]
    high_risk_regions: List[str]


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
    Get all layer data for a specific region (municipality)
    """
    region_data = {}
    layers = ["coca", "violence", "armed_groups", "murders", "poverty"]
    
    all_data = await db.geo_data.find(
        {"layer_type": {"$in": layers}},
        {"_id": 0}
    ).to_list(5)
    
    for data in all_data:
        layer_type = data.get("layer_type")
        for feature in data.get("features", []):
            if feature["properties"].get("name") == region_name:
                region_data[layer_type] = feature["properties"].get("value", 0)
                break
    
    return {
        "region": region_name,
        "data": region_data
    }

@api_router.get("/correlation/analysis", response_model=CorrelationAnalysis)
async def get_correlation_analysis():
    """
    Analyze correlations between different layers and identify hotspots
    """
    layers = ["coca", "violence", "armed_groups", "murders", "poverty"]
    
    all_regions_data = {}
    
    all_data = await db.geo_data.find(
        {"layer_type": {"$in": layers}},
        {"_id": 0}
    ).to_list(5)
    
    for data in all_data:
        layer = data.get("layer_type")
        for feature in data.get("features", []):
            region_name = feature["properties"].get("name")
            value = feature["properties"].get("value", 0)
            
            if region_name not in all_regions_data:
                all_regions_data[region_name] = {}
            all_regions_data[region_name][layer] = value
    
    hotspots = []
    for region, data in all_regions_data.items():
        active_layers = sum(1 for v in data.values() if v > 0)
        if active_layers >= 3:
            total_score = sum([
                normalize_value(data.get('coca', 0), 50000),
                normalize_value(data.get('violence', 0), 1000),
                normalize_value(data.get('armed_groups', 0), 100),
                normalize_value(data.get('murders', 0), 3000),
                normalize_value(data.get('poverty', 0), 70)
            ])
            
            hotspots.append({
                "region": region,
                "risk_score": round(total_score, 2),
                "active_factors": active_layers,
                "data": data
            })
    
    hotspots.sort(key=lambda x: x['risk_score'], reverse=True)
    
    coca_violence_regions = [r for r, d in all_regions_data.items() 
                             if d.get('coca', 0) > 0 and d.get('violence', 0) > 0]
    coca_poverty_regions = [r for r, d in all_regions_data.items() 
                            if d.get('coca', 0) > 0 and d.get('poverty', 0) > 0]
    all_factors_regions = [r for r, d in all_regions_data.items() 
                           if all(d.get(layer_name, 0) > 0 for layer_name in layers)]
    
    total_regions = len(all_regions_data)
    correlations = {
        "coca_violence": round(len(coca_violence_regions) / total_regions * 100, 1) if total_regions > 0 else 0,
        "coca_poverty": round(len(coca_poverty_regions) / total_regions * 100, 1) if total_regions > 0 else 0,
        "all_factors": round(len(all_factors_regions) / total_regions * 100, 1) if total_regions > 0 else 0
    }
    
    high_risk_regions = [h['region'] for h in hotspots[:10]]
    
    return {
        "hotspots": hotspots[:15],
        "correlations": correlations,
        "high_risk_regions": high_risk_regions
    }

def normalize_value(value: float, max_val: float) -> float:
    """Normalize value to 0-100 scale"""
    return min((value / max_val) * 100, 100) if max_val > 0 else 0


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