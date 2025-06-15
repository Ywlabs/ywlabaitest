<template>
  <div class="compliance">
    <div class="compliance-header">
      <i class="fas fa-balance-scale"></i>
      <div class="header-text">
        <h2>준법경영</h2>
        <p class="slogan">윤리와 투명성으로 신뢰받는 기업</p>
      </div>
    </div>
    <div class="compliance-content">
      <section class="vision-section">
        <h3>준법경영 비전</h3>
        <p>영우랩스는 '윤리적이고 투명한 경영'을 최우선 가치로 삼고 있습니다. 모든 임직원이 준법과 윤리를 바탕으로 한 의사결정을 통해 지속가능한 기업 가치를 실현하겠습니다.</p>
      </section>

      <section class="principles-section">
        <h3>준법경영 원칙</h3>
        <div class="principles-grid">
          <div class="principle-card">
            <h4>윤리경영</h4>
            <ul>
              <li>임직원 윤리강령 준수</li>
              <li>부패방지 및 청렴성 확보</li>
              <li>공정한 거래 관행</li>
            </ul>
          </div>

          <div class="principle-card">
            <h4>투명성</h4>
            <ul>
              <li>정보공시 의무 준수</li>
              <li>이해관계자 소통 강화</li>
              <li>공정한 지배구조</li>
            </ul>
          </div>

          <div class="principle-card">
            <h4>리스크 관리</h4>
            <ul>
              <li>내부통제 체계 구축</li>
              <li>법규 준수 모니터링</li>
              <li>위기관리 체계</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="system-section">
        <h3>준법경영 체계</h3>
        <div class="system-timeline">
          <div class="system-item">
            <div class="system-step">01</div>
            <div class="system-content">
              <h4>준법경영 조직</h4>
              <p>전담 조직을 통한 체계적인 준법경영 관리</p>
            </div>
          </div>

          <div class="system-item">
            <div class="system-step">02</div>
            <div class="system-content">
              <h4>교육 및 점검</h4>
              <p>정기적인 준법교육과 모니터링 실시</p>
            </div>
          </div>

          <div class="system-item">
            <div class="system-step">03</div>
            <div class="system-content">
              <h4>신고 및 조치</h4>
              <p>윤리신고센터 운영 및 신속한 조치</p>
            </div>
          </div>
        </div>
      </section>

      <section class="certification-section">
        <h3>인증 및 평가</h3>
        <div class="certification-grid">
          <div class="certification-item">
            <div class="certification-icon">
              <i class="fas fa-award"></i>
            </div>
            <h4>ISO 37001</h4>
            <p>부패방지경영시스템</p>
          </div>

          <div class="certification-item">
            <div class="certification-icon">
              <i class="fas fa-shield-alt"></i>
            </div>
            <h4>ISO 37301</h4>
            <p>준법경영시스템</p>
          </div>

          <div class="certification-item">
            <div class="certification-icon">
              <i class="fas fa-check-circle"></i>
            </div>
            <h4>ESG 평가</h4>
            <p>지배구조 우수기업</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Compliance'
}
</script>

<style scoped>
.compliance {
  padding: 2rem;
}

.compliance h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.compliance-content {
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

.principles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.principle-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.principle-card h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.principle-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.principle-card li {
  color: #4a4a4a;
  margin-bottom: 0.5rem;
  padding-left: 1.2rem;
  position: relative;
}

.principle-card li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.system-timeline {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.system-item {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.system-step {
  min-width: 60px;
  height: 60px;
  background: #42b983;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.system-content h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.system-content p {
  color: #4a4a4a;
  margin: 0;
}

.certification-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  text-align: center;
}

.certification-item {
  padding: 1.5rem;
}

.certification-icon {
  font-size: 2.5rem;
  color: #42b983;
  margin-bottom: 1rem;
}

.certification-item h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.certification-item p {
  color: #4a4a4a;
  margin: 0;
}

@media (max-width: 1024px) {
  .principles-grid,
  .certification-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .principles-grid,
  .certification-grid {
    grid-template-columns: 1fr;
  }

  .system-item {
    flex-direction: column;
    gap: 1rem;
  }

  .system-step {
    margin: 0 auto;
  }
}

.compliance-header {
  display: flex;
  align-items: center;
  background: #f4f8f6;
  border-radius: 10px;
  padding: 1.5rem 2rem 1.5rem 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(66,185,131,0.07);
}
.compliance-header i {
  font-size: 2.5rem;
  color: #42b983;
  margin-right: 1.5rem;
}
.compliance-header .header-text h2 {
  color: #2355d6;
  margin-bottom: 0.3rem;
  font-size: 2rem;
}
.compliance-header .slogan {
  color: #4a4a4a;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}
</style> 