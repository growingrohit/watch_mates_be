/**
 * Threads list page: list threads, create thread, navigate to detail.
 */
(function () {
  const layout = document.querySelector(".chat-layout");
  if (!layout) return;

  const threadsApi = layout.dataset.threadsApi;
  const loginUrl = layout.dataset.loginUrl;
  const listEl = document.getElementById("threads-list");
  const emptyEl = document.getElementById("threads-empty");
  const newThreadBtn = document.getElementById("new-thread-btn");
  const newThreadPanel = document.getElementById("new-thread-panel");
  const newThreadForm = document.getElementById("new-thread-form");
  const cancelThreadBtn = document.getElementById("cancel-thread-btn");
  const alertBox = document.getElementById("alert-box");

  function showAlert(message, type) {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.classList.remove("alert-hidden");
  }

  function threadDetailUrl(threadId) {
    return `/chat/threads/${threadId}/`;
  }

  function renderThreadItem(thread) {
    const item = document.createElement("a");
    item.className = "thread-item";
    item.href = threadDetailUrl(thread.id);

    const avatar = document.createElement("img");
    avatar.className = "thread-item-avatar";
    avatar.alt = "";
    avatar.src = thread.profile_image || ChatAPI.defaultAvatar(thread.name);

    const body = document.createElement("div");
    body.className = "thread-item-body";

    const top = document.createElement("div");
    top.className = "thread-item-top";
    const title = document.createElement("strong");
    title.textContent = thread.name || "Untitled thread";
    const time = document.createElement("span");
    time.className = "thread-item-time";
    time.textContent = ChatAPI.formatDateTime(thread.last_message_time);
    top.append(title, time);

    const preview = document.createElement("p");
    preview.className = "thread-item-preview";
    preview.textContent = thread.last_message_preview || "No messages yet";

    body.append(top, preview);
    item.append(avatar, body);
    return item;
  }

  async function loadThreads() {
    const { ok, status, body } = await ChatAPI.listThreads(threadsApi);

    if (status === 401) {
      AuthAPI.clearTokens();
      window.location.href = loginUrl;
      return;
    }

    if (!ok) {
      showAlert(body.message || "Failed to load threads.", "error");
      return;
    }

    const threads = body.data || [];
    listEl.innerHTML = "";

    if (!threads.length) {
      emptyEl.classList.remove("hidden");
      return;
    }

    emptyEl.classList.add("hidden");
    threads.forEach((thread) => listEl.appendChild(renderThreadItem(thread)));
  }

  newThreadBtn.addEventListener("click", () => {
    newThreadPanel.classList.remove("hidden");
  });

  cancelThreadBtn.addEventListener("click", () => {
    newThreadPanel.classList.add("hidden");
    newThreadForm.reset();
  });

  newThreadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      name: newThreadForm.name.value.trim(),
      kind: newThreadForm.kind.value,
    };
    const image = newThreadForm.profile_image.value.trim();
    if (image) payload.profile_image = image;

    const submitBtn = newThreadForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;

    const { ok, body } = await ChatAPI.createThread(threadsApi, payload);
    submitBtn.disabled = false;

    if (!ok) {
      const errors = Object.entries(body)
        .filter(([key]) => key !== "message")
        .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(", ") : val}`)
        .join(" · ");
      showAlert(errors || body.message || "Could not create thread.", "error");
      return;
    }

    newThreadPanel.classList.add("hidden");
    newThreadForm.reset();
    window.location.href = threadDetailUrl(body.data.id);
  });

  loadThreads();
})();
