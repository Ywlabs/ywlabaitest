<template>
  <div class="aimasasiki">
    <div class="content">
      <h1>AIMASASIKI</h1>
      <p>AI 기술로 더 즐거운 세상을 만들어갑니다</p>
      <div class="features">
        <div class="feature">
          <h2>AI 기반 맞춤형 서비스</h2>
          <p>사용자의 니즈를 정확히 파악하여 최적화된 서비스를 제공합니다.</p>
        </div>
        <div class="feature">
          <h2>실시간 상호작용</h2>
          <p>자연스러운 대화형 인터페이스로 사용자 경험을 향상시킵니다.</p>
        </div>
        <div class="feature">
          <h2>지속적인 학습과 개선</h2>
          <p>사용자 피드백을 기반으로 지속적으로 서비스를 개선합니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIMASASIKI'
}
</script>

<style scoped>
.aimasasiki {
  padding: 2rem;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.feature h2 {
  color: #42b983;
  margin-bottom: 1rem;
}

.feature p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .aimasasiki {
    padding: 1rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  p {
    font-size: 1rem;
  }
}
</style> 