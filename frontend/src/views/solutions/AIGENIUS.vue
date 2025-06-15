<template>
  <div class="aigenius">
    <h2>AI 기반 기업 지능화</h2>
    
    <div class="aigenius-content">
      <section class="overview-section">
        <h3>솔루션 개요</h3>
        <p>AIGENIUS(AI Generative Enterprise Intelligence & Understanding System)는 영우랩스의 최신 생성형 AI 기술을 활용한 기업 지능화 솔루션입니다. 기업의 모든 데이터를 생성형 AI로 분석하고 이해하여 최적의 의사결정을 지원합니다.</p>
      </section>

      <section class="features-section">
        <h3>주요 기능</h3>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-brain"></i>
            </div>
            <h4>지능형 데이터 분석</h4>
            <ul>
              <li>생성형 AI 기반 데이터 이해</li>
              <li>맥락 기반 패턴 분석</li>
              <li>실시간 인사이트 도출</li>
            </ul>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-comments"></i>
            </div>
            <h4>AI 비서</h4>
            <ul>
              <li>맥락 이해 기반 대화</li>
              <li>업무 자동화 지원</li>
              <li>맞춤형 보고서 생성</li>
            </ul>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-chart-network"></i>
            </div>
            <h4>지식 그래프</h4>
            <ul>
              <li>기업 지식 자동 구축</li>
              <li>연관성 기반 추론</li>
              <li>의사결정 지원</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="benefits-section">
        <h3>기대 효과</h3>
        <div class="benefits-grid">
          <div class="benefit-item">
            <div class="benefit-number">50%</div>
            <p>의사결정 시간 단축</p>
          </div>
          <div class="benefit-item">
            <div class="benefit-number">45%</div>
            <p>업무 효율성 향상</p>
          </div>
          <div class="benefit-item">
            <div class="benefit-number">99%</div>
            <p>맥락 이해 정확도</p>
          </div>
        </div>
      </section>

      <section class="cases-section">
        <h3>적용 사례</h3>
        <div class="cases-timeline">
          <div class="case-item">
            <div class="case-date">2024.03</div>
            <div class="case-content">
              <h4>금융기관 A사</h4>
              <p>고객 상담 처리 시간 60% 단축</p>
            </div>
          </div>

          <div class="case-item">
            <div class="case-date">2024.02</div>
            <div class="case-content">
              <h4>제조업체 B사</h4>
              <p>생산 계획 최적화로 수익 35% 증가</p>
            </div>
          </div>

          <div class="case-item">
            <div class="case-date">2024.01</div>
            <div class="case-content">
              <h4>연구기관 C사</h4>
              <p>연구 데이터 분석 시간 70% 감소</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIGENIUS'
}
</script>

<style scoped>
.aigenius {
  padding: 2rem;
}

.aigenius h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.aigenius-content {
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