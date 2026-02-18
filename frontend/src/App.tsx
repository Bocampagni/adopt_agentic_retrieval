import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Sidebar } from "@/components/Sidebar";
import { ChatArea } from "@/components/ChatArea";
import { DatabaseStructure } from "@/components/DatabaseStructure";
import { useChatStore } from "@/stores/chatStore";
import "./App.css";

const queryClient = new QueryClient();

function MainContent() {
  const sidebarView = useChatStore((s) => s.sidebarView);

  if (sidebarView === "database") return <DatabaseStructure />;
  return <ChatArea />;
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="app">
        <Sidebar />
        <MainContent />
      </div>
    </QueryClientProvider>
  );
}
