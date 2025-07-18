import React from 'react';
import { useParams } from 'react-router-dom';

export default function ItemDetail() {
  const { id } = useParams();
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Item Detail</h1>
        <p className="mt-1 text-sm text-gray-500">
          Viewing item ID: {id}
        </p>
      </div>
      
      <div className="card p-6">
        <p className="text-gray-500">Item detail view will be implemented here.</p>
      </div>
    </div>
  );
}