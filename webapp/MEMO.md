# Django自分用メモ
ゆるゆるやっていき

## プロジェクトの作成
よくわからんが `django-admin startproject <projectname>` でできる。
次に `python manage.py migrate` でデータベースを作成。
小規模ならsqliteでよさそうだし、どうせ作っても小規模なのでsqlite以外は無視する方針でいく。

## アプリ追加の概要
Qiitaにあったものをそのままメモしていく。

1. `python manage.py startapp <appname>` でアプリケーションを追加
    -この際に`urls.py`を作成し、`path('', views.index, name='index')`と追記する
2. `<appname>/models.py` にそのアプリで使用するモデルを記述する
    -"modelについて"を参照
3. `<projectname>/settings.py` の `INSTALLED_APPS` に作成したアプリを追加する
4. `python manage.py makemigrations` でデータベースを更新
5. `<appname>/views.py` にモデルの表示や操作(追加、編集など)を記述する。htmlもここで用意。
6. `<appname>/urls.py` を記述し、url,viewsと紐づけ
7. `<projectname>/urls.py` から `<appname>/urls.py` を読み込む

### その他
- 管理者ユーザーの追加
    `python manage.py createsuperuser`で作成
- 日本語化
    `<projectname>/settings.py` の `LANGUAGE_CODE` を `ja` に変更

## modelsについて
このクラスはDBのテーブルを表す。
例えば`models.~Field`はカラムを表現しており、`CharField`には文字列、`IntegerField`には整数が記録される。

- リレーションシップフィールド
これはSQLで言うところの外部キーで、モデル同士の関係を表す。
PollアプリでいうQuestion<->Choiceの関係を作る。
Django2.0からon_deleteを指定するのが必須になった。
外部キーで子になっているフィールドを削除する際に、親も削除するのかを設定する。
よくわからんから`DO_NOTHING`とか入れておくと動く(適当)

## url.py のルーティングについて
まずは `<projectname>/urls.py` 内のurlpatternが呼び出される。
- include関数
    include関数は参照先の`url.py`の内容を呼んでいる。
    `path('polls/', include('polls.urls'))` の参照先で `''` という記述があったら、`polls/` に対する処理になる。
    もちろん `'vote/'` という記述があったら、`polls/vote/` に対する処理になる。