import { useChatStore } from "@/stores/chatStore";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import { ModelSelector } from "./ModelSelector";

export function ChatArea() {
  // Subscribe to the active conversation so we re-render when its messages change
  const active = useChatStore((s) => {
    const id = s.activeConversationId;
    return id ? s.conversations.find((c) => c.id === id) : null;
  });

  return (
    <main className="chat-area">
      <header className="chat-area__header">
        <ModelSelector />
      </header>
      <div className="chat-area__body">
        {!active ? (
          <div className="chat-area__empty">
            <p className="chat-area__empty-title">New conversation</p>
            <p className="chat-area__empty-hint">
              Start a new chat from the sidebar or type below to create one.
            </p>
          </div>
        ) : (
          <MessageList messages={active.messages} />
        )}
      </div>
      <div className="chat-area__footer">
        <MessageInput />
      </div>
    </main>
  );
}
