// popup 逻辑: 保存语言设置
const srcLang = document.getElementById('srcLang');
const dstLang = document.getElementById('dstLang');

chrome.storage.local.get(['srcLang', 'dstLang'], (data) => {
  if (data.srcLang) srcLang.value = data.srcLang;
  if (data.dstLang) dstLang.value = data.dstLang;
});

srcLang.addEventListener('change', () => {
  chrome.storage.local.set({ srcLang: srcLang.value });
});
dstLang.addEventListener('change', () => {
  chrome.storage.local.set({ dstLang: dstLang.value });
});
