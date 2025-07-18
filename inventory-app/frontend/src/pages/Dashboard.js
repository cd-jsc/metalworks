import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  CubeIcon,
  BuildingStorefrontIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { stockLevelAPI, itemAPI, batchAPI, stockMovementAPI } from '../services/api';
import { toast } from 'react-toastify';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalItems: 0,
    totalQuantity: 0,
    lowStockItems: 0,
    expiringSoon: 0,
    locations: []
  });
  const [lowStockItems, setLowStockItems] = useState([]);
  const [expiringBatches, setExpiringBatches] = useState([]);
  const [recentMovements, setRecentMovements] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [
        stockSummary,
        lowStock,
        expiring,
        movements
      ] = await Promise.all([
        stockLevelAPI.summary(),
        itemAPI.lowStock(),
        batchAPI.expiringSoon(),
        stockMovementAPI.recent()
      ]);

      setStats({
        totalItems: stockSummary.data.total_items,
        totalQuantity: stockSummary.data.total_quantity,
        lowStockItems: lowStock.data.length,
        expiringSoon: expiring.data.length,
        locations: stockSummary.data.locations
      });

      setLowStockItems(lowStock.data.slice(0, 5));
      setExpiringBatches(expiring.data.slice(0, 5));
      setRecentMovements(movements.data.slice(0, 10));
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color, link, change }) => (
    <div className="card p-6">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <Icon className={`h-8 w-8 ${color}`} />
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd className="flex items-baseline">
              <div className="text-2xl font-semibold text-gray-900">{value}</div>
              {change && (
                <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                  change.type === 'increase' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {change.type === 'increase' ? (
                    <ArrowTrendingUpIcon className="h-4 w-4 flex-shrink-0" />
                  ) : (
                    <ArrowTrendingDownIcon className="h-4 w-4 flex-shrink-0" />
                  )}
                  <span className="sr-only">{change.type === 'increase' ? 'Increased' : 'Decreased'} by</span>
                  {change.value}
                </div>
              )}
            </dd>
          </dl>
        </div>
      </div>
      {link && (
        <div className="mt-4">
          <Link to={link} className="text-sm font-medium text-primary-600 hover:text-primary-500">
            View details →
          </Link>
        </div>
      )}
    </div>
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your inventory management system
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Items"
          value={stats.totalItems.toLocaleString()}
          icon={CubeIcon}
          color="text-blue-600"
          link="/items"
        />
        <StatCard
          title="Total Quantity"
          value={stats.totalQuantity.toLocaleString()}
          icon={BuildingStorefrontIcon}
          color="text-green-600"
          link="/stock-levels"
        />
        <StatCard
          title="Low Stock Items"
          value={stats.lowStockItems}
          icon={ExclamationTriangleIcon}
          color="text-yellow-600"
          link="/items?filter=low_stock"
        />
        <StatCard
          title="Expiring Soon"
          value={stats.expiringSoon}
          icon={ClockIcon}
          color="text-red-600"
          link="/batches?filter=expiring"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Stock by Location Chart */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Stock by Location</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats.locations}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="location__name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total_qty" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Stock Distribution Pie Chart */}
        <div className="card p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Stock Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats.locations}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ location__name, percent }) => `${location__name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="total_qty"
              >
                {stats.locations.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tables Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Low Stock Items */}
        <div className="card">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Low Stock Items</h3>
          </div>
          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Item
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Current Stock
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Reorder Point
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {lowStockItems.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{item.name}</div>
                        <div className="text-sm text-gray-500">{item.sku}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{item.total_quantity}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{item.reorder_point}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-6 py-3 border-t border-gray-200">
            <Link to="/items?filter=low_stock" className="text-sm text-primary-600 hover:text-primary-500">
              View all low stock items →
            </Link>
          </div>
        </div>

        {/* Expiring Batches */}
        <div className="card">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Expiring Batches</h3>
          </div>
          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Batch
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Item
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Expiry Date
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {expiringBatches.map((batch) => (
                  <tr key={batch.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-gray-900">{batch.batch_number}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm text-gray-900">{batch.item_name}</div>
                        <div className="text-sm text-gray-500">{batch.item_sku}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-red-600">{batch.expiry_date}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-6 py-3 border-t border-gray-200">
            <Link to="/batches?filter=expiring" className="text-sm text-primary-600 hover:text-primary-500">
              View all expiring batches →
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Movements */}
      <div className="card">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Stock Movements</h3>
        </div>
        <div className="overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Reference
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Item
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quantity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentMovements.map((movement) => (
                <tr key={movement.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm font-medium text-gray-900">{movement.reference_number}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`badge ${
                      movement.movement_type === 'receipt' ? 'badge-green' :
                      movement.movement_type === 'issue' ? 'badge-red' :
                      movement.movement_type === 'transfer_in' ? 'badge-blue' :
                      movement.movement_type === 'transfer_out' ? 'badge-yellow' :
                      'badge-gray'
                    }`}>
                      {movement.movement_type.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm text-gray-900">{movement.item_name}</div>
                      <div className="text-sm text-gray-500">{movement.item_sku}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-900">{movement.quantity}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-900">{movement.location_name}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-500">
                      {new Date(movement.created_at).toLocaleDateString()}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="px-6 py-3 border-t border-gray-200">
          <Link to="/stock-movements" className="text-sm text-primary-600 hover:text-primary-500">
            View all movements →
          </Link>
        </div>
      </div>
    </div>
  );
}