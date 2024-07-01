// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import CustomerList from "./components/Customers/CustomerList";
import CustomerDetails from "./components/Customers/CustomerDetails";
import CustomerForm from "./components/Customers/CustomerForm";
import ProductList from "./components/Products/ProductList";
import ProductForm from "./components/Products/ProductForm";
import ProductDetails from "./components/Products/ProductDetails";
import OrderForm from "./components/Order/OrderForm";


const App = () => {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/newcustomer" element={<CustomerForm />} />
        <Route path="/customers" element={<CustomerList />} />
        <Route path="/customers/:id" element={<CustomerDetails />} />
        <Route path="/newproduct" element={<ProductForm />} />
        <Route path="/products" element={<ProductList />} />
        <Route path="products/:id" element={<ProductDetails />} />
        <Route path="/orders" element={<OrderForm />} />
        
      </Routes>
    </>
  );
};

export default App;
