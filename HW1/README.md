	請將程式碼放上Github上，用網路教學的方式來撰寫作業，讓有基礎Python經驗的人可以根據你的教案做出同樣的功能來，
	或是在未來你想用這份作業的程式時，你可以根據這份教案快速上手，小組完成後成員互相fork一份。內容至少要包含下列幾項:

	1.你選擇用甚麼樣的套件來做網路爬蟲?為什麼要用這個套件
	2.請用流程圖的方式告訴我們你是怎麼抓到你的目標資料，流程圖的畫法不拘，主要易懂就好
	3.完整的範例程式
	4.Demo的示範畫面以及解說
	5.至少設想並列出5種當別人使用你的程式最有可能會遇到的錯誤情況，並提供解決辦法

# HW1 

## 1.使用套件及選擇此套件的原因
這次使用的套件包含了request及beautifulsoup, 這兩個都是頗為常見的爬蟲套件。
request:選用request的原因在於,透過https使用restful-api做get, post時, user的query都需要經過header的認證來確保送來的query有
效的, 而request套件即幫忙我們做了這件事。
beautifulsoup:此套件為parse html常見的套件, bs能幫我們取出html中我們想要選取的部分, 直接轉成我們要的資料格式。

## 2.抓取目標資料之流程圖
![image](http://github.com/LeoChang84/FinTech-1/tree/master/HW1/img/flow.png)

## 3.範例程式
```
    res = requests.get('https://www.moneydj.com/etf/x/Basic/ETF/X/xdjbcd/Basic0003BCD.xdjbcd?etfid='+Symbol+'&b='+start_date+'&c='+stop_date)
    doc = bs(res.text, 'lxml')
```

## 4.Demo及示範畫面

//TODO

## 5.注意事項
* 請確認python版本為3.6或以上
* 執行以下指令, 並成功安裝

```
pip3 install -r requirements.txt
```

* 您所執行的branch必須為master
* //TODO
* //TODO

