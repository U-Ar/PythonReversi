PYTHONREVERSI -----------------------------------------------------

play.pyの実行によりGUI起動、コンピュータとリバーシ対戦が可能
盤面の表現として、ゲーム木探索にはビットボード、
棋譜の保存用に二次元配列を利用する

アルファベータ法により指定した深さまでゲーム木を探索する
ビットボード版の評価関数は現在貧弱

盤面の保存再生機能、待った機能付き


LOG-----------------------------------------------------------------
色、読みの深さを指定可能にした
オセロの通常プレイが可能になった
gameboard.previous_stepのstringvarに直前の手を表示
結果表示を実装
感想戦モードの実装
諸ウィンドウを新たに生成するバージョンをtest.pyとして開発終了、
盤面右スペースのフレームをUIとして利用するバージョンを正式版play.pyとして
開発開始
棋譜の保存、再生機能の実装 ファイル形式.kif(後述)
--------------------------------------------------------------------


現在抱える問題
・評価関数のオプション変更機能が未実装、Board.value_func()
を差し替えるのが適切か?
・ビット演算による高速かつ強力な評価関数の未実装


追加実装(希望的観測)機能
オプション（メニュー）から
プレイヤーサイドの描画方法を選択可能にする
(何も表示しない、設置可能位置のハイライト、評価値の表示)


実装中に得た反省
・オブジェクト指向で作る意味が分かった
盤面に紐づけられた変数など、GUIウィジェットそのものに紐づけて
保存したいときにはウィジェットの機能を継承したうえで
変数スロットを確保できるのが便利だった
これにより他の関数からでも変数を参照できるようになった


################board.py##########################################


class-----Board(b)---------------
内部でボードを管理、置かれた石の履歴を管理

メソッドreverse,checkなどで構成され、色の指定など
は外部のゲーム管理に依存する

本クラスが担当するのは判定と石を置いた際の機械的処理と棋譜の保存

class variables--------------------------------
self.board
self.reversed_list
self.reversed_record
self.co_record
self.color_record

methods-----------------------------------------

check(self,color,co)
color 色
co 確認したい座標のタプル(x,y)
ひっくり返せる・・・True
返せない・・・False


reverse(self,color,co)
各方面を返せるか確認したうえで返す
※返せるか確認の部分はあらかじめ確認が入っているため省略可能かもしれないので要検討
返した部分はreversed_listに記録[co1,co2...]
毎ターンごとにreversed_listをreversed_recordに格納
置いた座標はco_recordに格納


undo(self)
reversed_recordとco_recordの直近をとって(破壊的)
返された部分を返しなおす、石を置いた位置をNONEに直す


undo_(self)
待った用メソッド
undoと類似、直前に打った側の色の返り値を持つ


check_gameover(self,color)
どちらも続行不能と判定されたときGAMEOVERを返す
colorの逆側のみ続行可能な時PASSを返す
通常の時NORMALを返す


put_stone(self,color,co)
reverseの処理をよりゲーム内に組み込むために最適化したもの
reverseを行った後、check_gameoverを実行
返り値にcheck_gameoverの値をもつ


count_stone(self)
石数のカウント　返り値 black,white


print_board(self)
デバッグ用コンソール表示関数


value_func(self)
評価関数(仮)
静的な評価
環境が整ったらここを強化していく
新たな関数で置き換える?


functions-----------------------------------------------------

move_first(depth,b,limit)
move_second(depth,b,limit)
先手後手の動作を記述した関数
アルファベータ法によりdepthで指定された深さまで読む


play(first_depth,second_depth)
両者AIで戦わせる関数
主にデバッグ用


negamax(color,depth,b,limit)
move_first/secondの引数に色を追加、評価値を先手後手で反転
させることで一関数での記述を可能に


play_negamax(first_depth,second_depth)
両者negamaxで戦わせる関数
主にデバッグ用

co_to_str(co)
座標に対して棋譜用の文字列を返す関数

##################test.py#######################################
旧GUI

ウィンドウには主に3～4種類を予定
スタート画面
オプション画面


class---------------------------------------------------------

GameOptionButton(tkinter.Button)(master)
ゲーム開始前のオプション画面起動用ボタン
command変数に格納可能なのが関数のポインタのみのためメソッド化

GameOption(tkinter.Frame)(master)
オプション画面
黒/白、ステップ数、評価関数の種類を選択

GameBoardButton(tkinter.Button)(master)
オプション画面に表示する開始ボタン
マスターであるGameoptionから色、ステップ数、評価関数を取得して
boot_gameboardでGameBoardを起動する
gameboard_window(Tk())にGameBoardとコンソールを配置、メニューで
新規ゲーム、タイトル画面、中断、その他オプションを配置

GameBoard(tkinter.Canvas)(master,color,steps,ai)
盤面を描画すると同時に石を置く処理をBoardクラスに渡す
	methods

	put_stone()
	盤面に紐づけるプレイヤー側の関数
	石を置く処理の後にai_puts_stoneに渡す

	ai_puts_stone()

	render_board(color)
	盤面描画関数
	引数colorがプレイヤー側の色self.colorと一致すれば
	オプションに基づきハイライト処理の実行(予定)
	
	undo()
        直前の手をなかったことにして巻き戻すメソッド
	破壊的であり、recordも失われる
	methodsのundoの後に描画しなおしプレイ可能にする

QuitButton(tkinter.Button)(master)
終了ボタン


----------------.kif----------------------------------
棋譜情報保存用テキストファイル形式

#comment                   (#で始まる1行目はコメント)
20XX/XX/XX XX:XX:XX        (対局開始日時)
B black_player
W white_player
XX XX                      (黒、白の石数)
1 B F5                     (手数 手番 座標)
2 W F6
....
60 B G2






