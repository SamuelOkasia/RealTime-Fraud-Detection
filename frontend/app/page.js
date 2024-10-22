// 'use client' directive ensures this component will run on the client-side only.
'use client';

import './page.css';
import { useState } from 'react';
import { Form, Input, Button, Select, Typography, Alert } from 'antd';
import TransactionHistory from '@/components/TransactionHistory/TransactionHistory';  // Import custom TransactionHistory component

const { Title } = Typography;  // Destructure Typography for easy access to Title component

/**
 * Home Component - This is the main page for submitting a transaction and viewing transaction history.
 * It handles form submission, error handling, and displays a real-time transaction history.
 */
export default function Home() {
  // State to manage form input values for a new transaction
  const [transaction, setTransaction] = useState({
    amount: '',
    location: 'New York',  // Default location
    user_id: '',
  });

  // State to store the response message after form submission
  const [responseMessage, setResponseMessage] = useState('');
  
  // State to store any error message encountered during form submission
  const [error, setError] = useState('');
  
  // State to manage loading state for submit button
  const [loading, setLoading] = useState(false);

  /**
   * handleSubmit - Handles form submission, sends a POST request to the backend to submit a transaction.
   * 
   * @param {Object} values - The form values (amount, location, user_id).
   */
  const handleSubmit = async (values) => {
    setError('');
    setLoading(true);  // Set loading state when the form is submitted

    // Helper function to format the current date and time into ISO format
    const formatDate = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');
      return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
    };
    const formattedTime = formatDate(new Date());

    // Try-catch block to handle API request to the backend
    try {
      const res = await fetch(`http://fraud-detection-alb-467209949.eu-west-2.elb.amazonaws.com/api/transaction`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...values,
          time: formattedTime,  // Include the formatted time in the request body
        }),
      });

      const data = await res.json();
      setResponseMessage(data.status);  // Display success message
    } catch (err) {
      setError('An error occurred while submitting the transaction');  // Display error message
    } finally {
      setLoading(false);  // Reset loading state after the API request completes
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem', margin: '2rem 0' }}>
      <Title level={2} style={{ color: '#ffffff' }}>Real-Time Fraud Detection</Title>

       {/* Informational message about Kafka service being down */}
       <Alert 
          message="Due to the running cost of using Amazon MSK, the Kafka service is currently not running. For demonstration purposes, please watch the video below showing the full Fraud Detection service in action."
          type="info"
          showIcon 
        />


      {/* Embedded local video for demonstration purposes */}
      <div style={{ width: '100%', display: 'flex', justifyContent: 'center', margin: '1rem 0' }}>
        <video width="560" height="315" controls>
          <source src="/videos/demo.mp4" type="video/mp4" />  {/* Path to local video */}
          Your browser does not support the video tag.
        </video>
      </div>
      
      {error && <Alert message={error} type="error" showIcon />}  // Display error alert if error occurs
      
      {/* Ant Design Form component to handle input for submitting a transaction */}
      <Form
        onFinish={handleSubmit}  // Function triggered on form submission
        initialValues={transaction}  // Initial values for form fields
        layout="inline"
        style={{
          backgroundColor: '#151921',
          padding: '10px',
          borderRadius: '8px',
          display: 'flex',
          width: 1000,
          border: '1px solid #38435a',
          alignItems: 'center',
          justifyItems: 'center'
        }}
      >
        {/* Form item for Amount input */}
        <Form.Item
          label={<span style={{ color: 'white', marginRight: '1.5rem' }}>Amount: </span>}
          name="amount"
          rules={[{ required: true, message: 'Please input the amount' }]}  // Validation rule
          style={{ width: '200px' }}
        >
          <Input
            type="number"
            placeholder='Amount'
            size='medium'
            style={{
              color: 'white',
              backgroundColor: '#151921',
              border: '1px solid #38435a',
            }}
          />
        </Form.Item>

        {/* Form item for Location select dropdown */}
        <Form.Item
          label={<span style={{ color: 'white' }}>Location: </span>}
          name="location"
          rules={[{ required: true, message: 'Please select a location' }]}  // Validation rule
          style={{ width: '200px', borderRadius: '8px' }}
        >
          <Select
            size='medium'
            style={{
              color: 'white',
              backgroundColor: '#151921',
              border: '1px solid #38435a',
              borderRadius: '8px'
            }}
            className="custom-select"
            dropdownStyle={{ backgroundColor: '#ffffff', color: 'white' }}  // Custom style for dropdown
          >
            {/* Dropdown options for selecting a location */}
            <Select.Option value="New York">New York</Select.Option>
            <Select.Option value="San Francisco">San Francisco</Select.Option>
            <Select.Option value="Los Angeles">Los Angeles</Select.Option>
            <Select.Option value="Chicago">Chicago</Select.Option>
            <Select.Option value="Houston">Houston</Select.Option>
          </Select>
        </Form.Item>

        {/* Form item for User ID input */}
        <Form.Item
          label={<span style={{ color: 'white', marginRight: '1.5rem' }}>User ID</span>}
          name="user_id"
          rules={[{ required: true, message: 'Please input the User ID' }]}  // Validation rule
          style={{ width: '200px' }}
          size='medium'
        >
          <Input
            style={{
              color: 'white',
              backgroundColor: '#151921',
              border: '1px solid #38435a',
              borderRadius: '8px'
            }}
          />
        </Form.Item>

        {/* Submit button */}
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Submit
          </Button>
        </Form.Item>

        {/* Show success message if transaction is successfully submitted */}
        {responseMessage && <Alert message='Sent' type="success" showIcon size='medium' />}
      </Form>

      {/* Display transaction history component */}
      <TransactionHistory />
    </div>
  );
}
