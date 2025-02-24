import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from '@emotion/styled';
import { signup } from '../api/auth';
import axiosInstance from '../api/axios.js';
import { useAuth } from '../contexts/AuthContext';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
`;

const SignupBox = styled.div`
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
`;

const Title = styled.h1`
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2rem;
  text-align: center;
  font-weight: 600;
`;

const Form = styled.form`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-size: 0.9rem;
  color: #4a5568;
  font-weight: 500;
`;

const Input = styled.input`
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s;
  
  &:focus {
    outline: none;
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
  }
  
  &::placeholder {
    color: #a0aec0;
  }
`;

const Button = styled.button`
  padding: 0.75rem;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 1rem;
  
  &:hover {
    background-color: #3182ce;
    transform: translateY(-1px);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const ErrorMessage = styled.p`
  color: #e53e3e;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
  background-color: #fff5f5;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #fed7d7;
`;

const FieldError = styled.span`
  color: #e53e3e;
  font-size: 0.8rem;
  margin-top: 0.2rem;
`;

const LoginLink = styled(Link)`
  margin-top: 1.5rem;
  color: #4299e1;
  text-decoration: none;
  text-align: center;
  display: block;
  font-size: 0.9rem;
  
  &:hover {
    text-decoration: underline;
  }
`;

const SignupPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    nickname: '',
    password: '',
    password2: '',
  });
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // 필드 에러 초기화
    setFieldErrors(prev => ({
      ...prev,
      [name]: ''
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // 1. 회원가입
      await signup(formData);
      
      // 2. 자동 로그인 수행
      const loginData = {
        username: formData.username,
        password: formData.password
      };
      await login(loginData);
      
      // 3. 선호도 선택 페이지로 이동
      navigate('/preferences');
    } catch (error) {
      if (typeof error === 'string') {
        setError(error);
      } else if (error.non_field_errors) {
        setError(error.non_field_errors[0]);
      } else if (error.message) {
        setError(error.message);
      } else {
        setError('회원가입 중 오류가 발생했습니다.');
      }
    }
  };

  return (
    <Container>
      <SignupBox>
        <Title>회원가입</Title>
        <Form onSubmit={handleSubmit}>
          <InputGroup>
            <Label htmlFor="username">아이디</Label>
            <Input
              id="username"
              type="text"
              name="username"
              placeholder="아이디를 입력하세요"
              value={formData.username}
              onChange={handleChange}
              required
            />
            {fieldErrors.username && <FieldError>{fieldErrors.username}</FieldError>}
          </InputGroup>
          <InputGroup>
            <Label htmlFor="nickname">닉네임</Label>
            <Input
              id="nickname"
              type="text"
              name="nickname"
              placeholder="닉네임을 입력하세요"
              value={formData.nickname}
              onChange={handleChange}
              required
            />
            {fieldErrors.nickname && <FieldError>{fieldErrors.nickname}</FieldError>}
          </InputGroup>
          <InputGroup>
            <Label htmlFor="password">비밀번호</Label>
            <Input
              id="password"
              type="password"
              name="password"
              placeholder="비밀번호를 입력하세요"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {fieldErrors.password && <FieldError>{fieldErrors.password}</FieldError>}
          </InputGroup>
          <InputGroup>
            <Label htmlFor="password2">비밀번호 확인</Label>
            <Input
              id="password2"
              type="password"
              name="password2"
              placeholder="비밀번호를 다시 입력하세요"
              value={formData.password2}
              onChange={handleChange}
              required
            />
            {fieldErrors.password2 && <FieldError>{fieldErrors.password2}</FieldError>}
          </InputGroup>
          <Button type="submit">가입하기</Button>
        </Form>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        <LoginLink to="/login">이미 계정이 있으신가요? 로그인</LoginLink>
      </SignupBox>
    </Container>
  );
};

export default SignupPage; 