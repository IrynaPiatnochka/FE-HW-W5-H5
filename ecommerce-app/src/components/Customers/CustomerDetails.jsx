import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

const CustomerDetails = () => {
  const { id } = useParams();
  const [customer, setCustomer] = useState(null);

  useEffect(() => {
    fetchCustomer();
  }, []);

  const fetchCustomer = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/customers/${id}`);
      if (!response.ok) {
        throw new Error("Failed to fetch customer");
      }
      const data = await response.json();
      setCustomer(data);
    } catch (error) {
      console.error("Error fetching customer:", error);
    }
  };

  if (!customer) {
    return <p>Loading customer details...</p>;
  }

  return (
    <div>
      <h1>Customer Details</h1>
      <Card>
        <Card.Body>
          <Card.Title>{customer.customer_name}</Card.Title>
          <Card.Text>Email: {customer.email}</Card.Text>
          <Card.Text>Phone: {customer.phone}</Card.Text>
        </Card.Body>
      </Card>
      <Link to={`/customers`} className="btn btn-primary mr-2">
        Back
      </Link>
    </div>
  );
};

export default CustomerDetails;
