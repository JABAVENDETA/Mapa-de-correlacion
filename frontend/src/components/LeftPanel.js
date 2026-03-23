import { MapPin } from '@phosphor-icons/react';
import LayerToggle from './LayerToggle';

const LAYERS = [
  { id: 'coca', name: 'Cultivos de Coca', color: '#a3e635', icon: 'leaf' },
  { id: 'violence', name: 'Violencia', color: '#f97316', icon: 'warning' },
  { id: 'armed_groups', name: 'Grupos Armados', color: '#06b6d4', icon: 'users' },
  { id: 'murders', name: 'Asesinatos', color: '#e11d48', icon: 'crosshair' },
  { id: 'poverty', name: 'Pobreza', color: '#eab308', icon: 'coins' }
];

export default function LeftPanel({ activeLayers, onToggleLayer }) {
  return (
    <div 
      className="floating-panel top-6 left-6 w-80"
      data-testid="left-panel"
    >
      <div className="bg-zinc-950/80 backdrop-blur-2xl border border-white/10 rounded-lg shadow-2xl p-6">
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <MapPin size={24} weight="duotone" className="text-zinc-400" />
            <h1 className="font-chivo font-bold text-2xl text-zinc-100 tracking-tight">
              COLOMBIA
            </h1>
          </div>
          <p className="text-xs uppercase tracking-wide text-zinc-500 font-plex">
            Mapa de Impacto del Narcotráfico
          </p>
        </div>

        <div className="space-y-1">
          <h2 className="text-xs uppercase tracking-wide text-zinc-500 mb-3 font-plex">
            Capas de Datos
          </h2>
          {LAYERS.map(layer => (
            <LayerToggle
              key={layer.id}
              layer={layer}
              isActive={activeLayers[layer.id]}
              onToggle={() => onToggleLayer(layer.id)}
            />
          ))}
        </div>

        <div className="mt-6 pt-6 border-t border-white/10">
          <div className="text-xs text-zinc-500 space-y-1">
            <p>Datos basados en fuentes públicas</p>
            <p className="text-zinc-600">UNODC, DANE, Gobierno de Colombia</p>
          </div>
        </div>
      </div>
    </div>
  );
}