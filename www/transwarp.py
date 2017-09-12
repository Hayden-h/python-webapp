# !usr/bin/env python
# _*_ coding:utf-8 _*_
import db

class Field(object):
	def __init__(self, name, column_type):
		self.name = name
		self.column_type = column_type

	def __str__(self):
		return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
	def __init__(self, name):
		super(StringField, self).__init__(name, 'varchar(100')

class IntegerField(Field):
	def __init__(self, name, primary_key):
		super(IntegerField, self).__init__(name, 'biginy')
		self.primary_key = primary_key

class ModelMetaclass(type):
	def __new__(cls, name, bases, attrs):
		if name=='Model':
			return type.__new__(cls, name, bases, attrs)

		mappings = dict()
		for k, v in attrs.iteritems():
			if isinstance(v, Field):
				print('Found mapping: %s==>%s' % (k, v))
				mappings[k] = v
				if isinstance(v, IntegerField) and v.primary_key:
					primary_key = v
					print('Found primary key:%s==>%s' % (k, v))

		for k in mappings.iterkeys():
			attrs.pop(k)

		attrs['__table__'] = name
		attrs['__primary_key__'] = primary_key
		attrs['__mappings__'] = mappings
		return type.__new__(cls, name, bases, attrs)


class Model(dict):
	__metaclass__ = ModelMetaclass

	def __init__(self, **kw):
		super(Model, self).__init__(**kv)

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
			fields.append[v.name]
			params.append('?')
			args.append(getattr(self, k, None))

		sql = 'insert into %s (%s) values(%s)' % (self.__table__, ','.join(fields), ','.join(params))
		print('SQL: %s' % sql)
		print('ARGS: %s' % str(args))

	def insert(self):
		params = {}
    	for k, v in self.__mappings__.iteritems():
    		params[v.name] = getattr(self, k)
    	db.insert(self.__table__, **params)
    	# return self

	@classmethod
	def get(cls, pk):
		d = db.select_one('select * from %s where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
		return cls(**d) if d else None

    


# 通过类方法实现主键查找
# user = User.get('123')





