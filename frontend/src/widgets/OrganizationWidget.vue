<template>
  <div class="org-chart-widget">
    <div class="org-header">
      <h3>영우랩스 조직도</h3>
      <button class="close-btn" @click="$emit('close')" title="닫기">×</button>
    </div>
    <CommonLoading v-if="loading" message="직원 정보를 불러오는 중..." />
    <CommonError v-else-if="error" :message="error" @retry="fetchEmployees" />
    <ul v-else class="employee-list">
      <li v-for="emp in employees" :key="emp.id" class="employee-item">
        <div class="emp-row">
          <span class="emp-name">{{ emp.name }}</span>
          <span class="emp-position">{{ emp.position }}</span>
        </div>
        <div class="emp-dept">{{ emp.department }}</div>
        <div class="emp-contact" v-if="emp.phone || emp.email">
          <span v-if="emp.phone">📱 {{ emp.phone }}</span>
          <span v-if="emp.phone && emp.email"> &nbsp;|&nbsp; </span>
          <span v-if="emp.email">✉️ {{ emp.email }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import api from '@/common/axios'
import CommonLoading from '@/components/CommonLoading.vue'
import CommonError from '@/components/CommonError.vue'

export default {
  name: 'OrganizationWidget',
  components: { CommonLoading, CommonError },
  data() {
    return {
      employees: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchEmployees();
  },
  methods: {
    async fetchEmployees() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get('/api/employee/list')
        if (res.data && res.data.success && Array.isArray(res.data.data)) {
          this.employees = res.data.data
        } else {
          this.error = res.data.message || '직원 데이터를 불러오는데 실패했습니다.'
        }
      } catch (e) {
        this.error = '네트워크 오류가 발생했습니다.'
      } finally {
        this.loading = false
      }
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
.emp-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}
.emp-name {
  font-weight: bold;
  font-size: 1.1em;
}
.emp-position {
  font-size: 0.98em;
  color: #555;
}
.emp-dept {
  font-size: 0.95em;
  color: #555;
}
.emp-contact {
  font-size: 0.85em;
  color: #888;
  margin-top: 2px;
}
.org-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  margin-top: 0;
}
.org-chart-widget h3 {
  text-align: left;
  margin: 0;
  padding: 0;
  font-size: 1.08em;
  color: #666;
  font-weight: bold;
}
</style> 