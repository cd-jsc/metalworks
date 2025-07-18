import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Items from './pages/Items';
import ItemDetail from './pages/ItemDetail';
import Locations from './pages/Locations';
import LocationDetail from './pages/LocationDetail';
import StockLevels from './pages/StockLevels';
import StockMovements from './pages/StockMovements';
import Batches from './pages/Batches';
import Categories from './pages/Categories';
import Suppliers from './pages/Suppliers';
import CycleCounts from './pages/CycleCounts';
import CycleCountDetail from './pages/CycleCountDetail';
import Reports from './pages/Reports';

function App() {
  return (
    <Router>
      <div className="App">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/items" element={<Items />} />
            <Route path="/items/:id" element={<ItemDetail />} />
            <Route path="/locations" element={<Locations />} />
            <Route path="/locations/:id" element={<LocationDetail />} />
            <Route path="/stock-levels" element={<StockLevels />} />
            <Route path="/stock-movements" element={<StockMovements />} />
            <Route path="/batches" element={<Batches />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/suppliers" element={<Suppliers />} />
            <Route path="/cycle-counts" element={<CycleCounts />} />
            <Route path="/cycle-counts/:id" element={<CycleCountDetail />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </Layout>
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    </Router>
  );
}

export default App;