# -*- coding: windows-1250 -*-
import redis


class LicitOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def uj_kategoria(self, kat_nev):
        if self.r.sismember('kategoriak', kat_nev):
            print('Mar van ilyen kategoria!')
            return
        self.r.sadd('kategoriak', kat_nev)

    def targy_regisztralasa(self, nev, kiallitasi_ar, leiras, letrehozo_neve):
        t_azon = str(self.r.incr('t_azon'))
        self.r.sadd('targy_azonositok', t_azon)
        self.r.hmset('targy_' + t_azon, {
            'nev': nev,
            'kiallitasi_ar': kiallitasi_ar,
            'leiras': leiras,
            'letrehozo_neve': letrehozo_neve
        })
        return t_azon

    def targy_kategoriahoz_rendelese(self, t_azon, kat_nev):
        if not (self.r.sismember('kategoriak', kat_nev)):
            print(f'Nincs {kat_nev} kategoria!')
            return
        if not (self.r.sismember('targy_azonositok', t_azon)):
            print(f'Nincs {t_azon} targy azonosito!')
            return

        self.r.sadd(t_azon + '_kategoriak', kat_nev)

    def targy_kivetele_kategoriabol(self, t_azon, kat_nev):
        if not (self.r.sismember('kategoriak', kat_nev)):
            print(f'Nincs {kat_nev} kategoria!')
            return
        if not (self.r.sismember('targy_azonositok', t_azon)):
            print(f'Nincs {t_azon} targy azonosito!')
            return
        self.r.srem(t_azon + '_kategoriak', kat_nev)

    def uj_felhasznalo(self, nev, email):
        self.r.hset('felhasznalo_adatok', email, nev)

    def felhasznalo_lista(self):
        print(self.r.hgetall('felhasznalo_adatok'))

    def felhasznalo_licital(self, t_azon, email, ar):
        if not (self.r.hexists('felhasznalo_adatok', email)):
            print(f'Nincs {email} email cim!')
            return
        if not (self.r.sismember('targy_azonositok', t_azon)):
            print(f'Nincs {t_azon} targy azonosito!')
            return

        di = dict()
        di[email] = ar
        self.r.zadd(t_azon + '_licitek', di)

    def legnagyobb_licites_felhasznalo(self, t_azon):
        if not (self.r.sismember('targy_azonositok', t_azon)):
            print(f'Nincs {t_azon} targy azonosito!')
            return
        email = str(self.r.zrevrange(t_azon + '_licitek', 0, 0)[0])
        nev = self.r.hget('felhasznalo_adatok', 'gabor@gmail.com')
        print(f'Email: {email}, nev: {nev}')

    # kikialltasi ar szerint
    def targylista_ar_csokkenoen(self):
        azonositok = self.r.smembers('targy_azonositok')
        for azon in azonositok:
            ar = self.r.hget('targy_' + azon, 'kiallitasi_ar')
            di = dict()
            di[azon] = ar
            self.r.zadd('kikialltasi_szerint_temp', di)

        for azon in self.r.zrevrange('kikialltasi_szerint_temp', 0, -1):
            print(self.r.hgetall('targy_' + azon))

        self.r.delete('kikialltasi_szerint_temp')

    def adott_targyra_licitalok_listaja_csokkenoen(self):
        for azon in self.r.smembers('targy_azonositok'):
            if self.r.exists(azon + '_licitek'):
                print(self.r.zrevrange(azon + '_licitek', 0, -1, withscores=True))
            else:
                print(f'A {azon} azonositoju targyra nincsen meg licit!')

    def legnagyobb_licit_osszeg_adott_targyra(self, t_azon):
        if not (self.r.sismember('targy_azonositok', t_azon)):
            print(f'Nincs {t_azon} targy azonosito!')
            return
        max_licites_email = str(self.r.zrevrange(t_azon + '_licitek', 0, 0)[0])
        print(self.r.zscore(t_azon + '_licitek', max_licites_email))

    def targylista_letrehozo_neve_alapjan(self):
        targy_azonositok = self.r.smembers('targy_azonositok')
        ls = []
        for azon in targy_azonositok:
            ls.append(self.r.hgetall('targy_' + azon))
        for i in sorted(ls, key=lambda i: (i['letrehozo_neve'], i['kiallitasi_ar'])):
            print(i)

    def adott_kategoria_targyai(self, kat_nev):
        ls = []
        for azon in self.r.smembers('targy_azonositok'):
            for kat in self.r.smembers(azon + '_kategoriak'):
                if kat_nev == kat:
                    ls.append(azon)
        print(ls)

    def targyak_amik_ket_kategoriaban_is_szerepelnek(self, kat_nev1, kat_nev2):
        ls = []
        for azon in self.r.smembers('targy_azonositok'):
            if self.r.sismember(azon + '_kategoriak', kat_nev1) and self.r.sismember(azon + '_kategoriak', kat_nev2):
                ls.append(azon)

        print(ls)

    def uj_tulajdonosok_listaja(self):
        ...
