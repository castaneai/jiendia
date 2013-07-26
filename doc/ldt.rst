LDTファイルを開く
===================

jiendia.io.archive.ldtにあるLdtArchiveクラスを使うとLDTファイルを開くことができます。
LDTファイルは行と列を持つデータベースファイルとなっています。
LdtArchiveクラスのcolumnsは列情報を、rowsは行を取り出すことができます。

.. code-block:: python
	
	from jiendia.io.archive.ldt import LdtArchive
	
	with LdtArchive('/path/to/ITEM_1.LDT', encoding = 'cp932') as ldt:
	    # 1行目のデータを取り出す
		first_row = ldt.rows[0]
	

SPFファイルの中にあるLDTファイルを開く
==========================================

LDTファイルは通常SPFファイルの中に格納されています。
SPFファイルの中にあるLDTファイルをLdtArchiveとして開くこともできます。

.. code-block:: python

	from jiendia.io.archive.spf import SpfArchive
	from jiendia.io.archive.ldt import LdtArchive
	
	with SpfArchive('/path/to/ROWID.SPF', encoding = 'cp932') as spf:
	    ldt_file = spf.open_entry('/DATA/LDT/ITEM_1.LDT')
	    with LdtArchive(ldt_file, encoding = 'cp932') as ldt:
	        first_row = ldt.rows[0]
