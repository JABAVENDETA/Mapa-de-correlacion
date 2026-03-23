import { Switch } from '@/components/ui/switch';
import { Circle } from '@phosphor-icons/react';

export default function LayerToggle({ layer, isActive, onToggle }) {
  return (
    <div 
      className="flex items-center justify-between p-3 rounded-md bg-white/5 border border-white/5 hover:bg-white/10 transition-colors cursor-pointer"
      onClick={onToggle}
      data-testid={`layer-toggle-${layer.id}`}
    >
      <div className="flex items-center gap-3">
        <Circle 
          size={16} 
          weight="fill" 
          style={{ color: layer.color }}
        />
        <span className="text-sm font-plex text-zinc-200">{layer.name}</span>
      </div>
      <Switch 
        checked={isActive}
        onCheckedChange={onToggle}
        data-testid={`layer-switch-${layer.id}`}
        style={{
          '--switch-color': layer.color
        }}
      />
    </div>
  );
}