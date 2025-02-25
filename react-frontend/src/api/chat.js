import axiosInstance from './axios';

const API_URL = "http://127.0.0.1:8000/ws/chat/";

export const sendMessage = async (message) => {
    try {
        const response = await axiosInstance.post(API_URL, { message });

        // 서버에서 응답을 받으면 안성재, 백종원의 응답 및 음성 파일 URL을 포함할 가능성이 있음
        return {
            ansungjae_text: response.data.ansungjae_text, // 안성재 답변
            ansungjae_audio: response.data.ansungjae_audio || null, // 안성재 음성 파일
            paik_text: response.data.paik_text, // 백종원 답변
            paik_audio: response.data.paik_audio || null, // 백종원 음성 파일
        };
    } catch (error) {
        console.error("Error sending message:", error);
        return { 
            ansungjae_text: "오류가 발생했습니다.", 
            ansungjae_audio: null, 
            paik_text: "오류가 발생했습니다.", 
            paik_audio: null 
        };
    }
};
