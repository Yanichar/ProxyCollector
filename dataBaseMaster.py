import sqlite3


class DataBaseMaster(object):
    def __init__(self) -> None:
        super().__init__()
        self.conn = sqlite3.connect('proxy.db')

        # make sure that table is exist
        c = self.conn.cursor()
        try:
            c.execute('''CREATE TABLE proxy_list
                         (
                             id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             ip TEXT NOT NULL,
                             port INTEGER NOT NULL,
                             location TEXT,
                             type TEXT NOT NULL,
                             online INTEGER DEFAULT NULL,
                             last_seen DATETIME DEFAULT NULL,
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP       
                         )
                         '''
                      )
        except sqlite3.OperationalError:
            pass

        self.conn.commit()

    def check_proxy(self, proxy):
        c = self.conn.cursor()
        t = (proxy["ip"], proxy["port"])
        c.execute('SELECT * FROM proxy_list WHERE ip=? AND port=?', t)
        if c.fetchone():
            return True
        else:
            return False

    def add_proxys(self, proxy_list):
        added_proxy_counter = 0
        c = self.conn.cursor()

        for proxy in proxy_list:
            if not self.check_proxy(proxy):
                added_proxy_counter += 1
                t = (proxy["ip"], proxy["port"], proxy["location"], proxy["type"])
                c.execute('INSERT INTO proxy_list ("ip", "port", "location", "type")'
                          ' VALUES (?,?,?,?)', t)

        self.conn.commit()

        return added_proxy_counter



