<template>
  <div class="solution">
    <h1>AIMASASIKI</h1>
    <div class="solution-content">
      <div class="solution-header">
        <h2>AI 기반 제조 생산성 향상 솔루션</h2>
        <p class="subtitle">스마트 제조를 위한 AI 기반 생산성 최적화 솔루션</p>
      </div>
      
      <div class="solution-features">
        <div class="feature">
          <h3>실시간 생산 모니터링</h3>
          <p>생산라인의 실시간 데이터 수집 및 분석으로 생산성 향상</p>
        </div>
        <div class="feature">
          <h3>예측 유지보수</h3>
          <p>AI 기반 장비 고장 예측으로 사전 유지보수 가능</p>
        </div>
        <div class="feature">
          <h3>품질 관리</h3>
          <p>컴퓨터 비전 기반 불량품 검출 시스템</p>
        </div>
      </div>

      <div class="solution-benefits">
        <h3>주요 효과</h3>
        <ul>
          <li>생산성 30% 향상</li>
          <li>설비 가동률 25% 개선</li>
          <li>불량률 40% 감소</li>
          <li>에너지 사용량 20% 절감</li>
        </ul>
      </div>

      <div class="contact-section">
        <h3>문의하기</h3>
        <p>더 자세한 정보가 필요하신가요?</p>
        <router-link to="/contact" class="contact-button">문의하기</router-link>
      </div>
    </div>
    <FloatingMenu />
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'AIMASASIKI',
  components: { FloatingMenu },
  methods: {
    navigateTo(url) {
      if (url) {
        this.$router.push(url)
      }
    }
  }
}
</script>

<style scoped>
.solution {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.solution-content {
  margin-top: 2rem;
}

.solution-header {
  text-align: center;
  margin-bottom: 3rem;
}

.solution-header h2 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.subtitle {
  color: #666;
  font-size: 1.2rem;
}

.solution-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.feature h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature p {
  color: #666;
  line-height: 1.6;
}

.solution-benefits {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 3rem;
}

.solution-benefits h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.solution-benefits ul {
  list-style-type: none;
  padding: 0;
}

.solution-benefits li {
  color: #666;
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}

.solution-benefits li::before {
  content: '✓';
  color: #42b983;
  position: absolute;
  left: 0;
}

.contact-section {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.contact-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.contact-button {
  display: inline-block;
  background: #42b983;
  color: white;
  padding: 1rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  margin-top: 1rem;
  transition: background-color 0.3s;
}

.contact-button:hover {
  background: #3aa876;
}

.floating-menu {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.floating-button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.floating-button:hover {
  background: #0056b3;
}
</style> 