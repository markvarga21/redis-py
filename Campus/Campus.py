# -*- coding: windows-1250 -*-
import redis


class CFOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def uj_helyszin(self, helyszin):
        if self.r.sismember('s_helyszinek', helyszin):
            print(f'Mar letezik a {helyszin} helyszin!')
            return
        else:
            self.r.sadd('s_helyszinek', helyszin)

    def helyszin_lista(self):
        print(self.r.smembers('s_helyszinek'))

    def jo_idopont(self, kezdet, veg):
        if self.r.scard('s_esemenyek') > 0:
            for esemeny in self.r.smembers('s_esemenyek'):
                kezdet_int = int(kezdet)
                veg_int = int(veg)

                k = int(self.r.hget(esemeny, 'kezdet'))
                v = int(self.r.hget(esemeny, 'vegezet'))

                if not ((kezdet_int < k and veg_int <= k) or (v <= kezdet_int and v < veg_int)):
                    return False
                else:
                    return True
        else:
            return True

    def uj_esemeny(self, helyszin, kezdet, veg, megnevezes, felelosnev, felelostel):
        if not (self.r.sismember('s_helyszinek', helyszin)):
            print(f'A {helyszin} helyszin nem letezik meg!')
            return
        if not (self.jo_idopont(kezdet, veg)) or kezdet > veg:
            print('Rossz idopont!')
            return

        azonosito = self.r.incrby('azon', 1)

        self.r.hmset('esemeny_' + str(azonosito), {
            'helyszin': helyszin,
            'kezdet': kezdet,
            'vegezet': veg,
            'megnevezes': megnevezes,
            'felelosnev': felelosnev,
            'felelostel': felelostel
        })

        self.r.sadd('s_esemenyek', 'esemeny_' + str(azonosito))

    def idopont_kozotti_esemenyek(self, mettol, meddig):
        for esemeny in self.r.smembers('s_esemenyek'):
            if int(self.r.hget(esemeny, 'kezdet')) >= int(mettol) and int(self.r.hget(esemeny, 'vegezet')) <= int(meddig):
                helyszin = self.r.hget(esemeny, 'helyszin')
                megnevezes = self.r.hget(esemeny, 'megnevezes')
                k = self.r.hget(esemeny, 'kezdet')
                v = self.r.hget(esemeny, 'vegezet')
                felelosnev = self.r.hget(esemeny, 'felelosnev')
                print(f'Helyszin: {helyszin}, megnevezes: {megnevezes}, kezdet: {k}, veg: {v}, felelosnev: {felelosnev}')

    def osszes_esemeny(self):
        for esemeny in self.r.smembers('s_esemenyek'):
            helyszin = self.r.hget(esemeny, 'helyszin')
            megnevezes = self.r.hget(esemeny, 'megnevezes')
            k = self.r.hget(esemeny, 'kezdet')
            v = self.r.hget(esemeny, 'vegezet')
            felelosnev = self.r.hget(esemeny, 'felelosnev')
            print(f'Helyszin: {helyszin}, megnevezes: {megnevezes}, kezdet: {k}, veg: {v}, felelosnev: {felelosnev}')

    def uj_jegytipus(self, nev, ar, erv_kezd, erv_vege):
        jegytipus_azonosito = self.r.incrby('jegytipus_azon', 1)
        self.r.sadd('s_jegytipusok', 'jegytipus_'+str(jegytipus_azonosito))

        self.r.hmset('jegytipus_'+str(jegytipus_azonosito), {
            'nev': nev,
            'ar': ar,
            'erv_kezd': erv_kezd,
            'erv_vege': erv_vege
        })

    def jegytipus_lista(self):
        for i in self.r.smembers('s_jegytipusok'):
            print(self.r.hgetall(i))

    def uj_vendeg(self, email, nev, szuldat, nem):
        self.r.sadd('s_vendegek', email)
        self.r.hmset(email, {
            'nev': nev,
            'szul_dat': szuldat,
            'nem': nem
        })

    def vendeg_lista(self):
        for i in self.r.smembers('s_vendegek'):
            print(i)
            print(self.r.hgetall(i))

    def jegyet_vasarol(self, email, jegytipus):
        if self.r.sismember('s_vendegek', email):
            self.r.lpush(email+"_jegyei", jegytipus)
        else:
            print(f'Nem letezik vendeg a {email} cimmel!')
            return

    def esemenyt_likeolja(self, email, esemeny):
        if not(self.r.sismember('s_esemenyek', esemeny)) or not(self.r.sismember('s_vendegek', email)):
            print('Rossz email vagy esemeny')
            return
        self.r.sadd(str(email)+'_likejai', esemeny)

        self.r.zincrby("z_lajkok", 1, esemeny)

    def esemeny_lista(self):
        for i in self.r.zrevrange('z_lajkok', 0, -1):
            print(self.r.hgetall(i))

    def vendeg_altal_likeolt(self, email):
        for i in self.r.smembers(str(email) + '_likejai'):
            print(i)

