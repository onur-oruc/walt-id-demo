import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getAllDids = async () => {
  const walletId = import.meta.env.VITE_OEM_WALLET_ID;
  const token = import.meta.env.VITE_OEM_TOKEN;
  const response = await axios.get(`${API_URL}/oem/wallet/dids`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const getAllCredentials = async () => {
  const walletId = import.meta.env.VITE_OEM_WALLET_ID;
  const token = import.meta.env.VITE_OEM_TOKEN;
  const response = await axios.get(`${API_URL}/oem/wallet/credentials`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
}; 