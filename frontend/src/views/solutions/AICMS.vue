<template>
  <div class="aicms">
    <h2>AI 기반 고객 관리</h2>
    
    <div class="aicms-content">
      <section class="overview-section">
        <h3>솔루션 개요</h3>
        <p>AICMS(AI Customer Management System)는 인공지능을 활용한 스마트 고객 관리 솔루션입니다. 고객 데이터 분석과 AI 기반 예측으로 고객 만족도를 높이고 비즈니스 성과를 개선합니다.</p>
      </section>

      <section class="features-section">
        <h3>주요 기능</h3>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-users"></i>
            </div>
            <h4>고객 프로파일링</h4>
            <ul>
              <li>고객 행동 패턴 분석</li>
              <li>세그먼트 자동 분류</li>
              <li>맞춤형 프로필 생성</li>
            </ul>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-comments"></i>
            </div>
            <h4>스마트 상담</h4>
            <ul>
              <li>AI 챗봇 상담</li>
              <li>감정 분석 기반 응대</li>
              <li>실시간 상담 품질 관리</li>
            </ul>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-chart-pie"></i>
            </div>
            <h4>데이터 분석</h4>
            <ul>
              <li>고객 만족도 분석</li>
              <li>이탈 위험 예측</li>
              <li>맞춤형 마케팅 제안</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="benefits-section">
        <h3>기대 효과</h3>
        <div class="benefits-grid">
          <div class="benefit-item">
            <div class="benefit-number">40%</div>
            <p>고객 만족도 향상</p>
          </div>
          <div class="benefit-item">
            <div class="benefit-number">35%</div>
            <p>상담 처리 시간 단축</p>
          </div>
          <div class="benefit-item">
            <div class="benefit-number">25%</div>
            <p>고객 이탈률 감소</p>
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
              <p>고객 만족도 45% 향상 달성</p>
            </div>
          </div>

          <div class="case-item">
            <div class="case-date">2024.02</div>
            <div class="case-content">
              <h4>통신사 B사</h4>
              <p>상담 처리 시간 40% 단축</p>
            </div>
          </div>

          <div class="case-item">
            <div class="case-date">2024.01</div>
            <div class="case-content">
              <h4>유통업체 C사</h4>
              <p>고객 이탈률 30% 감소</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.aicms {
  padding: 2rem;
}

.aicms h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.aicms-content {
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