<template>
  <div class="environment">
    <h1>환경경영</h1>
    <div class="environment-content">
      <div class="environment-header">
        <h2>지속가능한 환경 경영</h2>
        <p class="subtitle">영우랩스는 환경 보호를 위한 책임 있는 경영을 실천합니다.</p>
      </div>

      <div class="environment-sections">
        <div class="section">
          <h3>환경 경영 목표</h3>
          <ul>
            <li>탄소중립 달성</li>
            <li>에너지 효율성 향상</li>
            <li>자원 재활용 확대</li>
            <li>친환경 제품 개발</li>
          </ul>
        </div>

        <div class="section">
          <h3>주요 환경 활동</h3>
          <ul>
            <li>재생에너지 사용 확대</li>
            <li>폐기물 감량 및 재활용</li>
            <li>녹색 물류 시스템 구축</li>
            <li>환경 교육 프로그램 운영</li>
          </ul>
        </div>

        <div class="section">
          <h3>환경 성과</h3>
          <ul>
            <li>탄소배출량 감소</li>
            <li>에너지 사용량 절감</li>
            <li>재활용률 향상</li>
            <li>친환경 인증 획득</li>
          </ul>
        </div>
      </div>

      <div class="environment-initiatives">
        <h3>환경 보호 이니셔티브</h3>
        <div class="initiative-grid">
          <div class="initiative-item">
            <h4>그린 오피스</h4>
            <p>사무실 내 에너지 절약 및 친환경 소재 사용</p>
          </div>
          <div class="initiative-item">
            <h4>친환경 개발</h4>
            <p>저전력 소프트웨어 솔루션 개발</p>
          </div>
          <div class="initiative-item">
            <h4>녹색 물류</h4>
            <p>친환경 운송 및 배송 시스템 구축</p>
          </div>
          <div class="initiative-item">
            <h4>환경 교육</h4>
            <p>직원 대상 환경 보호 교육 프로그램</p>
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
  name: 'Environment',
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
.environment {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.environment-content {
  margin-top: 2rem;
}

.environment-header {
  text-align: center;
  margin-bottom: 3rem;
}

.environment-header h2 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.subtitle {
  color: #666;
  font-size: 1.2rem;
}

.environment-sections {
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

.environment-initiatives {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
}

.environment-initiatives h3 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
}

.initiative-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.initiative-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.initiative-item h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.initiative-item p {
  color: #666;
  line-height: 1.6;
}
</style> 