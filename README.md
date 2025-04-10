<<<<<<< HEAD
# Gemini AI 聊天機器人

這是一個使用 Python 開發的 AI 聊天機器人，採用 Google 的 Gemini AI 模型。提供網頁介面和命令列介面兩種方式與 AI 進行互動。

## 功能特點

- 現代化響應式網頁介面
- 命令列介面用於測試和快速互動
- 使用 Google 的 Gemini AI 模型
- 可部署至 Vercel 平台

## 安裝步驟

1. 安裝必要的套件：
```bash
pip install -r requirements.txt
```

2. 應用程式已設定使用 vercel.json 檔案中指定的 Gemini API 金鑰和模型。

## 使用方式

### 網頁介面

執行網頁介面：
```bash
python api/app.py
```
然後在瀏覽器中開啟 `http://localhost:5000`

### 命令列介面

使用命令列介面：
```bash
python api/app.py --cli
```

## 部署說明

應用程式已設定可部署至 Vercel 平台。相關設定可在 `vercel.json` 檔案中找到。

## 環境變數

應用程式使用以下環境變數：
- GEMINI_API_KEY：您的 Google Gemini API 金鑰
- GEMINI_MODEL：使用的 Gemini 模型（預設：gemini-1.5-flash）

這些設定已配置在 vercel.json 檔案中，方便部署時使用。 
=======
# test
>>>>>>> 8c7205c4177b5acc0a70fb86f0374805e47c298b
