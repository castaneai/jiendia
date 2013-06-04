LDTファイルを開く
===================

jiendia.io.ldtパッケージにあるLdtArchiveクラスを使うとLDTファイルを開くことができます。

.. code-block:: python
	
	from jiendia.io.ldt import LdtArchive
	
	with LdtArchive('/path/to/ITEM_1.LDT', encoding = 'cp932') as ldt:
		first_row = ldt.rows[0]
	

SPFファイルの中にあるLDTファイルを開く
==========================================

SpfArchiveオブジェクトのopen_entryメソッドを使うと、SPFの中にあるLDTファイルを直接取り出すことができます。

.. code-block:: python

	from jiendia.io.spf import SpfArchive
	
	with SpfArchive('/latale/path/ROWID.SPF', encoding = 'cp932') as spf:
		ldt = spf.open_entry('DATA/LDT/ITEM_1.LDT')
		
