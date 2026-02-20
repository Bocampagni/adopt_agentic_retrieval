/**
 * OpenRouter model list. Swap or add models here; IDs must match OpenRouter.
 * @see https://openrouter.ai/models
 */
export interface ModelOption {
  id: string;
  name: string;
  description?: string;
}

export const MODELS: ModelOption[] = [
  { id: "openai/gpt-4o", name: "GPT-4o", description: "OpenAI" },
  { id: "google/gemini-2.0-flash-001", name: "Gemini 2.0 Flash", description: "Google" },
];

export const DEFAULT_MODEL_ID = MODELS[0].id;
