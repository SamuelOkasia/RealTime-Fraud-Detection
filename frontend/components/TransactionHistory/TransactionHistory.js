'use client';

import React, { useEffect, useState } from 'react';
import { Table, Typography, Alert, Tag } from 'antd';
import './TransactionHistory.css';  // Custom CSS for table styling

const { Title } = Typography;

/**
 * TransactionHistory Component
 * 
 * This component renders a table that displays transaction history in real-time using WebSockets.
 * Transactions are updated as new data is received from the backend via WebSocket.
 */
const TransactionHistory = () => {
  // State to manage the list of transactions
  const [transactions, setTransactions] = useState([]);
  
  // State to manage any error that occurs with WebSocket connection
  const [error, setError] = useState('');

  /**
   * useEffect Hook - Establishes a WebSocket connection on component mount.
   * 
   * - Receives new transaction data from the backend in real-time and updates the transaction history.
   * - Handles WebSocket connection, message reception, and error handling.
   */
  useEffect(() => {
    // Initialize WebSocket connection to the backend
    const ws = new WebSocket(`ws://fraud-detection-alb-467209949.eu-west-2.elb.amazonaws.com/api/ws`);

    // When WebSocket connection is established
    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    // On receiving new data from the WebSocket connection
    ws.onmessage = (event) => {
      console.log('Received data from WebSocket:', event.data);
      const data = JSON.parse(event.data);

      // Update the transaction list by adding the new transaction to the top
      setTransactions((prevTransactions) => [data, ...prevTransactions]);
    };

    // Handle WebSocket errors
    ws.onerror = (err) => {
      console.error('WebSocket encountered error:', err.message);
      setError('WebSocket error. Please try again later.');
      ws.close();
    };

    // Clean up WebSocket connection when component unmounts
    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      ws.close();  // Close the WebSocket connection on cleanup
    };
  }, []);

  // Sort transactions by time (latest first)
  const sortedTransactions = transactions.sort((a, b) => new Date(b.time) - new Date(a.time));

  // Define columns for the Ant Design Table component
  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },  // Display transaction ID
    {
      title: 'Amount',
      dataIndex: 'amount',
      key: 'amount',
      render: (amount) =>
        new Intl.NumberFormat('en-GB', {
          style: 'currency',
          currency: 'GBP',
        }).format(amount),
    },  // Display transaction amount
    { title: 'Location', dataIndex: 'location', key: 'location' },  // Display transaction location
    { title: 'User ID', dataIndex: 'user_id', key: 'user_id' },  // Display user ID associated with transaction
    {
      title: 'Time',
      dataIndex: 'time',
      key: 'time',
      render: (text) => new Date(text).toLocaleString(),  // Format time in a readable format
    },
    {
      // Display fraud status with conditional styling
      title: 'Fraud Status',
      dataIndex: 'is_fraud',
      key: 'is_fraud',
      render: (isFraud) => (
        <Tag
          style={{
            backgroundColor: isFraud ? '#5E0003' : '#0F2F00',  // Dark red for fraud, green for legit
            color: isFraud ? '#E52848' : '#199B00',  // Lighter red for fraud, lighter green for legit
            border: isFraud ? '1px solid #92001F' : '1px solid #2D5500',  // Custom border colors
          }}
        >
          {isFraud ? 'Fraud' : 'Legit'}
        </Tag>
      ),
    }
  ];

  return (
    <div style={{ width: 1000, padding: '1rem', border: '1px solid #38435a', borderRadius: '8px' }}>
      {/* Optional title for transaction history */}
      {/* <Title level={2} style={{ color: 'white' }}>Transaction History</Title> */}
      
      {/* Display error message if WebSocket error occurs */}
      {error && <Alert message={error} type="error" showIcon />}

      {/* Ant Design Table component to display transaction data */}
      <Table
        dataSource={sortedTransactions}  // Pass sorted transactions to table
        columns={columns}  // Define table columns
        rowKey="id"  // Unique key for each row (transaction ID)
        pagination={{ pageSize: 20 }}  // Limit pagination to 20 rows per page
        className="custom-table"  // Custom styling for table
      />
    </div>
  );
};

export default TransactionHistory;
