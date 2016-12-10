# s3_lambda_thumbnail_converter
s3への保存をトリガーにサムネイルを作成するLambdaのやつ

- s3:ObjectCreated イベントをトリガーにしてLambdaを起動
- <s>出力先は同じバケットの別pathの同ファイル名のもの（ex. /input/test.img → /output/test.img）</s>
- 色々な事情から同じファイルに書き出すようにした
- <s>サムネイルのサイズはLambdaのDescriptionに書き出した</s>
  - <s>いい方法なのかは知らない</s>
  - <s>Lambdaでの環境変数ってどう設定すればいいのかわからなかったので試しにやってみただけ</s>
  - 環境変数が実装されてました

- Lambdaの環境変数に{ STYLES: 'tiny=200;small=300;medium=400;large=600;huge=800;' }のようにサムネイルのサイズを指定する（数字は変換後の画像の幅のピクセル数）
  - get_sizes()を変更すればいいと思うよ
  - Lambdaの環境変数にはカンマが使えないらしくjsonを入れることは出来ませんでした。。。
- [TODO]オリジナルのファイル名に2バイト文字が入るとおかしくなるのを直す
  - URLエンコードされてたのでデコードしてもうまくいかった

- Lambdaのsuffixの指定を忘れないように