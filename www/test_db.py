# !usr/bin/env python
# _*_ coding:utf-8 _*_

print('\n====== test_db.py start ======\n')

from models import User, Blog, Comment
from transwarp import db

# db.create_engine(user='www-data', password='www-data', database='awesome')
db.create_engine(user='www-data', password='www-data', database='awesome.db')
u = User(name='Test', email='test@example.com', password='1234567890', image='about:blank')
u.insert()
print 'new user id:', u.id

u1 = User.find_first('where email=?', 'test@example.com')
print 'find user\'s name:', u1.name
u1.delete()

u2 = User.find_first('where email=?', 'test@example.com')
print 'find user:', u2

print('\n====== test_db.py end ======\n')
