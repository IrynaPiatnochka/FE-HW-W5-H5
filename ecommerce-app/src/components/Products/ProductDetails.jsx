import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import { Link } from "react-router-dom";

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetchProduct();
  }, []);

  const fetchProduct = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/products/${id}`);
      if (!response.ok) {
        throw new Error('Failed to fetch product');
      }
      const data = await response.json();
      setProduct(data);
    } catch (error) {
      console.error('Error fetching product:', error);
    }
  };

  if (!product) {
    return <p>Loading product details...</p>;
  }

  return (
    <div>
      <h1>Product Details</h1>
      <Card>
        <Card.Body>
          <Card.Title>{product.product_name}</Card.Title>
          <Card.Text>Price: ${product.price}</Card.Text>
          <Card.Text>Description: {product.description}</Card.Text>
        </Card.Body>
      </Card>
      <Link to={`/products`} className="btn btn-primary mr-2">
        Back
      </Link>
    </div>
  );
};

export default ProductDetails;
