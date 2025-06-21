// 환경별 설정 관리
const env = import.meta.env.MODE || 'development';

const config = {
  development: {
    API_BASE_URL: '/api',
    APP_ENV: 'development',
    APP_TITLE: 'YWLABS AI Platform (Dev)',
    DEBUG: true,
    LOG_LEVEL: 'debug'
  },
  production: {
    API_BASE_URL: '/api',
    APP_ENV: 'production',
    APP_TITLE: 'YWLABS AI Platform',
    DEBUG: false,
    LOG_LEVEL: 'info'
  }
};

export const currentConfig = config[env] || config.development;

// 환경변수 우선 사용, 없으면 기본값 사용
export const getConfig = (key) => {
  const envKey = `VITE_${key}`;
  return import.meta.env[envKey] || currentConfig[key];
};

export default currentConfig; 