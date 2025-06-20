<template>
  <div class="sales-widget-box">
    <div class="sales-widget-header">
      <select v-model="selectedYear" @change="fetchSales" class="year-select">
        <option v-for="y in years" :key="y" :value="y">{{ y }}년</option>
      </select>
      <button class="close-btn" @click="$emit('close')">X</button>
    </div>
    <div class="sales-widget-title">영우랩스의 {{ selectedYear }}년 매출정보입니다.</div>
    <CommonLoading v-if="loading" message="매출 정보를 불러오는 중..." />
    <CommonError v-else-if="error" :message="error" @retry="fetchSales" />
    <div v-else class="sales-widget-content">
      <div class="sales-row">
        <span>달성매출 :</span>
        <span class="sales-value">{{ formatNumber(salesData.total_sales) }} 원</span>
      </div>
      <div class="sales-row">
        <span>영업이익율 :</span>
        <span :class="['profit-rate', profitRateClass(salesData.profit_rate)]">
          {{ (salesData.profit_rate * 100).toFixed(1) }}% 달성
        </span>
      </div>
      <div class="ai-section">
        <div class="ai-title">영우랩스의 올해 AI 예측 매출은 다음과 같습니다.</div>
        <div class="ai-row">
          <span class="ai-label">AI 예측 매출:</span>
          <span class="ai-value">{{ formatNumber(aiPredictData.total_sales) }} 원</span>
        </div>
      </div>
      <div class="sales-widget-desc">
        ※ 실제 집계와 AI 예측값은 참고용입니다. 분석결과는 매월 말 갱신됩니다.
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import api from '@/common/axios';
import CommonLoading from '@/components/CommonLoading.vue';
import CommonError from '@/components/CommonError.vue';

export default defineComponent({
  name: 'SalesWidget',
  components: { CommonLoading, CommonError },
  props: {
    year: {
      type: Number,
      default: () => new Date().getFullYear()
    }
  },
  setup(props) {
    // 연도 선택 목록 (2015~2025)
    const years = Array.from({ length: 11 }, (_, i) => 2015 + i);
    const selectedYear = ref(props.year ?? new Date().getFullYear());
    const salesData = ref({ total_sales: 0, profit_rate: 0 });
    const aiPredictData = ref({ total_sales: 0 });
    const loading = ref(false);
    const error = ref('');
    const thisYear = new Date().getFullYear();

    // 숫자 포맷 함수
    const formatNumber = (num: number) => num ? num.toLocaleString('ko-KR') : '-';

    // 이익율 색상 규칙
    const profitRateClass = (rate: number) => {
      const percent = rate * 100;
      if (percent < 0) return 'profit-red';
      if (percent <= 5) return 'profit-yellow';
      if (percent <= 10) return 'profit-blue';
      return 'profit-red';
    };

    // 연도별 매출 데이터 조회
    const fetchSales = async () => {
      loading.value = true;
      error.value = '';
      try {
        const res = await api.get(`/api/sales/${selectedYear.value}`);
        if (res.data && res.data.success) {
          salesData.value = res.data.data;
        } else {
          error.value = res.data.message || '매출 데이터를 불러올 수 없습니다.';
        }
      } catch (e: any) {
        error.value = '매출 조회 중 네트워크 오류가 발생했습니다.';
      } finally {
        loading.value = false;
      }
    };

    // AI 예측(올해 기준) 데이터 조회
    const fetchAIPredict = async () => {
      try {
        const res = await api.get(`/api/sales/${thisYear}`);
        if (res.data && res.data.success) {
          aiPredictData.value = res.data.data.ai_predict;
        }
      } catch (e) {
        console.error("AI 예측 매출 로딩 실패", e)
      }
    };

    onMounted(() => {
      fetchSales();
      fetchAIPredict();
    });
    watch(selectedYear, fetchSales);

    return {
      years,
      selectedYear,
      salesData,
      aiPredictData,
      loading,
      error,
      formatNumber,
      profitRateClass,
      fetchSales
    };
  }
});
</script>

<style scoped>
.sales-widget-box {
  padding: 20px;
  background: #f4f8fb;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  text-align: center;
  position: relative;
  min-width: 320px;
  max-width: 420px;
  margin: 0 auto;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: none;
  font-size: 1.3em;
  color: #888;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: 50%;
  transition: background 0.15s, color 0.15s;
  z-index: 2;
}
.close-btn:hover {
  background: #e0e6ef;
  color: #d32f2f;
}
.year-select {
  font-size: 1em;
  padding: 2px 8px;
  border: 1px solid #aaa;
  border-radius: 2px;
  margin-bottom: 8px;
}
.sales-widget-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 6px;
  gap: 8px;
}
.sales-widget-title {
  font-size: 1.08em;
  color: #666;
  margin-bottom: 8px;
  border-bottom: 1px dotted #bbb;
  padding-bottom: 2px;
}
.sales-widget-loading,
.sales-widget-error {
  color: #d32f2f;
  margin: 18px 0 12px 0;
  text-align: center;
}
.sales-widget-content {
  margin-top: 8px;
}
.sales-row {
  margin: 8px 0 4px 0;
  font-size: 1.08em;
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: center;
}
.sales-value {
  font-weight: bold;
  color: #2355d6;
  font-size: 1.1em;
}
.profit-rate {
  font-weight: bold;
  font-size: 1.1em;
}
.profit-red {
  color: #d32f2f;
}
.profit-yellow {
  color: #e6a23c;
}
.profit-blue {
  color: #409eff;
}
.ai-section {
  margin-top: 18px;
  border-top: 1px dashed #bbb;
  padding-top: 10px;
}
.ai-title {
  color: #444;
  font-size: 1em;
  margin-bottom: 4px;
}
.ai-row {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 1.08em;
  justify-content: center;
}
.ai-label {
  color: #d32f2f;
  font-weight: 500;
}
.ai-value {
  font-weight: bold;
  color: #222;
}
.sales-widget-desc {
  margin-top: 14px;
  font-size: 0.97em;
  color: #888;
  text-align: left;
}
</style> 