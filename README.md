# プロジェクト演習Ⅰ・テーマD

## 第２回
### tkinterで電卓実装
#### 追加機能
- 四則演算
- オールクリアボタン：entryに入力されている数字，数式の文字列全体をdeleteする


## 第３回
### tkinterで迷路実装
#### 3限：基本機能
- 練習問題をやって迷路の基本構造を作成した。
#### 4限：追加機能
- スタート地点とゴール地点の追加：スタート地点とゴール地点を固定して色を塗った。


## 第４回
### pygameでゲームの実装
- ゲーム概要:
    - rensyu04/dodge_bomb.pyを実行すると，1600x900のスクリーンに草原が描画され，こうかとんを移動させ飛び回る爆弾から逃げるゲーム。
    - こうかとんが爆弾と接触するとゲームオーバーで終了する。
- プログラムの説明:
    - dodge_bomb.pyをコマンドラインから実行すると，pygameの初期化，main関数の順に処理が進む。
    - ゲームオーバーによりmain関数から抜けると，pygameの初期化を解除し，プログラムが終了する。
    - main関数では，clockの生成，スクリーンの生成，背景画像の描画，こうかとんの描画，爆弾の描画を行う。
    - main関数の無限ループでは，キー操作に応じたこうかとんの移動，指定速度に応じた爆弾の移動を行う。
    - Rectクラスのcolliderectメソッドにより，こうかとんと爆弾の接触を判定する。
    - check_bound関数では，こうかとんや爆弾の座標がスクリーン外にならないようにチェックする。
- 追加機能:
    一度当たるとこうかとん、爆弾の位置リセットされて新しく始まる。2回当たるとゲームが終了する。
    一度当たるとこうかとんの画像が8に変わる。


## 第５回
### pygameで実装（前回のプログラムを拡張）
- ゲーム概要:
    - こうかとんが5つの爆弾から逃げるゲーム。
    - こうかとんが爆弾と接触するとゲームオーバー。
- プログラムの説明:
    - Screenクラス、Birdクラス、Bombクラスを作成して、main関数を見やすく直した。
- 追加機能:
    - 爆弾が壁に当たると少しだけ速くなる。
    - 爆弾の大きさがランダムで出現するようにした。
    - 一度当たるとこうかとんの画像が8に変わり、新しくゲームが始まる。また、爆弾が10個に増える。
    - 計2回当たるとゲームが終了する。

## 第6回
### ゲーム開発
- ゲーム名:
    - 逃げるな！こうかとん！
- ゲーム概要:
    - サンプルゲームのchimp.pyを改良して逃げるこうかとんを叩くゲームを開発した。
    - 画面上を動いて逃げるこうかとんを捕まえるゲーム。
    - マウスの動きに合わせて腕が動き、クリックしたら腕が振り下ろされる。
    - 腕が当たったらこうかとんがびっくりして回転し、腕が当たらなかったらミスになる。
    - また、腕が当たるとこうかとんの動くスピードがランダムだ変わる。
    - こうかとんに10回腕を振り下ろすか、5回ミスになったらゲームが終了。
- プログラムの説明:
    - load_image、load_sound関数で画像や音声の読み込み。
    - Fistクラスで腕の動きを処理。
    - birdクラスでこうかとんの動きを処理し、腕が当たった時の変化。
    - main関数でゲームができるように処理。