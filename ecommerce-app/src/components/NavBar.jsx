// src/components/NavBar.js
import React from "react";
import { NavLink } from "react-router-dom";

const NavBar = () => {
  return (
    <nav>
      <ul>
      <li>
          <NavLink exact to="/newcustomer" activeClassName="active">
            Add New Customers
          </NavLink>
        </li>
        <li>
          <NavLink exact to="/customers" activeClassName="active">
            Customers
          </NavLink>
        </li>
        <li>
          <NavLink exact to="/newproduct" activeClassName="active">
            Add New Product
          </NavLink>
        </li>
        <li>
          <NavLink exact to="/products" activeClassName="active">
            Products
          </NavLink>
        </li>
        <li>
          <NavLink exact to="/neworder" activeClassName="active">
            Add New Product
          </NavLink>
        </li>
        <li>
          <NavLink exact to="/orders" activeClassName="active">
            Orders
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
