# -*- coding: windows-1250 -*-
import uuid

import redis


class UtasitasOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def regisztral(self, nev, jelszo):
        if self.r.hexists('felhasznalok', nev):
            print(f'Mar letezik felhasznalo a {nev} nevvel!')
            return
        self.r.hset('felhasznalok', nev, jelszo)

    def bejelentkezik(self, nev, jelszo):
        if self.r.hget('felhasznalok', nev) == jelszo:
            token = uuid.uuid4()
            self.r.sadd(nev+'_aktiv_tokenjei', str(token))
            return token

    def elfelejtett_jelszo(self, felhnev):
        print(self.r.hget('felhasznalok', felhnev))

    def kijelentkezik(self, nev):
        self.r.delete(nev+'_aktiv_tokenjei')

    def felhasznalok_listaja(self):
        return self.r.hkeys('felhasznalok')

    def felhasznalo_bejelentkezve_vane(self, nev):
        if self.r.scard(nev + '_aktiv_tokenjei') > 0:
            print(f'{nev} be van jelentkezve!')
        else:
            print(f'{nev} nincs bejelentkezve!')

    def utasitast_ad_ki(self, token, utasitas):
        nev = ''
        for i in self.felhasznalok_listaja():
            if self.r.sismember(str(i) + '_aktiv_tokenjei', str(token)):
                nev = str(i)
                break
        if nev == '':
            print('Nincs ilyen aktiv token!')
            return

        self.r.lpush(nev + '_utasitasai', utasitas)

    def utolso_utasitas(self, nev, to):
        print(self.r.lrange(nev + '_utasitasai', 0, to-1))







