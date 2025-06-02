<template>
  <div class="careers">
    <h1>채용공고</h1>
    <div class="careers-content">
      <div class="job-list">
        <div class="job-item">
          <h3>AI 개발자</h3>
          <div class="job-details">
            <p class="job-type">정규직</p>
            <p class="job-location">서울 강남구</p>
          </div>
          <div class="job-description">
            <h4>주요업무</h4>
            <ul>
              <li>AI 모델 개발 및 최적화</li>
              <li>머신러닝 알고리즘 구현</li>
              <li>데이터 분석 및 처리</li>
            </ul>
            <h4>자격요건</h4>
            <ul>
              <li>Python, TensorFlow/PyTorch 경험</li>
              <li>AI/ML 프로젝트 경험</li>
              <li>컴퓨터공학 또는 관련 전공</li>
            </ul>
          </div>
          <button class="apply-button">지원하기</button>
        </div>

        <div class="job-item">
          <h3>프론트엔드 개발자</h3>
          <div class="job-details">
            <p class="job-type">정규직</p>
            <p class="job-location">서울 강남구</p>
          </div>
          <div class="job-description">
            <h4>주요업무</h4>
            <ul>
              <li>Vue.js 기반 웹 애플리케이션 개발</li>
              <li>UI/UX 구현</li>
              <li>프론트엔드 성능 최적화</li>
            </ul>
            <h4>자격요건</h4>
            <ul>
              <li>Vue.js 또는 React 경험</li>
              <li>웹 개발 프로젝트 경험</li>
              <li>컴퓨터공학 또는 관련 전공</li>
            </ul>
          </div>
          <button class="apply-button">지원하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'Careers',
  components: { FloatingMenu },
  // ...기존 코드...
}
</script>

<style scoped>
.careers {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.careers-content {
  margin-top: 2rem;
}

.job-list {
  display: grid;
  gap: 2rem;
}

.job-item {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.job-item h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.job-details {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.job-type, .job-location {
  color: #666;
  font-size: 0.9rem;
}

.job-description {
  margin-bottom: 1.5rem;
}

.job-description h4 {
  color: #2c3e50;
  margin: 1rem 0 0.5rem;
}

.job-description ul {
  list-style-type: disc;
  margin-left: 1.5rem;
  color: #666;
}

.job-description li {
  margin-bottom: 0.5rem;
}

.apply-button {
  background: #42b983;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.apply-button:hover {
  background: #3aa876;
}
</style> 