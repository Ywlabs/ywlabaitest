<template>
  <div class="org-chart-widget">
    <h3>조직도</h3>
    <div class="org-chart-container">
      <div v-if="loading" class="loading">
        <span class="spinner"></span> 로딩중...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else class="org-tree">
        <div class="org-node root">
          <div class="node-content">
            <span class="title">영우랩스</span>
          </div>
          <div class="children">
            <div v-for="(dept, index) in departments" :key="index" class="org-node">
              <div class="node-content dept-header" @click="toggleDepartment(index)">
                <span class="title">{{ dept.dept }}</span>
                <span class="count">({{ dept.employees.length }}명)</span>
                <span class="toggle-icon">{{ expandedDepts[index] ? '▼' : '▶' }}</span>
              </div>
              <div class="children" v-if="expandedDepts[index] && dept.employees.length > 0">
                <div v-for="employee in dept.employees" :key="employee.id" class="org-node employee">
                  <div class="node-content">
                    <div class="employee-info">
                      <span class="name">{{ employee.name }}</span>
                      <span class="position">{{ employee.position }}</span>
                      <span class="contact">
                        <span v-if="employee.email" class="email">{{ employee.email }}</span>
                        <span v-if="employee.phone" class="phone">{{ employee.phone }}</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrganizationChart',
  data() {
    return {
      loading: true,
      error: null,
      departments: [],
      expandedDepts: {},
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
    }
  },
  async created() {
    await this.fetchOrganizationData()
  },
  methods: {
    toggleDepartment(index) {
      this.expandedDepts[index] = !this.expandedDepts[index]
    },
    async fetchOrganizationData() {
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/employee/list`)
        if (!response.ok) {
          throw new Error('직원 정보를 불러오는데 실패했습니다.')
        }
        const employees = await response.json()
        console.log('API Response:', employees)
        
        // 부서별로 직원 그룹화
        const deptGroups = {}
        employees.forEach(emp => {
          const dept = emp.dept_nm || '미지정'
          if (!deptGroups[dept]) {
            deptGroups[dept] = []
          }
          deptGroups[dept].push({
            id: emp.id,
            name: emp.name,
            position: emp.position,
            email: emp.email,
            phone: emp.phone,
            dept_nm: emp.dept_nm,
            sns: emp.sns
          })
        })

        this.departments = Object.entries(deptGroups).map(([dept, employees]) => ({
          dept,
          employees
        }))
        
        console.log('Processed departments:', this.departments)
        
        // 부서 데이터가 로드되면 expandedDepts 초기화
        this.departments.forEach((_, index) => {
          this.expandedDepts[index] = false
        })
      } catch (error) {
        console.error('Error fetching organization data:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.org-chart-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.org-chart-widget h3 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #42b983;
  font-size: 1.1rem;
}

.org-chart-container {
  flex: 1;
  overflow: auto;
  padding: 10px;
}

.org-tree {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.org-node {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.node-content {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 12px 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dept-header {
  cursor: pointer;
  transition: background-color 0.2s;
}

.dept-header:hover {
  background: #e9ecef;
}

.toggle-icon {
  margin-left: auto;
  font-size: 0.8rem;
  color: #666;
}

.root .node-content {
  background: #42b983;
  color: white;
}

.title {
  font-weight: 600;
}

.employee-info {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  padding: 0 5px;
}

.name {
  font-weight: 600;
  min-width: 80px;
  color: #000000;
}

.position {
  color: #666;
  min-width: 80px;
}

.contact {
  display: flex;
  flex-direction: column;
  margin-left: auto;
  font-size: 0.9rem;
}

.email {
  color: #666;
}

.phone {
  color: #666;
  margin-top: 2px;
}

.count {
  font-size: 0.9rem;
  color: #666;
}

.root .count {
  color: rgba(255, 255, 255, 0.8);
}

.children {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 20px;
  position: relative;
}

.children::before {
  content: '';
  position: absolute;
  left: -10px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e0e0e0;
}

.employee .node-content {
  background: #ffffff;
  border: 1px solid #e0e0e0;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}

.error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #dc3545;
  text-align: center;
  padding: 20px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #42b983;
  border-top: 2px solid #e0e0e0;
  border-radius: 50%;
  margin-right: 10px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 