import React from 'react';
import { useParams } from 'react-router-dom';

export default function WarehouseDetail() {
  const { id } = useParams();
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Warehouse Detail</h1>
        <p className="mt-1 text-sm text-gray-500">
          Viewing warehouse ID: {id}
        </p>
      </div>
      
      <div className="card p-6">
        <p className="text-gray-500">Warehouse detail view will be implemented here.</p>
      </div>
    </div>
  );
}