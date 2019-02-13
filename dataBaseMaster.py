import sqlite3


class DataBaseMaster(object):
    def __init__(self) -> None:
        super().__init__()

        conn = sqlite3.connect('proxy.db')

        # make sure that table is exist
        c = conn.cursor()
        try:
            c.execute('''CREATE TABLE proxy_list
                         (
                             id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             ip TEXT NOT NULL,
                             port INTEGER NOT NULL,
                             location TEXT,
                             type TEXT NOT NULL,
                             online INTEGER DEFAULT NULL,
                             latency FLOAT,
                             status TEXT DEFAULT NULL,
                             last_seen DATETIME DEFAULT NULL,
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP       
                         )
                         '''
                      )
        except sqlite3.OperationalError:
            pass

        conn.commit()
        conn.close()

    def check_proxy(self, proxy, conn):
        c = conn.cursor()
        t = (proxy["ip"], proxy["port"])
        c.execute('SELECT * FROM proxy_list WHERE ip=? AND port=?', t)
        if c.fetchone():

            result = True
        else:
            result = False

        return result

    def add_proxys(self, proxy_list):

        conn = sqlite3.connect('proxy.db')
        added_proxy_counter = 0
        c = conn.cursor()

        for proxy in proxy_list:
            if not self.check_proxy(proxy, conn):
                added_proxy_counter += 1
                t = (proxy["ip"], proxy["port"], proxy["location"], proxy["type"])
                c.execute('INSERT INTO proxy_list ("ip", "port", "location", "type")'
                          ' VALUES (?,?,?,?)', t)

        conn.commit()
        conn.close()

        return added_proxy_counter

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_proxy_to_check(self):
        conn = sqlite3.connect('proxy.db')
        c = conn.cursor()
        c.row_factory = self._dict_factory

        c.execute('SELECT * FROM proxy_list WHERE status IS NULL ORDER BY timestamp LIMIT 1')
        proxy = c.fetchone()

        t = (proxy["id"], )
        c.execute('UPDATE proxy_list SET status="locked" WHERE id=?', t)

        conn.commit()
        conn.close()
        return proxy

    def update_online_status(self, proxy_id, online, latency):
        conn = sqlite3.connect('proxy.db')
        c = conn.cursor()

        t = (online, latency, proxy_id)
        c.execute('UPDATE proxy_list SET '
                  'online=?,'
                  ' status=null,'
                  ' timestamp=CURRENT_TIMESTAMP,'
                  ' latency=?'
                  ' WHERE id=?', t)

        conn.commit()
        conn.close()
