import os
import psycopg2
import logging

class IntegrationService():
  def __init__(self) -> None:
    self.db_host = os.environ['DB_HOST']
    self.db_port = os.environ['DB_PORT']
    self.db_user = os.environ['DB_USER']
    self.db_password = os.environ['DB_PASSWORD']
    self.db_name = os.environ['DB_NAME']


  async def __get_dsn_without_password(self) -> str:
    return f'dbname={self.db_name} user={self.db_user} host={self.db_host} port={self.db_port}'
  

  async def __get_full_dsn(self) -> str:
    return f'dbname={self.db_name} user={self.db_user} password={self.db_password} host={self.db_host} port={self.db_port}'
  

  async def get_last_request_id(self) -> int:
    stmt = 'SELECT MAX(requestid) FROM integration1cimporthistory'

    dsn = await self.__get_full_dsn()
    dsn_without_password = await self.__get_dsn_without_password()

    connection = psycopg2.connect(dsn)
    logging.debug(f'{__name__}.get_last_request_id - connected to [{dsn_without_password}]')

    cursor = connection.cursor()

    cursor.execute(stmt)

    result = cursor.fetchone()

    if result is None:
      logging.error(f'{__name__}.get_last_request_id - request `{stmt}` returned `None`, used `1` like last request id')
      return 1
    
    cursor.close()
    connection.close()
    logging.debug(f'{__name__}.get_last_request_id - disconnected from [{dsn_without_password}]')

    last_request_id = int(result[0])
    logging.info(f'{__name__}.get_last_request_id - last request id [{last_request_id}]')

    return last_request_id
  

  async def save_json_data(self, next_request_id: int, host: str, org_code: str, data: str) -> bool:
    stmt = f"INSERT INTO integration1cimporthistory (requestdatetime, fromhost, ourorgcode, content, isprocessed) VALUES (NOW(), '{host}', '{org_code}', '{data}', false)"

    dsn = await self.__get_full_dsn()
    dsn_without_password = await self.__get_dsn_without_password()

    connection = psycopg2.connect(dsn)
    logging.debug(f'{__name__}.save_json_data - connected to [{dsn_without_password}]')

    cursor = connection.cursor()

    cursor.execute(stmt)

    affected_count = cursor.rowcount

    # Если INSERT не сработал или вставил больше 1 строки, откатываем и закрываем соединение
    if affected_count != 1:
      logging.error(f'{__name__}.save_json_data - request `{stmt}` must affected 1 row, but affected {affected_count}, rollback...')
      connection.rollback()

      cursor.close()
      connection.close()
      logging.debug(f'{__name__}.get_last_request_id - disconnected from [{dsn_without_password}]')
      
      return False
    
    # Если 1 строка успешно добавилась, то проводим коммит и завершаем работу
    connection.commit()
    logging.error(f'{__name__}.save_json_data - affected {affected_count}, changes commited')

    cursor.close()
    connection.close()
    logging.debug(f'{__name__}.get_last_request_id - disconnected from [{dsn_without_password}]')

    return True
