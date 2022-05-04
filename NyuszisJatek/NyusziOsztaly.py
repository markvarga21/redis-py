# -*- coding: windows-1250 -*-
import redis


class NyusziOsztaly():

    def __init__(self):
        redis_host = '192.168.1.218'
        redis_port = 6379

        self.r = redis.Redis(host=redis_host, port=redis_port,
                             decode_responses=True)

    def uj_jatekszoba(self, jsz_nev):
        if self.r.sismember('jatekszobak', jsz_nev):
            print(f'Mar van {jsz_nev} nevvel egy jatekszoba!')
            return
        # nyuszit is inicializaljuk/letrehozzuk erre a szobara vonatkozoan
        self.r.incr(jsz_nev + '_nyuszi')

        self.r.sadd('jatekszobak', jsz_nev)

    def felhasznalo_jatekszobaba_lep(self, jsz_nev, felh):
        if not (self.r.sismember('jatekszobak', jsz_nev)):
            print(f'Nincs {jsz_nev} nevvel egy jatekszoba!')
            return
        self.r.sadd(jsz_nev + '_felhasznalok', felh)

    def jatekszoba_lista(self):
        print(self.r.smembers('jatekszobak'))

    def felhasznalo_tippel(self, jsz_nev, felh, pozicio):
        if not (self.r.sismember('jatekszobak', jsz_nev)):
            print(f'Nincs {jsz_nev} nevvel egy jatekszoba!')
            return
        if not (self.r.sismember(jsz_nev + '_felhasznalok', felh)):
            print(f'Nincs {felh} felhasznalo!')
            return

        # aktualis jatekhoz tippek tarolasa
        self.r.incr(felh + '_' + jsz_nev + '_tippszam')

        # megnezzuk eltalalja e a poziciot
        igazi_nyuszi_pozicio = int(self.r.get(jsz_nev + '_nyuszi'))
        if igazi_nyuszi_pozicio == int(pozicio):
            # aktualis jatekhoz sikeres tippek szamanak tarolasa
            self.r.incr(felh + '_' + jsz_nev + '_sikeres_tippszam')

            # a felhasznalo kap egy pontot
            self.r.zincrby(jsz_nev + '_pontszamok', 1, felh)
            # megnezzuk van e nyertes, ha igen akkor nyuszit 1-es poziciora
            # valaki nyertes, ha a pontszama 10-nem tobbszorose, egyszerubb igy nyilvantartani a
            # pontszamokat, es az uj jatekokat
            # self.r.zrevrange(jsz_nev + '_pontszamok', 0, 0) -> felh
            # utanna meg elkerjuk a pontszamat
            top_jatekos_nev = str(self.r.zrevrange(jsz_nev + '_pontszamok', 0, 0)[0])
            top_pontszam = self.r.zscore(jsz_nev + '_pontszamok', top_jatekos_nev)
            if top_pontszam % 10 == 0 and top_pontszam != 0:
                print('Nyertes at')
                # van nyertes
                self.r.set(jsz_nev + '_nyuszi', 1)
                # le kell vinni 1-re mivel az aktualis tippszamot taroljuk
                self.r.set(felh + '_' + jsz_nev + '_tippszam', 1)
                # a sikeres tipp szamot is le kell vinni 1-re
                self.r.set(felh + '_' + jsz_nev + '_sikeres_tippszam', 1)
                self.r.incr(felh + '_ennyiszer_jatszott')
            else:
                # leptejuk a nyuszit jobbra
                print('Leptet')
                self.leptet(jsz_nev)

    def leptet(self, jsz_nev):
        # ha elerte a veget
        if self.r.get(jsz_nev + '_nyuszi') == 10:
            self.r.set(jsz_nev + '_nyuszi', 1)
        # ha meg nem erte el a veget
        else:
            self.r.incr(jsz_nev + '_nyuszi')

    def felhasznalok_pontszama(self, jsz_nev):
        print(self.r.zrange(jsz_nev + '_pontszamok', 0, -1, withscores=True))

    def hol_a_nyuszi(self, jsz_nev):
        print(self.r.get(jsz_nev + '_nyuszi'))

    def felhasznaloi_rangsor_adott_jatekra(self, jsz_nev):
        # sikeres tippek alapjan nezzuk a rangsort, mivel aktualis jatekrol van szo
        for felh in self.r.smembers(jsz_nev + '_felhasznalok'):
            di = dict()
            sikeres_tippek = self.r.get(felh + '_' + jsz_nev + '_sikeres_tippszam')
            di[felh] = sikeres_tippek
            self.r.zadd('temp', di)
        # kiiras
        self.r.zrevrange('temp', 0, -1, withscores=True)
        self.r.delete('temp')

    def felhasznaloi_rangsor_osszes_jatekra(self):
        jatekszobak = self.r.smembers('jatekszobak')
        for i in range(1, len(jatekszobak) + 1):
            # paronknet osszeuniozza a jatekszobak rangsorait
            self.r.zunionstore('ossz_rangsor_temp', jatekszobak[i], jatekszobak[i - 1])

        print(self.r.zrevrange('ossz_rangsor_temp', 0, -1, withscores=True))
        self.r.delete('ossz_rangsor_temp')

    def felhasznalo_hanyszor_jatszott(self):
        for jsz_nev in self.r.smembers('jatekszobak'):
            for felh in self.r.smembers(jsz_nev + '_felhasznalok'):
                self.r.sadd('osszes_felhasznalo', felh)
        # kiiras
        for felh in self.r.smembers('osszes_felhasznalo'):
            self.r.get(felh + '_ennyiszer_jatszott')

        self.r.delete('osszes_felhasznalo')

    def felh_lista_jatszott_jatekok_alapjan_csokkenoen(self):
        for jsz_nev in self.r.smembers('jatekszobak'):
            for felh in self.r.smembers(jsz_nev + '_felhasznalok'):
                self.r.sadd('osszes_felhasznalo', felh)
        for felh in self.r.smembers('osszes_felhasznalo'):
            di = dict()
            di[felh] = self.r.get(felh + '_ennyiszer_jatszott')
            self.r.zadd('temp', di)
        # kiiras
        print(self.r.zrevrange('temp', 0, -1, withscores=True))
        # temp-ek torlese
        self.r.delete('temp')
        self.r.delete('osszes_felhasznalo')

    def felh_lista_atlag_pontszam_alapjan(self):
        # ossz pontszamok szamolasa
        # jatekszobak = self.r.smembers('jatekszobak')
        for i in self.r.smembers('jatekszobak'):
            # paronknet osszeuniozza a jatekszobak rangsorait
            self.r.zunionstore('ossz_rangsor_temp', ['oszes_rangsor_temp', i + '_pontszamok'], aggregate='sum')

        for felh in self.r.zrevrange('ossz_rangsor_temp', 0, -1):
            felh_ossz_pontszam = float(self.r.zscore('ossz_rangsor_temp', felh))
            felh_ennyiszer_jatszott = float(self.r.get(felh + '_ennyiszer_jatszott'))
            di = dict()
            di[felh] = felh_ossz_pontszam / felh_ennyiszer_jatszott
            self.r.zadd('atlag_pontos_temp', di)

        # kiiras
        print(self.r.zrevrange('atlag_pontos_temp', 0, -1, withscores=True))

        self.r.delete('atlag_pontos_temp')
        self.r.delete('ossz_rangsor_temp')

    def felhasznalo_pontjai_lista(self):
        for i in self.r.smembers('jatekszobak'):
            # paronknet osszeuniozza a jatekszobak rangsorait
            if self.r.exists(i + '_pontszamok'):
                self.r.zunionstore('ossz_rangsor_temp', ['oszes_rangsor_temp', i + '_pontszamok'], aggregate='sum')

        print(self.r.zrevrange('ossz_rangsor_temp', 0, -1, withscores=True))
        self.r.delete('ossz_rangsor_temp')

    def jatekszoba_aktualis_jatekhoz_tartozo_tippek_szama(self):
        jatekszobak = self.r.smembers('jatekszobak')
        for jsz_nev in jatekszobak:
            osszes_tipp = 0
            for felh in self.r.smembers(jsz_nev + '_felhasznalok'):
                osszes_tipp = self.r.get(felh + '_' + jsz_nev + '_tippszam')
            print(f'Jatekszoba neve: {jsz_nev}, osszes tippek szama: {osszes_tipp}')

    def jatekszoba_aktualis_ossz_talalatok_szama(self):
        jatekszobak = self.r.smembers('jatekszobak')
        for jsz_nev in jatekszobak:
            ossz_talalat = 0
            for felh in self.r.smembers(jsz_nev + '_felhasznalok'):
                ossz_talalat = self.r.get(felh + '_' + jsz_nev + '_sikeres_tippszam')
            if ossz_talalat == None:
                ossz_talalat = 0
            print(f'Jatekszoba neve: {jsz_nev}, osszes tippek szama: {ossz_talalat}')


    def legjobb_jatekos(self):
        for i in self.r.smembers('jatekszobak'):
            # paronknet osszeuniozza a jatekszobak rangsorait
            if self.r.exists(i + '_pontszamok'):
                self.r.zunionstore('ossz_rangsor_temp', ['oszes_rangsor_temp', i + '_pontszamok'], aggregate='sum')

        print(self.r.zrevrange('ossz_rangsor_temp', 0, 0, withscores=True))
        self.r.delete('ossz_rangsor_temp')
