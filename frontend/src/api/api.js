import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  timeout: parseInt(process.env.REACT_APP_TIMEOUT) || 5000,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (username, email, password) =>
    api.post('/api/auth/register', { username, email, password }),
  login: (email, password) =>
    api.post('/api/auth/login', { email, password }),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    return Promise.resolve();
  },
  getProfile: () => api.get('/api/auth/profile'),
};

// Products API
export const productsAPI = {
  getAll: (page = 1, perPage = 10, category = '', search = '') =>
    api.get('/api/products', {
      params: { page, per_page: perPage, category, search },
    }),
  getById: (id) => api.get(`/api/products/${id}`),
  create: (data) => api.post('/api/products', data),
  update: (id, data) => api.put(`/api/products/${id}`, data),
  delete: (id) => api.delete(`/api/products/${id}`),
  getCategories: () => api.get('/api/products/categories'),
};

// Cart API
export const cartAPI = {
  get: () => api.get('/api/cart'),
  add: (productId, quantity) =>
    api.post('/api/cart/add', { product_id: productId, quantity }),
  update: (itemId, quantity) =>
    api.put(`/api/cart/${itemId}`, { quantity }),
  remove: (itemId) => api.delete(`/api/cart/${itemId}`),
  clear: () => api.delete('/api/cart'),
};

// Orders API
export const ordersAPI = {
  getAll: () => api.get('/api/orders'),
  getById: (id) => api.get(`/api/orders/${id}`),
  create: (data) => api.post('/api/orders', data),
  updateStatus: (id, status) => api.put(`/api/orders/${id}`, { status }),
};

export default api;
