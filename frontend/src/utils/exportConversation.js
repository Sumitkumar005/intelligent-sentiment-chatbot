export const exportAsText = (messages, conversationTitle) => {
  const title = conversationTitle || 'Conversation Export';
  const date = new Date().toLocaleString();
  let text = `${title}\n`;
  text += `Exported: ${date}\n`;
  text += `${'='.repeat(50)}\n\n`;
  messages.forEach((msg) => {
    const sender = msg.sender === 'user' ? 'You' : 'Bot';
    const timestamp = new Date(msg.timestamp).toLocaleTimeString();
    const sentiment = msg.sentiment ? ` [${msg.sentiment}]` : '';
    text += `[${timestamp}] ${sender}${sentiment}:\n`;
    text += `${msg.message_text}\n\n`;
  });
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `conversation-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
};
export const exportAsJSON = (messages, conversationTitle) => {
  const data = {
    title: conversationTitle || 'Conversation Export',
    exportedAt: new Date().toISOString(),
    messages: messages.map(msg => ({
      sender: msg.sender,
      text: msg.message_text,
      sentiment: msg.sentiment,
      timestamp: msg.timestamp
    }))
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `conversation-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
};