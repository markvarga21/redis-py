from UtasitasNaplozas2.UtasitasOsztaly import UtasitasOsztaly

rf = UtasitasOsztaly()

# rf.regisztralas('Aladar', '123')
# rf.regisztralas('Anna', '123')
# rf.regisztralas('Gabor', '123')
# rf.regisztralas('Janos', '123')
#
# rf.felhasznalo_lista()

# AnnaToken1 = rf.bejelentkezik('Anna', '123')
# AnnaToken2 = rf.bejelentkezik('Anna', '123')
# GaborToken = rf.bejelentkezik('Gabor', '123')

# rf.elfelejtett_jelszo('Anna')

# rf.bejelentkezik('Janos', '123')
# rf.kijelentkezik('Janos')

# print('Token ervenyesseg check:')
# print(rf.ervenyes_token('Anna', AnnaToken1))
# print(rf.ervenyes_token('Anna', '123'))
#
# rf.token_utasitast_ad_ki(AnnaToken1, 'cd ..')
# rf.token_utasitast_ad_ki(AnnaToken1, 'cd /alma')
# rf.token_utasitast_ad_ki(GaborToken, 'cd /korte')
#
# print('Anna utasitasai:')
# rf.uccso_szaz_utasitas('Anna')
# print('Gabor utasitasai:')
# rf.uccso_szaz_utasitas('Gabor')

JanosToken = rf.bejelentkezik('Janos', '123')
JanosToken2 = rf.bejelentkezik('Janos', '123')
print('Valid-e Janos tokenje: {}'.format(rf.ervenyes_token('Janos', JanosToken)))
rf.token_utasitast_ad_ki(JanosToken, 'utasitas1')
rf.token_utasitast_ad_ki(JanosToken, 'utasitas2')
rf.token_utasitast_ad_ki(JanosToken2, 'utasitas3')

print('Janos utasitasai:')
rf.uccso_szaz_utasitas('Janos')

