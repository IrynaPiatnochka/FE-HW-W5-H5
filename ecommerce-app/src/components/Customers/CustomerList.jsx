import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button, Table } from "react-bootstrap";

const CustomerList = () => {
  const [customers, setCustomers] = useState([{}]);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/customers");
      if (!response.ok) {
        throw new Error("Failed to fetch customers");
      }
      const data = await response.json();
      setCustomers(data);
    } catch (error) {
      console.error("Error fetching customers:", error);
    }
  };

  const deleteCustomer = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000//customers/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Failed to delete customer");
      }
      // Refresh customer list after deletion
      fetchCustomers();
    } catch (error) {
      console.error("Error deleting customer:", error);
    }
  };

  return (
    <div>
      <h1>Customer List</h1>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.id}>
              <td>{customer.id}</td>
              <td>{customer.customer_name}</td>
              <td>{customer.email}</td>
              <td>{customer.phone}</td>
              <td>
                <Link
                  to={`/customers/${customer.id}`}
                  className="btn btn-primary mr-2"
                >
                  View
                </Link>
                <Button
                  variant="danger"
                  onClick={() => deleteCustomer(customer.id)}
                >
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default CustomerList;
