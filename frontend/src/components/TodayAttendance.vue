<template>
  <div class="attendance-widget">
    <h3>오늘의 출근현황</h3>
    <div class="attendance-list">
      <div v-if="loading" class="loading">
        <span class="spinner"></span> 로딩중...
      </div>
      <div v-else class="attendance-stats">
        <div class="stat-item">
          <span class="label">출근</span>
          <span class="value">{{ stats.attended }}</span>
        </div>
        <div class="stat-item">
          <span class="label">지각</span>
          <span class="value">{{ stats.late }}</span>
        </div>
        <div class="stat-item">
          <span class="label">미출근</span>
          <span class="value">{{ stats.absent }}</span>
        </div>
      </div>
      <div class="member-list">
        <div v-for="member in members" :key="member.id" class="member-item">
          <div class="profile">
            <div class="info">
              <span class="name">{{ member.name }}</span>
              <span class="department">{{ member.department }}</span>
            </div>
          </div>
          <div class="status" :class="member.status">
            {{ getStatusText(member.status) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TodayAttendance',
  data() {
    return {
      loading: true,
      stats: {
        attended: 0,
        late: 0,
        absent: 0
      },
      members: []
    }
  },
  async created() {
    await this.fetchAttendanceData()
  },
  methods: {
    async fetchAttendanceData() {
      try {
        // TODO: API 연동
        // 임시 데이터
        this.members = [
          {
            id: 1,
            name: '홍길동',
            department: '개발팀',
            profileImage: null,
            status: 'attended',
            time: '09:00'
          },
          {
            id: 2,
            name: '김철수',
            department: '인사팀',
            profileImage: null,
            status: 'late',
            time: '09:15'
          },
          {
            id: 3,
            name: '이영희',
            department: '영업팀',
            profileImage: null,
            status: 'absent',
            time: null
          }
        ]
        
        // 통계 계산
        this.stats = {
          attended: this.members.filter(m => m.status === 'attended').length,
          late: this.members.filter(m => m.status === 'late').length,
          absent: this.members.filter(m => m.status === 'absent').length
        }
      } catch (error) {
        console.error('Error fetching attendance data:', error)
      } finally {
        this.loading = false
      }
    },
    getStatusText(status) {
      const statusMap = {
        attended: '출근',
        late: '지각',
        absent: '미출근'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style scoped>
.attendance-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.attendance-widget h3 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #42b983;
  font-size: 1.1rem;
}

.attendance-list {
  flex: 1;
  overflow-y: auto;
}

.attendance-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-item .label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-item .value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.member-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.member-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
  object-fit: cover;
}

.info {
  display: flex;
  flex-direction: column;
}

.name {
  font-weight: 600;
  color: #2c3e50;
}

.department {
  font-size: 0.9rem;
  color: #666;
}

.status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status.attended {
  background: #e8f5e9;
  color: #2e7d32;
}

.status.late {
  background: #fff3e0;
  color: #ef6c00;
}

.status.absent {
  background: #ffebee;
  color: #c62828;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
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