<template>
  <div class="history">
    <h2>걸어온 길</h2>
    <div class="history-content">
      <div class="timeline">
        <div class="timeline-item">
          <div class="year">2024</div>
          <div class="events">
            <div class="event">
              <span class="month">03</span>
              <p>AI 챗봇 솔루션 'ChatGPT Plus' 출시</p>
            </div>
            <div class="event">
              <span class="month">01</span>
              <p>시리즈 A 투자 유치 (50억원)</p>
            </div>
          </div>
        </div>

        <div class="timeline-item">
          <div class="year">2023</div>
          <div class="events">
            <div class="event">
              <span class="month">12</span>
              <p>대한민국 ICT 대상 수상</p>
            </div>
            <div class="event">
              <span class="month">09</span>
              <p>자연어 처리 엔진 'NLP Core' 출시</p>
            </div>
            <div class="event">
              <span class="month">06</span>
              <p>해외 지사 설립 (싱가포르)</p>
            </div>
          </div>
        </div>

        <div class="timeline-item">
          <div class="year">2022</div>
          <div class="events">
            <div class="event">
              <span class="month">12</span>
              <p>벤처기업 인증 획득</p>
            </div>
            <div class="event">
              <span class="month">08</span>
              <p>AI 기반 문서 분석 솔루션 출시</p>
            </div>
          </div>
        </div>

        <div class="timeline-item">
          <div class="year">2021</div>
          <div class="events">
            <div class="event">
              <span class="month">12</span>
              <p>시드 투자 유치 (20억원)</p>
            </div>
            <div class="event">
              <span class="month">06</span>
              <p>첫 번째 AI 솔루션 출시</p>
            </div>
          </div>
        </div>

        <div class="timeline-item">
          <div class="year">2020</div>
          <div class="events">
            <div class="event">
              <span class="month">03</span>
              <p>영우랩스 설립</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'History'
}
</script>

<style scoped>
.history {
  padding: 2rem;
}

.history h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.timeline {
  position: relative;
  padding: 2rem 0;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 120px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e0e0e0;
}

.timeline-item {
  display: flex;
  margin-bottom: 3rem;
  position: relative;
}

.year {
  width: 100px;
  font-size: 1.4rem;
  font-weight: bold;
  color: #2c3e50;
  text-align: right;
  padding-right: 2rem;
}

.events {
  flex: 1;
  padding-left: 2rem;
}

.event {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
  position: relative;
}

.event::before {
  content: '';
  position: absolute;
  left: -2rem;
  top: 0.5rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #42b983;
}

.month {
  font-weight: bold;
  color: #42b983;
  margin-right: 1rem;
  min-width: 40px;
}

.event p {
  color: #4a4a4a;
  margin: 0;
  line-height: 1.6;
}
</style> 