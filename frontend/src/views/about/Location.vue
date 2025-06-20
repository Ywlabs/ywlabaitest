<template>
  <div class="location">
    <h1>오시는길</h1>
    <div class="location-content">
      <div class="map-container">
        <iframe
          width="100%"
          height="400"
          frameborder="0"
          style="border:0"
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q=37.557345,127.155927&hl=ko&z=17&output=embed"
          title="영우랩스 위치"
        ></iframe>
      </div>
      <div class="location-info">
        <h3>영우랩스 본사</h3>
        <div class="info-item">
          <h4>주소</h4>
          <p>서울특별시 강동구 고덕비즈밸리로 26 A동 1513호</p>
        </div>
        <div class="info-item">
          <h4>대표전화</h4>
          <p>02-6287-2788</p>
        </div>
        <div class="info-item">
          <h4>이메일</h4>
          <p>amma76@ywlabs.com</p>
        </div>
        <div class="info-item">
          <h4>교통편</h4>
          <ul>
            <li>지하철: 5호선 고덕역 4번 출구에서 도보 10분</li>
            <li>버스: 고덕비즈밸리 정류장 하차</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Location'
}
</script>

<style scoped>
.location {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.location-content {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.map-container {
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.map-placeholder {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e0e0e0;
  color: #666;
}

.location-info {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.location-info h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.info-item {
  margin-bottom: 1.5rem;
}

.info-item h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.info-item p {
  color: #666;
  margin: 0;
}

.info-item ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  color: #666;
}

.info-item li {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .location-content {
    grid-template-columns: 1fr;
  }
}
</style> 