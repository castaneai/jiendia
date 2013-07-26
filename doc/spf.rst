SPFファイルを開く
===================

SPFファイルを開くにはjiendia.io.archive.spfにあるSpfArchiveクラスを使います。
日本版のラテールでは文字エンコーディングにcp932を使うとよいでしょう。

.. code-block:: python
	
	from jiendia.io.archive.spf import SpfArchive
	
	with SpfArchive('/path/to/ROWID.SPF', encoding = 'cp932') as spf:
	    # SPFの中にあるエントリの名前を列挙する
	    for entry in spf.entries:
	        print(entry.name)

SPFの中にあるファイル（エントリ）を扱う
==========================================

SPFファイルの中にあるファイルは「エントリ」という単位で扱います。
エントリの名前はSPFファイル内での相対パス（大抵はDATA/から始まる）で表されています。
get_entry関数を使うと指定した名前のエントリを取り出すことができます。

.. code-block:: python

	from jiendia.io.archive.spf import SpfArchive

	with SpfArchive('/path/to/ROWID.SPF', encoding = 'cp932') as spf:
		entry = spf.get_entry('DATA/LDT/ITEM_1.LDT')
        print(entry.name) # 'DATA/LDT/ITEM_1.LDT'

エントリをファイルとして開く
========================================

エントリをファイルとして開くことができます。
open_entry関数で指定した名前のエントリをファイルとして開くことができます。

.. code-block:: python

    from jiendia.io.archive.spf import SpfArchive

    with SpfArchive('/path/to/ROWID.SPF', encoding = 'cp932') as spf:
        file = spf.open_entry('DATA/LDT/ITEM_1.LDT')
