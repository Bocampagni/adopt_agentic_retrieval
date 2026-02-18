import { useChatStore } from "@/stores/chatStore";
import type { SidebarView } from "@/stores/chatStore";

const NAV_ITEMS: { id: SidebarView; label: string; icon: string }[] = [
  { id: "chat", label: "Conversations", icon: "💬" },
  { id: "database", label: "Database", icon: "🗄️" },
];

export function Sidebar() {
  const sidebarView = useChatStore((s) => s.sidebarView);
  const setSidebarView = useChatStore((s) => s.setSidebarView);
  const conversations = useChatStore((s) => s.conversations);
  const activeConversationId = useChatStore((s) => s.activeConversationId);
  const setActiveConversation = useChatStore((s) => s.setActiveConversation);
  const createConversation = useChatStore((s) => s.createConversation);
  const deleteConversation = useChatStore((s) => s.deleteConversation);

  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <span className="sidebar__logo">A</span>
        <span className="sidebar__brand-name">Agentic Chat</span>
      </div>

      <nav className="sidebar__tabs">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`sidebar__tab ${sidebarView === item.id ? "sidebar__tab--active" : ""}`}
            onClick={() => setSidebarView(item.id)}
          >
            <span className="sidebar__tab-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar__content">
        {sidebarView === "chat" && (
          <>
            <button
              type="button"
              className="sidebar__new"
              onClick={() => createConversation()}
            >
              + New chat
            </button>
            <div className="sidebar__list">
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
            </div>
          </>
        )}

        {sidebarView === "database" && (
          <div className="sidebar__section-hint">
            <p>Explore the connected data source structure and preview sample rows.</p>
          </div>
        )}
      </div>
    </aside>
  );
}
