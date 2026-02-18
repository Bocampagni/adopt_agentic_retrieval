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
  { id: "anthropic/claude-3.5-sonnet", name: "Claude 3.5 Sonnet", description: "Anthropic" },
  { id: "openai/gpt-4o", name: "GPT-4o", description: "OpenAI" },
  { id: "google/gemini-2.0-flash-001", name: "Gemini 2.0 Flash", description: "Google" },
  { id: "meta-llama/llama-3.3-70b-instruct", name: "Llama 3.3 70B", description: "Meta" },
  { id: "mistralai/mistral-large-2411", name: "Mistral Large", description: "Mistral" },
];

export const DEFAULT_MODEL_ID = MODELS[0].id;
