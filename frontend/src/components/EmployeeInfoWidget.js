import React, { useState, useEffect } from 'react';
import { 
    Box, 
    Typography, 
    CircularProgress,
    Alert
} from '@mui/material';

const EmployeeInfoWidget = ({ employeeId }) => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [employeeData, setEmployeeData] = useState(null);

    useEffect(() => {
        const fetchEmployeeData = async () => {
            try {
                setLoading(true);
                setError(null);
                
                const response = await fetch(`/api/employee/list?employee_id=${employeeId}`);
                if (!response.ok) {
                    throw new Error('직원 정보를 불러오는데 실패했습니다.');
                }

                const result = await response.json();
                if (result.status === 'success' && result.data) {
                    setEmployeeData(result.data);
                } else {
                    throw new Error(result.message || '직원 정보를 불러오는데 실패했습니다.');
                }
            } catch (err) {
                console.error('Error fetching employee data:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        if (employeeId) {
            fetchEmployeeData();
        }
    }, [employeeId]);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" p={2}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box p={2}>
                <Alert severity="error">{error}</Alert>
            </Box>
        );
    }

    if (!employeeData) {
        return (
            <Box p={2}>
                <Alert severity="info">직원 정보가 없습니다.</Alert>
            </Box>
        );
    }

    return (
        <Box p={2}>
            <Typography variant="h6" gutterBottom>
                {employeeData.name} ({employeeData.position})
            </Typography>
            <Typography variant="body2" color="textSecondary">
                부서: {employeeData.department}
            </Typography>
            <Typography variant="body2" color="textSecondary">
                이메일: {employeeData.email}
            </Typography>
            <Typography variant="body2" color="textSecondary">
                전화번호: {employeeData.phone}
            </Typography>
        </Box>
    );
};

export default EmployeeInfoWidget; 