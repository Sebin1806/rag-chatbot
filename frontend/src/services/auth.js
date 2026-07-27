import API from "./api";

// Register
export const register = async (userData) => {
  const response = await API.post("/auth/register", userData);
  return response.data;
};

// Login
export const login = async (credentials) => {
  const response = await API.post("/auth/login", credentials);

  // Save JWT
  localStorage.setItem(
    "access_token",
    response.data.access_token
  );

  localStorage.setItem(
    "username",
    response.data.username
  );

  return response.data;
};

// Logout
export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("username");
};

// Check Login
export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};

// Get Token
export const getToken = () => {
  return localStorage.getItem("access_token");
};

// Get Username
export const getUsername = () => {
  return localStorage.getItem("username");
};