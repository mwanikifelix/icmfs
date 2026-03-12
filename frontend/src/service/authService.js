/* import api from '@/api/api';

export const authService = {

    async login(username, password) {
        // simplejwt expects { username, password } by default
        const response = await api.post('/api/accounts/login/', { username, password });
        const { access, refresh } = response.data;

        // Store tokens — router guard checks localStorage.getItem('token')
        localStorage.setItem('token', access);
        localStorage.setItem('refresh_token', refresh);

        // Fetch logged-in user profile to store role
        const userResponse = await api.get('/api/accounts/me/', {
            headers: { Authorization: `Bearer ${access}` },
        });
        localStorage.setItem('user', JSON.stringify(userResponse.data));
        localStorage.setItem('role', userResponse.data.role || userResponse.data.user_type || '');

        return userResponse.data;
    },

    async refreshToken() {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) throw new Error('No refresh token');

        const response = await api.post('/api/accounts/refresh/', { refresh });
        localStorage.setItem('token', response.data.access);
        return response.data.access;
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('role');
    },

    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    isAuthenticated() {
        return !!localStorage.getItem('token');
    },
}; */



import api from '@/api/api';

const authService = {

  // ── Login ─────────────────────────────────────────────────
  async login(username, password) {
    const response = await api.post('/api/accounts/login/', { username, password });
    const { access, refresh } = response.data;

    localStorage.setItem('token', access);
    localStorage.setItem('refresh_token', refresh);

    // Fetch and store user profile immediately after login
    await authService.fetchMe();

    return response.data;
  },

  // ── Fetch current user from backend ──────────────────────
  async fetchMe() {
    const response = await api.get('/api/accounts/me/');
    const user = response.data;

    localStorage.setItem('user', JSON.stringify(user));

    // Store role separately for the router guard
    const role = user.role || user.user_type || user.groups?.[0] || '';
    localStorage.setItem('role', role);

    return user;
  },

  // ── Get user from localStorage (sync, no API call) ───────
  getUser() {
    try {
      const raw = localStorage.getItem('user');
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  // ── Display name with fallback chain ─────────────────────
  getDisplayName() {
    const user = authService.getUser();
    if (!user) return 'User';
    if (user.full_name)  return user.full_name;
    if (user.first_name) return `${user.first_name} ${user.last_name || ''}`.trim();
    if (user.username)   return user.username;
    return 'User';
  },

  // ── Role ─────────────────────────────────────────────────
  getRole() {
    return (
      localStorage.getItem('role') ||
      authService.getUser()?.role ||
      authService.getUser()?.user_type ||
      ''
    );
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },

  // ── Logout ────────────────────────────────────────────────
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('role');
  },

  // ── Refresh token ─────────────────────────────────────────
  async refresh() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) throw new Error('No refresh token');
    const response = await api.post('/api/accounts/refresh/', { refresh: refreshToken });
    localStorage.setItem('token', response.data.access);
    return response.data.access;
  },
};

export { authService };
export default authService;