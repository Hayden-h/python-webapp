# !usr/bin/env python
# _*_ coding:utf-8 _*_

'''
database operation module
'''

print('\n====== db.py start ======\n')

import threading, time, uuid, functools, logging, os

#数据库引擎对象
class _Engine(object):
	def __init__(self, connect):
		self._connect = connect
	def connect(self):
		return self._connect()

def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
	import sqlite3
	global engine

	if engine is not None:
		raise DBError('Engine is already initialized')
	params = dict(user=user, password=password, database=database, host=host, port=port)
	defaults = dict(use_unicode=True, charset='utf-8', collation='utf8_general_ci', autocommit=False)

	for k, v in defaults.iteritems():
		params[k] = kw.pop(k, v)

	params.update(kw)
	params['buffered'] = True
	# engine = _Engine(lambda: sqlite3.connect(**params))
	db_path = os.path.join(os.path.abspath('.'), database)
	engine = _Engine(lambda: sqlite3.connect(db_path))
	print('=== Init sqlite3 engine ok ===')
	print('=== sqlite3 path: %s ===\n' % db_path)

#持有数据库连接的上下文对象：
class _DbCtx(threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0

	def is_init(self):
		return not self.connection is None

	def init(self):
		self.connection = _LasyConnection()
		self.transactions = 0

	def cleanup(self):
		self.connection.cleanup()
		self.connection = None

	def cursor(self):
		return self.connection.cursor()


class _ConnectionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_cleanup = True
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()

	# @with_connection
	# def select(sql, *args):
	# 	pass

	# @with_connection
	# def update(sql, *args):
	# 	pass

	# @with_transaction
	# def do_in_transaction:
	# 	pass

def connection():
	return _ConnectionCtx()

class _TransactionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_close_conn = True
		_db_ctx.transactions = _db_ctx.transactions + 1
		return self
	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		_db_ctx.transactions = _db_ctx.transactions - 1
		try:
			if _db_ctx.transactions == 0:
				if exctype is None:
					self.commit()
				else:
					self.rollback()
		finally:
			if self.should_close_conn:
				_db_ctx.cleanup()

	def commit(self):
		global _db_ctx
		try:
			_db_ctx.connection.commit()
		except:
			_db_ctx.connection.rollback()
			raise

	def rollback(self):
		global _db_ctx
		_db_ctx.connection.rollback()

def transaction():
	return _TransactionCtx()

def with_connection(func):
	@functools.wraps(func)
	def _wrapper(*args, **kw):
		print 'call %s():' % func.__name__
		with connection():
			return func(*args, **kw)
	return _wrapper

def with_transaction(func):
	@functools.wraps(func)
	def _wrapper(*args, **kw):
		_start = time.time()
		with transaction():
			return func(*args, **kw)
		_profiling(_start)
	return _wrapper

@with_connection
def select(sql, *args):
	pass

@with_connection
def update(sql, *args):
	pass


engine = None
_db_ctx = _DbCtx()



def next_id(t=None):
	if t is None:
		t = time.time()
	return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)

# 
# end
#

print('\n====== db.py end ======\n')



