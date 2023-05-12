# -*- coding:utf-8 -*-
# @FileName : Container.py
# @Time     : 2023/5/11 11:00
# @Author   : qingyao
import inspect
class Container:
    dependencies = {}

    @classmethod
    def register(cls, key, dependency):
        cls.dependencies[key] = dependency

    @classmethod
    def resolve(cls, key):
        return cls.dependencies[key]

def inject(*dependencies):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            deps = [Container.resolve(dep) for dep in dependencies]
            return fn(*args, *deps, **kwargs)
        return wrapper
    return decorator
if __name__ == "__main__":
    run_code = 0
