import axios from 'axios';

// Vite 환경변수 사용
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});

// 토큰 갱신 상태 관리
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

// 토큰 만료 시간 확인 함수
const isTokenExpiringSoon = (token) => {
  if (!token) return false;
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expTime = payload.exp * 1000; // 밀리초로 변환
    const currentTime = Date.now();
    const timeUntilExpiry = expTime - currentTime;
    
    // 10분(600,000ms) 이내에 만료되면 갱신 필요
    return timeUntilExpiry < 600000;
  } catch (error) {
    console.error('토큰 파싱 오류:', error);
    return false;
  }
};

// 토큰 갱신 함수
const refreshToken = async () => {
  try {
    const currentToken = localStorage.getItem('jwt_token');
    if (!currentToken) {
      throw new Error('갱신할 토큰이 없습니다.');
    }
    
    // 토큰 갱신 API 호출 (백엔드에서 구현 필요)
    const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {}, {
      headers: {
        'Authorization': `Bearer ${currentToken}`
      }
    });
    
    const { token: newToken } = response.data;
    if (newToken) {
      localStorage.setItem('jwt_token', newToken);
      return newToken;
    }
    
    throw new Error('새 토큰을 받지 못했습니다.');
  } catch (error) {
    console.error('토큰 갱신 실패:', error);
    throw error;
  }
};

// 요청 인터셉터: JWT 토큰 자동 첨부 및 갱신
api.interceptors.request.use(async config => {
  const token = localStorage.getItem('jwt_token');
  
  if (token) {
    // 토큰이 곧 만료될 예정인지 확인
    if (isTokenExpiringSoon(token)) {
      if (!isRefreshing) {
        isRefreshing = true;
        
        try {
          const newToken = await refreshToken();
          config.headers['Authorization'] = `Bearer ${newToken}`;
        } catch (error) {
          // 갱신 실패 시 로그아웃 처리
          localStorage.removeItem('jwt_token');
          localStorage.removeItem('user_info');
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
          return Promise.reject(error);
        } finally {
          isRefreshing = false;
        }
      } else {
        // 이미 갱신 중인 경우 대기
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          config.headers['Authorization'] = `Bearer ${token}`;
          return config;
        }).catch(err => {
          return Promise.reject(err);
        });
      }
    } else {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
  }
  
  return config;
});

// 응답 인터셉터: 401(인증 만료) 시 토큰 갱신 시도
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 이미 갱신 중인 경우 대기
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`;
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }
      
      originalRequest._retry = true;
      isRefreshing = true;
      
      try {
        const newToken = await refreshToken();
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // 갱신 실패 시 로그아웃 처리
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('user_info');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    
    return Promise.reject(error);
  }
);

// 사용자 활동 감지 및 토큰 갱신
let activityTimeout;
const resetActivityTimeout = () => {
  clearTimeout(activityTimeout);
  activityTimeout = setTimeout(async () => {
    const token = localStorage.getItem('jwt_token');
    if (token && isTokenExpiringSoon(token)) {
      try {
        await refreshToken();
        console.log('사용자 활동 기반 토큰 갱신 완료');
      } catch (error) {
        console.error('활동 기반 토큰 갱신 실패:', error);
      }
    }
  }, 300000); // 5분마다 체크
};

// 이벤트 리스너 등록
const setupActivityListeners = () => {
  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
  events.forEach(event => {
    document.addEventListener(event, resetActivityTimeout, true);
  });
  
  // 페이지 가시성 변경 시
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      resetActivityTimeout();
    }
  });
  
  // 탭 포커스 시
  window.addEventListener('focus', resetActivityTimeout);
};

// 초기화
setupActivityListeners();
resetActivityTimeout();

export default api; 