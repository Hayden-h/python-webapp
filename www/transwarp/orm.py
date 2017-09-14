# !usr/bin/env python
# _*_ coding:utf-8 _*_

print('\n====== orm.py start ======\n')

import db
import logging
logging.basicConfig(level=logging.INFO)

class Field(object):
	_count = 0

	def __init__(self, **kw):
		self.name = kw.get('name', None)
		self.column_type = kw.get('column_type', None)
		self.default = kw.get('default', None)
		self.primary_key = kw.get('primary_key', False)
		self.nullable = kw.get('nullable', False)
		self.updatable = kw.get('updatable', True)
		self.insertable = kw.get('insertable', True)
		self.ddl = kw.get('ddl', '')
		self._order = Field._count
		Field._count = Field._count + 1

	def __str__(self):
		return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
	def __init__(self, **kw):
		if not 'default' in kw:
			kw['default'] = ''
		if not 'ddl' in kw:
			kw['ddl'] = 'varchar(255)'
		super(StringField, self).__init__(**kw)

class IntegerField(Field):
	def __init__(self, **kw):
		if not 'default' in kw:
			kw['default'] = 0
		if not 'ddl' in kw:
			kw['ddl'] = 'bigint'
		super(IntegerField, self).__init__(**kw)

class FloatField(Field):
	def __init__(self, **kw):
		if not 'default' in kw:
			kw['default'] = 0.0
		if not 'ddl' in kw:
			kw['ddl'] = 'real'
		super(FloatField, self).__init__(**kw)
class TextField(Field):
	def __init(self, **kw):
		if not 'default' in kw:
			kw['default'] = ''
		if not 'ddl' in kw:
			kw['ddl'] = 'text'
		super(TextField, self).__init__(**kw)

class BooleanField(Field):
	def __init__(self, **kw):
		if not 'default' in kw:
			kw['default'] = False
		if not 'ddl' in kw:
			kw['ddl'] = 'bool'
		super(BooleanField, self).__init__(**kw)

class ModelMetaclass(type):
	def __new__(cls, name, bases, attrs):
		if name=='Model':
			return type.__new__(cls, name, bases, attrs)

		mappings = dict()
		primary_key = None
		
		for k, v in attrs.iteritems():
			if isinstance(v, Field):
				print('Found mapping: %s==>%s' % (k, v))

				if not v.name:
					v.name = k

				mappings[k] = v
				if v.primary_key:
					primary_key = k
					print('******Found primary key:%s==>%s' % (k, v))

		for k in mappings.iterkeys():
			attrs.pop(k)

		attrs['__table__'] = name
		attrs['__primary_key__'] = primary_key
		attrs['__mappings__'] = mappings
		return type.__new__(cls, name, bases, attrs)


class Model(dict):
	__metaclass__ = ModelMetaclass

	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	def save(self):
		fields = []
		params = []
		args = []

		for k, v in self.__mappings__.iteritems():
			logging
			fields.append[v.name]
			params.append('?')
			args.append(getattr(self, k, None))

		sql = 'insert into %s (%s) values(%s)' % (self.__table__, ','.join(fields), ','.join(params))
		print('SQL: %s' % sql)
		print('ARGS: %s' % str(args))

	def insert(self):
		params = {}
		for k, v in self.__mappings__.iteritems():
			logging.info('debug-insert:k:%s,v:%s,v.name:%s' % (k, v, v.name))
			if v.insertable:
				if not hasattr(self, k):
					setattr(self, k, v.default)
				params[v.name] = getattr(self, k)

		db.insert(self.__table__, **params)
		return self
    	
	@classmethod
	def get(cls, pk):
		d = db.select_one('select * from %s where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
		return cls(**d) if d else None

    


# 通过类方法实现主键查找
# user = User.get('123')

print('\n====== orm.py end ======\n')





