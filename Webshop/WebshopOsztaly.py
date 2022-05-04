# -*- coding: windows-1250 -*-
import redis
import uuid

class WebshopOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def regisztral(self, nev, jelszo, email, valodi_nev, szul_dat):
        if self.r.sismember('felhasznalonevek', nev):
            print('Mar van ilyen felhasznalo!')
            return
        self.r.hmset(nev + '_adatok', {
                        'jelszo': jelszo,
                        'email': email,
                        'valodi_nev': valodi_nev,
                        'szul_dat': szul_dat
        })
        self.r.sadd('felhasznalonevek', nev)

    def felhasznalo_lista(self):
        for i in self.r.smembers('felhasznalonevek'):
            print(self.r.hgetall(i + '_adatok'))

    def elfelejtett_jelszo(self, nev):
        print(self.r.hget(nev + '_adatok', 'jelszo'))

    def bejelentkezik(self, nev, jelszo):
        if not(self.r.sismember('felhasznalonevek', nev)):
            print('Nem letezik ilyen felhasznalonev!')
            return
        if self.r.hget(nev + '_adatok', 'jelszo') != jelszo:
            print('Helytelen jelszo!')
            return

        token = str(uuid.uuid4())
        self.r.sadd(nev + '_tokenek', token)

        return token

    def felhasznalo_torles_email(self, email):
        for nev in self.r.smembers('felhasznalonevek'):
            if self.r.hget(nev + '_adatok', 'email') == email:
                self.r.delete(nev + '_tokenek')
                self.r.delete(nev + '_adatok')
                self.r.srem('felhasznalonevek', nev)
                return
        print('Valami rosszul ment torles kozben!')

    def felhasznalo_torles_nev(self, nev):
        if not(self.r.sismember('felhasznalonevek', nev)):
            print('Nem letezik ilyen felhaszhanlonev!')
            return
        self.r.delete(nev + '_tokenek')
        self.r.delete(nev + '_adatok')
        self.r.srem('felhasznalonevek', nev)

    def ervenyes_token(self, nev, token):
        if self.r.sismember(nev + '_tokenek', token):
            return True
        else:
            return False

    def uj_cikk(self, nev, ar):
        azonosito = str(self.r.incr('cikk_azon'))
        self.r.sadd('cikk_azonositok', azonosito)
        self.r.hmset('cikk_' + azonosito + '_adatok', {
                        'nev': nev,
                        'ar': ar
        })

    def cikk_lista(self):
        for i in self.r.smembers('cikk_azonositok'):
            print(self.r.hgetall('cikk_' + i + '_adatok'))

    def aktiv_e(self, token):
        for nev in self.r.smembers('felhasznalonevek'):
            if self.r.get(nev + '_tokenek') == None:
                return False
        return True

    def kosarba_tesz(self, token, cikk_azon, db):
        if not(self.aktiv_e(token)):
            print('A felhasznalo nem aktiv!')
            return
        if not(self.r.sismember('cikk_azonositok', cikk_azon)):
            print('Nincs ilyen cikk azonosito')
            return
        if db <= 0:
            return
        self.r.hset(token + '_kosara', cikk_azon, db)

    def darabszam_valtoztatas(self, token, cikk_azon, uj_darab):
        self.r.hset(token + '_kosara', cikk_azon, uj_darab)

    def kosar_tartalom_lista(self, token):
        print(self.r.hgetall(token + '_kosara'))




