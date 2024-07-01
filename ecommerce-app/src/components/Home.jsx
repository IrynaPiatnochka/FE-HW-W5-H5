import React from 'react';

const Home = () => {
  return (
    <div style={{
      backgroundImage: `url('https://png.pngtree.com/thumb_back/fw800/background/20230930/pngtree-a-dark-night-in-a-city-with-a-street-full-of-image_13138100.png')`, 
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      height: 'calc(100vh - 56px)', 
      justifyContent: 'center',
      alignItems: 'center',
      color: 'white',
      textAlign: 'center',
      fontSize: '2rem'
    }}>
      <h2>E-Commerce</h2>
    </div>
  );
};

export default Home;