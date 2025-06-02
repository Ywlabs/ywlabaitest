import React, { useState } from 'react';
import { Box, Typography, Button } from '@mui/material';
import EmployeeInfoWidget from './EmployeeInfoWidget';
import axios from 'axios';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [activeWidget, setActiveWidget] = useState(null);

    const handleButtonClick = async (targetUrl) => {
        if (targetUrl === '/api/employee-info') {
            setActiveWidget('employee_info');
        }
    };

    const handleSendMessage = async (message) => {
        try {
            const response = await axios.post('/api/chat', { question: message });
            
            if (response.data.status === 'success') {
                const newMessage = {
                    type: 'ai',
                    content: response.data.response,
                    targetUrl: response.data.target_url,
                    buttonText: response.data.button_text,
                    showWidget: response.data.show_widget,
                    widgetType: response.data.widget_type
                };
                
                setMessages(prev => [...prev, newMessage]);
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <Box>
            {/* 메시지 목록 */}
            {messages.map((message, index) => (
                <Box key={index} mb={2}>
                    <Typography>{message.content}</Typography>
                    {message.targetUrl && message.buttonText && (
                        <Button 
                            variant="contained" 
                            onClick={() => handleButtonClick(message.targetUrl)}
                        >
                            {message.buttonText}
                        </Button>
                    )}
                </Box>
            ))}

            {/* 위젯 영역 */}
            {activeWidget === 'employee_info' && (
                <Box mt={2}>
                    <EmployeeInfoWidget />
                </Box>
            )}
        </Box>
    );
};

export default Chat; 