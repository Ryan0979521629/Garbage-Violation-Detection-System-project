## 此為專題之內容簡介
介紹影片： https://www.youtube.com/watch?v=Ba3QV_6B4h8

題目主旨：台灣的交通問題日益嚴重，其中一個不容忽視的問題是駕駛人亂丟垃圾的行為。這種亂象將增加城市街道和公共場所的垃圾堆積量，不僅破壞的城市景觀，還可能導致騎乘人員的安全隱患，引發交通事故。本計畫旨在解決台灣行車時亂丟垃圾之行為，設計與實作一套『垃圾監測違規辨識系統』，該系統將透過物件辨識以及深度學習技術，準確辨識駕駛的違規亂丟垃圾行為，並記錄該車輛的車牌，以此警示民眾不要因貪求方便而做出違規丟棄垃圾之行為。
---
運用技術：使用DeepSort將不同幀之間的相同物件視為同一物件，並給予編號，透過我們團隊設定的事件處理，當畫面中的物件在短時間內Y軸距離移動超過我們所設定的動態閥值，將會去回朔該物件在每一幀中的位置，並且根據移動的X值速度和方向，回推出是哪位叫使人所丟棄之垃圾，最終呼叫車牌辨識模型，並回傳給使用者。動態閥值的設定是根據垃圾物件出現時，其方框的大小所決定。若越小，則閥值越低。這是因為我們發現，當畫面距離越遠時，垃圾掉落相對於畫面的Y值幅度會較小。然而近距離時，垃圾相對於畫面的Y值幅度會較大。若使用相同的標準將易錯判垃圾為掉落狀態與否，因此我們根據垃圾在畫面中的大小去設定閥值以達到更好的效果。
---
使用模型：共分為Yolov8m、yolov8x、yolov9-C、yolov9-E、PRB-FPN 此五種模型針對我們團隊所自行label的dataset進行訓練，得出來的mean Average Precision(mAP)各為下圖，可以發現yolov9-E的mAP相較於yolov8x和PRB-FPN來說還要低，然而，再我們實際測量時，卻發現yolov9-E反而具備優秀的物件追蹤能力及穩定性，因此最後本系統採用Yolov9-E作為核心模型。
Yolov8m
![1](https://github.com/user-attachments/assets/e2c9d2b3-7073-4e2f-a280-c799be4e86ac)
Yolov8x
![2png](https://github.com/user-attachments/assets/19ade3bc-41d7-405f-955a-8ae5fa533aa2)
Yolov9-c
![3](https://github.com/user-attachments/assets/7d05549a-7a12-427c-a10b-607c95396af2)
Yolov9-E
![4](https://github.com/user-attachments/assets/889e3320-7bb6-4143-9938-4818ab800947)
PRB-FPN
![5](https://github.com/user-attachments/assets/fa943149-cd99-4d89-9b4f-fa1042b8841c)
---

