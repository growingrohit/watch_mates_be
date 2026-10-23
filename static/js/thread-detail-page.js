/**
 * Thread detail page: list messages (paginated), send new text messages.
 */
(function () {
  const layout = document.querySelector(".chat-detail");
  if (!layout) return;

  const threadId = layout.dataset.threadId;
  const threadApi = layout.dataset.threadApi;
  const messagesApi = layout.dataset.messagesApi;
  const loginUrl = layout.dataset.loginUrl;

  const threadTitle = document.getElementById("thread-title");
  const threadMeta = document.getElementById("thread-meta");
  const threadAvatar = document.getElementById("thread-avatar");
  const messagesList = document.getElementById("messages-list");
  const messagesEmpty = document.getElementById("messages-empty");
  const loadMoreBtn = document.getElementById("load-more-btn");
  const messageForm = document.getElementById("message-form");
  const alertBox = document.getElementById("alert-box");

  let currentPage = 1;
  let hasMore = false;
  const allMessages = [];

  function showAlert(message, type) {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.classList.remove("alert-hidden");
  }

  function renderThreadHeader(thread) {
    threadTitle.textContent = thread.name || "Untitled thread";
    threadMeta.textContent = `${thread.kind} · ${thread.members?.length || 0} members`;
    threadAvatar.src = thread.profile_image || ChatAPI.defaultAvatar(thread.name);
    threadAvatar.hidden = false;
  }

  function renderMessage(message) {
    const item = document.createElement("article");
    item.className = "message-item";
    item.dataset.messageId = message.id;

    const meta = document.createElement("header");
    meta.className = "message-meta";
    meta.innerHTML = `<strong>${message.created_by_username}</strong><time>${ChatAPI.formatDateTime(message.created_at)}</time>`;

    const body = document.createElement("div");
    body.className = "message-body";

    if (message.kind === "text") {
      body.textContent = message.content;
    } else if (message.kind === "media") {
      body.innerHTML = `<span class="message-tag">[${message.media_kind}]</span> <a href="${message.media_url}" target="_blank" rel="noopener">${message.media_url}</a>`;
    } else if (message.kind === "link") {
      body.innerHTML = `<span class="message-tag">[${message.platform}]</span> <a href="${message.link}" target="_blank" rel="noopener">${message.link}</a>`;
    } else {
      body.textContent = message.last_message_preview || "Message";
    }

    item.append(meta, body);
    return item;
  }

  function paintMessages() {
    messagesList.innerHTML = "";
    const ordered = [...allMessages].reverse();
    if (!ordered.length) {
      messagesEmpty.classList.remove("hidden");
      return;
    }
    messagesEmpty.classList.add("hidden");
    ordered.forEach((msg) => messagesList.appendChild(renderMessage(msg)));
    messagesList.scrollTop = messagesList.scrollHeight;
  }

  async function loadMessages(page = 1, append = false) {
    const { ok, status, body } = await ChatAPI.listMessages(messagesApi, page);

    if (status === 401) {
      AuthAPI.clearTokens();
      window.location.href = loginUrl;
      return;
    }

    if (!ok) {
      showAlert(body.message || "Failed to load messages.", "error");
      return;
    }

    const results = body.data?.results || [];
    if (append) {
      allMessages.push(...results);
    } else {
      allMessages.length = 0;
      allMessages.push(...results);
    }

    hasMore = Boolean(body.data?.next);
    loadMoreBtn.classList.toggle("hidden", !hasMore);
    paintMessages();
  }

  async function loadThread() {
    const { ok, status, body } = await ChatAPI.getThread(threadApi);

    if (status === 401) {
      AuthAPI.clearTokens();
      window.location.href = loginUrl;
      return;
    }

    if (!ok) {
      showAlert(body.message || "Thread not found.", "error");
      return;
    }

    renderThreadHeader(body.data);
  }

  loadMoreBtn.addEventListener("click", async () => {
    currentPage += 1;
    await loadMessages(currentPage, true);
  });

  messageForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const content = messageForm.content.value.trim();
    if (!content) return;

    const submitBtn = messageForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;

    const { ok, body } = await ChatAPI.createMessage(messagesApi, {
      kind: "text",
      content,
    });

    submitBtn.disabled = false;

    if (!ok) {
      showAlert(body.message || "Could not send message.", "error");
      return;
    }

    messageForm.reset();
    allMessages.unshift(body.data);
    paintMessages();
  });

  loadThread();
  loadMessages(1, false);
})();
