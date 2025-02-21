import sys

from pydantic import ConfigDict
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional, Text, List, Dict, Tuple, Any
from pathlib import Path
from os.path import join
import pymssql
from contextlib import contextmanager

class EnvModel(BaseSettings):
    mssql_host: Optional[str]
    mssql_port: Optional[str]
    mssql_user: Optional[str]
    mssql_password: Optional[str]
    mssql_database: Optional[str]

    mysql_host: Optional[str]
    mysql_port: Optional[str]
    mysql_user: Optional[str]
    mysql_password: Optional[str]
    mysql_database: Optional[str]
    model_config = SettingsConfigDict(
        env_file = str(join(Path(__file__).parent,'.env')),
        env_file_encoding = 'utf-8',
        case_sensitive = False,
    )

class DataRedirect:
    def __init__(self):
        self.settings = EnvModel()
        self.mssql_conn = None
        self.mysql_conn = None

    @contextmanager
    def connect_mssql(self):

        try:
            self.mssql_conn = pymssql.connect(
                host=self.settings.mssql_host,
                port=self.settings.mssql_port,
                user=self.settings.mssql_user,
                password=self.settings.mssql_password,
                database=self.settings.mssql_database,
            )
            with self.mssql_conn.cursor() as cursor:
                yield cursor
        except Exception as e:
            print("SQL Server模块存在异常!"+"----------"*5+">")
            raise e
        finally:
            if self.mssql_conn:
                self.mssql_conn.close()
                self.mssql_conn = None


    def get_user_from_mssql(self)->List[Tuple[Any, ...]] | None:
        with self.connect_mssql() as cursor:
            cursor.execute(Text('select id,user,keyid from sys_user'))
            return cursor.fetchall()
            # return None

    def set_user_to_mysql(self)->bool:
        data = self.get_user_from_mssql()
        if data is None:
            return False
        else:
            """
            暂无的导入逻辑
            """
            return True

    def run(self):
        data = self.set_user_to_mysql()
        if data:
            print("数据导入Mysql成功!")
            sys.exit(0)
        else:
            print("SQL Server数据库,获取数据为空!")
            sys.exit(-1)



if __name__ == '__main__':
    data_redirect = DataRedirect()
    data_redirect.run()