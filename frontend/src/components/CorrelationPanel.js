import { useState, useEffect } from 'react';
import { Lightning, Warning } from '@phosphor-icons/react';
import axios from 'axios';
import NetworkGraph from './NetworkGraph';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function CorrelationPanel() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    loadCorrelationData();
  }, []);

  const loadCorrelationData = async () => {
    try {
      const response = await axios.get(`${API}/correlation/analysis`);
      setAnalysis(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading correlation data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div 
        className="floating-panel bottom-6 left-6 w-96"
        style={{ animation: 'slideIn 0.5s ease-out 0.4s backwards' }}
      >
        <div className="bg-zinc-950/80 backdrop-blur-2xl border border-white/10 rounded-lg shadow-2xl p-6">
          <div className="text-zinc-400 font-mono text-sm">Analizando correlaciones...</div>
        </div>
      </div>
    );
  }

  if (!analysis) return null;

  return (
    <div 
      className="floating-panel bottom-6 left-6 w-96"
      data-testid="correlation-panel"
      style={{ animation: 'slideIn 0.5s ease-out 0.4s backwards' }}
    >
      <div className="bg-zinc-950/80 backdrop-blur-2xl border border-white/10 rounded-lg shadow-2xl p-6">
        <div 
          className="flex items-center justify-between cursor-pointer"
          onClick={() => setExpanded(!expanded)}
        >
          <div className="flex items-center gap-2">
            <Lightning size={20} weight="duotone" className="text-yellow-500" />
            <h2 className="font-chivo font-bold text-lg text-zinc-100 tracking-tight">
              Análisis de Correlación
            </h2>
          </div>
          <button 
            className="text-zinc-400 hover:text-zinc-200 transition-colors text-xl w-6 h-6 flex items-center justify-center"
            data-testid="correlation-toggle"
          >
            {expanded ? '−' : '+'}
          </button>
        </div>

        {!expanded && (
          <div className="mt-4">
            <div className="flex items-center gap-2 text-sm text-zinc-400">
              <Warning size={16} weight="fill" className="text-orange-500" />
              <span>{analysis.high_risk_regions.length} zonas de alto riesgo detectadas</span>
            </div>
          </div>
        )}

        {expanded && (
          <div className="mt-4 space-y-4">
            <div className="bg-white/5 border border-white/5 rounded-md p-4">
              <h3 className="text-xs uppercase tracking-wide text-zinc-500 mb-3 font-plex">
                Correlaciones Identificadas
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-400">Coca + Violencia</span>
                  <span className="font-mono text-sm text-orange-500 font-semibold">
                    {analysis.correlations.coca_violence}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-400">Coca + Pobreza</span>
                  <span className="font-mono text-sm text-yellow-500 font-semibold">
                    {analysis.correlations.coca_poverty}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-400">Todos los Factores</span>
                  <span className="font-mono text-sm text-rose-500 font-semibold">
                    {analysis.correlations.all_factors}%
                  </span>
                </div>
              </div>
            </div>

            <NetworkGraph hotspots={analysis.hotspots} />

            <div className="bg-white/5 border border-white/5 rounded-md p-4">
              <h3 className="text-xs uppercase tracking-wide text-zinc-500 mb-3 font-plex">
                Top Zonas Calientes
              </h3>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {analysis.hotspots.slice(0, 8).map((hotspot, index) => (
                  <div 
                    key={hotspot.region}
                    className="flex justify-between items-center py-1"
                    data-testid={`hotspot-${index}`}
                  >
                    <div className="flex items-center gap-2">
                      <div 
                        className="w-1.5 h-1.5 rounded-full"
                        style={{
                          backgroundColor: hotspot.risk_score > 300 ? '#e11d48' : 
                                          hotspot.risk_score > 250 ? '#f97316' : '#eab308'
                        }}
                      />
                      <span className="text-xs text-zinc-300 font-plex">
                        {hotspot.region}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-zinc-500">
                        {hotspot.active_factors} factores
                      </span>
                      <span className="font-mono text-xs font-semibold text-rose-400">
                        {hotspot.risk_score}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="text-xs text-zinc-600 pt-2 border-t border-white/5">
              <p>Score de riesgo basado en convergencia de múltiples factores</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}