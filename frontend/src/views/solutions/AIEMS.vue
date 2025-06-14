<template>
  <div class="aiems">
    <h2>AI 기반 에너지 관리</h2>
    
    <div class="aiems-content">
      <section class="overview-section">
        <h3>솔루션 개요</h3>
        <p>AIEMS(AI Energy Management System)는 영우랩스의 특화된 AI 기술을 활용한 스마트 에너지 관리 솔루션입니다. 실시간 에너지 모니터링, 탄소중립 관리, 생성형 AI 기반 최적화로 기업의 에너지 효율을 극대화합니다.</p>
      </section>

      <section class="features-section">
        <h3>주요 기능</h3>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-chart-line"></i>
            </div>
            <h4>에너지 통합 대시보드</h4>
            <ul>
              <li>실시간 에너지 사용량 모니터링</li>
              <li>다양한 에너지원 통합 관리</li>
              <li>직관적인 데이터 시각화</li>
            </ul>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-leaf"></i>
            </div>
            <h4>탄소중립 대시보드</h4>
            <ul>
              <li>탄소배출량 실시간 추적</li>
              <li>탄소중립 목표 달성 관리</li>
              <li>ESG 지표 통합 분석</li>
            </ul>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-robot"></i>
            </div>
            <h4>생성형 AI 최적화</h4>
            <ul>
              <li>AI 기반 에너지 사용 최적화</li>
              <li>맞춤형 절감 방안 제안</li>
              <li>예측적 유지보수 관리</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="benefits-section">
        <h3>기대 효과</h3>
        <div class="benefits-grid">
          <div class="benefit-item">
            <div class="benefit-number">40%</div>
            <p>에너지 비용 절감</p>
          </div>
          <div class="benefit-item">
            <div class="benefit-number">35%</div>
            <p>탄소배출량 감소</p>
          </div>
          <div class="benefit-item">
            <div class="benefit-number">98%</div>
            <p>예측 정확도</p>
          </div>
        </div>
      </section>

      <section class="cases-section">
        <h3>적용 사례</h3>
        <div class="cases-timeline">
          <div class="case-item">
            <div class="case-date">2024.03</div>
            <div class="case-content">
              <h4>제조업체 A사</h4>
              <p>탄소중립 목표 2년 조기 달성</p>
            </div>
          </div>

          <div class="case-item">
            <div class="case-date">2024.02</div>
            <div class="case-content">
              <h4>상업시설 B사</h4>
              <p>에너지 비용 45% 절감 달성</p>
            </div>
          </div>

          <div class="case-item">
            <div class="case-date">2024.01</div>
            <div class="case-content">
              <h4>공공기관 C사</h4>
              <p>ESG 평가 등급 2단계 상승</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIEMS'
}
</script>

<style scoped>
.aiems {
  padding: 2rem;
}

.aiems h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.aiems-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

section {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

section h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.4rem;
}

.overview-section p {
  color: #4a4a4a;
  line-height: 1.8;
  font-size: 1.1rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.feature-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.feature-icon {
  font-size: 2.5rem;
  color: #42b983;
  margin-bottom: 1rem;
}

.feature-card h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.feature-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
}

.feature-card li {
  color: #4a4a4a;
  margin-bottom: 0.5rem;
  padding-left: 1.2rem;
  position: relative;
}

.feature-card li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  text-align: center;
}

.benefit-item {
  padding: 1.5rem;
}

.benefit-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.benefit-item p {
  color: #4a4a4a;
  margin: 0;
}

.cases-timeline {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.case-item {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.case-date {
  min-width: 100px;
  color: #42b983;
  font-weight: bold;
}

.case-content h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.case-content p {
  color: #4a4a4a;
  margin: 0;
}

@media (max-width: 1024px) {
  .features-grid,
  .benefits-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .features-grid,
  .benefits-grid {
    grid-template-columns: 1fr;
  }

  .case-item {
    flex-direction: column;
    gap: 0.5rem;
  }

  .case-date {
    min-width: auto;
  }
}
</style> 