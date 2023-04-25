import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
/*
  When application is wrapped in <React.StrictMode> - components will render twice in development environments. 
  This is for error/warning detection. 
  Strict mode will intentionally invoke the following class component functions twice: 
  constructors, the render method, and the shouldComponentUpdate methods. 
  Read more about strict mode in the docs.
*/

  // <React.StrictMode>
    <App />
  // </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
