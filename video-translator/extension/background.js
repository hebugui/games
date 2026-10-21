// 后台服务: 点击图标切换开关状态
chrome.action.onClicked.addListener((tab) => {
  chrome.storage.local.get('enabled', (data) => {
    const next = !data.enabled;
    chrome.storage.local.set({ enabled: next });
  });
});
