import React from 'react';
import styled from '@emotion/styled';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 2rem;
  font-size: 2.5rem;
`;

const Subtitle = styled.h2`
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
`;

const Description = styled.p`
  color: #777;
  line-height: 1.6;
  margin-bottom: 2rem;
  font-size: 1.1rem;
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
`;

const FeatureCard = styled.div`
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const FeatureTitle = styled.h3`
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.2rem;
`;

const FeatureDescription = styled.p`
  color: #666;
  line-height: 1.5;
`;

const ActionCard = styled.div`
  margin-top: 3rem;
  padding: 2rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;

  &:hover {
    transform: translateY(-5px);
  }
`;

const ActionTitle = styled.h3`
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.4rem;
`;

const ActionDescription = styled.p`
  color: #666;
  margin-bottom: 1rem;
`;

const ActionButton = styled.button`
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #0056b3;
  }
`;

const MainPage = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleActionClick = () => {
    if (isAuthenticated) {
      navigate('/chat');
    } else {
      navigate('/login');
    }
  };

  return (
    <Container>
      <Title>BWMovie 추천 시스템</Title>
      <Subtitle>당신만을 위한 맞춤 영화 추천</Subtitle>
      <Description>
        BWMovie는 사용자의 취향을 분석하여 최적의 영화를 추천해드립니다.<br />
        새로운 영화 경험을 시작해보세요.
      </Description>
      
      <FeatureGrid>
        <FeatureCard>
          <FeatureTitle>개인 맞춤 추천</FeatureTitle>
          <FeatureDescription>
            사용자의 취향과 시청 기록을 분석하여 최적의 영화를 추천해드립니다.
          </FeatureDescription>
        </FeatureCard>
        
        <FeatureCard>
          <FeatureTitle>다양한 장르</FeatureTitle>
          <FeatureDescription>
            액션, 로맨스, 코미디, SF 등 다양한 장르의 영화를 제공합니다.
          </FeatureDescription>
        </FeatureCard>
        
        <FeatureCard>
          <FeatureTitle>실시간 업데이트</FeatureTitle>
          <FeatureDescription>
            최신 영화 정보와 평점을 실시간으로 업데이트합니다.
          </FeatureDescription>
        </FeatureCard>
      </FeatureGrid>

      <ActionCard onClick={handleActionClick}>
        {isAuthenticated ? (
          <>
            <ActionTitle>AI 채팅으로 영화 추천받기</ActionTitle>
            <ActionDescription>
              AI와 대화하면서 당신의 취향에 맞는 영화를 추천받아보세요.
            </ActionDescription>
            <ActionButton>채팅 시작하기</ActionButton>
          </>
        ) : (
          <>
            <ActionTitle>로그인하고 시작하기</ActionTitle>
            <ActionDescription>
              로그인하여 개인화된 영화 추천 서비스를 경험해보세요.
            </ActionDescription>
            <ActionButton>로그인하기</ActionButton>
          </>
        )}
      </ActionCard>
    </Container>
  );
};

export default MainPage; 