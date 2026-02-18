import { MODELS } from "@/config/models";
import { useChatStore } from "@/stores/chatStore";

export function ModelSelector() {
  const selectedModelId = useChatStore((s) => s.selectedModelId);
  const setSelectedModelId = useChatStore((s) => s.setSelectedModelId);

  return (
    <div className="model-selector">
      <label htmlFor="model-select" className="model-selector__label">
        Model
      </label>
      <select
        id="model-select"
        className="model-selector__select"
        value={selectedModelId}
        onChange={(e) => setSelectedModelId(e.target.value)}
        aria-label="Select model"
      >
        {MODELS.map((m) => (
          <option key={m.id} value={m.id}>
            {m.name}
          </option>
        ))}
      </select>
    </div>
  );
}
