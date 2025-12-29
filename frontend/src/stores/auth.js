import { defineStore } from "pinia";
import api from "@/api/axios";


export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access"),
    refreshToken: localStorage.getItem("refresh"),
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(credentials) {
      const res = await api.post("/accounts/login/", credentials);

      this.accessToken = res.data.access;
      this.refreshToken = res.data.refresh;

      localStorage.setItem("access", this.accessToken);
      localStorage.setItem("refresh", this.refreshToken);

      // IMPORTANT: do NOT await loadUser here
    },

    async loadUser() {
      const res = await api.get("/accounts/me/");
      this.user = res.data;
    },

    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;

      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
    },
  },
});
