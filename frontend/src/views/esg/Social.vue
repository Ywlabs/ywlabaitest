<template>
  <div class="social">
    <div class="social-header">
      <i class="fas fa-hands-helping"></i>
      <div class="header-text">
        <h2>사회공헌</h2>
        <p class="slogan">기술로 만드는 따뜻한 세상</p>
      </div>
    </div>
    <div class="social-content">
      <section class="vision-section">
        <h3>사회공헌 비전</h3>
        <p>영우랩스는 '기술로 만드는 따뜻한 세상'을 실현하기 위해 다양한 사회공헌 활동을 펼치고 있습니다. 임직원과 함께하는 나눔 문화를 통해 지역사회와 상생하는 기업이 되겠습니다.</p>
      </section>

      <section class="programs-section">
        <h3>주요 사회공헌 프로그램</h3>
        <div class="programs-grid">
          <div class="program-card">
            <h4>기술 나눔</h4>
            <ul>
              <li>청소년 코딩 교육 지원</li>
              <li>디지털 격차 해소 프로그램</li>
              <li>IT 멘토링 활동</li>
            </ul>
          </div>

          <div class="program-card">
            <h4>인재 육성</h4>
            <ul>
              <li>장학금 지원</li>
              <li>인턴십 프로그램</li>
              <li>취업 멘토링</li>
            </ul>
          </div>

          <div class="program-card">
            <h4>지역 상생</h4>
            <ul>
              <li>지역 축제 지원</li>
              <li>소상공인 지원</li>
              <li>지역 문화 프로그램</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="activities-section">
        <h3>최근 사회공헌 활동</h3>
        <div class="activities-timeline">
          <div class="activity-item">
            <div class="activity-date">2024.03</div>
            <div class="activity-content">
              <h4>청소년 코딩 캠프</h4>
              <p>전국 100명의 청소년을 대상으로 AI 코딩 교육 실시</p>
            </div>
          </div>

          <div class="activity-item">
            <div class="activity-date">2024.02</div>
            <div class="activity-content">
              <h4>디지털 교육 지원</h4>
              <p>지역 아동센터에 컴퓨터 기기 및 교육 프로그램 지원</p>
            </div>
          </div>

          <div class="activity-item">
            <div class="activity-date">2024.01</div>
            <div class="activity-content">
              <h4>연말 나눔 행사</h4>
              <p>임직원 참여 봉사활동 및 연말 기부금 전달</p>
            </div>
          </div>
        </div>
      </section>

      <section class="participation-section">
        <h3>임직원 참여</h3>
        <div class="participation-stats">
          <div class="stat-item">
            <div class="stat-number">85%</div>
            <p>임직원 참여율</p>
          </div>
          <div class="stat-item">
            <div class="stat-number">1,200</div>
            <p>연간 봉사 시간</p>
          </div>
          <div class="stat-item">
            <div class="stat-number">15</div>
            <p>지원 단체 수</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Social'
}
</script>

<style scoped>
.social {
  padding: 2rem;
}

.social-header {
  display: flex;
  align-items: center;
  background: #f7f3fa;
  border-radius: 10px;
  padding: 1.5rem 2rem 1.5rem 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(66,185,131,0.07);
}
.social-header i {
  font-size: 2.5rem;
  color: #a259c4;
  margin-right: 1.5rem;
}
.social-header .header-text h2 {
  color: #a259c4;
  margin-bottom: 0.3rem;
  font-size: 2rem;
}
.social-header .slogan {
  color: #4a4a4a;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

.social-content {
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

.programs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.program-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.program-card h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.program-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.program-card li {
  color: #4a4a4a;
  margin-bottom: 0.5rem;
  padding-left: 1.2rem;
  position: relative;
}

.program-card li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.activities-timeline {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.activity-item {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.activity-date {
  min-width: 100px;
  color: #42b983;
  font-weight: bold;
}

.activity-content h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.activity-content p {
  color: #4a4a4a;
  margin: 0;
}

.participation-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  text-align: center;
}

.stat-item {
  padding: 1.5rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.stat-item p {
  color: #4a4a4a;
  margin: 0;
}

@media (max-width: 1024px) {
  .programs-grid,
  .participation-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .programs-grid,
  .participation-stats {
    grid-template-columns: 1fr;
  }

  .activity-item {
    flex-direction: column;
    gap: 0.5rem;
  }

  .activity-date {
    min-width: auto;
  }
}
</style> 