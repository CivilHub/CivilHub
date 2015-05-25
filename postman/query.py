from __future__ import unicode_literals
from types import MethodType

from django import VERSION
from django.db.models.sql.query import Query
from django.utils import six


class Proxy(object):
    """
    Code base for an instance proxy.
    """

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        target = self._target
        f = getattr(target, name)
        if isinstance(f, MethodType):
            if six.PY3:
                return MethodType(f.__func__, self)
            else:
                return MethodType(f.__func__, self, target.__class__)
        else:
            return f

    def __setattr__(self, name, value):
        if name != '_target':
            setattr(self._target, name, value)
        else:
            object.__setattr__(self, name, value)

    # added for Django 1.7, object has to be callable
    # see db/models/sql/compiler.py/quote_name_unless_alias()
    def __call__(self, name):
        return self._target(name)


class CompilerProxy(Proxy):
    """
    A proxy to a compiler.
    """

    # @Override
    def as_sql(self, *args, **kwargs):
        sql, params = self._target.as_sql(*args, **kwargs)
        if not sql:  # is the case with a Paginator on an empty folder
            return sql, params
        # mimics compiler.py/SQLCompiler/get_from_clause() and as_sql()
        qn = self.quote_name_unless_alias
        qn2 = self.connection.ops.quote_name
        alias = self.query.tables[0]
        if VERSION >= (1, 8):
            from_clause = self.query.alias_map[alias]
            alias = from_clause.table_alias
            clause_sql, _ = self.compile(from_clause)  # clause_sql, clause_params
            clause = ' '.join(['FROM', clause_sql])
            from django.db.models.sql.constants import INNER as inner_join
        else:
            # Django 1.4, 1.5: name, alias, join_type, lhs, lhs_col, col, nullable
            # Django 1.6, 1.7: name, alias, join_type, lhs, join_cols, _, join_field
            name, alias, _, _, _, _, _ = self.query.alias_map[alias]
            alias_str = '' if alias == name else ' {0}'.format(alias)
            clause = 'FROM {0}{1}'.format(qn(name), alias_str)
            inner_join = self.query.INNER
        index = sql.index(clause) + len(clause)
        extra_table, extra_params = self.union(self.query.pm_get_extra())
        new_sql = [
            sql[:index],
            ' {0} ({1}) {2} ON ({3}.{4} = {2}.{5})'.format(
                inner_join, extra_table, self.query.pm_alias_prefix, qn(alias), qn2('id'), qn2('id')),
        ]
        if index < len(sql):
            new_sql.append(sql[index:])
        new_sql = ''.join(new_sql)
        return new_sql, extra_params + params

    def union(self, querysets):
        """
        Join several querysets by a UNION clause. Returns the SQL string and the list of parameters.
        """
        result_sql, result_params = [], []
        for qs in querysets:
            sql, params = qs.query.sql_with_params()
            result_sql.append(sql)
            result_params.extend(params)
        return ' UNION '.join(result_sql), tuple(result_params)


class PostmanQuery(Query):
    """
    A custom SQL query.
    """
    pm_alias_prefix = 'PM'

    # @Override
    def __init__(self, *args, **kwargs):
        super(PostmanQuery, self).__init__(*args, **kwargs)
        self._pm_table = None

    # @Override
    def clone(self, *args, **kwargs):
        obj = super(PostmanQuery, self).clone(*args, **kwargs)
        obj._pm_table = self._pm_table
        return obj

    # @Override
    def get_compiler(self, *args, **kwargs):
        compiler = super(PostmanQuery, self).get_compiler(*args, **kwargs)
        return CompilerProxy(compiler)

    def pm_set_extra(self, table):
        self._pm_table = table

    def pm_get_extra(self):
        return self._pm_table
