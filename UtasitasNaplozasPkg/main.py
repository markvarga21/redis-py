from UtasitasNaplozas import UtasitasOsztaly

rf = UtasitasOsztaly()

# rf.regisztral('felh1', 'jelszo1')
# rf.regisztral('felh2', 'jelszo2')
# rf.regisztral('felh2', 'jelszo22')

# rf.bejelentkezik('felh1', 'jelszo1')
# rf.bejelentkezik('felh1', 'jelszo1')

# rf.elfelejtett_jelszo('felh1')

# rf.kijelentkezik('felh1')

print(rf.felhasznalok_listaja())


# rf.kijelentkezik('felh1')

# rf.felhasznalo_bejelentkezve_vane('felh1')

# token1 = rf.bejelentkezik('felh1', 'jelszo1')
# token2 = rf.bejelentkezik('felh1', 'jelszo1')
#
# rf.utasitast_ad_ki(token1, 'print')
# rf.utasitast_ad_ki(token1, 'history')
# rf.utasitast_ad_ki(token2, 'cd')

rf.utolso_utasitas('felh1', 2)



