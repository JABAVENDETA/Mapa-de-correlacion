import { useState, useEffect } from 'react';
import axios from 'axios';
import MapComponent from '@/components/MapComponent';
import LeftPanel from '@/components/LeftPanel';
import RightPanel from '@/components/RightPanel';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Dashboard() {
  const [activeLayers, setActiveLayers] = useState({
    coca: true,
    violence: true,
    armed_groups: true,
    murders: true,
    poverty: true
  });
  
  const [layerData, setLayerData] = useState({});
  const [stats, setStats] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      const layers = ['coca', 'violence', 'armed_groups', 'murders', 'poverty'];
      const layerPromises = layers.map(layer => 
        axios.get(`${API}/layers/${layer}`)
      );
      
      const statsResponse = axios.get(`${API}/stats`);
      
      const [statsData, ...layerResponses] = await Promise.all([
        statsResponse,
        ...layerPromises
      ]);
      
      const newLayerData = {};
      layers.forEach((layer, index) => {
        newLayerData[layer] = layerResponses[index].data;
      });
      
      setLayerData(newLayerData);
      setStats(statsData.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const toggleLayer = (layerName) => {
    setActiveLayers(prev => ({
      ...prev,
      [layerName]: !prev[layerName]
    }));
  };

  const handleRegionClick = async (regionName) => {
    try {
      const response = await axios.get(`${API}/region/${regionName}`);
      setSelectedRegion(response.data);
    } catch (error) {
      console.error('Error fetching region data:', error);
    }
  };

  if (loading) {
    return (
      <div className="w-screen h-screen bg-zinc-950 flex items-center justify-center">
        <div className="text-zinc-400 font-mono text-lg">Cargando datos...</div>
      </div>
    );
  }

  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <MapComponent 
        activeLayers={activeLayers}
        layerData={layerData}
        onRegionClick={handleRegionClick}
      />
      
      <LeftPanel 
        activeLayers={activeLayers}
        onToggleLayer={toggleLayer}
      />
      
      <RightPanel 
        stats={stats}
        selectedRegion={selectedRegion}
      />
    </div>
  );
}