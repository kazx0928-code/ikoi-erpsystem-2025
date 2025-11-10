param(
    [string]$Customer = "いこい住宅 お客様",
    [int]$Amount = 550000,
    [string]$Item = "住宅リフォーム一式",
    [string]$Date = (Get-Date -Format "yyyy年MM月dd日"),
    [int]$ReceiptNo = 1001
)

$text = @"
株式会社いこい住宅
〒700-XXXX 岡山市北区○○町1-2-3
TEL: 086-XXX-XXXX　FAX: 086-XXX-XXXX

                              領　収　書

No. $ReceiptNo                              $Date

$Customer 様

下記の通り領収いたしました。

　　品名：$Item
　　金額：¥{0:N0}（税込）


                           金　　壱阡阡阡阡円也

                           株式会社いこい住宅
                           岡山市北区○○町1-2-3
                           代表取締役　岡　太郎
"@ -f $Amount

$text | Out-File -Encoding UTF8 ".\receipt\領収書_No$ReceiptNo.txt"
$text | Set-Clipboard
Write-Host "領収書No.$ReceiptNo 生成完了（クリップボードにもコピー済）"
