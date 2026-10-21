# 家庭物品位置备忘 Android App

一个轻量级原生 WebView 壳，把 `family-memory.html` 打包进 App，支持物品位置录入/查找，数据用 localStorage 本地持久化。

## 技术方案

- 纯原生 Android（Java + WebView），无 Cordova/Capacitor 等重依赖
- 用 AndroidX `WebViewAssetLoader` 以 `https://appassets.androidplatform.net` 域加载 assets 里的 HTML
  - 关键：走 https 域才能让 WebView 的 `localStorage`（DOM Storage）正常持久化，数据不会丢
- `minSdk 21`（Android 5.0+），APK 体积约几十 KB~1MB

## 目录结构

```
family-memory-app/
├── settings.gradle
├── build.gradle
├── gradle.properties
├── gradle/wrapper/gradle-wrapper.properties
└── app/
    ├── build.gradle
    ├── proguard-rules.pro
    └── src/main/
        ├── AndroidManifest.xml
        ├── assets/index.html          ← 网页本体（从 family-memory.html 复制）
        ├── java/com/familymemory/app/MainActivity.java
        └── res/
            ├── layout/activity_main.xml
            ├── values/{strings,styles,colors}.xml
            ├── drawable/ic_launcher_foreground.xml
            └── mipmap-hdpi/ic_launcher.xml
```

## 编译步骤（需要 Android Studio）

1. 安装 Android Studio（自带 Android SDK + Gradle）
2. 用 Android Studio 打开 `family-memory-app` 目录
3. 等 Gradle 同步完成（首次会下载 AGP 8.2.2、Gradle 8.4 及依赖，需联网）
4. 菜单 **Build → Generate Signed Bundle / APK → APK**（或用 Debug 直接连手机 Run）
5. 生成的 APK 在 `app/build/outputs/apk/` 下，安装到手机即可

> 首次同步若提示缺少 `gradle-wrapper.jar`：在 Android Studio 里 File → Sync Project，AS 会自动补全 wrapper；或命令行在项目根目录运行 `gradle wrapper`。

## 修改网页内容

直接改 `app/src/main/assets/index.html`，重新编译即可。网页源码在上级目录 `family-memory.html`，改完记得复制覆盖到 assets。

## 已知说明

- 数据存在 App 的 WebView localStorage 里，卸载 App 会清空数据
- 如需备份/迁移，可在网页里加「导出/导入 JSON」功能（网页本身已支持，见源码）
