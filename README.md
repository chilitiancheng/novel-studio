# 纸间 · 小说文本加工工作台

支持剧情路线编辑、书信、日记本、打印小票、撕拉票根、乱码文字与音乐播放器，并输出 AO3 HTML/CSS。

正文保存在访问者自己的浏览器中。网站升级不会将正文上传到 GitHub。请定期“保存到本地”备份草稿；无痕浏览、清理浏览器存储或更换设备不会保留本机草稿。

## 发布与更新

仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。首次部署后以 Actions 中 `github-pages` 环境显示的网址为准。

后续修改 `dist/` 文件并推送到 `main`，Actions 会检查代码、发布网站。网址保持不变，访问者刷新网页即可使用新版。新版本需要提交到仓库，聊天中生成的本地文件不会自行上传。

公开发布仅包含 `dist/` 四个应用文件，不包含个人作品、草稿 JSON 或白乌山独立工作台。

## 本地预览

运行 `python3 -m http.server 8000 --directory dist`，浏览器访问 `http://localhost:8000`。

运行 `node --check dist/app.js` 与 `python3 verify.py` 检查发布文件。

## 音乐说明

独立 HTML 网页可跨剧情页持续播放；AO3 代码仅使用原生音频，无法保证隐藏页后的持续播放。媒体需使用允许外部播放的 HTTPS 直链。
