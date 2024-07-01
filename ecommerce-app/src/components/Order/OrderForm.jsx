import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button } from 'react-bootstrap';

const OrderForm = () => {
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [customerId, setCustomerId] = useState('');
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchCustomers();
    fetchProducts();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/customers');
      if (!response.ok) {
        throw new Error('Failed to fetch customers');
      }
      const data = await response.json();
      setCustomers(data);
    } catch (error) {
      console.error('Error fetching customers:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/products');
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ customer_id: customerId, product_id: productId, quantity }),
      });
      if (!response.ok) {
        throw new Error('Failed to add order');
      }
      // Redirect to order list after successful submission
      navigate('/orders');
    } catch (error) {
      console.error('Error adding order:', error);
    }
  };

  return (
    <div>
      <h1>Add Order</h1>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="customerId">
          <Form.Label>Customer</Form.Label>
          <Form.Control
            as="select"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
            required
          >
            <option value="">Select customer...</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.customer_name}
              </option>
            ))}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="productId">
          <Form.Label>Product</Form.Label>
          <Form.Control
            as="select"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            required
          >
            <option value="">Select product...</option>
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.product_name}
              </option>
            ))}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="quantity">
          <Form.Label>Quantity</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </div>
  );
};

export default OrderForm;
