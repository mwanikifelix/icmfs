import api from "@/services/api";

export function testBackend() {
  return api.get("/health/");
}
