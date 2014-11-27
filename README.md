Query By Example [QBE]
======================

What is it?
-----------

QBE will generate SQL statement dynamically depending on users inputs and show the results

Tech Stack
----------

	Python 2.7
	Framework: Django
	JQuery 1.11.1
	Default database: Sqlite3	

Libraries used
--------------

	- Sqlalchemy [http://www.sqlalchemy.org/]
	- NetworkX   [https://networkx.github.io/] 	
	
	You can use, 
	- pip install -r requirements.txt
	
How to test
-----------

	Go to qbe folder
	run command: python manage.py runserver --nothreading --noreload
	open http://localhost:8000/
	
