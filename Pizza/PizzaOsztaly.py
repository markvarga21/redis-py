# -*- coding: windows-1250 -*-
import redis

class PizzaOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def uj_pizza(self, pizza_azon, ar):
        if self.r.sismember('pizza_azonositok', pizza_azon):
            print('Mar van ilyen azonositoval pizza!')
            return
        self.r.sadd('pizza_azonositok', pizza_azon)
        self.r.hset('pizzak', pizza_azon, ar)

    def pizza_ar_modositas(self, azon, uj_ar):
        if not(self.r.sismember('pizza_azonositok', azon)):
            print('Nincs ilyen azonositoju pizza!')
            return
        self.r.hset('pizzak', azon, uj_ar)

    def feltet_hozzaadasa(self, azon, feltet):
        if not(self.r.sismember('pizza_azonositok', azon)):
            print('Nincs ilyen azonositoju pizza!')
            return
        self.r.sadd(azon + '_feltetek', feltet)

    def pizza_lista_feltettel(self):
        for azon in self.r.hkeys('pizzak'):
            print(f'Azonosito: {azon}')
            print('Ar: {}'.format(self.r.hget('pizzak', azon)))
            print('Feltetek: {}'.format(self.r.smembers(azon + '_feltetek')))

    def megrendeles_felvetel(self, bejoveteli_ido, cim, azonosito):
        if self.r.sismember('megrendelesek', azonosito):
            print('Mar vna ilyen rendeles azonosito!')
            return
        self.r.sadd('megrendelesek', azonosito)
        self.r.hmset('rendeles_' + azonosito, {
                    'bejoveteli_ido': bejoveteli_ido,
                    'cim': cim
        })

    def pizza_rendelese_megrendeleshez(self, megrendeles_azonosito, pizza_azon, db):
        if not(self.r.sismember('megrendelesek', megrendeles_azonosito)):
            print('Nincs ilyen megrendeles azonosito!')
            return
        if not(self.r.sismember('pizza_azonositok', pizza_azon)):
            print('Nincs ilyen azonositoju pizza!')
            return
        self.r.hset(megrendeles_azonosito + '_pizzai', pizza_azon, db)
        for i in range(db):
            self.r.rpush('sutnivalo_pizzak', pizza_azon)
            self.r.rpush('sutnivalo_megrendeles_azonositok', megrendeles_azonosito)

    def soron_kovetkezo_sutnivalo_pizza(self):
        print(self.r.lrange('sutnivalo_pizzak', 0, 0))

    # a szakacs elkezdi sutni a soroon kovetkezo pizzakat, szepen sorban
    def szakacs_elkezdi_sutni_a_pizzat(self):
        self.r.rpush('sutobeli_pizzak', self.r.lpop('sutnivalo_pizzak', 1))
        self.r.rpush('sutobeli_megrendeles_azonositok', self.r.lpop('sutnivalo_megrendeles_azonositok', 1))
        
    def pizza_kesz(self):
        self.r.rpush('kesz_pizzak', self.r.lpop('sutobeli_pizzak', 1))
        self.r.rpush('kesz_megrendeles_azonositok', self.r.lpop('sutobeli_megrendeles_azonositok', 1))

    def kesz_de_meg_ki_nem_szallitott_pizzak(self):
        print(self.r.lrange('kesz_pizzak', 0, -1))

    def pizza_kiszallitasa(self, megrendeles_azon):
        osszes_db_szam = self.r.hvals(megrendeles_azon + '_pizzai')
        ls = self.r.lrange('kesz_megrendeles_azonositok', 0, -1)
        # if ls.count(megrendeles_azon) == osszes_db_szam:




