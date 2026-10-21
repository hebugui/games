// 字幕叠加层: 连接本地转写后台 WebSocket, 实时显示原文+译文
(function () {
  if (window.__vtInjected) return;
  window.__vtInjected = true;

  let box = null;
  let ws = null;
  let reconnectTimer = null;
  const WS_URL = 'ws://127.0.0.1:8765';

  function ensureBox() {
    if (box) return box;
    box = document.createElement('div');
    box.id = 'vt-subtitle-box';
    document.body.appendChild(box);
    return box;
  }

  function show(text) {
    const b = ensureBox();
    b.style.display = 'block';
    b.innerHTML = '';
    if (text.src) {
      const s = document.createElement('div');
      s.className = 'vt-src';
      s.textContent = text.src;
      b.appendChild(s);
    }
    if (text.dst) {
      const d = document.createElement('div');
      d.className = 'vt-dst';
      d.textContent = text.dst;
      b.appendChild(d);
    }
    // 3 秒无新字幕自动隐藏
    clearTimeout(window.__vtHideTimer);
    window.__vtHideTimer = setTimeout(() => {
      if (b) b.style.display = 'none';
    }, 3000);
  }

  function connect() {
    try {
      ws = new WebSocket(WS_URL);
    } catch (e) {
      scheduleReconnect();
      return;
    }
    ws.onopen = () => {
      show({ src: '字幕服务已连接', dst: '等待语音...' });
    };
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        show(data);
      } catch (e) {}
    };
    ws.onclose = scheduleReconnect;
    ws.onerror = scheduleReconnect;
  }

  function scheduleReconnect() {
    clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(connect, 3000);
  }

  connect();
})();
