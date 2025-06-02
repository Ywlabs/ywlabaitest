<template>
  <div class="today-vacation">
    <h3>오늘의 휴가자</h3>
    <div class="vacation-list">
      <div v-if="vacationers.length === 0" class="no-vacation">
        오늘 휴가자는 없습니다.
      </div>
      <div v-else class="vacation-items">
        <div v-for="vacation in vacationers" :key="vacation.id" class="vacation-item">
          <div class="vacation-info">
            <span class="name">{{ vacation.name }}</span>
            <span class="department">{{ vacation.department }}</span>
            <span class="type">{{ vacation.vacationType }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TodayVacation',
  data() {
    return {
      loading: true,
      vacationers: []
    }
  },
  async created() {
    await this.fetchVacationers()
  },
  methods: {
    async fetchVacationers() {
      try {
        // TODO: API 연동
        // 임시 데이터
        this.vacationers = [
          {
            id: 1,
            name: '홍길동',
            department: '개발팀',
            profileImage: null,
            vacationType: '연차',
            startDate: '2024-03-20',
            endDate: '2024-03-21'
          },
          {
            id: 2,
            name: '김철수',
            department: '인사팀',
            profileImage: null,
            vacationType: '오전반차',
            startDate: '2024-03-20',
            endDate: '2024-03-20'
          }
        ]
      } catch (error) {
        console.error('Error fetching vacationers:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.today-vacation {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.2em;
}

.vacation-list {
  min-height: 100px;
}

.no-vacation {
  color: #666;
  text-align: center;
  padding: 20px;
}

.vacation-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.vacation-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.vacation-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.name {
  font-weight: 500;
  color: #333;
}

.department {
  color: #666;
  font-size: 0.9em;
}

.type {
  color: #007bff;
  font-size: 0.9em;
  margin-left: auto;
}
</style> 