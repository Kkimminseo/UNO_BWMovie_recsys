import React from 'react';
import styled from '@emotion/styled';
import { useNavigate, Link } from 'react-router-dom';
import { logout } from '../api/auth';
import { useAuth } from '../contexts/AuthContext';

const Nav = styled.nav`
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const NavContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.h1`
  color: #007bff;
  margin: 0;
  font-size: 1.5rem;
  cursor: pointer;
  
  &:hover {
    color: #0056b3;
  }
`;

const NavLinks = styled.div`
  display: flex;
  align-items: center;
  gap: 2rem;
`;

const NavLink = styled(Link)`
  color: #333;
  text-decoration: none;
  font-size: 1rem;
  
  &:hover {
    color: #007bff;
  }
`;

const Button = styled.button`
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  background-color: ${props => props.primary ? '#007bff' : '#f8f9fa'};
  color: ${props => props.primary ? '#fff' : '#333'};
  
  &:hover {
    background-color: ${props => props.primary ? '#0056b3' : '#e9ecef'};
  }
`;

const Navbar = () => {
  const navigate = useNavigate();
  const { setIsAuthenticated } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
      setIsAuthenticated(false);
      navigate('/');
    } catch (error) {
      console.error('로그아웃 중 오류가 발생했습니다:', error);
    }
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  return (
    <Nav>
      <NavContainer>
        <Logo onClick={handleLogoClick}>BWMovie</Logo>
        <NavLinks>
          <NavLink to="/chat">AI 채팅</NavLink>
          <Button onClick={handleLogout}>로그아웃</Button>
        </NavLinks>
      </NavContainer>
    </Nav>
  );
};

export default Navbar; 