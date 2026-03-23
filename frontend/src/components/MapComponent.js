import { MapContainer, TileLayer, GeoJSON, ZoomControl } from 'react-leaflet';
import { useEffect, useState } from 'react';
import L from 'leaflet';

const LAYER_COLORS = {
  coca: '#a3e635',
  violence: '#f97316',
  armed_groups: '#06b6d4',
  murders: '#e11d48',
  poverty: '#eab308'
};

const LAYER_NAMES = {
  coca: 'Cultivos de Coca',
  violence: 'Violencia',
  armed_groups: 'Grupos Armados',
  murders: 'Asesinatos',
  poverty: 'Pobreza'
};

export default function MapComponent({ activeLayers, layerData, onRegionClick }) {
  const [map, setMap] = useState(null);

  const getLayerStyle = (layerType) => (feature) => {
    const value = feature.properties.value || 0;
    const maxValue = getMaxValue(layerType);
    const opacity = value > 0 ? 0.3 + (value / maxValue) * 0.5 : 0;

    return {
      fillColor: LAYER_COLORS[layerType],
      weight: 1,
      opacity: 0.6,
      color: LAYER_COLORS[layerType],
      fillOpacity: opacity
    };
  };

  const getMaxValue = (layerType) => {
    const features = layerData[layerType]?.features || [];
    return Math.max(...features.map(f => f.properties.value || 0), 1);
  };

  const onEachFeature = (layerType) => (feature, layer) => {
    const name = feature.properties.name;
    const value = feature.properties.value || 0;
    
    if (value > 0) {
      layer.bindPopup(
        `<div class="p-2">
          <div class="font-chivo font-bold text-base mb-1">${name}</div>
          <div class="text-zinc-400 text-sm">${LAYER_NAMES[layerType]}</div>
          <div class="font-mono text-lg mt-1" style="color: ${LAYER_COLORS[layerType]}">
            ${value.toLocaleString()}
          </div>
        </div>`
      );

      layer.on({
        mouseover: (e) => {
          const layer = e.target;
          layer.setStyle({
            weight: 2,
            fillOpacity: 0.8
          });
        },
        mouseout: (e) => {
          const layer = e.target;
          layer.setStyle(getLayerStyle(layerType)(feature));
        },
        click: () => {
          onRegionClick(name);
        }
      });
    }
  };

  return (
    <div className="map-container" data-testid="map-container">
      <MapContainer
        center={[4.5709, -74.2973]}
        zoom={6}
        zoomControl={false}
        style={{ width: '100%', height: '100%' }}
        whenCreated={setMap}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        
        <ZoomControl position="bottomright" />

        {Object.keys(LAYER_COLORS).map(layerType => {
          if (!activeLayers[layerType] || !layerData[layerType]) return null;
          
          return (
            <GeoJSON
              key={`${layerType}-${activeLayers[layerType]}`}
              data={layerData[layerType]}
              style={getLayerStyle(layerType)}
              onEachFeature={onEachFeature(layerType)}
            />
          );
        })}
      </MapContainer>
    </div>
  );
}