# -*- coding: windows-1250 -*-
import uuid

import redis


class UtasitasOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def regisztralas(self, nev, jelszo):
        if self.r.sismember('felhasznalonevek', nev):
            print('Mar van ilyen nev!')
            return
        self.r.hset('felhasznalo_adatok', nev, jelszo)
        self.r.sadd('felhasznalonevek', nev)

    def felhasznalo_lista(self):
        for i in self.r.smembers('felhasznalonevek'):
            print(i)
            print(self.r.hget('felhasznalo_adatok', i))

    def bejelentkezik(self, nev, jelszo):
        if self.r.hget('felhasznalo_adatok', nev) != jelszo:
            print('Rossz jelszo!')
            return

        token = str(uuid.uuid4())

        self.r.sadd(nev + '_tokenek', token)

        return token

    def kijelentkezik(self, nev):
        self.r.delete(nev + '_tokenek')

    def elfelejtett_jelszo(self, nev):
        if not(self.r.sismember('felhasznalonevek',  nev)):
            print('Nincs ilyen felhasznalo!')
            return
        print(self.r.hget('felhasznalo_adatok', nev))


    def ervenyes_token(self, nev, token):
        if self.r.sismember(nev + '_tokenek', token):
            return True
        else:
            return False

    def token_utasitast_ad_ki(self, token, utasitas):
        felhasznalo_nev = ''
        for nev in self.r.smembers('felhasznalonevek'):
            for t in self.r.smembers(nev + '_tokenek'):
                if t == token:
                    felhasznalo_nev = nev
                    break

        self.r.lpush(felhasznalo_nev + '_utasitasai', utasitas)

    def uccso_szaz_utasitas(self, nev):
        print(self.r.lrange(nev + '_utasitasai', 0, -1))