jiendia 
=========

Data parser for LaTale Online.

Dependencies
=============

- pybinary (jiendia.io)
- sqlalchemy (jiendia.sql)

Examples
=========

Reading archive files(SPF, LDT, TBL, MFT, SEQ, ...)
----------------------------------------------------

```python
# read .SPF archive
from jiendia.io import open_archive

with open_archive('/path/to/ROWID.SPF', encoding = 'utf8') as spf:
	for entry in spf.entries:
		print(spf.entry_name)
```
