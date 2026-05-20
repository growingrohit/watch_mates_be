/**
 * Reusable client for accounts auth APIs.
 * Expects JSON responses: { message, data?, tokens? }
 */
const AuthAPI = (() => {
  const TOKEN_KEYS = {
    access: "watch_mates_access",
    refresh: "watch_mates_refresh",
  };

  async function request(url, payload) {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    let body = {};
    try {
      body = await response.json();
    } catch (_) {
      body = { message: "Invalid server response." };
    }

    return { ok: response.ok, status: response.status, body };
  }

  function storeTokens(tokens) {
    if (!tokens) return;
    if (tokens.access) {
      localStorage.setItem(TOKEN_KEYS.access, tokens.access);
    }
    if (tokens.refresh) {
      localStorage.setItem(TOKEN_KEYS.refresh, tokens.refresh);
    }
  }

  function clearTokens() {
    localStorage.removeItem(TOKEN_KEYS.access);
    localStorage.removeItem(TOKEN_KEYS.refresh);
  }

  function getAccessToken() {
    return localStorage.getItem(TOKEN_KEYS.access);
  }

  return {
    TOKEN_KEYS,
    storeTokens,
    clearTokens,
    getAccessToken,
    async login(url, username, password) {
      return request(url, { username, password });
    },
    async register(url, payload) {
      return request(url, payload);
    },
  };
})();

window.AuthAPI = AuthAPI;
