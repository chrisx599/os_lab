# -*- coding:utf-8 -*-
# @FileName : Container.py
# @Time     : 2023/5/11 11:00
# @Author   : qingyao
class Container:
    """
        容器，存放所有需要控制单一变量的实例化对象，实现单例类，解决调用过程需要大量传递参数而导致的实例化对象问题
        所有类公用的全局对象岑在dependencies内部
    """

    dependencies = {}

    @classmethod
    def register(cls, key, dependency):
        """
        将实例化的对象注册到dependencies中
        :param key: 对象名
        :param dependency:对象实例
        :return: none
        """
        cls.dependencies[key] = dependency

    @classmethod
    def resolve(cls, key):
        """
        :param key:代取出对象注册时名称
        :return:取出对象
        """
        return cls.dependencies[key]

def inject(*dependencies):
    """
    使用方法：@inject("param1","param2","param3"...),函数的注解，用于传递参数，参数名与函数的参数名和注册时名称相同对应
    :param dependencies: 多个参数，
    :return:无
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            deps = [Container.resolve(dep) for dep in dependencies]
            return fn(*args, *deps, **kwargs)
        return wrapper
    return decorator
if __name__ == "__main__":
    run_code = 0
