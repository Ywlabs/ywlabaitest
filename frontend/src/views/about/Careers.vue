<template>
  <div class="careers">
    <h2>채용공고</h2>
    <div class="careers-content">
      <div class="job-list">
        <div class="job-item">
          <div class="job-header">
            <h3>AI 엔지니어 (NLP)</h3>
            <span class="job-type">정규직</span>
          </div>
          <div class="job-details">
            <div class="detail-item">
              <h4>주요업무</h4>
              <ul>
                <li>자연어 처리 모델 개발 및 최적화</li>
                <li>챗봇 시스템 설계 및 구현</li>
                <li>텍스트 분석 알고리즘 개발</li>
              </ul>
            </div>
            <div class="detail-item">
              <h4>자격요건</h4>
              <ul>
                <li>컴퓨터공학 또는 관련 전공</li>
                <li>Python, PyTorch/TensorFlow 경험</li>
                <li>NLP 프로젝트 경험</li>
              </ul>
            </div>
            <div class="detail-item">
              <h4>우대사항</h4>
              <ul>
                <li>대규모 언어 모델 경험</li>
                <li>클라우드 환경 개발 경험</li>
                <li>오픈소스 기여 경험</li>
              </ul>
            </div>
          </div>
          <button class="apply-btn">지원하기</button>
        </div>

        <div class="job-item">
          <div class="job-header">
            <h3>프론트엔드 개발자</h3>
            <span class="job-type">정규직</span>
          </div>
          <div class="job-details">
            <div class="detail-item">
              <h4>주요업무</h4>
              <ul>
                <li>Vue.js 기반 웹 애플리케이션 개발</li>
                <li>UI/UX 개선 및 최적화</li>
                <li>신규 기능 설계 및 구현</li>
              </ul>
            </div>
            <div class="detail-item">
              <h4>자격요건</h4>
              <ul>
                <li>3년 이상의 프론트엔드 개발 경험</li>
                <li>Vue.js 또는 React 실무 경험</li>
                <li>HTML5, CSS3, JavaScript 전문성</li>
              </ul>
            </div>
            <div class="detail-item">
              <h4>우대사항</h4>
              <ul>
                <li>TypeScript 개발 경험</li>
                <li>반응형 웹 개발 경험</li>
                <li>UI/UX 디자인 경험</li>
              </ul>
            </div>
          </div>
          <button class="apply-btn">지원하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Careers'
}
</script>

<style scoped>
.careers {
  padding: 2rem;
}

.careers h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.job-item {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.job-header h3 {
  color: #2c3e50;
  font-size: 1.4rem;
  margin: 0;
}

.job-type {
  background: #42b983;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.job-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.detail-item h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.detail-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.detail-item li {
  color: #4a4a4a;
  margin-bottom: 0.5rem;
  position: relative;
  padding-left: 1.2rem;
}

.detail-item li::before {
  content: '•';
  color: #42b983;
  position: absolute;
  left: 0;
}

.apply-btn {
  background: #42b983;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.apply-btn:hover {
  background: #3aa876;
}
</style> 