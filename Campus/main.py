from Campus import CFOsztaly

rf = CFOsztaly()

# rf.uj_helyszin('Viztorony')
# rf.uj_helyszin('Stadion')
# rf.uj_helyszin('Nagyerdo')

# rf.helyszin_lista()

# rf.uj_esemeny('Nagyerdo', "123", "456", 'Dua Lipa', 'Aladar', '0620')
# rf.uj_esemeny('Stadion', "500", "600", '30Y', 'Aladar', '0620')

# rf.idopont_kozotti_esemenyek("100", "600")

# rf.osszes_esemeny()

# rf.uj_jegytipus('felnott', '5500', '123', '456')
# rf.uj_jegytipus('gyerek', '5500', '123', '456')
# rf.uj_jegytipus('napos', '5500', '123', '456')

# rf.jegytipus_lista()

# rf.uj_vendeg('aladar@gmail.com', 'Aladar', '20015456', 'ferfi')
# rf.uj_vendeg('gabor@gmail.com', 'Gabor', '20015456', 'ferfi')
# rf.uj_vendeg('anna@gmail.com', 'Anna', '20015422', 'no')
# rf.uj_vendeg('milan@gmail.com', 'Milan', '20015422', 'ferfi')
# rf.uj_vendeg('zsuzsa@gmail.com', 'Zsuzsa', '20015422', 'no')
# rf.vendeg_lista()

# rf.jegyet_vasarol('aladat@gmail.com', 'felnott')
# rf.jegyet_vasarol('aladat@gmail.com', 'napos')

# rf.jegyet_vasarol('aladatdd@gmail.com', 'napos')

# rf.esemenyt_likeolja('aladar@gmail.com', 'esemeny_1')
# rf.esemenyt_likeolja('gabor@gmail.com', 'esemeny_2')
# rf.esemenyt_likeolja('anna@gmail.com', 'esemeny_1')

# rf.esemenyt_likeolja('zsuzsa@gmail.com', 'esemeny_2')
# rf.esemenyt_likeolja('milan@gmail.com', 'esemeny_2')
rf.esemenyt_likeolja('anna@gmail.com', 'esemeny_2')

rf.esemeny_lista()

print()

rf.vendeg_altal_likeolt('anna@gmail.com')

