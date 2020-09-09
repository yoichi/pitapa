# PiTaPa倶楽部から明細をダウンロードする

## 使い方

```
python3 download_meisai.py yyyymm
````

## エラー

### ログイン失敗

```
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"ご利用代金・明細照会"}
```

### yyyymm がない場合

```
selenium.common.exceptions.NoSuchElementException: Message: Cannot locate option with value: yyyymm
```

## 動作環境

* Python version 3.6 or later
* Docker
