<template>
  <div class="solution">
    <h1>AICDMS</h1>
    <div class="solution-content">
      <div class="solution-header">
        <h2>AI 기반 중대재해 모니터링 시스템</h2>
        <p class="subtitle">스마트 안전 관리를 위한 AI 솔루션</p>
      </div>
      
      <div class="solution-features">
        <div class="feature">
          <h3>실시간 위험 감지</h3>
          <p>AI 기반 실시간 안전 위험 요소 감지 및 분석</p>
        </div>
        <div class="feature">
          <h3>예측적 안전 관리</h3>
          <p>중대재해 발생 가능성 사전 예측 및 대응</p>
        </div>
        <div class="feature">
          <h3>자동 대응 시스템</h3>
          <p>위험 상황 발생 시 자동 대응 및 보고 체계</p>
        </div>
      </div>

      <div class="solution-benefits">
        <h3>주요 효과</h3>
        <ul>
          <li>안전사고 예방률 70% 향상</li>
          <li>위험 감지 시간 80% 단축</li>
          <li>안전 관리 비용 40% 절감</li>
          <li>긴급 대응 시간 60% 감소</li>
        </ul>
      </div>

      <div class="contact-section">
        <h3>문의하기</h3>
        <p>더 자세한 정보가 필요하신가요?</p>
        <router-link to="/contact" class="contact-button">문의하기</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AICDMS'
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
</style> 