<template>
  <div class="greeting">
    <FloatingMenu />
    <h2>인사말</h2>
    <div class="greeting-content">
      <div class="ceo-message">
        <h3>안녕하세요, 영우랩스 대표이사 홍길동입니다.</h3>
        <p>
          영우랩스는 'AI로 더 나은 세상을 만든다'는 비전으로 2020년 설립되었습니다.
          우리는 인공지능 기술을 통해 기업과 개인의 일상을 더 스마트하고 효율적으로 만들기 위해 노력하고 있습니다.
        </p>
        <p>
          특히 자연어 처리와 머신러닝 분야에서의 혁신적인 솔루션을 통해
          고객의 비즈니스 성장을 지원하고 있습니다.
        </p>
        <div class="vision-mission">
          <div class="vision">
            <h4>Vision</h4>
            <p>AI 기술로 더 나은 세상을 만든다</p>
          </div>
          <div class="mission">
            <h4>Mission</h4>
            <p>혁신적인 AI 솔루션으로 고객의 성공을 지원한다</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Greeting'
}
</script>

<style scoped>
.greeting {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.greeting h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.greeting-content {
  line-height: 1.8;
}

.ceo-message h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.4rem;
}

.ceo-message p {
  margin-bottom: 1.5rem;
  color: #4a4a4a;
}

.vision-mission {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.vision, .mission {
  flex: 1;
}

.vision h4, .mission h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.vision p, .mission p {
  color: #666;
  font-weight: 500;
}
</style> 