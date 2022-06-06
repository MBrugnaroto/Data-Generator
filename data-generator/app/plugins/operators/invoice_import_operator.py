import os
from os.path import join
from datetime import datetime
from ..hooks.mariadb_hook import MariaDBHook


class   InvoiceImportGenerator():
    def __init__(self,
                 id,
                 path_dump,
                 host=None, 
                 port=None, 
                 user=None, 
                 password=None) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.path_dump = path_dump
        self.database = "DB_TEST"
        self.host = host or "127.0.0.1"
        self.port = port or 3306
        self.user = user or os.environ.get("USER") or 'root'
        self.pw = password or os.environ.get('PASSWORD') or '' 
        self.id = id

    def call_dump(self, hook, table, dl_table):
        hook.bulk_load(join(
                            self.path_dump,
                            f"{dl_table}",
                            f"generate_date={self.date}.csv"),
                            table)


    def executor(self):
        hook = MariaDBHook(
                    database=self.database,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.pw
        )
        dump_start = datetime.now()
        self.call_dump(hook, "notas_fiscais", "invoices")
        self.call_dump(hook, "itens_notas_fiscais", "items")
        dump_end = datetime.now()
        total = (dump_end-dump_start).total_seconds()
        
        hook.insert_data("round_statistics", 
                    ["id", "function_total_time", "operator"], 
                    [self.id, total, "import"])
        