import { useMutation } from "@tanstack/react-query";
import { sendMessage, type ChatResponse } from "@/api/chat";
import { useChatStore } from "@/stores/chatStore";
import type { ChatMessage } from "@/stores/chatStore";

export type SendMessageVariables = {
  conversationId: string;
  messages: ChatMessage[];
  model: string;
};

export function useSendMessage() {
  const appendToConversation = useChatStore((s) => s.appendToConversation);

  return useMutation({
    mutationFn: async ({
      messages,
      model,
    }: SendMessageVariables): Promise<ChatResponse> => {
      return sendMessage(
        messages.map((m) => ({ role: m.role, content: m.content })),
        model
      );
    },
    onSuccess: (data, variables) => {
      if (data.message.content !== undefined) {
        appendToConversation(variables.conversationId, {
          role: "assistant",
          content: data.message.content,
          table: data.table ?? undefined,
        });
      }
    },
  });
}
