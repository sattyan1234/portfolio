# ポートフォリオ
# オンライン対戦ボードゲーム集

## プロジェクト概要
AWS上で稼働するオンライン対戦型ボードゲーム集です。  
WebブラウザからURLにアクセスするだけで、以下のゲームを遊べます。
- オセロ
- 将棋
- 軍議

特徴:
-
-
-
---

## 使用技術
### サーバーサイド


### フロントエンド


### インフラ


---

## ディレクトリ構成
```
portfolio/
 ├─ games/                # ローカルで動くPygameコード
 │   ├─ othello/
 │   ├─ shogi/
 │   └─ gungi/
 ├─ server/               # サーバー側（Flask＋Socket.IO）
 │   ├─ app.py
 │   ├─ requirements.txt
 │   └─ game_logic/
 ├─ frontend/             # Web UI（HTML/CSS/JS）
 │   ├─ index.html
 │   ├─ style.css
 │   └─ main.js
 └─ docs/                 # ドキュメント・構成図
     ├─ README.md
     └─ diagram.png
```


---

## URL（デモ環境）
[http://<EC2のパブリックIP>:8000](http://<EC2のパブリックIP>:8000)
（※AWS EC2で稼働中）

---

## 遊び方
1. 上記URLにアクセス
2. 「オセロ」「将棋」など、遊びたいゲームを選択
3. 1人プレイ or 対人戦を選択して開始

---

## 実装ポイント
-
-

---

## 役割分担
- 担当
  - 
  - 
  - 
- 担当
  - 
  - 
  - 
- 担当
  - 
  - 
  - 
- 担当
  - 
  - 
  - 

---

## 今後の改善点
- ユーザー認証機能の追加
- スマホUIの最適化
- ゲーム履歴の保存機能

---

## スクリーンショット
![トップ画面](docs/screenshot.png)

---

## 動作方法（ローカル開発）
```bash
# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# 必要ライブラリのインストール
pip install -r requirements.txt

# サーバー起動
cd server
python app.py
ブラウザで http://localhost:8000 にアクセス

---
