<template>
  <div class="energy-widget-box">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <span class="widget-title">에너지 절감 팁</span>
    </div>
    <div class="widget-content">
      <p>에너지 절약을 위한 팁을 제공합니다.</p>
      <ul class="tip-list">
        <li>불필요한 조명 끄기</li>
        <li>대기전력 차단</li>
        <li>적정 온도 유지</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EnergyTipWidget',
}
</script>

<style scoped>
.energy-widget-box {
  background: transparent;
  border-radius: 8px;
  box-shadow: none;
  padding: 20px 10px 10px 10px;
  min-width: 320px;
  max-width: 420px;
  margin: 0 auto;
  position: relative;
  z-index: 9999 !important;
  display: block !important;
  opacity: 1 !important;
  visibility: visible !important;
}
.close-btn {
  position: absolute;
  top: 16px;
  right: 12px;
  z-index: 100;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 16px;
  line-height: 22px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  transition: background 0.2s;
  padding: 0;
}
.close-btn:hover {
  background: #f5f5f5;
}
.widget-header {
  font-weight: bold;
  font-size: 1.18em;
  margin-bottom: 12px;
  color: #2355d6;
  letter-spacing: 0.5px;
  text-align: center;
}
.widget-title {
  font-size: 1.22em;
  font-weight: 700;
  color: #2355d6;
  letter-spacing: 0.5px;
}
.widget-content p {
  margin: 0 0 10px 0;
  font-size: 1.08em;
  color: #333;
  text-align: center;
  font-weight: 500;
}
.tip-list {
  margin: 0;
  padding-left: 0;
  color: #2355d6;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}
.tip-list li {
  background: #f4f8fb;
  border-radius: 16px;
  padding: 7px 18px;
  font-size: 1.05em;
  color: #2355d6;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(35,85,214,0.06);
  display: flex;
  align-items: center;
  gap: 8px;
}
.tip-list li::before {
  content: '💡';
  margin-right: 6px;
  font-size: 1.1em;
}
</style> 