import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { itemAPI } from '../services/api';
import { toast } from 'react-toastify';

export default function Items() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await itemAPI.list();
      setItems(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
      toast.error('Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  const filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.sku.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Items</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your inventory items and master data
          </p>
        </div>
        <button className="btn-primary">
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Item
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <MagnifyingGlassIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search items..."
          className="input pl-10"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Items Table */}
      <div className="card">
        <div className="table-container">
          <table className="table">
            <thead className="table-header">
              <tr>
                <th className="table-header-cell">SKU</th>
                <th className="table-header-cell">Name</th>
                <th className="table-header-cell">Category</th>
                <th className="table-header-cell">Unit</th>
                <th className="table-header-cell">Stock</th>
                <th className="table-header-cell">Status</th>
                <th className="table-header-cell">Actions</th>
              </tr>
            </thead>
            <tbody className="table-body">
              {filteredItems.map((item) => (
                <tr key={item.id} className="table-row">
                  <td className="table-cell">
                    <Link to={`/items/${item.id}`} className="text-primary-600 hover:text-primary-500">
                      {item.sku}
                    </Link>
                  </td>
                  <td className="table-cell">{item.name}</td>
                  <td className="table-cell">{item.category_name || '-'}</td>
                  <td className="table-cell">{item.unit_of_measure}</td>
                  <td className="table-cell">{item.total_quantity || 0}</td>
                  <td className="table-cell">
                    <span className={`badge ${
                      item.is_low_stock ? 'badge-red' : 
                      item.is_active ? 'badge-green' : 'badge-gray'
                    }`}>
                      {item.is_low_stock ? 'Low Stock' : 
                       item.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="table-cell">
                    <Link to={`/items/${item.id}`} className="text-primary-600 hover:text-primary-500">
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}