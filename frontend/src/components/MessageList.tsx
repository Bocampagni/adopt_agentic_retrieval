import type { ChatMessage } from "@/stores/chatStore";
import { DataTable } from "./DataTable";

interface MessageListProps {
  messages: ChatMessage[];
}

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) return null;
  return (
    <ul className="message-list" aria-label="Chat messages">
      {messages.map((m, i) => (
        <li
          key={i}
          className={`message message--${m.role}${m.table ? " message--has-table" : ""}`}
          data-role={m.role}
        >
          <span className="message__role">{m.role === "user" ? "You" : "Assistant"}</span>
          <div className="message__content">{m.content}</div>
          {m.table && <DataTable columns={m.table.columns} rows={m.table.rows} />}
        </li>
      ))}
    </ul>
  );
}
