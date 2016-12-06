# s3_lambda_thumbnail_converter
s3への保存をトリガーにサムネイルを作成するLambdaのやつ

- s3:ObjectCreated イベントをトリガーにしてLambdaを起動
- 出力先は同じバケットの別pathの同ファイル名のもの（ex. /input/test.img → /output/test.img）
- サムネイルのサイズはLambdaのDescriptionに書き出した
  - いい方法なのかは知らない
  - Lambdaでの環境変数ってどう設定すればいいのかわからなかったので試しにやってみただけ