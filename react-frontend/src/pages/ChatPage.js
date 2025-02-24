import React, { useState, useRef, useEffect } from 'react';
import styled from '@emotion/styled';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SendIcon from '@mui/icons-material/Send';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 0.5rem;
  height: 85vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  position: fixed;
  top: calc(50% + 32px);
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  z-index: 1;
`;

const Title = styled.h1`
  color: #333;
  margin: 0;
  text-align: center;
  font-size: 1.3rem;
  padding: 0.5rem 0;
`;

const ChatContainer = styled.div`
  flex: 1;
  min-height: 0;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 0.8rem;
  overflow-y: auto;
  margin-bottom: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  height: calc(70vh - 120px);
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 1rem 1.2rem;
  border-radius: 1.2rem;
  background-color: ${props => props.isUser ? '#1a73e8' : '#f1f3f4'};
  color: ${props => props.isUser ? '#fff' : '#333'};
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  word-wrap: break-word;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);

  .message-time {
    font-size: 0.75rem;
    color: ${props => props.isUser ? 'rgba(255, 255, 255, 0.7)' : '#666'};
    margin-top: 0.5rem;
  }

  .message-content {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
  }
`;

const InputContainer = styled.form`
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem 0;
  position: relative;
  bottom: 0;
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
  background-color: #1a73e8;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: #1557b0;
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const TypingIndicator = styled.div`
  padding: 0.8rem 1rem;
  background-color: #e9ecef;
  border-radius: 1rem;
  align-self: flex-start;
  color: #666;
  font-style: italic;
`;

const LoadingDots = styled.span`
  &::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
    
    @keyframes dots {
      0%, 20% { content: ''; }
      40% { content: '.'; }
      60% { content: '..'; }
      80%, 100% { content: '...'; }
    }
  }
`;

const AIIcon = styled.img`
  width: 24px;
  height: 24px;
  object-fit: contain;
`;

const Spinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-left: 8px;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // 초기 안내 메시지 추가
    setMessages([{
      text: "안녕하세요! 어떤영화를 추천해드릴까요?",
      isUser: false
    }]);

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
        setIsLoading(false);
      } catch (error) {
        console.error("❌ WebSocket 메시지 JSON 파싱 오류:", error);
        setIsLoading(false);
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
    
    socket.send(JSON.stringify({ message: inputMessage }));
    setMessages(prev => [...prev, { text: inputMessage, isUser: true }]);
    setInputMessage('');
    setIsLoading(true);
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
            <div className="message-content">
              {!message.isUser && <SmartToyIcon style={{ color: '#1a73e8' }} />}
              <span>{message.text}</span>
            </div>
            <div className="message-time">
              {new Date().toLocaleTimeString('ko-KR', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </MessageBubble>
        ))}
        {isLoading && (
          <TypingIndicator>
            <SmartToyIcon style={{ color: '#1a73e8' }} />
            AI가 답변을 작성중입니다<LoadingDots />
          </TypingIndicator>
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
          전송 {isLoading && <Spinner />} {!isLoading && <SendIcon />}
        </Button>
      </InputContainer>
    </Container>
  );
};

export default ChatPage;
