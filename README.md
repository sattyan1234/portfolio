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

## ディレクトリ構成
```
portfolio/
├── server/
│   ├── app.py            #メインサーバー(Flask)  
│   ├── logic/            #ゲームの関数などロジック部分
│   │   ├── othello/
│   │   │   └── logic_othello.py
│   │   ├── shogi/
│   │   │   └── logic_shogi.py
│   │   └── gungi/
│   │       └── logic_gungi.py
│   ├── html/            #html
│   │   ├── start_index.html        
│   │   ├── othello.html
│   │   ├── shogi.html
│   │   └── gungi.html
│   └── static/
│       ├── css/            #css
│       │    ├── start_style.css
│       │    ├── othellostyle.css
│       │    ├── shogistyle.js
│       │    └── gungistyle.js
│       └── js/            #JS
│            ├── start_main.js
│            ├── othellomain.js
│            ├── othello_image/
│            ├── shogimain.js
│            ├── shogi_image/
│            ├── gungimain.js
│            └── gungi_image/
│
├── games/           #ローカルで遊べるゲームのフォルダ
|
└── README.md
```
---

## URL（デモ環境）
[http://<EC2のパブリックIP>:8000](http://<EC2のパブリックIP>:8000)
（※AWS EC2で稼働）

---

## 遊び方
1. 上記URLにアクセス
2. 「オセロ」「将棋」「軍議」から遊びたいゲームを選択
3. 1人プレイ or 対人戦を選択して開始

---

## 実装ポイント
-
-

---

## 開発方針
- 開発モデルはウォーターフォールを参考にしつつ、実装段階で小さなアジャイルサイクルを回しました。
- 実装難易度を段階的に上げることで、UI・通信・ゲームロジックの拡張に対応できるよう設計しました。
    - **1.オセロ**：最もシンプルなロジックで、基本の通信処理とUI連携を実装
    - **2.将棋**：駒の種類・ルールが複雑なため、データ構造とサーバー設計を拡張
    - **3.軍議**：高さの概念を追加。戦略性が高く、カスタムルール対応のため、設計をより汎用化
    - **4.公開**：Pygameによるローカル実装をFlask＋Socket.IOに移行。AWS上にデプロイしてオンライン版として公開可能な形に。

## 役割分担
sattyan1234 - 開発リーダー ・ サーバー管理 ・ ロジック(ローカル)担当
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

## ゲーム概要
  - **オセロ**：
  - **将棋**：
  - **軍議**：
    
---

## 今後の改善点
- ユーザー認証機能の追加
- スマホUIの最適化
- ゲーム履歴の保存機能

python app.py
ブラウザで http://localhost:8000 にアクセス

---
