<template>
  <div class="greeting">
    <FloatingMenu />
    <div class="greeting-content">
      <div class="ceo-message">
        <h3>안녕하세요, 영우랩스 대표이사 JASON 입니다.</h3>
        <p>
          영우랩스는 'AI로 더 나은 세상을 만든다'는 비전으로 2015년 설립되었습니다.
          4차 산업 중심의 IOT 기술을 기반으로 지속성장하였으며, 
          현재는 에너지 빅 데이터 기반의 사용자 경험형 AI 기술에 대한  연구개발 및 솔루션 개발을  통해 
          기업과 개인의 일상을 더 스마트하고 효율적으로 만들기 위해 노력하고 있습니다.
        </p>
        <p>
          특히 자연어 처리와 머신러닝 분야에서의 혁신적인 솔루션을 통해 고객의 비즈니스 성장을 지원하고 있습니다.
          영우랩스는 현재 대한민국 최대의 자연어 처리 기술 업체로 성장하고 있습니다.
        </p>
        <p>
          우리는 AI 기술의 발전이 인류의 삶을 더욱 풍요롭게 만들 것이라 믿습니다. 
          이를 위해 끊임없는 혁신과 도전을 이어가고 있으며, 
          고객과 함께 성장하는 파트너십을 소중히 여기고 있습니다.
        </p>
        <div class="vision-mission">
          <div class="vision">
            <h4>Vision</h4>
            <p>AI 기술로 더 나은 세상을 만든다</p>
            <ul>
              <li>혁신적인 AI 솔루션 개발</li>
              <li>지속 가능한 기술 혁신</li>
              <li>인류의 삶의 질 향상</li>
            </ul>
          </div>
          <div class="mission">
            <h4>Mission</h4>
            <p>혁신적인 AI 솔루션으로 고객의 성공을 지원한다</p>
            <ul>
              <li>고객 맞춤형 AI 솔루션 제공</li>
              <li>최고의 기술력과 서비스</li>
              <li>지속적인 연구개발 투자</li>
            </ul>
          </div>
        </div>
        <div class="core-values">
          <h4>Core Values</h4>
          <div class="values-grid">
            <div class="value-item">
              <h5>혁신</h5>
              <p>끊임없는 도전과 혁신을 통해 새로운 가치를 창출합니다.</p>
            </div>
            <div class="value-item">
              <h5>신뢰</h5>
              <p>고객과의 약속을 지키고 신뢰를 바탕으로 성장합니다.</p>
            </div>
            <div class="value-item">
              <h5>협력</h5>
              <p>함께 일하는 즐거움을 알고 상생의 가치를 추구합니다.</p>
            </div>
            <div class="value-item">
              <h5>성장</h5>
              <p>지속적인 학습과 발전을 통해 더 나은 미래를 만듭니다.</p>
            </div>
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.greeting h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  text-align: center;
  position: relative;
  padding-bottom: 1rem;
}

.greeting h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: #2355d6;
}

.greeting-content {
  line-height: 1.8;
}

.ceo-message h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.4rem;
  font-weight: 600;
}

.ceo-message p {
  margin-bottom: 1.5rem;
  color: #4a4a4a;
  font-size: 1.1rem;
}

.vision-mission {
  display: flex;
  gap: 2rem;
  margin: 2rem 0;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.vision, .mission {
  flex: 1;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.vision h4, .mission h4 {
  color: #2355d6;
  margin-bottom: 1rem;
  font-size: 1.3rem;
  font-weight: 600;
}

.vision p, .mission p {
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 1rem;
}

.vision ul, .mission ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.vision ul li, .mission ul li {
  color: #666;
  margin-bottom: 0.5rem;
  padding-left: 1.2rem;
  position: relative;
}

.vision ul li::before, .mission ul li::before {
  content: '•';
  color: #2355d6;
  position: absolute;
  left: 0;
}

.core-values {
  margin-top: 3rem;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.core-values h4 {
  color: #2355d6;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-align: center;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.value-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.value-item:hover {
  transform: translateY(-5px);
}

.value-item h5 {
  color: #2355d6;
  font-size: 1.2rem;
  margin-bottom: 0.8rem;
  font-weight: 600;
}

.value-item p {
  color: #666;
  margin: 0;
  font-size: 1rem;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .vision-mission {
    flex-direction: column;
  }
  
  .values-grid {
    grid-template-columns: 1fr;
  }
}
</style> 