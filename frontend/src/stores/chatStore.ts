import { create } from "zustand";
import { persist } from "zustand/middleware";
import { DEFAULT_MODEL_ID } from "@/config/models";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  table?: { columns: string[]; rows: any[][] } | null;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: number;
}

interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  selectedModelId: string;
  setSelectedModelId: (id: string) => void;
  setActiveConversation: (id: string | null) => void;
  createConversation: () => string;
  addMessage: (conversationId: string, message: ChatMessage) => void;
  appendToConversation: (conversationId: string, message: ChatMessage) => void;
  getConversation: (id: string) => Conversation | undefined;
  updateConversationTitle: (id: string, title: string) => void;
  deleteConversation: (id: string) => void;
}

function generateId(): string {
  return crypto.randomUUID?.() ?? `conv-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function firstLine(text: string, maxLen = 40): string {
  const line = text.split(/\n/)[0]?.trim() ?? "";
  return line.length > maxLen ? line.slice(0, maxLen) + "…" : line || "New chat";
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      conversations: [],
      activeConversationId: null,
      selectedModelId: DEFAULT_MODEL_ID,

      setSelectedModelId: (id) => set({ selectedModelId: id }),

      setActiveConversation: (id) => set({ activeConversationId: id }),

      createConversation: () => {
        const id = generateId();
        const conv: Conversation = {
          id,
          title: "New chat",
          messages: [],
          createdAt: Date.now(),
        };
        set((s) => ({
          conversations: [conv, ...s.conversations],
          activeConversationId: id,
        }));
        return id;
      },

      addMessage: (conversationId, message) => {
        set((s) => {
          const conv = s.conversations.find((c) => c.id === conversationId);
          if (!conv) return s;
          const title =
            conv.messages.length === 0 && message.role === "user"
              ? firstLine(message.content)
              : conv.title;
          return {
            conversations: s.conversations.map((c) =>
              c.id === conversationId
                ? { ...c, title, messages: [...c.messages, message] }
                : c
            ),
          };
        });
      },

      appendToConversation: (conversationId, message) => {
        get().addMessage(conversationId, message);
      },

      getConversation: (id) => get().conversations.find((c) => c.id === id),

      updateConversationTitle: (id, title) => {
        set((s) => ({
          conversations: s.conversations.map((c) =>
            c.id === id ? { ...c, title } : c
          ),
        }));
      },

      deleteConversation: (id) => {
        set((s) => {
          const next = s.conversations.filter((c) => c.id !== id);
          const active =
            s.activeConversationId === id
              ? next[0]?.id ?? null
              : s.activeConversationId;
          return { conversations: next, activeConversationId: active };
        });
      },
    }),
    { name: "chat-storage" }
  )
);
