import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

export default function NetworkGraph({ hotspots }) {
  const svgRef = useRef();
  const [dimensions] = useState({ width: 340, height: 300 });

  useEffect(() => {
    if (!hotspots || hotspots.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const topRegions = hotspots.slice(0, 10);
    
    const nodes = topRegions.map((region, i) => ({
      id: region.region,
      risk: region.risk_score,
      factors: region.active_factors,
      data: region.data
    }));

    const links = [];
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const shared = countSharedFactors(nodes[i].data, nodes[j].data);
        if (shared >= 2) {
          links.push({
            source: nodes[i].id,
            target: nodes[j].id,
            value: shared
          });
        }
      }
    }

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(60))
      .force('charge', d3.forceManyBody().strength(-150))
      .force('center', d3.forceCenter(dimensions.width / 2, dimensions.height / 2))
      .force('collision', d3.forceCollide().radius(25));

    const g = svg.append('g');

    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#3f3f46')
      .attr('stroke-opacity', d => 0.3 + (d.value / 5) * 0.4)
      .attr('stroke-width', d => d.value / 2);

    const node = g.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g');

    node.append('circle')
      .attr('r', d => 8 + (d.risk / 50))
      .attr('fill', d => {
        if (d.risk > 300) return '#e11d48';
        if (d.risk > 250) return '#f97316';
        return '#eab308';
      })
      .attr('stroke', '#fafafa')
      .attr('stroke-width', 1)
      .style('cursor', 'pointer');

    node.append('text')
      .text(d => d.id.split(' ')[0])
      .attr('x', 0)
      .attr('y', -15)
      .attr('text-anchor', 'middle')
      .attr('fill', '#a1a1aa')
      .attr('font-size', '9px')
      .attr('font-family', 'IBM Plex Sans')
      .style('pointer-events', 'none');

    node.append('title')
      .text(d => `${d.id}\nRiesgo: ${d.risk}\nFactores: ${d.factors}`);

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    const zoom = d3.zoom()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    return () => simulation.stop();
  }, [hotspots, dimensions]);

  const countSharedFactors = (data1, data2) => {
    const factors = ['coca', 'violence', 'armed_groups', 'murders', 'poverty'];
    return factors.filter(f => (data1[f] || 0) > 0 && (data2[f] || 0) > 0).length;
  };

  return (
    <div className="bg-white/5 border border-white/5 rounded-md p-4">
      <h3 className="text-xs uppercase tracking-wide text-zinc-500 mb-3 font-plex">
        Red de Conexiones
      </h3>
      <div className="text-xs text-zinc-600 mb-2">
        Regiones conectadas por factores compartidos
      </div>
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        style={{ background: 'transparent' }}
      />
      <div className="flex items-center gap-3 mt-2 text-xs text-zinc-600">
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-rose-600"></div>
          <span>Crítico</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-orange-500"></div>
          <span>Alto</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
          <span>Medio</span>
        </div>
      </div>
    </div>
  );
}