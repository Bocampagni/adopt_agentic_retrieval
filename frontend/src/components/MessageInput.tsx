import { useState } from "react";
import { useSendMessage } from "@/hooks/useSendMessage";
import { useChatStore } from "@/stores/chatStore";
import { DEFAULT_MODEL_ID } from "@/config/models";

export function MessageInput() {
  const [value, setValue] = useState("");
  const activeConversationId = useChatStore((s) => s.activeConversationId);
  const getConversation = useChatStore((s) => s.getConversation);
  const addMessage = useChatStore((s) => s.addMessage);
  const createConversation = useChatStore((s) => s.createConversation);
  const selectedModelId = useChatStore((s) => s.selectedModelId) || DEFAULT_MODEL_ID;

  const sendMutation = useSendMessage();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = value.trim();
    if (!text || sendMutation.isPending) return;

    let convId = activeConversationId;
    if (!convId) {
      convId = createConversation();
    }
    const userMessage = { role: "user" as const, content: text };
    addMessage(convId, userMessage);
    setValue("");

    const conv = getConversation(convId);
    const messages = conv?.messages ?? [userMessage];

    sendMutation.mutate({
      conversationId: convId,
      messages,
      model: selectedModelId,
    });
  };

  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <textarea
        className="message-input__field"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
          }
        }}
        placeholder="Type a message…"
        rows={1}
        disabled={sendMutation.isPending}
        aria-label="Message"
      />
      <button
        type="submit"
        className="message-input__submit"
        disabled={!value.trim() || sendMutation.isPending}
        aria-label="Send"
      >
        {sendMutation.isPending ? "…" : "Send"}
      </button>
    </form>
  );
}
