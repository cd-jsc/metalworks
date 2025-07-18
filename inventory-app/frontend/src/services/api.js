import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  // Categories
  categories: '/categories/',
  categorySelectOptions: '/categories/select_options/',
  
  // Tags
  tags: '/tags/',
  tagSelectOptions: '/tags/select_options/',
  
  // Suppliers
  suppliers: '/suppliers/',
  supplierSelectOptions: '/suppliers/select_options/',
  
  // Warehouses
  warehouses: '/warehouses/',
  warehouseSelectOptions: '/warehouses/select_options/',
  warehouseStockSummary: (id) => `/warehouses/${id}/stock_summary/`,
  
  // Locations
  locations: '/locations/',
  locationSelectOptions: '/locations/select_options/',
  locationStockSummary: (id) => `/locations/${id}/stock_summary/`,
  
  // Bin Locations
  binLocations: '/bin-locations/',
  binLocationSelectOptions: '/bin-locations/select_options/',
  
  // Product Templates
  productTemplates: '/product-templates/',
  productTemplateSelectOptions: '/product-templates/select_options/',
  
  // Product Variants
  productVariants: '/product-variants/',
  productVariantSelectOptions: '/product-variants/select_options/',
  
  // Items
  items: '/items/',
  itemSelectOptions: '/items/select_options/',
  itemsLowStock: '/items/low_stock/',
  itemStockHistory: (id) => `/items/${id}/stock_history/`,
  itemAdjustStock: (id) => `/items/${id}/adjust_stock/`,
  itemGenerateBarcode: (id) => `/items/${id}/generate_barcode/`,
  
  // Barcodes
  barcodes: '/barcodes/',
  barcodeLookupItem: '/barcodes/lookup_item/',
  
  // Labels
  labels: '/labels/',
  labelPrint: (id) => `/labels/${id}/print_label/`,
  
  // Batches
  batches: '/batches/',
  batchesExpiringSoon: '/batches/expiring_soon/',
  batchesExpired: '/batches/expired/',
  
  // Stock Levels
  stockLevels: '/stock-levels/',
  stockLevelsSummary: '/stock-levels/summary/',
  
  // Stock Movements
  stockMovements: '/stock-movements/',
  stockMovementsRecent: '/stock-movements/recent/',
  stockMovementsTransfer: '/stock-movements/transfer/',
  
  // Stock Reservations
  stockReservations: '/stock-reservations/',
  stockReservationsActive: '/stock-reservations/active/',
  stockReservationsExpiring: '/stock-reservations/expiring/',
  
  // Cycle Counts
  cycleCounts: '/cycle-counts/',
  cycleCountStart: (id) => `/cycle-counts/${id}/start_count/`,
  cycleCountComplete: (id) => `/cycle-counts/${id}/complete_count/`,
  
  // Cycle Count Items
  cycleCountItems: '/cycle-count-items/',
  cycleCountItemCount: (id) => `/cycle-count-items/${id}/count_item/`,
};

// Generic API functions
export const apiService = {
  // GET requests
  get: (url, params = {}) => api.get(url, { params }),
  
  // POST requests
  post: (url, data = {}) => api.post(url, data),
  
  // PUT requests
  put: (url, data = {}) => api.put(url, data),
  
  // PATCH requests
  patch: (url, data = {}) => api.patch(url, data),
  
  // DELETE requests
  delete: (url) => api.delete(url),
};

// Specific API functions
export const categoryAPI = {
  list: (params) => apiService.get(endpoints.categories, params),
  create: (data) => apiService.post(endpoints.categories, data),
  get: (id) => apiService.get(`${endpoints.categories}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.categories}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.categories}${id}/`),
  selectOptions: () => apiService.get(endpoints.categorySelectOptions),
};

export const tagAPI = {
  list: (params) => apiService.get(endpoints.tags, params),
  create: (data) => apiService.post(endpoints.tags, data),
  get: (id) => apiService.get(`${endpoints.tags}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.tags}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.tags}${id}/`),
  selectOptions: () => apiService.get(endpoints.tagSelectOptions),
};

export const supplierAPI = {
  list: (params) => apiService.get(endpoints.suppliers, params),
  create: (data) => apiService.post(endpoints.suppliers, data),
  get: (id) => apiService.get(`${endpoints.suppliers}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.suppliers}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.suppliers}${id}/`),
  selectOptions: () => apiService.get(endpoints.supplierSelectOptions),
};

export const warehouseAPI = {
  list: (params) => apiService.get(endpoints.warehouses, params),
  create: (data) => apiService.post(endpoints.warehouses, data),
  get: (id) => apiService.get(`${endpoints.warehouses}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.warehouses}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.warehouses}${id}/`),
  selectOptions: () => apiService.get(endpoints.warehouseSelectOptions),
  stockSummary: (id) => apiService.get(endpoints.warehouseStockSummary(id)),
};

export const locationAPI = {
  list: (params) => apiService.get(endpoints.locations, params),
  create: (data) => apiService.post(endpoints.locations, data),
  get: (id) => apiService.get(`${endpoints.locations}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.locations}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.locations}${id}/`),
  selectOptions: () => apiService.get(endpoints.locationSelectOptions),
  stockSummary: (id) => apiService.get(endpoints.locationStockSummary(id)),
};

export const binLocationAPI = {
  list: (params) => apiService.get(endpoints.binLocations, params),
  create: (data) => apiService.post(endpoints.binLocations, data),
  get: (id) => apiService.get(`${endpoints.binLocations}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.binLocations}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.binLocations}${id}/`),
  selectOptions: () => apiService.get(endpoints.binLocationSelectOptions),
};

export const productTemplateAPI = {
  list: (params) => apiService.get(endpoints.productTemplates, params),
  create: (data) => apiService.post(endpoints.productTemplates, data),
  get: (id) => apiService.get(`${endpoints.productTemplates}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.productTemplates}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.productTemplates}${id}/`),
  selectOptions: () => apiService.get(endpoints.productTemplateSelectOptions),
};

export const productVariantAPI = {
  list: (params) => apiService.get(endpoints.productVariants, params),
  create: (data) => apiService.post(endpoints.productVariants, data),
  get: (id) => apiService.get(`${endpoints.productVariants}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.productVariants}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.productVariants}${id}/`),
  selectOptions: () => apiService.get(endpoints.productVariantSelectOptions),
};

export const itemAPI = {
  list: (params) => apiService.get(endpoints.items, params),
  create: (data) => apiService.post(endpoints.items, data),
  get: (id) => apiService.get(`${endpoints.items}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.items}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.items}${id}/`),
  selectOptions: () => apiService.get(endpoints.itemSelectOptions),
  lowStock: () => apiService.get(endpoints.itemsLowStock),
  stockHistory: (id) => apiService.get(endpoints.itemStockHistory(id)),
  adjustStock: (id, data) => apiService.post(endpoints.itemAdjustStock(id), data),
  generateBarcode: (id, data) => apiService.post(endpoints.itemGenerateBarcode(id), data),
};

export const barcodeAPI = {
  list: (params) => apiService.get(endpoints.barcodes, params),
  create: (data) => apiService.post(endpoints.barcodes, data),
  get: (id) => apiService.get(`${endpoints.barcodes}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.barcodes}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.barcodes}${id}/`),
  lookupItem: (data) => apiService.post(endpoints.barcodeLookupItem, data),
};

export const labelAPI = {
  list: (params) => apiService.get(endpoints.labels, params),
  create: (data) => apiService.post(endpoints.labels, data),
  get: (id) => apiService.get(`${endpoints.labels}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.labels}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.labels}${id}/`),
  print: (id, data) => apiService.post(endpoints.labelPrint(id), data),
};

export const batchAPI = {
  list: (params) => apiService.get(endpoints.batches, params),
  create: (data) => apiService.post(endpoints.batches, data),
  get: (id) => apiService.get(`${endpoints.batches}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.batches}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.batches}${id}/`),
  expiringSoon: () => apiService.get(endpoints.batchesExpiringSoon),
  expired: () => apiService.get(endpoints.batchesExpired),
};

export const stockLevelAPI = {
  list: (params) => apiService.get(endpoints.stockLevels, params),
  create: (data) => apiService.post(endpoints.stockLevels, data),
  get: (id) => apiService.get(`${endpoints.stockLevels}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.stockLevels}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.stockLevels}${id}/`),
  summary: () => apiService.get(endpoints.stockLevelsSummary),
};

export const stockMovementAPI = {
  list: (params) => apiService.get(endpoints.stockMovements, params),
  create: (data) => apiService.post(endpoints.stockMovements, data),
  get: (id) => apiService.get(`${endpoints.stockMovements}${id}/`),
  recent: () => apiService.get(endpoints.stockMovementsRecent),
  transfer: (data) => apiService.post(endpoints.stockMovementsTransfer, data),
};

export const stockReservationAPI = {
  list: (params) => apiService.get(endpoints.stockReservations, params),
  create: (data) => apiService.post(endpoints.stockReservations, data),
  get: (id) => apiService.get(`${endpoints.stockReservations}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.stockReservations}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.stockReservations}${id}/`),
  active: () => apiService.get(endpoints.stockReservationsActive),
  expiring: () => apiService.get(endpoints.stockReservationsExpiring),
};

export const cycleCountAPI = {
  list: (params) => apiService.get(endpoints.cycleCounts, params),
  create: (data) => apiService.post(endpoints.cycleCounts, data),
  get: (id) => apiService.get(`${endpoints.cycleCounts}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.cycleCounts}${id}/`, data),
  delete: (id) => apiService.delete(`${endpoints.cycleCounts}${id}/`),
  start: (id) => apiService.post(endpoints.cycleCountStart(id)),
  complete: (id) => apiService.post(endpoints.cycleCountComplete(id)),
};

export const cycleCountItemAPI = {
  list: (params) => apiService.get(endpoints.cycleCountItems, params),
  get: (id) => apiService.get(`${endpoints.cycleCountItems}${id}/`),
  update: (id, data) => apiService.put(`${endpoints.cycleCountItems}${id}/`, data),
  count: (id, data) => apiService.post(endpoints.cycleCountItemCount(id), data),
};

export default api;