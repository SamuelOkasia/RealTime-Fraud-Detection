import { render, screen, act } from '@testing-library/react';
import TransactionHistory from '../TransactionHistory/TransactionHistory';

test('renders "No data" message when there are no transactions', () => {
  render(<TransactionHistory />);

  // Check for the "No data" message from Ant Design's Table component
  const noDataMessage = screen.getByText(/No data/i);
  expect(noDataMessage).toBeInTheDocument();
});

test('renders transactions in the table when data is received via WebSocket', async () => {
  // Mock WebSocket and its methods
  const mockWebSocket = {
    onopen: jest.fn(),
    onmessage: jest.fn(),
    onerror: jest.fn(),
    onclose: jest.fn(),
    close: jest.fn(),
    send: jest.fn(),
  };

  global.WebSocket = jest.fn(() => mockWebSocket);

  // Render the component
  render(<TransactionHistory />);

  // Simulate receiving WebSocket data
  const mockTransaction = {
    id: '1',
    amount: 100,
    location: 'NY',
    user_id: '123',
    time: new Date().toISOString(),
    is_fraud: false,
  };

  // Wrap the onmessage call in act() to ensure the state update is completed
  await act(async () => {
    mockWebSocket.onmessage({
      data: JSON.stringify(mockTransaction),
    });
  });

  // Wait for the transaction data to appear in the table using findByText
  const amountCell = await screen.findByText('100');
  expect(amountCell).toBeInTheDocument();

  const locationCell = await screen.findByText('NY');
  expect(locationCell).toBeInTheDocument();

  const userIdCell = await screen.findByText('123');
  expect(userIdCell).toBeInTheDocument();
});
