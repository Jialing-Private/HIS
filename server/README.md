首次使用：

1. ```python 
   python manage.py migrate
   ```

2. ```python
   python manage.py makemigrations
   ```

3. ```python
   python manage.py migrate
   ```

更新数据库后（仅作修改（该 操作会导致现有存储的数据错误外）或添加的列允许空或删除列）：

1. ```python
   python manage.py makemigrations
   ```

2. ```python
   python manage.py migrate
   ```