# -*- coding: windows-1250 -*-
from datetime import datetime

import redis

class SzavazasOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def uj_cikk(self, cim, link, posztolo, posztolasi_datum):
        azon = str(self.r.incr('cikk_azon'))
        self.r.hmset('cikk_' + azon, {
            'cim': cim,
            'link': link,
            'posztolo': posztolo,
            'posztolasi_datum': posztolasi_datum
        })
        self.r.sadd('cikk_azonositok', azon)
        self.r.lpush('cikk_azonositok_datum_szerint', azon)

    def cikk_adatok(self, azon):
        if not(self.r.sismember('cikk_azonositok', azon)):
            print('Nincs ilyen azonositoju cikk!')
            return
        print(self.r.hgetall('cikk_' + azon))

    def cikk_lista(self):
        for azon in self.r.smembers('cikk_azonositok'):
            print(self.r.hgetall('cikk_' + azon))

    def szavazas(self, felhasznalo, cikk_azon):
        if not(self.r.sismember('cikk_azonositok', cikk_azon)):
            print('Nincs ilyen azonositoju cikk!')
            return

        if self.r.sismember(felhasznalo + '_szavazatai', cikk_azon):
            print('Csak egyszer lehet szavazni egy cikkre!')
            return

        # cikk_posztolasi_datum = datetime.strptime(str(self.r.hget('cikk_'+  cikk_azon, 'posztolasi_datum')), '%m/%d/%y %H:%M:%S')
        #
        # if (datetime.now()-cikk_posztolasi_datum).days > 7:
        #     print('Nem lehet 7 napnal kesobbi cikkre szavazni!')
        #     return

        self.r.sadd(felhasznalo + '_szavazatai', cikk_azon)

        self.r.zincrby('szavazatok', 1, cikk_azon)

    def cikk_lista_szavazatszam_alapjan_csokkenoen(self):
        print(self.r.zrevrange('szavazatok', 0, -1, withscores=True))

    def legutoljara_posztolt_cikk(self):
        print(self.r.lrange('cikk_azonositok_datum_szerint', 0, 0))

    def cikk_lista_posztido_alapjan_csokkenoen(self):
        ls = self.r.lrange('cikk_azonositok_datum_szerint', 0, -1)
        for i in reversed(ls):
            print(i)

    def legtobb_szavazatos_cikk(self):
        print(self.r.zrevrange('szavazatok', 0, 0))

    def uj_csoport(self, csoport_nev):
        if self.r.sismember('csoportnevek', csoport_nev):
            print('Mar van ilyen csoport nev!')
            return
        self.r.sadd('csoportnevek', csoport_nev)

    def cikk_csopihoz_rendeles(self, csoport, cikk_azon):
        if not(self.r.sismember('cikk_azonositok', cikk_azon)):
            print('Nem letezik ilyen cikk azonosito!')
            return
        self.r.sadd(csoport + '_cikkek', cikk_azon)

    def csoport_cikk_lista(self, csoport):
        for azon in self.r.smembers(csoport + '_cikkek'):
            print(self.r.hgetall('cikk_' + azon))

    def csoportcikkek_szavazat_alapjan_csokkenoen(self, csoport):
        ls = []
        for azon in self.r.zrevrange('szavazatok', 0, -1, withscores=False):
            if self.r.sismember(csoport + '_cikkek', azon):
                ls.append(azon)
        print(ls)

    def csoportcikkek_datum_alapjan_csokkenoen(self, csoport):
        for azon in reversed(self.r.lrange('cikk_azonositok_datum_szerint', 0, -1)):
            if self.r.sismember(csoport + '_cikkek', azon):
                print(azon)

    def pontszamos_szavazas(self, cikk_azon, szavazat, felhasznalo):
        if not(self.r.sismember('cikk_azonositok', cikk_azon)):
            print('Nem letezik ilyen cikk azonosito!')
            return
        self.r.zincrby('szavazatok', cikk_azon, szavazat)
        self.r.sadd(felhasznalo + '_szavazatai', cikk_azon)


