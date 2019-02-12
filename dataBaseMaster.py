import sqlite3
import threading


class DataBaseMaster(object):
    def __init__(self) -> None:
        super().__init__()
        self.mutex = threading.Lock()

        self.mutex.acquire()
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
                             last_seen DATETIME DEFAULT NULL,
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP       
                         )
                         '''
                      )
        except sqlite3.OperationalError:
            pass

        conn.commit()
        conn.close()
        self.mutex.release()

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
        self.mutex.acquire()

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
        self.mutex.release()

        return added_proxy_counter



