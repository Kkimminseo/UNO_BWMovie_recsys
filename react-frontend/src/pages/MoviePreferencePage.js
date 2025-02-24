import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { movieApi } from '../api/movieApi';
import styled from '@emotion/styled';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

const Title = styled.h1`
  text-align: center;
  margin-bottom: 1rem;
`;

const SubTitle = styled.p`
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
`;

const MovieGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
`;

const MovieCard = styled.div`
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
  border: ${props => props.selected ? '3px solid #3B82F6' : '3px solid transparent'};

  &:hover {
    transform: translateY(-5px);
  }
`;

const MovieImage = styled.img`
  width: 100%;
  height: 300px;
  object-fit: cover;
`;

const MovieTitle = styled.div`
  padding: 1rem;
  text-align: center;
  font-weight: 500;
`;

const SubmitButton = styled.button`
  display: block;
  width: 200px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: ${props => props.disabled ? '#94A3B8' : '#3B82F6'};
  color: white;
  border: none;
  border-radius: 8px;
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  font-size: 1rem;
  font-weight: 500;

  &:hover {
    background-color: ${props => props.disabled ? '#94A3B8' : '#2563EB'};
  }
`;

const MoviePreferencePage = () => {
  const [movies, setMovies] = useState([]);
  const [selectedMovies, setSelectedMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await movieApi.getInitialMovies();
        setMovies(response.data);
      } catch (error) {
        console.error('영화 목록 로딩 실패:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMovies();
  }, []);

  const handleMovieSelect = (movieId) => {
    setSelectedMovies(prev => {
      if (prev.includes(movieId)) {
        return prev.filter(id => id !== movieId);
      }
      if (prev.length < 5) {
        return [...prev, movieId];
      }
      return prev;
    });
  };

  const handleSubmit = async () => {
    try {
      await movieApi.saveMoviePreferences(selectedMovies);
      navigate('/'); // 메인 페이지로 이동
    } catch (error) {
      console.error('선호도 저장 실패:', error);
      alert('선호도 저장에 실패했습니다. 다시 시도해주세요.');
    }
  };

  if (isLoading) {
    return <Container>로딩 중...</Container>;
  }

  return (
    <Container>
      <Title>좋아하는 영화를 선택해주세요</Title>
      <SubTitle>최대 5개까지 선택할 수 있습니다. ({selectedMovies.length}/5)</SubTitle>
      
      <MovieGrid>
        {movies.map(movie => (
          <MovieCard 
            key={movie.id}
            selected={selectedMovies.includes(movie.id)}
            onClick={() => handleMovieSelect(movie.id)}
          >
            <MovieImage 
              src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} 
              alt={movie.original_title} 
            />
            <MovieTitle>{movie.original_title}</MovieTitle>
          </MovieCard>
        ))}
      </MovieGrid>

      <SubmitButton 
        disabled={selectedMovies.length === 0}
        onClick={handleSubmit}
      >
        선택 완료
      </SubmitButton>
    </Container>
  );
};

export default MoviePreferencePage; 