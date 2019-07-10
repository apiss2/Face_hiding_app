# Face_hiding_app
Twitterに投稿する写真中の顔を検出して、自動で隠すアプリを作成中。

## Dependencies
* Python 3.6
* openCV 4.1

## TODO
- どんな機能を作るか具体的に検討する
- 検出精度が悪いので色々試す

## Face_detection model weight
[Google drive](https://drive.google.com/open?id=1heFHKwlvYBGoa7ynB-h8Fq_gs31pYNQH) にあるcaffe modelを `face_detection_test/models/` 配下に置くと顔認識が可能になる

## instruction
1. `$ git clone ...`する
2. 仮想環境を切り替える
    - `$ cd face-venv/Scripts`
    - `$ activate`を実行
3. アプリを実行する
    - `Face_hiding_app/face_detection_test`に移動
    - `$ py face_detection_dnn.py`で実行
    - 変換する画像を切り替えたい場合はl56,l57のコメントアウトを入れ替える
