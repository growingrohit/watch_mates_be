/**
 * Auth page: tab switching, login & register forms via AuthAPI.
 */
(function () {
  const card = document.querySelector(".auth-card");
  if (!card) return;

  const loginApiUrl = card.dataset.loginApi;
  const registerApiUrl = card.dataset.registerApi;
  const alertBox = document.getElementById("alert-box");

  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const tabs = document.querySelectorAll(".auth-tab");
  const panels = document.querySelectorAll(".auth-panel");
  const switchLinks = document.querySelectorAll("[data-switch-tab]");

  function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.classList.remove("alert-hidden");
  }

  function hideAlert() {
    alertBox.classList.add("alert-hidden");
  }

  function setActiveTab(tabName) {
    tabs.forEach((tab) => {
      const isActive = tab.dataset.tab === tabName;
      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-selected", isActive ? "true" : "false");
    });
    panels.forEach((panel) => {
      panel.classList.toggle("is-visible", panel.dataset.panel === tabName);
    });
    hideAlert();
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => setActiveTab(tab.dataset.tab));
  });

  switchLinks.forEach((link) => {
    link.addEventListener("click", () => setActiveTab(link.dataset.switchTab));
  });

  function formToObject(form) {
    const data = {};
    new FormData(form).forEach((value, key) => {
      if (String(value).trim() !== "") {
        data[key] = value;
      }
    });
    return data;
  }

  function setSubmitting(form, loading) {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = loading;
      btn.dataset.originalText = btn.dataset.originalText || btn.textContent;
      btn.textContent = loading ? "Please wait…" : btn.dataset.originalText;
    }
  }

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideAlert();
    setSubmitting(loginForm, true);

    const username = loginForm.username.value.trim();
    const password = loginForm.password.value;

    const { ok, status, body } = await AuthAPI.login(loginApiUrl, username, password);

    setSubmitting(loginForm, false);

    if (ok) {
      AuthAPI.storeTokens(body.tokens);
      showAlert(`${body.message} Redirecting…`, "success");
      setTimeout(() => {
        window.location.href = "/";
      }, 800);
      return;
    }

    showAlert(body.message || "Login failed.", status === 404 ? "info" : "error");
  });

  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideAlert();
    setSubmitting(registerForm, true);

    const payload = formToObject(registerForm);
    const { ok, body } = await AuthAPI.register(registerApiUrl, payload);

    setSubmitting(registerForm, false);

    if (ok) {
      AuthAPI.storeTokens(body.tokens);
      showAlert(`${body.message} You can sign in now.`, "success");
      setActiveTab("login");
      loginForm.username.value = payload.username;
      return;
    }

    const errors = Object.entries(body)
      .filter(([key]) => key !== "message")
      .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(", ") : val}`)
      .join(" · ");
    showAlert(errors || body.message || "Registration failed.", "error");
  });
})();
