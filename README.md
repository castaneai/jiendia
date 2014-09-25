jiendia 
=========
ラテールのデータ構造を読み取るライブラリ

使用例
=========

ローディング画像をloadings/に保存する
---------------------------

```python
import jiendia
import fnmatch
import os


os.makedirs("./loadings")
spf = jiendia.open("path/to/BANX.SPF")
loading_files = [file for file in spf.contain_files if fnmatch.fnmatch(file.path, "LOADING/*.PNG")]
for file in loading_files:
    open("loadings/" + file.name, "wb").write(file.open().read())
```
