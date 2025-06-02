<template>
  <div class="greeting">
    <FloatingMenu />
    <h1>인사말</h1>
    <div class="greeting-content">
      <div class="ceo-message">
        <h2>대표이사 인사말</h2>
        <p>안녕하세요, 영우랩스 대표이사입니다.</p>
        <p>영우랩스는 AI 기술을 통해 더 나은 미래를 만들어가고 있습니다.</p>
        <p>고객 여러분의 성공적인 비즈니스를 위해 최선을 다하겠습니다.</p>
      </div>
    </div>
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'Greeting',
  components: { FloatingMenu },
  // ...기존 코드...
}
</script>

<style scoped>
.greeting {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.greeting-content {
  margin-top: 2rem;
}

.ceo-message {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.ceo-message h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.ceo-message p {
  color: #666;
  line-height: 1.8;
  margin-bottom: 1rem;
}
</style> 