<template>
  <div class="social">
    <h1>사회공헌</h1>
    <div class="social-content">
      <div class="social-header">
        <h2>더 나은 사회를 위한 기여</h2>
        <p class="subtitle">영우랩스는 기술의 힘으로 사회적 가치를 창출합니다.</p>
      </div>

      <div class="social-sections">
        <div class="section">
          <h3>교육 지원</h3>
          <ul>
            <li>IT 교육 프로그램 운영</li>
            <li>장학금 지원</li>
            <li>멘토링 프로그램</li>
            <li>기술 교육 콘텐츠 제공</li>
          </ul>
        </div>

        <div class="section">
          <h3>지역 사회 기여</h3>
          <ul>
            <li>지역 축제 지원</li>
            <li>봉사 활동 참여</li>
            <li>지역 기업 협력</li>
            <li>문화 행사 후원</li>
          </ul>
        </div>

        <div class="section">
          <h3>기술 나눔</h3>
          <ul>
            <li>오픈소스 프로젝트</li>
            <li>기술 세미나 개최</li>
            <li>스타트업 멘토링</li>
            <li>기술 공유 프로그램</li>
          </ul>
        </div>
      </div>

      <div class="social-programs">
        <h3>주요 사회공헌 프로그램</h3>
        <div class="program-grid">
          <div class="program-item">
            <h4>코딩 교육</h4>
            <p>청소년을 위한 무료 코딩 교육 프로그램 운영</p>
            <ul>
              <li>주 1회 정기 교육</li>
              <li>실무 프로젝트 참여</li>
              <li>멘토링 제공</li>
            </ul>
          </div>
          <div class="program-item">
            <h4>기술 나눔</h4>
            <p>지역 기업 대상 기술 지원 프로그램</p>
            <ul>
              <li>기술 컨설팅</li>
              <li>디지털 전환 지원</li>
              <li>맞춤형 솔루션 제공</li>
            </ul>
          </div>
          <div class="program-item">
            <h4>사회혁신</h4>
            <p>사회문제 해결을 위한 기술 프로젝트</p>
            <ul>
              <li>공공 서비스 개발</li>
              <li>사회적 기업 지원</li>
              <li>혁신 아이디어 발굴</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="social-impact">
        <h3>사회적 영향</h3>
        <div class="impact-stats">
          <div class="stat-item">
            <span class="number">1,000+</span>
            <span class="label">교육 수혜자</span>
          </div>
          <div class="stat-item">
            <span class="number">50+</span>
            <span class="label">지원 기업</span>
          </div>
          <div class="stat-item">
            <span class="number">100+</span>
            <span class="label">봉사 시간</span>
          </div>
        </div>
      </div>
    </div>
    <FloatingMenu />
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'Social',
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
.social {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.social-content {
  margin-top: 2rem;
}

.social-header {
  text-align: center;
  margin-bottom: 3rem;
}

.social-header h2 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.subtitle {
  color: #666;
  font-size: 1.2rem;
}

.social-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.section ul {
  list-style-type: none;
  padding: 0;
}

.section li {
  color: #666;
  margin-bottom: 1rem;
  padding-left: 1.5rem;
  position: relative;
}

.section li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.social-programs {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 3rem;
}

.social-programs h3 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
}

.program-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.program-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.program-item h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.program-item p {
  color: #666;
  margin-bottom: 1rem;
}

.program-item ul {
  list-style-type: none;
  padding: 0;
}

.program-item li {
  color: #666;
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}

.program-item li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.social-impact {
  text-align: center;
}

.social-impact h3 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.impact-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.label {
  color: #666;
  font-size: 1.1rem;
}
</style> 