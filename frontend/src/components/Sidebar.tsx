import { useChatStore } from "@/stores/chatStore";

export function Sidebar() {
  const conversations = useChatStore((s) => s.conversations);
  const activeConversationId = useChatStore((s) => s.activeConversationId);
  const setActiveConversation = useChatStore((s) => s.setActiveConversation);
  const createConversation = useChatStore((s) => s.createConversation);
  const deleteConversation = useChatStore((s) => s.deleteConversation);

  return (
    <aside className="sidebar">
      <button
        type="button"
        className="sidebar__new"
        onClick={() => createConversation()}
        aria-label="New chat"
      >
        + New chat
      </button>
      <nav className="sidebar__nav" aria-label="Conversations">
        {conversations.map((c) => (
          <div
            key={c.id}
            className={`sidebar__item ${activeConversationId === c.id ? "sidebar__item--active" : ""}`}
          >
            <button
              type="button"
              className="sidebar__item-btn"
              onClick={() => setActiveConversation(c.id)}
            >
              {c.title}
            </button>
            <button
              type="button"
              className="sidebar__item-delete"
              onClick={(e) => {
                e.stopPropagation();
                deleteConversation(c.id);
              }}
              aria-label={`Delete ${c.title}`}
            >
              ×
            </button>
          </div>
        ))}
      </nav>
    </aside>
  );
}
