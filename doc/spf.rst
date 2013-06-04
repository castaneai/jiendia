SPFファイルを開く
===================

SPFファイルを開くにはjiendia.io.spfパッケージにあるSpfArchiveクラスを使います。

.. code-block:: python
	
	from jiendia.io.spf import SpfArchive
	
	with SpfArchive('/latale/path/ROWID.SPF', encoding = 'cp932') as spf:
		spf.get_entry('DATA/LDT/ITEM_1.LDT')
	
SPFの中にあるファイル（エントリ）を扱う
==========================================

SPFファイルの中にあるファイルは「エントリ」という単位で扱います。
エントリは名前・長さを持っています。

.. code-block:: python

	entry = spf.get_entry('DATA/LDT/ITEM_1.LDT')
	print(entry.entry_name) # 'DATA/LDT/ITEM_1.LDT'
	print(len(entry)) # エントリの長さが出力される
	

エントリをバイナリストリームとして開く
========================================

SPFファイルの中にあるファイルをバイナリストリームとして取り出すことができます。
entry.open()を呼び出すとio.Bytesオブジェクトが返ってきます。

.. code-block:: python

	with entry.open() as stream:
		print(stream.read())

