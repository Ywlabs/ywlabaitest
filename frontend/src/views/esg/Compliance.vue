<template>
  <div class="compliance">
    <h1>준법경영</h1>
    <div class="compliance-content">
      <div class="compliance-header">
        <h2>윤리적이고 투명한 경영</h2>
        <p class="subtitle">영우랩스는 윤리경영을 최우선 가치로 실천합니다.</p>
      </div>

      <div class="compliance-sections">
        <div class="section">
          <h3>윤리경영 원칙</h3>
          <ul>
            <li>공정한 거래</li>
            <li>투명한 경영</li>
            <li>법규 준수</li>
            <li>사회적 책임</li>
          </ul>
        </div>

        <div class="section">
          <h3>준법경영 체계</h3>
          <ul>
            <li>내부통제 시스템</li>
            <li>윤리경영 교육</li>
            <li>감사 및 모니터링</li>
            <li>리스크 관리</li>
          </ul>
        </div>

        <div class="section">
          <h3>주요 활동</h3>
          <ul>
            <li>정기 윤리경영 교육</li>
            <li>부패방지 정책 수립</li>
            <li>공급망 윤리경영 확산</li>
            <li>이해관계자 소통 강화</li>
          </ul>
        </div>
      </div>

      <div class="compliance-commitment">
        <h3>영우랩스의 약속</h3>
        <p>영우랩스는 모든 이해관계자와의 관계에서 윤리적이고 투명한 경영을 실천하며, 지속가능한 미래를 위해 노력하겠습니다.</p>
      </div>
    </div>
    <FloatingMenu />
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'Compliance',
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
.compliance {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.compliance-content {
  margin-top: 2rem;
}

.compliance-header {
  text-align: center;
  margin-bottom: 3rem;
}

.compliance-header h2 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.subtitle {
  color: #666;
  font-size: 1.2rem;
}

.compliance-sections {
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

.compliance-commitment {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.compliance-commitment h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.compliance-commitment p {
  color: #666;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto;
}
</style> 