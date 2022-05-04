from SzavazasCikkekre.SzavazasOsztaly import SzavazasOsztaly

rf = SzavazasOsztaly()

# rf.uj_cikk('Cikk1cime', 'cim1link.com', 'Aladar', '02/05/22 10:00:00')
# rf.uj_cikk('Regicikk', 'cim1link.com', 'Janos', '02/04/22 15:00:00')
# rf.uj_cikk('Cikk2cime', 'cim1link.com', 'Gabor', '01/05/22 15:00:00')
# rf.uj_cikk('Cikk3cime', 'cim1link.com', 'Anna', '29/05/22 15:00:00')

# rf.cikk_lista()

# print('Az elso cikk adatai:')
# rf.cikk_adatok('1')

# rf.szavazas('anna12', '1')
# rf.szavazas('anna12', '3')
# # hiba
# rf.szavazas('anna12', '1')
# rf.szavazas('anna12', '2')
# rf.szavazas('gabor34', '4')

# rf.cikk_lista_szavazatszam_alapjan_csokkenoen()
# rf.cikk_lista_posztido_alapjan_csokkenoen()
# rf.legutoljara_posztolt_cikk()
# rf.legtobb_szavazatos_cikk()

# rf.uj_csoport('elso_csoport')
# rf.uj_csoport('masodik_csoport')
#
# rf.cikk_csopihoz_rendeles('elso_csoport', '1')
# rf.cikk_csopihoz_rendeles('elso_csoport', '2')
#
# rf.cikk_csopihoz_rendeles('masodik_csoport', '3')
# rf.cikk_csopihoz_rendeles('masodik_csoport', '4')

# rf.csoport_cikk_lista('masodik_csoport')

# rf.csoportcikkek_szavazat_alapjan_csokkenoen('elso_csoport')
rf.cikk_adatok('2')
rf.cikk_adatok('1')
rf.csoportcikkek_datum_alapjan_csokkenoen('elso_csoport')