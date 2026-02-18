import { API_BASE } from "@/config/env";

export interface ApiChatMessage {
  role: string;
  content: string;
}

export interface TableData {
  columns: string[];
  rows: any[][];
}

export interface ChatResponse {
  message: { role: string; content: string };
  table: TableData | null;
}

export async function sendMessage(
  messages: ApiChatMessage[],
  model: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages, model }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail ?? "Chat request failed");
  }
  return res.json();
}

export interface SchemaResponse {
  table_name: string;
  columns: string[];
  sample_rows: any[][];
}

export async function fetchSchema(): Promise<SchemaResponse> {
  const res = await fetch(`${API_BASE}/api/schema`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail ?? "Schema request failed");
  }
  return res.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}
