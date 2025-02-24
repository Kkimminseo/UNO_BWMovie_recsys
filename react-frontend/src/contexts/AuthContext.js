import React, { createContext, useState, useContext } from 'react';
import { login as authLogin } from '../api/auth';

const AuthContext = createContext(null);

// AuthProvider 컴포넌트는 인증 상태를 관리하고, 자식 컴포넌트에 인증 관련 정보를 제공한다.
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem('access_token') // 로컬 스토리지에서 access_token이 존재하는지 확인하여 초기 인증 상태 설정
  );

  // 로그인 함수는 사용자 인증을 처리하고, 성공 시 인증 상태를 업데이트한다.
  const login = async (credentials) => {
    try {
      const response = await authLogin(credentials); // 인증 API 호출
      setIsAuthenticated(true); // 인증 성공 시 상태 업데이트
      return response; // 응답 반환
    } catch (error) {
      throw error; // 오류 발생 시 다시 던짐
    }
  };

  const value = {
    isAuthenticated,
    setIsAuthenticated,
    login
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>; // 자식 컴포넌트에 인증 정보 제공
};

// useAuth 훅은 AuthContext에서 인증 정보를 가져오는 데 사용된다.
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error('useAuth must be used within an AuthProvider'); // AuthProvider 외부에서 사용 시 오류 발생
  }
  return context; // 인증 정보 반환
}; 