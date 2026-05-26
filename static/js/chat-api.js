/**
 * Reusable client for chat REST APIs (JWT authenticated).
 */
const ChatAPI = (() => {
  async function parseJson(response) {
    try {
      return await response.json();
    } catch (_) {
      return { message: "Invalid server response." };
    }
  }

  async function authRequest(url, options = {}) {
    const token = window.AuthAPI?.getAccessToken();
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    const body = await parseJson(response);
    return { ok: response.ok, status: response.status, body };
  }

  return {
    listThreads(threadsUrl) {
      return authRequest(threadsUrl, { method: "GET" });
    },

    getThread(threadUrl) {
      return authRequest(threadUrl, { method: "GET" });
    },

    createThread(threadsUrl, payload) {
      return authRequest(threadsUrl, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    },

    listMessages(messagesUrl, page = 1) {
      const separator = messagesUrl.includes("?") ? "&" : "?";
      return authRequest(`${messagesUrl}${separator}page=${page}`, { method: "GET" });
    },

    createMessage(messagesUrl, payload) {
      return authRequest(messagesUrl, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    },

    formatDateTime(isoString) {
      if (!isoString) return "";
      const date = new Date(isoString);
      const now = new Date();
      const isToday = date.toDateString() === now.toDateString();
      if (isToday) {
        return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      }
      return date.toLocaleString([], {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    defaultAvatar(name) {
      const label = (name || "?").trim().charAt(0).toUpperCase();
      return `data:image/svg+xml,${encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect fill="#2a4a7a" width="64" height="64" rx="32"/><text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" fill="#fff" font-size="28" font-family="sans-serif">${label}</text></svg>`
      )}`;
    },
  };
})();

window.ChatAPI = ChatAPI;
