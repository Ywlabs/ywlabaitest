<template>
  <div class="animation-bg">
    <!-- .home 내부에만 적용되는 배경 애니메이션 -->
    <lottie-player
      src="/assets/json/Animation-background.json"
      background="transparent"
      speed="1"
      loop
      autoplay
    ></lottie-player>
  </div>
</template>

<script setup>
// 별도 스크립트 필요 없음
</script>

<style scoped>
/* .home 내부에 절대 위치, 상단에 딱 맞게 붙임 */
.animation-bg {
  position: absolute;
  top: -10%;
  left: 0;
  width: 100%;
  height: 95%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}
.animation-bg lottie-player {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 왜곡 없이 꽉 차게 */
  object-position: left center; /* 왼쪽에 딱 붙게 */
  display: block;
}
</style> 