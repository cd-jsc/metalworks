import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Items from './pages/Items';
import ItemDetail from './pages/ItemDetail';
import ProductTemplates from './pages/ProductTemplates';
import ProductVariants from './pages/ProductVariants';
import Categories from './pages/Categories';
import Tags from './pages/Tags';
import Warehouses from './pages/Warehouses';
import WarehouseDetail from './pages/WarehouseDetail';
import Locations from './pages/Locations';
import LocationDetail from './pages/LocationDetail';
import BinLocations from './pages/BinLocations';
import StockLevels from './pages/StockLevels';
import StockMovements from './pages/StockMovements';
import Batches from './pages/Batches';
import Suppliers from './pages/Suppliers';
import CycleCounts from './pages/CycleCounts';
import CycleCountDetail from './pages/CycleCountDetail';
import BarcodeScanner from './pages/BarcodeScanner';
import LabelPrinting from './pages/LabelPrinting';
import Reports from './pages/Reports';

function App() {
  return (
    <Router>
      <div className="App">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            
            {/* Inventory Routes */}
            <Route path="/items" element={<Items />} />
            <Route path="/items/:id" element={<ItemDetail />} />
            <Route path="/product-templates" element={<ProductTemplates />} />
            <Route path="/product-variants" element={<ProductVariants />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/tags" element={<Tags />} />
            <Route path="/batches" element={<Batches />} />
            
            {/* Location Routes */}
            <Route path="/warehouses" element={<Warehouses />} />
            <Route path="/warehouses/:id" element={<WarehouseDetail />} />
            <Route path="/locations" element={<Locations />} />
            <Route path="/locations/:id" element={<LocationDetail />} />
            <Route path="/bin-locations" element={<BinLocations />} />
            
            {/* Stock Management Routes */}
            <Route path="/stock-levels" element={<StockLevels />} />
            <Route path="/stock-movements" element={<StockMovements />} />
            <Route path="/cycle-counts" element={<CycleCounts />} />
            <Route path="/cycle-counts/:id" element={<CycleCountDetail />} />
            
            {/* Operations Routes */}
            <Route path="/barcode-scanner" element={<BarcodeScanner />} />
            <Route path="/label-printing" element={<LabelPrinting />} />
            <Route path="/suppliers" element={<Suppliers />} />
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