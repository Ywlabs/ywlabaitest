<template>
  <div class="esg">
    <div class="page-container">
      <div class="sidebar">
        <SideMenu>
          <h3>ESG</h3>
          <div class="menu-list">
            <router-link to="/esg/compliance" class="menu-item">준법경영</router-link>
            <router-link to="/esg/environment" class="menu-item">환경경영</router-link>
            <router-link to="/esg/social" class="menu-item">사회공헌</router-link>
          </div>
        </SideMenu>
      </div>
      <div class="content">
        <template v-if="$route.path === '/esg' || $route.path === '/esg/'">
          <h1>ESG 경영</h1>
          <section class="esg-intro">
            <p>
              <strong>ESG</strong>란 환경(Environment), 사회(Social), 지배구조(Governance)의 약자로, 기업의 지속가능성과 사회적 책임을 평가하는 핵심 기준입니다.<br>
              영우랩스는 ESG 경영을 통해 지속가능한 미래와 사회적 가치를 실현하고 있습니다.
            </p>
          </section>
          <section class="esg-vision">
            <h2>영우랩스의 ESG 비전</h2>
            <ul>
              <li>친환경 경영을 통한 탄소중립 실현</li>
              <li>사회적 책임과 윤리경영 강화</li>
              <li>투명하고 신뢰받는 지배구조 확립</li>
            </ul>
          </section>
          <section class="esg-pillars">
            <h2>ESG 3대 영역 실천</h2>
            <div class="esg-pillars-list">
              <div class="pillar">
                <h3>환경(Environment)</h3>
                <ul>
                  <li>에너지 효율화 및 친환경 기술 도입</li>
                  <li>탄소배출 저감 및 자원순환 확대</li>
                  <li>친환경 제품 및 서비스 개발</li>
                </ul>
              </div>
              <div class="pillar">
                <h3>사회(Social)</h3>
                <ul>
                  <li>임직원 복지 및 다양성 존중</li>
                  <li>지역사회 공헌 및 상생협력</li>
                  <li>고객 데이터 보호 및 정보보안 강화</li>
                </ul>
              </div>
              <div class="pillar">
                <h3>지배구조(Governance)</h3>
                <ul>
                  <li>투명한 의사결정과 윤리경영</li>
                  <li>이사회 독립성 및 책임경영 강화</li>
                  <li>공정거래 및 준법경영 실천</li>
                </ul>
              </div>
            </div>
          </section>
          <section class="esg-achievements">
            <h2>ESG 주요 성과</h2>
            <ul>
              <li>2023년 친환경 경영 우수기업 선정</li>
              <li>사회공헌 우수상 및 다수의 사회적 가치 창출</li>
              <li>정보보호 및 윤리경영 관련 인증 획득</li>
            </ul>
          </section>
        </template>
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import '@/assets/layout.css'
import SideMenu from '@/components/SideMenu.vue'

export default {
  name: 'ESG',
  components: { SideMenu }
}
</script>

<style scoped>
.esg {
  min-height: 100vh;
  padding-top: 80px;
}
.page-container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 80px);
}
.sidebar {
  width: 250px;
  background: #fff;
  border-right: 1px solid #eee;
  height: 100%;
  position: fixed;
  left: 0;
  top: 80px;
  z-index: 100;
}
.sidebar h3 {
  font-size: 1.15em;
  font-weight: bold;
  margin: 1.5rem 0 1rem 0;
  color: #2c3e50;
  border-bottom: 3px solid #42b983;
  padding-bottom: 0.5rem;
  width: 90%;
}
.content {
  flex: 1;
  margin-left: 250px;
  padding: 2rem;
}
.menu-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
}
.menu-item {
  color: #2c3e50;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
  font-weight: 500;
  display: block;
  width: 100%;
  text-align: left;
  box-sizing: border-box;
}
.menu-item:hover {
  background: #f8f9fa;
  color: #42b983;
}
.menu-item.router-link-active,
.menu-item.router-link-exact-active {
  background: #42b983;
  color: white;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(66,185,131,0.08);
}
.esg-intro {
  margin-bottom: 2rem;
  font-size: 1.1em;
  color: #333;
}
.esg-vision {
  margin-bottom: 2rem;
}
.esg-vision h2 {
  font-size: 1.2em;
  color: #2355d6;
  margin-bottom: 0.5rem;
}
.esg-vision ul {
  list-style: disc inside;
  color: #444;
  margin-left: 1.2em;
}
.esg-pillars {
  margin-bottom: 2rem;
}
.esg-pillars h2 {
  font-size: 1.2em;
  color: #2355d6;
  margin-bottom: 0.5rem;
}
.esg-pillars-list {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}
.pillar {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.2rem 1rem;
  flex: 1;
  min-width: 0;
}
.pillar h3 {
  color: #42b983;
  font-size: 1.1em;
  margin-bottom: 0.5rem;
}
.pillar ul {
  list-style: disc inside;
  color: #444;
  margin-left: 1.2em;
}
.esg-achievements {
  margin-bottom: 2rem;
}
.esg-achievements h2 {
  font-size: 1.2em;
  color: #2355d6;
  margin-bottom: 0.5rem;
}
.esg-achievements ul {
  list-style: disc inside;
  color: #444;
  margin-left: 1.2em;
}
</style> 