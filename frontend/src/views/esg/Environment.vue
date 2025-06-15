<template>
  <div class="environment">
    <div class="environment-header">
      <i class="fas fa-leaf"></i>
      <div class="header-text">
        <h2>환경경영</h2>
        <p class="slogan">지속가능한 미래, 친환경 혁신</p>
      </div>
    </div>
    <div class="environment-content">
      <section class="vision-section">
        <h3>환경경영 비전</h3>
        <p>영우랩스는 '2050 탄소중립' 실현을 위한 환경경영을 추진하고 있습니다. 친환경 기술 혁신과 지속가능한 생산체계 구축을 통해 미래 세대를 위한 환경 보호에 기여하겠습니다.</p>
      </section>

      <section class="initiatives-section">
        <h3>주요 환경경영 이니셔티브</h3>
        <div class="initiatives-grid">
          <div class="initiative-card">
            <h4>탄소배출량 감축</h4>
            <ul>
              <li>사무실 전기 사용량 20% 감축 목표</li>
              <li>클라우드 서버 에너지 효율화</li>
              <li>재택근무 확대를 통한 이동 배출량 감소</li>
            </ul>
          </div>

          <div class="initiative-card">
            <h4>친환경 제품 개발</h4>
            <ul>
              <li>AI 기반 에너지 최적화 솔루션 개발</li>
              <li>친환경 소프트웨어 아키텍처 설계</li>
              <li>그린 IT 기술 연구 및 적용</li>
            </ul>
          </div>

          <div class="initiative-card">
            <h4>자원 재활용</h4>
            <ul>
              <li>전자폐기물 재활용 프로그램 운영</li>
              <li>종이 사용량 최소화 및 디지털화</li>
              <li>재사용 가능한 개발 환경 구축</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="achievements-section">
        <h3>환경경영 성과</h3>
        <div class="achievements-grid">
          <div class="achievement-item">
            <div class="achievement-number">30%</div>
            <p>전년 대비 탄소배출량 감소</p>
          </div>
          <div class="achievement-item">
            <div class="achievement-number">100%</div>
            <p>재생에너지 전력 사용</p>
          </div>
          <div class="achievement-item">
            <div class="achievement-number">50%</div>
            <p>종이 사용량 감소</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Environment'
}
</script>

<style scoped>
.environment {
  padding: 2rem;
}

.environment h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.environment-content {
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

.vision-section p {
  color: #4a4a4a;
  line-height: 1.8;
  font-size: 1.1rem;
}

.initiatives-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.initiative-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.initiative-card h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.initiative-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.initiative-card li {
  color: #4a4a4a;
  margin-bottom: 0.5rem;
  padding-left: 1.2rem;
  position: relative;
}

.initiative-card li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  text-align: center;
}

.achievement-item {
  padding: 1.5rem;
}

.achievement-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.achievement-item p {
  color: #4a4a4a;
  margin: 0;
}

@media (max-width: 1024px) {
  .initiatives-grid,
  .achievements-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .initiatives-grid,
  .achievements-grid {
    grid-template-columns: 1fr;
  }
}

.environment-header {
  display: flex;
  align-items: center;
  background: #eafaf2;
  border-radius: 10px;
  padding: 1.5rem 2rem 1.5rem 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(66,185,131,0.07);
}
.environment-header i {
  font-size: 2.5rem;
  color: #42b983;
  margin-right: 1.5rem;
}
.environment-header .header-text h2 {
  color: #2c3e50;
  margin-bottom: 0.3rem;
  font-size: 2rem;
}
.environment-header .slogan {
  color: #388e3c;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}
</style> 