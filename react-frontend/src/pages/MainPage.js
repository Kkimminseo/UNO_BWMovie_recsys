import React from 'react';
import styled from '@emotion/styled';

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

const MainPage = () => {
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
    </Container>
  );
};

export default MainPage; 