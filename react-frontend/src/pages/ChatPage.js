import React, { useState, useRef, useEffect } from 'react';
import styled from '@emotion/styled';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
`;

const ChatContainer = styled.div`
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  overflow-y: auto;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 0.8rem 1rem;
  border-radius: 1rem;
  background-color: ${props => props.isUser ? '#007bff' : '#e9ecef'};
  color: ${props => props.isUser ? '#fff' : '#333'};
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  word-wrap: break-word;
`;

const InputContainer = styled.form`
  display: flex;
  gap: 1rem;
`;

const Input = styled.input`
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }
`;

const Button = styled.button`
  padding: 0 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  
  &:hover {
    background-color: #0056b3;
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const LoadingDots = styled.div`
  display: flex;
  gap: 0.3rem;
  padding: 0.8rem 1rem;
  background-color: #e9ecef;
  border-radius: 1rem;
  align-self: flex-start;
  
  span {
    width: 0.5rem;
    height: 0.5rem;
    background-color: #adb5bd;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
    
    &:nth-of-type(1) { animation-delay: -0.32s; }
    &:nth-of-type(2) { animation-delay: -0.16s; }
  }
  
  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    console.log("🔍 WebSocket 연결 시도...");
    const ws = new WebSocket("ws://localhost:8000/ws/chat/");

    ws.onopen = () => {
      console.log("✅ WebSocket 연결 성공!");
    };

    ws.onmessage = (event) => {
      console.log("📩 받은 메시지:", event.data);
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, { text: data.response, isUser: false }]);
      } catch (error) {
        console.error("❌ WebSocket 메시지 JSON 파싱 오류:", error);
      }
    };

    ws.onerror = (error) => {
      console.error("❌ WebSocket 오류 발생:", error);
    };

    ws.onclose = () => {
      console.log("❌ WebSocket 연결 종료");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  // 새 메시지가 추가될 때마다 스크롤을 맨 아래로 이동
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading || !socket) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    try {
      console.log("📤 메시지 전송:", userMessage);
      socket.send(JSON.stringify({ message: userMessage }));
    } catch (error) {
      setMessages(prev => [...prev, { text: '메시지 전송 실패', isUser: false, isError: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <Title>AI 채팅</Title>
      <ChatContainer ref={chatContainerRef}>
        {messages.map((message, index) => (
          <MessageBubble 
            key={index} 
            isUser={message.isUser}
            style={message.isError ? { backgroundColor: '#dc3545', color: '#fff' } : {}}
          >
            {message.text}
          </MessageBubble>
        ))}
        {isLoading && (
          <LoadingDots>
            <span />
            <span />
            <span />
          </LoadingDots>
        )}
      </ChatContainer>
      <InputContainer onSubmit={sendMessage}>
        <Input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="메시지를 입력하세요..."
          disabled={isLoading}
        />
        <Button type="submit" disabled={isLoading || !inputMessage.trim()}>
          전송
        </Button>
      </InputContainer>
    </Container>
  );
};

export default ChatPage;
