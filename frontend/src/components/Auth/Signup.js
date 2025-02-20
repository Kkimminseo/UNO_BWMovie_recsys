import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../../api/auth';
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Alert,
} from '@mui/material';

const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    password2: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.password2) {
      setError('비밀번호가 일치하지 않습니다.');
      return;
    }

    try {
      const response = await authAPI.signup({
        username: formData.username,
        password: formData.password,
      });
      console.log('회원가입 성공:', response);
      navigate('/login');
    } catch (error) {
      setError(error.message || '회원가입에 실패했습니다.');
    }
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          회원가입
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="사용자 이름"
            name="username"
            autoComplete="username"
            autoFocus
            value={formData.username}
            onChange={handleChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="비밀번호"
            type="password"
            id="password"
            autoComplete="new-password"
            value={formData.password}
            onChange={handleChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password2"
            label="비밀번호 확인"
            type="password"
            id="password2"
            autoComplete="new-password"
            value={formData.password2}
            onChange={handleChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            회원가입
          </Button>
          <Button
            fullWidth
            variant="text"
            onClick={() => navigate('/login')}
          >
            이미 계정이 있으신가요? 로그인
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Signup; 