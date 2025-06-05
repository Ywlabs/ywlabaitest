<template>
  <div class="org-chart-widget">
    <!-- 닫기 버튼: 오른쪽 상단 고정 -->
    <button class="close-btn" @click="$emit('close')" title="닫기">×</button>
    <h3>조직도</h3>
    <div v-if="loading" class="loading">불러오는 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul v-else class="employee-list">
      <li v-for="emp in employees" :key="emp.id" class="employee-item">
        <div class="emp-name">{{ emp.name }}</div>
        <div class="emp-position">{{ emp.position }}</div>
        <div class="emp-dept">{{ emp.department }}</div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});

export default {
  name: 'OrganizationWidget',
  data() {
    return {
      employees: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    try {
      const res = await api.get('/api/employee/list')
      if (res.data.status === 'success' && Array.isArray(res.data.data)) {
        this.employees = res.data.data
      } else {
        this.error = '직원 데이터가 올바르지 않습니다.'
      }
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.org-chart-widget {
  padding: 20px;
  background: #f4f8fb;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  text-align: center;
  position: relative; /* 닫기 버튼 위치를 위해 */
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
.employee-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.employee-item {
  background: #fff;
  margin-bottom: 10px;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.emp-name {
  font-weight: bold;
  font-size: 1.1em;
}
.emp-position, .emp-dept {
  font-size: 0.95em;
  color: #555;
}
.loading {
  color: #007bff;
  margin: 20px 0;
}
.error {
  color: #d32f2f;
  margin: 20px 0;
}
</style> 