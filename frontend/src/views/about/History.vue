<template>
  <div class="history">
    <h1>걸어온길</h1>
    <div class="history-content">
      <div class="timeline">
        <div class="timeline-item">
          <div class="year">2023</div>
          <div class="event">
            <h3>AIEMS 솔루션 출시</h3>
            <p>에너지 관리 시스템 솔루션 출시</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="year">2022</div>
          <div class="event">
            <h3>AIMASASIKI 솔루션 출시</h3>
            <p>제조 생산성 향상 솔루션 출시</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="year">2021</div>
          <div class="event">
            <h3>AICDMS 솔루션 출시</h3>
            <p>문서 관리 시스템 솔루션 출시</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="year">2020</div>
          <div class="event">
            <h3>영우랩스 설립</h3>
            <p>AI 솔루션 전문 기업으로 시작</p>
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
  name: 'History',
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
.history {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.history-content {
  margin-top: 2rem;
}

.timeline {
  position: relative;
  padding: 2rem 0;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 100%;
  background: #e0e0e0;
}

.timeline-item {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 3rem;
  position: relative;
}

.year {
  background: #42b983;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  margin: 0 2rem;
}

.event {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 300px;
}

.event h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.event p {
  color: #666;
  margin: 0;
}
</style> 