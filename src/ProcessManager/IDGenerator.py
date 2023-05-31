# -*- coding:utf-8 -*-
# @FileName : IDGenerator.py
# @Time     : 2023/3/18 17:26
# @Author   : qingyao

class IDGenerator:
    __id_generator = 0

    def create_id(self):
        self.__id_generator = self.__id_generator + 1
        return self.__id_generator
    def get_create_id(self):
        return self.__id_generator

if __name__ == "__main__":
    run_code = 0
    print(IDGenerator.create_id(IDGenerator))


