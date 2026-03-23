import { useEffect, useState } from 'react';
import { TrendUp, MapTrifold } from '@phosphor-icons/react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const LAYER_COLORS = {
  coca: '#a3e635',
  violence: '#f97316',
  armed_groups: '#06b6d4',
  murders: '#e11d48',
  poverty: '#eab308'
};

const LAYER_LABELS = {
  coca: 'Coca (ha)',
  violence: 'Violencia',
  armed_groups: 'Grupos',
  murders: 'Asesinatos',
  poverty: 'Pobreza (%)'
};

export default function RightPanel({ stats, selectedRegion }) {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (stats && stats.length > 0) {
      const data = stats.map(stat => ({
        name: LAYER_LABELS[stat.layer_name] || stat.layer_name,
        value: Math.round(stat.total_value),
        color: LAYER_COLORS[stat.layer_name]
      }));
      setChartData(data);
    }
  }, [stats]);

  return (
    <div 
      className="floating-panel top-6 right-6 w-96"
      data-testid="right-panel"
      style={{ animation: 'slideIn 0.5s ease-out 0.2s backwards' }}
    >
      <div className="bg-zinc-950/80 backdrop-blur-2xl border border-white/10 rounded-lg shadow-2xl p-6 space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <TrendUp size={20} weight="duotone" className="text-zinc-400" />
            <h2 className="font-chivo font-bold text-lg text-zinc-100 tracking-tight">
              Estadísticas Generales
            </h2>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {stats.map(stat => (
            <div 
              key={stat.layer_name}
              className="stat-card bg-white/5 border border-white/5 rounded-md p-4"
              data-testid={`stat-card-${stat.layer_name}`}
            >
              <div className="text-xs text-zinc-500 uppercase tracking-wide mb-1 font-plex">
                {LAYER_LABELS[stat.layer_name]}
              </div>
              <div 
                className="font-mono text-2xl font-bold mb-1"
                style={{ color: LAYER_COLORS[stat.layer_name] }}
              >
                {Math.round(stat.total_value).toLocaleString()}
              </div>
              <div className="text-xs text-zinc-600 font-plex">
                {stat.affected_regions} regiones
              </div>
            </div>
          ))}
        </div>

        {chartData.length > 0 && (
          <div className="bg-white/5 border border-white/5 rounded-md p-4">
            <h3 className="text-sm font-plex text-zinc-400 mb-4">Totales por Categoría</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chartData}>
                <XAxis 
                  dataKey="name" 
                  tick={{ fill: '#71717a', fontSize: 10 }}
                  axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
                />
                <YAxis 
                  tick={{ fill: '#71717a', fontSize: 10 }}
                  axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
                />
                <Tooltip 
                  contentStyle={{
                    background: 'rgba(9, 9, 11, 0.95)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '0.5rem',
                    backdropFilter: 'blur(24px)'
                  }}
                  labelStyle={{ color: '#fafafa' }}
                />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedRegion && (
          <div 
            className="bg-white/5 border border-white/5 rounded-md p-4"
            data-testid="selected-region-panel"
          >
            <div className="flex items-center gap-2 mb-3">
              <MapTrifold size={18} weight="duotone" className="text-zinc-400" />
              <h3 className="font-chivo font-bold text-base text-zinc-100">
                {selectedRegion.region}
              </h3>
            </div>
            <div className="space-y-2">
              {Object.entries(selectedRegion.data).map(([layer, value]) => (
                <div key={layer} className="flex justify-between items-center">
                  <span className="text-xs text-zinc-400 font-plex">
                    {LAYER_LABELS[layer]}
                  </span>
                  <span 
                    className="font-mono text-sm font-semibold"
                    style={{ color: LAYER_COLORS[layer] }}
                  >
                    {value.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}