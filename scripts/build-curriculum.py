"""Authoring source. Each line is a story fact, translation, question, and four explicit options."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
levels=[]
def reading(world,n,title,ar,scene,objective,intro,rows):
    facts=[]
    for row in rows.strip().splitlines():
        parts=[p.strip() for p in row.split('|')]
        assert len(parts)==7,(n,row,len(parts))
        facts.append(parts)
    assert len(facts)==10,(n,len(facts))
    text=' '.join(r[0] for r in facts)
    questions=[]
    for i,r in enumerate(facts):
        opts=r[3:]; shift=(n+i)%4; opts=opts[shift:]+opts[:shift]
        questions.append(dict(id=f'{world}-{n}-q{i+1}',ar=r[2],options=opts,answer=opts.index(r[3]),explanationAr=r[0],explanationId=r[1],category=['Tokoh dan kosakata','Informasi','Instruksi dan urutan','Konteks dan kesimpulan'][i%4]))
    vocab=[]
    for r in facts[:6]:vocab.append({'ar':r[3],'id':r[1]})
    levels.append(dict(id=f'{world}-{n}',world=world,number=n,title=title,titleAr=ar,scene=scene,objective=objective,mission=intro,character='Lulu si kelinci' if world=='istima' else 'Rafi si rubah',textAr=text,textId=' '.join(r[1] for r in facts),vocabulary=vocab,questions=questions,reward=['Kompas','Kristal','Kunci','Peta','Lentera','Permata','Daun emas','Lencana','Medali','Peti harta'][n-1]))
reading('istima',1,'Salam di gerbang hutan','التَّحِيَّةُ','forest','Memahami salam, sapaan, dan tanggapan dalam pertemuan sederhana.','Bantu Lulu mengenali teman-teman di gerbang hutan. Dengarkan seluruh cerita sebelum menjawab.', '''
فِي الصَّبَاحِ، وَصَلَ أَحْمَدُ إِلَى بَابِ الْغَابَةِ.|Pada pagi hari, Ahmad tiba di gerbang hutan.|مَنْ وَصَلَ إِلَى بَابِ الْغَابَةِ؟|أَحْمَدُ|سَلْمَى|عَلِيٌّ|مَرْيَمُ
قَالَ أَحْمَدُ لِصَدِيقِهِ: السَّلَامُ عَلَيْكُمْ يَا عَلِيُّ.|Ahmad berkata kepada temannya: Assalamualaikum, Ali.|مَاذَا قَالَ أَحْمَدُ لِعَلِيٍّ؟|السَّلَامُ عَلَيْكُمْ|إِلَى اللِّقَاءِ|تُصْبِحُ عَلَى خَيْرٍ|آسِفٌ
أَجَابَ عَلِيٌّ بِابْتِسَامَةٍ: وَعَلَيْكُمُ السَّلَامُ يَا صَدِيقِي.|Ali menjawab sambil tersenyum: Waalaikumussalam, temanku.|كَيْفَ أَجَابَ عَلِيٌّ؟|وَعَلَيْكُمُ السَّلَامُ|مَسَاءُ الْخَيْرِ|شُكْرًا|مَعَ السَّلَامَةِ
سَأَلَ أَحْمَدُ: كَيْفَ حَالُكَ فِي هَذَا الصَّبَاحِ؟|Ahmad bertanya: Bagaimana kabarmu pagi ini?|عَنْ مَاذَا سَأَلَ أَحْمَدُ؟|الْحَالِ|الْعُمْرِ|اللَّوْنِ|الطَّعَامِ
قَالَ عَلِيٌّ: أَنَا بِخَيْرٍ، وَالْحَمْدُ لِلَّهِ.|Ali berkata: Aku baik, alhamdulillah.|كَيْفَ حَالُ عَلِيٍّ؟|بِخَيْرٍ|مَرِيضٌ|حَزِينٌ|مُتْعَبٌ
ثُمَّ جَاءَتْ سَلْمَى تَحْمِلُ حَقِيبَةً صَغِيرَةً جَمِيلَةً.|Kemudian Salma datang membawa tas kecil yang indah.|مَاذَا تَحْمِلُ سَلْمَى؟|حَقِيبَةً|كُرَةً|كِتَابًا|قَلَمًا
قَالَتْ سَلْمَى لِلصَّدِيقَيْنِ: صَبَاحُ الْخَيْرِ يَا أَصْدِقَائِي.|Salma berkata kepada kedua teman: Selamat pagi, teman-temanku.|مَاذَا قَالَتْ سَلْمَى؟|صَبَاحُ الْخَيْرِ|مَسَاءُ الْخَيْرِ|تُصْبِحُ عَلَى خَيْرٍ|إِلَى اللِّقَاءِ
رَدَّ أَحْمَدُ وَعَلِيٌّ مَعًا: صَبَاحُ النُّورِ يَا سَلْمَى.|Ahmad dan Ali menjawab bersama: Selamat pagi, Salma.|مَا الرَّدُّ عَلَى صَبَاحِ الْخَيْرِ فِي الْقِصَّةِ؟|صَبَاحُ النُّورِ|آسِفٌ|مَعَ السَّلَامَةِ|مَرْحَبًا بِاللَّيْلِ
لَعِبَ الْأَصْدِقَاءُ الثَّلَاثَةُ قُرْبَ شَجَرَةٍ كَبِيرَةٍ.|Ketiga teman bermain di dekat pohon besar.|كَمْ صَدِيقًا لَعِبَ قُرْبَ الشَّجَرَةِ؟|ثَلَاثَةٌ|وَاحِدٌ|اِثْنَانِ|خَمْسَةٌ
وَعِنْدَ الرَّحِيلِ، قَالَ الْجَمِيعُ: مَعَ السَّلَامَةِ.|Saat berpisah, semuanya mengucapkan: Selamat jalan.|مَتَى قَالُوا مَعَ السَّلَامَةِ؟|عِنْدَ الرَّحِيلِ|عِنْدَ النَّوْمِ|عِنْدَ الْأَكْلِ|قَبْلَ اللَّعِبِ
''')
reading('istima',2,'Jembatan angka','الْأَرْقَامُ','forest','Mengenali jumlah satu sampai sepuluh dari cerita yang didengar.','Hitung bekal rombongan untuk menyeberangi jembatan.', '''
فِي يَوْمٍ جَمِيلٍ، حَمَلَ سَامِي خَرِيطَةً وَاحِدَةً لِلرِّحْلَةِ.|Pada hari yang indah, Sami membawa satu peta untuk perjalanan.|كَمْ خَرِيطَةً حَمَلَ سَامِي؟|وَاحِدَةً|اِثْنَتَيْنِ|ثَلَاثًا|أَرْبَعًا
وَضَعَ فِي حَقِيبَتِهِ قَلَمَيْنِ لِرَسْمِ الطَّرِيقِ.|Ia memasukkan dua pena ke tasnya untuk menggambar jalan.|كَمْ قَلَمًا وَضَعَ فِي الْحَقِيبَةِ؟|قَلَمَيْنِ|قَلَمًا وَاحِدًا|ثَلَاثَةَ أَقْلَامٍ|خَمْسَةَ أَقْلَامٍ
أَعْطَتْهُ أُمُّهُ ثَلَاثَ تُفَّاحَاتٍ حَمْرَاءَ لِلطَّرِيقِ.|Ibunya memberinya tiga apel merah sebagai bekal.|كَمْ تُفَّاحَةً أَعْطَتْهُ أُمُّهُ؟|ثَلَاثًا|أَرْبَعًا|خَمْسًا|سِتًّا
عِنْدَ الْجِسْرِ، رَأَى أَرْبَعَ سَمَكَاتٍ فِي النَّهْرِ.|Di jembatan, ia melihat empat ikan di sungai.|كَمْ سَمَكَةً رَأَى؟|أَرْبَعًا|ثَلَاثًا|سَبْعًا|تِسْعًا
كَانَتْ خَمْسُ زَهَرَاتٍ صَفْرَاءَ بِجَانِبِ النَّهْرِ.|Ada lima bunga kuning di tepi sungai.|كَمْ زَهْرَةً كَانَتْ بِجَانِبِ النَّهْرِ؟|خَمْسٌ|سِتٌّ|اِثْنَتَانِ|عَشْرٌ
وَسَمِعَ سِتَّةَ عَصَافِيرَ تُغَرِّدُ فَوْقَ الشَّجَرَةِ.|Ia mendengar enam burung berkicau di pohon.|كَمْ عُصْفُورًا سَمِعَ؟|سِتَّةً|خَمْسَةً|ثَلَاثَةً|ثَمَانِيَةً
جَمَعَ سَامِي سَبْعَ حَصَوَاتٍ صَغِيرَةٍ مِنَ الطَّرِيقِ.|Sami mengumpulkan tujuh kerikil kecil dari jalan.|كَمْ حَصَاةً جَمَعَ سَامِي؟|سَبْعًا|أَرْبَعًا|سِتًّا|تِسْعًا
وَرَأَى ثَمَانِيَ فَرَاشَاتٍ تَطِيرُ فَوْقَ الْأَزْهَارِ.|Ia melihat delapan kupu-kupu terbang di atas bunga.|كَمْ فَرَاشَةً رَأَى؟|ثَمَانِيًا|خَمْسًا|سَبْعًا|عَشْرًا
وَجَدَ تِسْعَ أَوْرَاقٍ خَضْرَاءَ تَحْتَ الشَّجَرَةِ الْكَبِيرَةِ.|Ia menemukan sembilan daun hijau di bawah pohon besar.|كَمْ وَرَقَةً وَجَدَ؟|تِسْعًا|سِتًّا|أَرْبَعًا|ثَلَاثًا
وَفِي النِّهَايَةِ، مَشَى عَشْرَ خُطُوَاتٍ إِلَى الْبَابِ.|Terakhir, ia melangkah sepuluh langkah menuju gerbang.|كَمْ خُطْوَةً مَشَى إِلَى الْبَابِ؟|عَشْرًا|تِسْعًا|ثَمَانِيًا|سَبْعًا
''')
reading('istima',3,'Taman warna','الْأَلْوَانُ','forest','Mengidentifikasi warna benda dalam satu deskripsi taman.','Temukan kristal warna yang tersembunyi di taman Lulu.', '''
دَخَلَتْ نُورُ حَدِيقَةً جَمِيلَةً ذَاتَ بَابٍ أَزْرَقَ.|Nur masuk taman indah yang memiliki gerbang biru.|مَا لَوْنُ بَابِ الْحَدِيقَةِ؟|أَزْرَقُ|أَحْمَرُ|أَصْفَرُ|أَخْضَرُ
رَأَتْ وَرْدَةً حَمْرَاءَ قُرْبَ الْبَابِ الْكَبِيرِ.|Ia melihat mawar merah dekat gerbang besar.|مَا لَوْنُ الْوَرْدَةِ؟|حَمْرَاءُ|بَيْضَاءُ|سَوْدَاءُ|زَرْقَاءُ
وَجَدَتْ زَهْرَةً صَفْرَاءَ بِجَانِبِ الْوَرْدَةِ الْحَمْرَاءِ.|Ia menemukan bunga kuning di samping mawar merah.|مَا لَوْنُ الزَّهْرَةِ؟|صَفْرَاءُ|خَضْرَاءُ|بُنِّيَّةٌ|سَوْدَاءُ
كَانَ عُشْبُ الْحَدِيقَةِ أَخْضَرَ وَنَاعِمًا تَحْتَ قَدَمَيْهَا.|Rumput taman hijau dan lembut di bawah kakinya.|مَا لَوْنُ الْعُشْبِ؟|أَخْضَرُ|أَبْيَضُ|أَحْمَرُ|بُرْتُقَالِيٌّ
جَلَسَتْ قِطَّةٌ بَيْضَاءُ عَلَى مَقْعَدٍ صَغِيرٍ.|Seekor kucing putih duduk di bangku kecil.|مَا لَوْنُ الْقِطَّةِ؟|بَيْضَاءُ|سَوْدَاءُ|صَفْرَاءُ|حَمْرَاءُ
وَكَانَ غُرَابٌ أَسْوَدُ فَوْقَ غُصْنِ شَجَرَةٍ.|Seekor gagak hitam berada di dahan pohon.|مَا لَوْنُ الْغُرَابِ؟|أَسْوَدُ|أَزْرَقُ|أَبْيَضُ|أَخْضَرُ
حَمَلَتْ نُورُ سَلَّةً بُنِّيَّةً فِيهَا بَعْضُ الْفَوَاكِهِ.|Nur membawa keranjang cokelat berisi beberapa buah.|مَا لَوْنُ السَّلَّةِ؟|بُنِّيَّةٌ|وَرْدِيَّةٌ|زَرْقَاءُ|بَيْضَاءُ
وَضَعَتْ بُرْتُقَالَةً بُرْتُقَالِيَّةَ اللَّوْنِ فِي السَّلَّةِ.|Ia memasukkan jeruk berwarna oranye ke keranjang.|مَا الْفَاكِهَةُ الْبُرْتُقَالِيَّةُ؟|الْبُرْتُقَالَةُ|التُّفَّاحَةُ|الْمَوْزَةُ|الْعِنَبُ
ثُمَّ رَأَتْ فَرَاشَةً بَنَفْسَجِيَّةً تَطِيرُ أَمَامَهَا.|Lalu ia melihat kupu-kupu ungu terbang di depannya.|مَا لَوْنُ الْفَرَاشَةِ؟|بَنَفْسَجِيَّةٌ|حَمْرَاءُ|سَوْدَاءُ|صَفْرَاءُ
وَعَادَتْ إِلَى بَيْتِهَا ذِي النَّافِذَةِ الْوَرْدِيَّةِ.|Ia pulang ke rumahnya yang berjendela merah muda.|مَا لَوْنُ نَافِذَةِ بَيْتِهَا؟|وَرْدِيَّةٌ|زَرْقَاءُ|خَضْرَاءُ|بُنِّيَّةٌ
''')
reading('istima',4,'Rumah keluarga penjaga','أُسْرَتِي','forest','Memahami hubungan anggota keluarga dan pekerjaan mereka.','Kunjungi keluarga penjaga hutan untuk menemukan potongan peta.', '''
أَنَا مَرْيَمُ، وَأَعِيشُ مَعَ أُسْرَتِي فِي بَيْتٍ قُرْبَ الْغَابَةِ.|Aku Maryam dan tinggal bersama keluargaku di rumah dekat hutan.|مَنْ تَتَحَدَّثُ عَنْ أُسْرَتِهَا؟|مَرْيَمُ|نُورُ|هِنْدٌ|سَلْمَى
فِي أُسْرَتِي سِتَّةُ أَشْخَاصٍ، وَنَحْنُ نُحِبُّ بَعْضَنَا.|Keluargaku berjumlah enam orang dan kami saling menyayangi.|كَمْ شَخْصًا فِي الْأُسْرَةِ؟|سِتَّةٌ|أَرْبَعَةٌ|خَمْسَةٌ|سَبْعَةٌ
أَبِي مُعَلِّمٌ، وَيُعَلِّمُ الْأَطْفَالَ فِي مَدْرَسَةِ الْقَرْيَةِ.|Ayahku guru dan mengajar anak-anak di sekolah desa.|مَا عَمَلُ الْأَبِ؟|مُعَلِّمٌ|طَبِيبٌ|بَائِعٌ|فَلَّاحٌ
أُمِّي طَبِيبَةٌ، وَتُسَاعِدُ الْمَرْضَى فِي الْمُسْتَشْفَى الْقَرِيبِ.|Ibuku dokter dan membantu pasien di rumah sakit dekat sini.|أَيْنَ تَعْمَلُ الْأُمُّ؟|فِي الْمُسْتَشْفَى|فِي السُّوقِ|فِي الْمَكْتَبَةِ|فِي الْمَزْرَعَةِ
أَخِي الْكَبِيرُ يُوسُفُ، وَعُمْرُهُ اِثْنَا عَشَرَ عَامًا.|Kakak laki-lakiku Yusuf, usianya dua belas tahun.|مَا اسْمُ الْأَخِ الْكَبِيرِ؟|يُوسُفُ|عَلِيٌّ|حَسَنٌ|سَامِي
أُخْتِي الصَّغِيرَةُ هِنْدٌ، وَهِيَ تُحِبُّ رَسْمَ الْأَشْجَارِ.|Adik perempuanku Hind, ia suka menggambar pohon.|مَاذَا تُحِبُّ هِنْدٌ؟|رَسْمَ الْأَشْجَارِ|لَعِبَ الْكُرَةِ|طَبْخَ الطَّعَامِ|قِرَاءَةَ الْخَرَائِطِ
جَدَّتِي تَسْكُنُ مَعَنَا، وَتَحْكِي لَنَا قِصَصًا قَبْلَ النَّوْمِ.|Nenek tinggal bersama kami dan bercerita sebelum tidur.|مَنْ تَحْكِي الْقِصَصَ؟|الْجَدَّةُ|الْأُخْتُ|الْأُمُّ|الْخَالَةُ
فِي الْمَسَاءِ، نَجْتَمِعُ جَمِيعًا حَوْلَ مَائِدَةِ الطَّعَامِ.|Pada malam hari kami berkumpul di meja makan.|مَتَى تَجْتَمِعُ الْأُسْرَةُ؟|فِي الْمَسَاءِ|عِنْدَ الْفَجْرِ|فِي الظُّهْرِ|فِي الصَّبَاحِ
يُسَاعِدُ يُوسُفُ أَبِي فِي تَرْتِيبِ الْحَدِيقَةِ يَوْمَ الْعُطْلَةِ.|Yusuf membantu ayah merapikan taman pada hari libur.|مَنْ يُسَاعِدُ الْأَبَ فِي الْحَدِيقَةِ؟|يُوسُفُ|هِنْدٌ|الْجَدَّةُ|مَرْيَمُ
وَأَنَا أُسَاعِدُ أُخْتِي فِي جَمْعِ أَلْوَانِهَا بَعْدَ الرَّسْمِ.|Aku membantu adikku mengumpulkan alat warnanya setelah menggambar.|مَاذَا تَجْمَعُ مَرْيَمُ مَعَ أُخْتِهَا؟|الْأَلْوَانَ|الْفَوَاكِهَ|الْكُتُبَ|الْأَحْذِيَةَ
''')
reading('istima',5,'Suara kebun binatang','الْحَيَوَانَاتُ','forest','Mengenali hewan melalui ciri, makanan, dan tempat hidup.','Dengarkan penjaga satwa dan cari hewan pembawa petunjuk.', '''
ذَهَبَ خَالِدٌ مَعَ أُخْتِهِ إِلَى حَدِيقَةِ الْحَيَوَانَاتِ صَبَاحًا.|Khalid pergi bersama saudara perempuannya ke kebun binatang pada pagi hari.|إِلَى أَيْنَ ذَهَبَ خَالِدٌ؟|حَدِيقَةِ الْحَيَوَانَاتِ|الْمَدْرَسَةِ|السُّوقِ|الْمَكْتَبَةِ
رَأَى فِيلًا كَبِيرًا لَهُ خُرْطُومٌ طَوِيلٌ وَأُذُنَانِ كَبِيرَتَانِ.|Ia melihat gajah besar dengan belalai panjang dan dua telinga besar.|أَيُّ حَيَوَانٍ لَهُ خُرْطُومٌ؟|الْفِيلُ|الْأَسَدُ|الْقِرْدُ|الْأَرْنَبُ
كَانَتِ الزَّرَافَةُ تَأْكُلُ أَوْرَاقَ الشَّجَرِ بِعُنُقِهَا الطَّوِيلِ.|Jerapah sedang memakan daun pohon dengan lehernya yang panjang.|مَاذَا تَأْكُلُ الزَّرَافَةُ؟|أَوْرَاقَ الشَّجَرِ|السَّمَكَ|اللَّحْمَ|الْخُبْزَ
سَمِعَ خَالِدٌ زَئِيرَ الْأَسَدِ مِنْ مَكَانٍ بَعِيدٍ.|Khalid mendengar auman singa dari tempat yang jauh.|أَيُّ صَوْتٍ سَمِعَ خَالِدٌ؟|زَئِيرَ الْأَسَدِ|مُوَاءَ الْقِطَّةِ|نُبَاحَ الْكَلْبِ|صَهِيلَ الْحِصَانِ
قَفَزَ قِرْدٌ صَغِيرٌ بَيْنَ الْأَغْصَانِ وَأَكَلَ مَوْزَةً.|Monyet kecil melompat di antara dahan dan memakan pisang.|مَاذَا أَكَلَ الْقِرْدُ؟|مَوْزَةً|جَزَرَةً|سَمَكَةً|تُفَّاحَةً
سَبَحَتْ بَطَّةٌ بَيْضَاءُ مَعَ صِغَارِهَا فِي الْبِرْكَةِ.|Bebek putih berenang bersama anak-anaknya di kolam.|أَيْنَ سَبَحَتِ الْبَطَّةُ؟|فِي الْبِرْكَةِ|فَوْقَ الشَّجَرَةِ|فِي الْقَفَصِ|تَحْتَ الْأَرْضِ
تَحْتَ شَجَرَةٍ، أَكَلَ أَرْنَبٌ أَبْيَضُ جَزَرَةً طَازَجَةً.|Di bawah pohon, kelinci putih memakan wortel segar.|مَا لَوْنُ الْأَرْنَبِ؟|أَبْيَضُ|أَسْوَدُ|بُنِّيٌّ|رَمَادِيٌّ
مَشَتْ سُلَحْفَاةٌ بِبُطْءٍ قُرْبَ صَخْرَةٍ فِي الْحَدِيقَةِ.|Seekor kura-kura berjalan perlahan dekat batu di kebun.|كَيْفَ مَشَتِ السُّلَحْفَاةُ؟|بِبُطْءٍ|بِسُرْعَةٍ|طَائِرَةً|قَافِزَةً
قَالَ الْحَارِسُ: لَا تُعْطُوا الْحَيَوَانَاتِ طَعَامًا مِنْ حَقَائِبِكُمْ.|Penjaga berkata: Jangan memberi hewan makanan dari tas kalian.|مَاذَا طَلَبَ الْحَارِسُ؟|عَدَمَ إِطْعَامِ الْحَيَوَانَاتِ|فَتْحَ الْأَقْفَاصِ|لَمْسَ الْأَسَدِ|دُخُولَ الْبِرْكَةِ
وَفِي النِّهَايَةِ، رَسَمَ خَالِدٌ الْفِيلَ فِي دَفْتَرِهِ.|Pada akhirnya Khalid menggambar gajah di bukunya.|أَيَّ حَيَوَانٍ رَسَمَ خَالِدٌ؟|الْفِيلَ|الزَّرَافَةَ|الْبَطَّةَ|السُّلَحْفَاةَ
''')
reading('istima',6,'Rahasia tubuh sehat','أَعْضَاءُ الْجِسْمِ','forest','Memahami nama anggota tubuh, fungsi, dan instruksi perawatan diri.','Ikuti petunjuk dokter desa agar tim siap melanjutkan perjalanan.', '''
زَارَتْ لَيْلَى طَبِيبَةَ الْقَرْيَةِ لِتَتَعَلَّمَ عَنِ الْجِسْمِ السَّلِيمِ.|Laila mengunjungi dokter desa untuk belajar tentang tubuh sehat.|مَنْ زَارَتْ لَيْلَى؟|طَبِيبَةَ الْقَرْيَةِ|مُعَلِّمَ الرِّيَاضَةِ|بَائِعَ الْفَوَاكِهِ|حَارِسَ الْغَابَةِ
قَالَتِ الطَّبِيبَةُ: لَنَا عَيْنَانِ نَرَى بِهِمَا الْأَشْيَاءَ.|Dokter berkata: Kita memiliki dua mata untuk melihat benda.|بِمَاذَا نَرَى الْأَشْيَاءَ؟|بِالْعَيْنَيْنِ|بِالْأُذُنَيْنِ|بِالْيَدَيْنِ|بِالْقَدَمَيْنِ
وَلَنَا أُذُنَانِ نَسْمَعُ بِهِمَا الْأَصْوَاتَ حَوْلَنَا جَيِّدًا.|Kita memiliki dua telinga untuk mendengar suara sekitar dengan baik.|كَمْ أُذُنًا لَنَا؟|أُذُنَانِ|أُذُنٌ وَاحِدَةٌ|ثَلَاثُ آذَانٍ|أَرْبَعُ آذَانٍ
نَشُمُّ رَائِحَةَ الْأَزْهَارِ الْجَمِيلَةِ بِالْأَنْفِ فِي الْحَدِيقَةِ.|Kita mencium aroma bunga yang indah dengan hidung di taman.|بِمَاذَا نَشُمُّ رَائِحَةَ الْأَزْهَارِ؟|بِالْأَنْفِ|بِالْفَمِ|بِالْعَيْنِ|بِالْيَدِ
نَأْكُلُ بِالْفَمِ، وَنُنَظِّفُ الْأَسْنَانَ بَعْدَ الْأَكْلِ لِنَحْمِيَهَا.|Kita makan dengan mulut dan membersihkan gigi setelah makan untuk menjaganya.|مَاذَا نُنَظِّفُ بَعْدَ الْأَكْلِ؟|الْأَسْنَانَ|الشَّعْرَ|الْأُذُنَ|الْقَدَمَ
طَلَبَتِ الطَّبِيبَةُ مِنْ لَيْلَى أَنْ تَغْسِلَ يَدَيْهَا بِالصَّابُونِ.|Dokter meminta Laila mencuci kedua tangannya dengan sabun.|بِمَاذَا تَغْسِلُ لَيْلَى يَدَيْهَا؟|بِالصَّابُونِ|بِالْعَصِيرِ|بِالرَّمْلِ|بِالزَّيْتِ
قَالَتْ: فِي كُلِّ يَدٍ خَمْسَةُ أَصَابِعَ لِلْإِمْسَاكِ بِالْأَشْيَاءِ.|Ia berkata: Pada setiap tangan ada lima jari untuk memegang benda.|كَمْ إِصْبَعًا فِي كُلِّ يَدٍ؟|خَمْسَةٌ|ثَلَاثَةٌ|سِتَّةٌ|عَشَرَةٌ
نَمْشِي بِالْقَدَمَيْنِ، وَنَلْبَسُ حِذَاءً مُنَاسِبًا عِنْدَ الْخُرُوجِ.|Kita berjalan dengan kedua kaki dan memakai sepatu yang sesuai saat keluar.|مَاذَا نَلْبَسُ لِحِمَايَةِ الْقَدَمَيْنِ؟|حِذَاءً|قُبَّعَةً|قُفَّازًا|وِشَاحًا
وَنَضَعُ قُبَّعَةً عَلَى الرَّأْسِ عِنْدَ الْمَشْيِ تَحْتَ الشَّمْسِ.|Kita memakai topi di kepala saat berjalan di bawah matahari.|أَيْنَ نَضَعُ الْقُبَّعَةَ؟|عَلَى الرَّأْسِ|عَلَى الْيَدِ|عَلَى الرُّكْبَةِ|عَلَى الْبَطْنِ
شَكَرَتْ لَيْلَى الطَّبِيبَةَ وَعَادَتْ لِتُعَلِّمَ أُخْتَهَا هَذِهِ النَّصَائِحَ.|Laila berterima kasih kepada dokter dan pulang untuk mengajarkan nasihat ini kepada adiknya.|لِمَاذَا عَادَتْ لَيْلَى إِلَى أُخْتِهَا؟|لِتُعَلِّمَهَا النَّصَائِحَ|لِتَأْخُذَ طَعَامَهَا|لِتَبِيعَ قُبَّعَتَهَا|لِتَرْسُمَ بَيْتَهَا
''')
reading('istima',7,'Sehari bersama penjelajah','أَنْشِطَتِي الْيَوْمِيَّةُ','forest','Memahami waktu dan urutan aktivitas harian dalam narasi.','Susun jadwal perjalanan dari cerita keseharian Hasan.', '''
أَنَا حَسَنٌ، وَأَسْتَيْقِظُ كُلَّ يَوْمٍ فِي السَّاعَةِ الْخَامِسَةِ صَبَاحًا لِأَبْدَأَ يَوْمِي بِنَشَاطٍ.|Aku Hasan dan bangun setiap hari pukul lima pagi agar memulai hari dengan semangat.|مَتَى يَسْتَيْقِظُ حَسَنٌ؟|فِي الْخَامِسَةِ|فِي السَّادِسَةِ|فِي السَّابِعَةِ|فِي الثَّامِنَةِ
أَغْسِلُ وَجْهِي وَأُصَلِّي، ثُمَّ أُرَتِّبُ سَرِيرِي فِي غُرْفَتِي الصَّغِيرَةِ بِنَفْسِي.|Aku mencuci muka dan salat, lalu merapikan tempat tidur sendiri di kamar kecilku.|مَاذَا يُرَتِّبُ حَسَنٌ؟|سَرِيرَهُ|فَصْلَهُ|حَدِيقَتَهُ|مَكْتَبَةَ الْمَدْرَسَةِ
أَتَنَاوَلُ الْخُبْزَ وَالْبَيْضَ وَأَشْرَبُ الْحَلِيبَ مَعَ أُسْرَتِي فِي السَّادِسَةِ.|Aku makan roti dan telur serta minum susu bersama keluarga pukul enam.|مَاذَا يَشْرَبُ حَسَنٌ فِي الْفُطُورِ؟|الْحَلِيبَ|الْقَهْوَةَ|عَصِيرَ الْعِنَبِ|الشَّايَ
أَذْهَبُ إِلَى الْمَدْرَسَةِ مَاشِيًا مَعَ صَدِيقِي عُمَرَ قَبْلَ السَّاعَةِ السَّابِعَةِ.|Aku berjalan kaki ke sekolah bersama temanku Umar sebelum pukul tujuh.|مَعَ مَنْ يَذْهَبُ إِلَى الْمَدْرَسَةِ؟|عُمَرَ|أَبِيهِ|أُخْتِهِ|جَدِّهِ
فِي الْفُسْحَةِ، أَلْعَبُ كُرَةَ الْقَدَمِ مَعَ زُمَلَائِي فِي مَلْعَبِ الْمَدْرَسَةِ.|Saat istirahat, aku bermain sepak bola bersama teman di lapangan sekolah.|مَاذَا يَفْعَلُ فِي الْفُسْحَةِ؟|يَلْعَبُ كُرَةَ الْقَدَمِ|يَنَامُ|يَطْبُخُ|يَسْبَحُ
أَعُودُ إِلَى الْبَيْتِ ظُهْرًا، وَأَتَنَاوَلُ الْغَدَاءَ مَعَ أُمِّي وَأَخِي الصَّغِيرِ.|Aku pulang siang dan makan bersama ibu dan adik laki-lakiku.|مَتَى يَعُودُ حَسَنٌ إِلَى الْبَيْتِ؟|ظُهْرًا|لَيْلًا|فَجْرًا|قَبْلَ الْفُطُورِ
بَعْدَ رَاحَةٍ قَصِيرَةٍ، أَكْتُبُ وَاجِبَاتِي عَلَى مَكْتَبِي قَبْلَ الْخُرُوجِ إِلَى الْحَدِيقَةِ.|Setelah beristirahat sebentar, aku mengerjakan PR di meja sebelum keluar ke taman.|مَاذَا يَفْعَلُ قَبْلَ الْخُرُوجِ لِلْحَدِيقَةِ؟|يَكْتُبُ وَاجِبَاتِهِ|يَنَامُ|يَتَنَاوَلُ الْعَشَاءَ|يَذْهَبُ لِلسُّوقِ
فِي الْعَصْرِ، أَسْقِي الْأَزْهَارَ وَأُسَاعِدُ أَبِي فِي تَنْظِيفِ حَدِيقَةِ بَيْتِنَا.|Sore hari aku menyiram bunga dan membantu ayah membersihkan taman rumah.|مَنْ يُسَاعِدُ حَسَنٌ فِي الْحَدِيقَةِ؟|أَبَاهُ|مُعَلِّمَهُ|عُمَرَ|جَدَّتَهُ
فِي الْمَسَاءِ، أَقْرَأُ قِصَّةً عَنِ الْبَحْرِ وَالسُّفُنِ لِأَخِي الصَّغِيرِ.|Malam hari aku membacakan cerita tentang laut dan kapal untuk adikku.|عَنْ مَاذَا يَقْرَأُ حَسَنٌ؟|الْبَحْرِ وَالسُّفُنِ|الصَّحْرَاءِ|الْفَضَاءِ|الطَّبْخِ
وَفِي السَّاعَةِ التَّاسِعَةِ لَيْلًا، أَنَامُ مُبَكِّرًا لِأَسْتَعِدَّ لِيَوْمٍ جَدِيدٍ جَمِيلٍ.|Pukul sembilan malam aku tidur lebih awal agar siap menyambut hari baru.|لِمَاذَا يَنَامُ مُبَكِّرًا؟|لِيَسْتَعِدَّ لِيَوْمٍ جَدِيدٍ|لِيَلْعَبَ لَيْلًا|لِيَفُوتَهُ الدَّرْسُ|لِيَذْهَبَ لِلسُّوقِ
''')
reading('istima',8,'Petunjuk desa sungai','الْأَمَاكِنُ وَالِاتِّجَاهَاتُ','forest','Mengikuti petunjuk arah dan mengenali letak tempat dalam desa.','Dengarkan rute menuju rumah penjaga peta tanpa tersesat.', '''
وَقَفَتْ سَارَةُ عِنْدَ مَدْخَلِ الْقَرْيَةِ وَسَأَلَتْ عَنْ طَرِيقِ بَيْتِ حَارِسِ الْخَرِيطَةِ.|Sarah berdiri di pintu masuk desa dan menanyakan jalan ke rumah penjaga peta.|أَيْنَ وَقَفَتْ سَارَةُ أَوَّلًا؟|عِنْدَ مَدْخَلِ الْقَرْيَةِ|فِي الْمَكْتَبَةِ|أَمَامَ الْبَيْتِ|عِنْدَ النَّهْرِ
قَالَ الْخَبَّازُ: اِمْشِي إِلَى الْأَمَامِ حَتَّى تَصِلِي إِلَى الْمَسْجِدِ ذِي الْبَابِ الْأَخْضَرِ.|Pembuat roti berkata: Berjalan lurus sampai masjid berpintu hijau.|إِلَى أَيْنَ تَمْشِي أَوَّلًا؟|إِلَى الْمَسْجِدِ|إِلَى الْجِسْرِ|إِلَى الْمَزْرَعَةِ|إِلَى الْبَحْرِ
الْمَدْرَسَةُ عَلَى يَمِينِ الْمَسْجِدِ، وَفِي سَاحَتِهَا شَجَرَةُ مَانْجُو كَبِيرَةٌ.|Sekolah di kanan masjid, dan di halamannya ada pohon mangga besar.|أَيْنَ الْمَدْرَسَةُ؟|عَلَى يَمِينِ الْمَسْجِدِ|خَلْفَ الْجِسْرِ|أَمَامَ الْبَحْرِ|دَاخِلَ السُّوقِ
وَعَلَى يَسَارِ الْمَسْجِدِ مَكْتَبَةٌ صَغِيرَةٌ تَفْتَحُ أَبْوَابَهَا فِي الصَّبَاحِ.|Di kiri masjid ada perpustakaan kecil yang buka pagi hari.|مَاذَا عَلَى يَسَارِ الْمَسْجِدِ؟|مَكْتَبَةٌ|مَدْرَسَةٌ|مَطْعَمٌ|مُسْتَشْفًى
بَعْدَ الْمَسْجِدِ، اِنْعَطِفِي يَمِينًا وَاسْلُكِي الطَّرِيقَ الْقَصِيرَ الْمُؤَدِّيَ إِلَى النَّهْرِ.|Setelah masjid, belok kanan dan ikuti jalan pendek menuju sungai.|إِلَى أَيِّ جِهَةٍ تَنْعَطِفُ بَعْدَ الْمَسْجِدِ؟|يَمِينًا|يَسَارًا|إِلَى الْخَلْفِ|إِلَى الشَّمَالِ مُبَاشَرَةً
سَتَجِدِينَ مَتْجَرَ الْفَوَاكِهِ أَمَامَ الْجِسْرِ الْخَشَبِيِّ، وَفِيهِ تُفَّاحٌ وَمَوْزٌ.|Kamu akan menemukan toko buah di depan jembatan kayu, berisi apel dan pisang.|أَيْنَ مَتْجَرُ الْفَوَاكِهِ؟|أَمَامَ الْجِسْرِ|خَلْفَ الْمَدْرَسَةِ|بِجَانِبِ الْبَحْرِ|دَاخِلَ الْمَسْجِدِ
اُعْبُرِي الْجِسْرَ بِهُدُوءٍ، وَسَتَرَيْنَ حَدِيقَةً جَمِيلَةً فِيهَا أَزْهَارٌ مُلَوَّنَةٌ.|Seberangi jembatan dengan tenang, dan kamu akan melihat taman berbunga warna-warni.|مَاذَا تَرَى بَعْدَ عُبُورِ الْجِسْرِ؟|حَدِيقَةً|مَطَارًا|مَصْنَعًا|مَلْعَبًا
بَيْتُ الْحَارِسِ خَلْفَ الْحَدِيقَةِ مُبَاشَرَةً، وَلَهُ نَافِذَتَانِ وَبَابٌ بُنِّيٌّ.|Rumah penjaga tepat di belakang taman, berjendela dua dan berpintu cokelat.|أَيْنَ بَيْتُ الْحَارِسِ؟|خَلْفَ الْحَدِيقَةِ|تَحْتَ الْجِسْرِ|دَاخِلَ الْمَدْرَسَةِ|أَمَامَ الْمَسْجِدِ
لَا تَسْلُكِي الطَّرِيقَ الطَّوِيلَ إِلَى الْجَبَلِ، لِأَنَّهُ بَعِيدٌ عَنْ بَيْتِ الْحَارِسِ.|Jangan mengikuti jalan panjang ke gunung karena jauh dari rumah penjaga.|أَيَّ طَرِيقٍ يَجِبُ أَنْ تَتَجَنَّبَ؟|طَرِيقَ الْجَبَلِ|طَرِيقَ النَّهْرِ|الْجِسْرَ|طَرِيقَ الْحَدِيقَةِ
شَكَرَتْ سَارَةُ الْخَبَّازَ، وَاتَّبَعَتِ التَّعْلِيمَاتِ حَتَّى وَصَلَتْ إِلَى الْبَيْتِ بِسَلَامٍ.|Sarah berterima kasih kepada pembuat roti dan mengikuti petunjuk sampai tiba dengan selamat.|لِمَاذَا وَصَلَتْ سَارَةُ بِسَلَامٍ؟|لِأَنَّهَا اتَّبَعَتِ التَّعْلِيمَاتِ|لِأَنَّهَا صَعِدَتِ الْجَبَلَ|لِأَنَّهَا عَادَتْ|لِأَنَّهَا سَبَحَتْ
''')
reading('istima',9,'Pesan dari pasar buah','فِي السُّوقِ','forest','Memahami percakapan belanja, harga, jumlah, dan uang kembalian.','Beli bekal yang tepat untuk ekspedisi berikutnya.', '''
فِي صَبَاحِ الْجُمُعَةِ، ذَهَبَتْ هَنَاءُ مَعَ أَبِيهَا إِلَى سُوقِ الْقَرْيَةِ لِشِرَاءِ الْفَوَاكِهِ.|Jumat pagi Hana pergi bersama ayah ke pasar desa untuk membeli buah.|مَتَى ذَهَبَتْ هَنَاءُ إِلَى السُّوقِ؟|صَبَاحَ الْجُمُعَةِ|مَسَاءَ الْخَمِيسِ|صَبَاحَ الْأَحَدِ|لَيْلَ السَّبْتِ
قَالَتْ لِلْبَائِعِ: السَّلَامُ عَلَيْكُمْ، هَلْ عِنْدَكَ تُفَّاحٌ طَازَجٌ هَذَا الْيَوْمَ؟|Ia berkata kepada penjual: Assalamualaikum, apakah ada apel segar hari ini?|عَنْ أَيِّ فَاكِهَةٍ سَأَلَتْ أَوَّلًا؟|التُّفَّاحِ|الْمَوْزِ|الْعِنَبِ|الْبُرْتُقَالِ
أَجَابَ الْبَائِعُ: نَعَمْ، عِنْدِي تُفَّاحٌ أَحْمَرُ جَمِيلٌ جَاءَ مِنَ الْمَزْرَعَةِ صَبَاحًا.|Penjual menjawab: Ya, ada apel merah indah yang datang dari kebun pagi ini.|مَا لَوْنُ التُّفَّاحِ؟|أَحْمَرُ|أَخْضَرُ|أَصْفَرُ|أَزْرَقُ
سَأَلَتْ هَنَاءُ عَنِ الثَّمَنِ، فَقَالَ: الْكِيلُوغْرَامُ بِعَشَرَةِ رِيَالَاتٍ فَقَطْ.|Hana menanyakan harga, lalu ia menjawab: Satu kilogram sepuluh riyal.|بِكَمْ كِيلُوغْرَامُ التُّفَّاحِ؟|بِعَشَرَةِ رِيَالَاتٍ|بِخَمْسَةٍ|بِثَلَاثَةٍ|بِعِشْرِينَ
طَلَبَتْ هَنَاءُ كِيلُوغْرَامًا وَاحِدًا مِنَ التُّفَّاحِ لِتُشَارِكَهُ مَعَ أُسْرَتِهَا.|Hana meminta satu kilogram apel untuk dibagikan kepada keluarga.|كَمْ كِيلُوغْرَامًا مِنَ التُّفَّاحِ طَلَبَتْ؟|وَاحِدًا|اِثْنَيْنِ|ثَلَاثَةً|أَرْبَعَةً
ثُمَّ قَالَ الْأَبُ: نُرِيدُ أَيْضًا كِيلُوغْرَامًا مِنَ الْمَوْزِ الْأَصْفَرِ النَّاضِجِ.|Ayah lalu berkata: Kami juga ingin satu kilogram pisang kuning matang.|مَاذَا طَلَبَ الْأَبُ؟|الْمَوْزَ|الْعِنَبَ|الْخُبْزَ|الْحَلِيبَ
وَكَانَ ثَمَنُ الْمَوْزِ خَمْسَةَ رِيَالَاتٍ، فَصَارَ الْمَجْمُوعُ خَمْسَةَ عَشَرَ رِيَالًا.|Harga pisang lima riyal, sehingga totalnya lima belas riyal.|كَمِ الْمَجْمُوعُ؟|خَمْسَةَ عَشَرَ|عَشَرَةٌ|عِشْرُونَ|خَمْسَةٌ
أَعْطَى الْأَبُ الْبَائِعَ وَرَقَةً نَقْدِيَّةً قِيمَتُهَا عِشْرُونَ رِيَالًا لِدَفْعِ الثَّمَنِ.|Ayah memberikan uang kertas dua puluh riyal untuk membayar.|كَمْ رِيَالًا أَعْطَى الْأَبُ الْبَائِعَ؟|عِشْرِينَ|عَشَرَةً|خَمْسَةً|ثَلَاثِينَ
أَعَادَ الْبَائِعُ إِلَيْهِ خَمْسَةَ رِيَالَاتٍ، وَوَضَعَ الْفَوَاكِهَ فِي سَلَّةٍ نَظِيفَةٍ.|Penjual mengembalikan lima riyal dan memasukkan buah ke keranjang bersih.|كَمِ الْبَاقِي؟|خَمْسَةُ رِيَالَاتٍ|رِيَالٌ وَاحِدٌ|عَشَرَةٌ|عِشْرُونَ
شَكَرَتْ هَنَاءُ الْبَائِعَ عَلَى مُسَاعَدَتِهِ، وَعَادَتْ مَعَ أَبِيهَا سَعِيدَةً بِالشِّرَاءِ.|Hana berterima kasih atas bantuan penjual lalu pulang bersama ayah dengan gembira.|كَيْفَ كَانَتْ هَنَاءُ عِنْدَ الْعَوْدَةِ؟|سَعِيدَةً|حَزِينَةً|خَائِفَةً|غَاضِبَةً
''')
reading('istima',10,'Gerbang ekspedisi besar','الْمُغَامَرَةُ الْكُبْرَى','forest','Menggabungkan pemahaman instruksi, dialog, waktu, dan tujuan perjalanan.','Dengarkan pesan burung hantu untuk menemukan kunci pulau.', '''
فِي صَبَاحٍ مُشْرِقٍ، اِجْتَمَعَ أَحْمَدُ وَسَلْمَى وَيُوسُفُ عِنْدَ الْجِسْرِ الْقَدِيمِ لِيَبْدَؤُوا مُغَامَرَتَهُمُ الْكُبْرَى.|Pada pagi cerah, Ahmad, Salma, dan Yusuf berkumpul di jembatan tua untuk memulai petualangan besar.|كَمْ مُغَامِرًا اِجْتَمَعَ عِنْدَ الْجِسْرِ؟|ثَلَاثَةٌ|اِثْنَانِ|أَرْبَعَةٌ|خَمْسَةٌ
قَالَتِ الْبُومَةُ الْحَكِيمَةُ لَهُمْ: تَبْدَأُ الرِّحْلَةُ فِي السَّاعَةِ الثَّامِنَةِ، فَاسْتَعِدُّوا وَتَعَاوَنُوا فِي كُلِّ خُطْوَةٍ.|Burung hantu bijak berkata: Perjalanan dimulai pukul delapan, bersiaplah dan bekerja sama di setiap langkah.|مَتَى تَبْدَأُ الرِّحْلَةُ؟|فِي الثَّامِنَةِ|فِي الْخَامِسَةِ|فِي التَّاسِعَةِ|فِي الْعَاشِرَةِ
حَمَلَ أَحْمَدُ الْخَرِيطَةَ، وَحَمَلَتْ سَلْمَى الطَّعَامَ، أَمَّا يُوسُفُ فَحَمَلَ زُجَاجَاتِ الْمَاءِ لِلْجَمِيعِ.|Ahmad membawa peta, Salma membawa makanan, sedangkan Yusuf membawa botol air untuk semua.|مَنْ حَمَلَ الْخَرِيطَةَ؟|أَحْمَدُ|سَلْمَى|يُوسُفُ|الْبُومَةُ
طَلَبَتِ الْبُومَةُ مِنْهُمْ أَنْ يَمْشُوا نَحْوَ الشَّرْقِ حَتَّى يَصِلُوا إِلَى شَجَرَةِ النَّخِيلِ الْعَالِيَةِ.|Burung hantu meminta mereka berjalan ke timur sampai pohon kurma tinggi.|إِلَى أَيِّ جِهَةٍ يَمْشُونَ؟|الشَّرْقِ|الْغَرْبِ|الشَّمَالِ|الْجَنُوبِ
تَحْتَ شَجَرَةِ النَّخِيلِ، وَجَدُوا صُنْدُوقًا أَزْرَقَ صَغِيرًا، وَلَكِنَّهُ كَانَ مُغْلَقًا بِقُفْلٍ قَوِيٍّ.|Di bawah pohon kurma mereka menemukan kotak biru kecil, tetapi terkunci dengan gembok kuat.|مَا لَوْنُ الصُّنْدُوقِ؟|أَزْرَقُ|أَحْمَرُ|أَخْضَرُ|أَصْفَرُ
سَمِعُوا أَرْنَبًا يَقُولُ: الْمِفْتَاحُ الذَّهَبِيُّ خَلْفَ الصَّخْرَةِ الْبَيْضَاءِ، وَلَيْسَ تَحْتَ الْجِسْرِ الْقَدِيمِ.|Mereka mendengar kelinci berkata: Kunci emas di belakang batu putih, bukan di bawah jembatan tua.|أَيْنَ الْمِفْتَاحُ؟|خَلْفَ الصَّخْرَةِ الْبَيْضَاءِ|تَحْتَ الْجِسْرِ|فِي النَّهْرِ|فَوْقَ النَّخْلَةِ
بَحَثَ يُوسُفُ خَلْفَ الصَّخْرَةِ، فَوَجَدَ الْمِفْتَاحَ وَنَادَى صَدِيقَيْهِ لِيَفْتَحُوا الصُّنْدُوقَ مَعًا بِفَرَحٍ.|Yusuf mencari di belakang batu, menemukan kunci, dan memanggil kedua temannya untuk membuka kotak bersama.|مَنْ وَجَدَ الْمِفْتَاحَ؟|يُوسُفُ|أَحْمَدُ|سَلْمَى|الْأَرْنَبُ
دَاخِلَ الصُّنْدُوقِ، وَجَدُوا رِسَالَةً تَدُلُّهُمْ عَلَى الْجَزِيرَةِ، وَثَلَاثَ مِيدَالِيَّاتٍ فِضِّيَّةٍ لِلْمُغَامِرِينَ الثَّلَاثَةِ.|Di dalam kotak ada surat penunjuk pulau dan tiga medali perak untuk ketiga penjelajah.|مَاذَا وَجَدُوا مَعَ الرِّسَالَةِ؟|ثَلَاثَ مِيدَالِيَّاتٍ|أَرْبَعَ كُرَاتٍ|خَمْسَ تُفَّاحَاتٍ|كِتَابًا وَاحِدًا
قَرَؤُوا فِي الرِّسَالَةِ: اِعْبُرُوا النَّهْرَ بِالْقَارِبِ مَعَ الْحَارِسِ، وَلَا تَسْبَحُوا لِأَنَّ الْمَاءَ عَمِيقٌ.|Mereka membaca: Seberangi sungai dengan perahu bersama penjaga, jangan berenang karena airnya dalam.|كَيْفَ يَعْبُرُونَ النَّهْرَ؟|بِالْقَارِبِ مَعَ الْحَارِسِ|بِالسِّبَاحَةِ|بِالْقَفْزِ|بِالسَّيَّارَةِ
شَكَرَ الْأَصْدِقَاءُ الْأَرْنَبَ وَالْبُومَةَ، وَعَرَفُوا أَنَّ التَّعَاوُنَ وَالِاسْتِمَاعَ الْجَيِّدَ يُسَاعِدَانِهِمْ عَلَى النَّجَاحِ.|Mereka berterima kasih kepada kelinci dan burung hantu, serta memahami bahwa kerja sama dan menyimak baik membantu keberhasilan.|مَا سَبَبُ نَجَاحِ الْأَصْدِقَاءِ؟|التَّعَاوُنُ وَالِاسْتِمَاعُ الْجَيِّدُ|السُّرْعَةُ فَقَطْ|الْعَمَلُ وَحْدَهُمْ|تَجَاهُلُ النَّصَائِحِ
''')
reading('qiraah',1,'Kata di kelasku','كَلِمَاتٌ فِي فَصْلِي','castle','Membaca kosakata benda kelas dalam teks pendek.','Baca catatan Rafi untuk menemukan benda pembuka perpustakaan.', '''
هَذَا فَصْلِي، وَهُوَ فَصْلٌ صَغِيرٌ وَنَظِيفٌ فِي مَدْرَسَتِي.|Ini kelasku, kelas yang kecil dan bersih di sekolahku.|كَيْفَ الْفَصْلُ؟|صَغِيرٌ وَنَظِيفٌ|كَبِيرٌ وَمُتَّسِخٌ|قَدِيمٌ وَمُظْلِمٌ|بَعِيدٌ وَمُغْلَقٌ
فِي فَصْلِي بَابٌ وَاحِدٌ، وَنَدْخُلُ مِنْهُ بِهُدُوءٍ.|Di kelasku ada satu pintu, kami masuk melaluinya dengan tenang.|كَمْ بَابًا فِي الْفَصْلِ؟|بَابٌ وَاحِدٌ|بَابَانِ|ثَلَاثَةُ أَبْوَابٍ|أَرْبَعَةُ أَبْوَابٍ
وَفِيهِ نَافِذَتَانِ، وَنَرَى مِنْهُمَا حَدِيقَةَ الْمَدْرَسَةِ الْجَمِيلَةَ.|Ada dua jendela, kami melihat taman sekolah yang indah melaluinya.|مَاذَا نَرَى مِنَ النَّافِذَتَيْنِ؟|حَدِيقَةَ الْمَدْرَسَةِ|السُّوقَ|الْبَحْرَ|الْمَطَارَ
السَّبُّورَةُ أَمَامَ التَّلَامِيذِ، وَيَكْتُبُ عَلَيْهَا الْمُعَلِّمُ.|Papan tulis di depan siswa dan guru menulis di atasnya.|أَيْنَ السَّبُّورَةُ؟|أَمَامَ التَّلَامِيذِ|خَلْفَ الْبَابِ|تَحْتَ الْمَكْتَبِ|فَوْقَ الشَّجَرَةِ
عَلَى مَكْتَبِي كِتَابٌ لِلْقِرَاءَةِ وَدَفْتَرٌ لِلْكِتَابَةِ.|Di mejaku ada buku bacaan dan buku tulis.|مَاذَا عَلَى الْمَكْتَبِ؟|كِتَابٌ وَدَفْتَرٌ|كُرَةٌ وَحِذَاءٌ|طَعَامٌ وَمَاءٌ|زَهْرَةٌ وَحَجَرٌ
قَلَمِي فِي الْمِقْلَمَةِ، وَأَسْتَخْدِمُهُ لِكِتَابَةِ اسْمِي.|Penaku ada di tempat pensil, kugunakan untuk menulis namaku.|أَيْنَ الْقَلَمُ؟|فِي الْمِقْلَمَةِ|تَحْتَ الْكُرْسِيِّ|عَلَى الْبَابِ|فِي الْحَدِيقَةِ
وَحَقِيبَتِي تَحْتَ مَكْتَبِي، وَفِيهَا بَعْضُ الْكُتُبِ.|Tasku di bawah meja, di dalamnya ada beberapa buku.|أَيْنَ الْحَقِيبَةُ؟|تَحْتَ الْمَكْتَبِ|فَوْقَ السَّبُّورَةِ|خَارِجَ الْفَصْلِ|عَلَى النَّافِذَةِ
أَجْلِسُ عَلَى كُرْسِيٍّ بُنِّيٍّ بِجَانِبِ صَدِيقِي.|Aku duduk di kursi cokelat di samping temanku.|مَا لَوْنُ الْكُرْسِيِّ؟|بُنِّيٌّ|أَحْمَرُ|أَخْضَرُ|أَصْفَرُ
وَالْمُعَلِّمُ يَقِفُ قُرْبَ السَّبُّورَةِ وَيَشْرَحُ لَنَا الدَّرْسَ.|Guru berdiri dekat papan tulis dan menjelaskan pelajaran.|مَنْ يَشْرَحُ الدَّرْسَ؟|الْمُعَلِّمُ|الطَّبِيبُ|الْبَائِعُ|الْحَارِسُ
نُرَتِّبُ فَصْلَنَا بَعْدَ الدَّرْسِ لِيَبْقَى نَظِيفًا وَجَمِيلًا.|Kami merapikan kelas setelah pelajaran agar tetap bersih dan indah.|لِمَاذَا نُرَتِّبُ الْفَصْلَ؟|لِيَبْقَى نَظِيفًا|لِنَنَامَ فِيهِ|لِنَبِيعَهُ|لِنُغْلِقَ النَّافِذَةَ
''')
reading('qiraah',2,'Inilah aku','هَذَا أَنَا','castle','Memahami identitas, sekolah, dan kesukaan dalam perkenalan tertulis.','Kenali pemilik kartu penjelajah yang ditemukan Rafi.', '''
اسْمِي فَارِسٌ، وَأَنَا تِلْمِيذٌ فِي مَدْرَسَةِ النُّورِ.|Namaku Faris, aku siswa di Sekolah An-Nur.|مَا اسْمُ التِّلْمِيذِ؟|فَارِسٌ|حَسَنٌ|عُمَرُ|خَالِدٌ
عُمْرِي تِسْعُ سَنَوَاتٍ، وَأَنَا فِي الصَّفِّ الثَّالِثِ.|Usiaku sembilan tahun dan aku duduk di kelas tiga.|كَمْ عُمْرُ فَارِسٍ؟|تِسْعُ سَنَوَاتٍ|سَبْعٌ|ثَمَانٍ|عَشْرٌ
أَسْكُنُ فِي قَرْيَةٍ صَغِيرَةٍ قُرْبَ نَهْرٍ جَمِيلٍ.|Aku tinggal di desa kecil dekat sungai yang indah.|أَيْنَ يَسْكُنُ فَارِسٌ؟|فِي قَرْيَةٍ|فِي جَزِيرَةٍ|فِي مَدِينَةٍ كَبِيرَةٍ|فِي قَلْعَةٍ
أَذْهَبُ إِلَى مَدْرَسَتِي بِالدَّرَّاجَةِ فِي كُلِّ صَبَاحٍ.|Aku pergi ke sekolah dengan sepeda setiap pagi.|كَيْفَ يَذْهَبُ إِلَى الْمَدْرَسَةِ؟|بِالدَّرَّاجَةِ|بِالْحَافِلَةِ|بِالسَّفِينَةِ|مَاشِيًا
لَوْنِيَ الْمُفَضَّلُ أَزْرَقُ، وَحَقِيبَتِي زَرْقَاءُ أَيْضًا.|Warna kesukaanku biru dan tasku juga biru.|مَا لَوْنُهُ الْمُفَضَّلُ؟|أَزْرَقُ|أَحْمَرُ|أَخْضَرُ|أَصْفَرُ
أُحِبُّ الرَّسْمَ، وَأَرْسُمُ الْجِبَالَ فِي وَقْتِ الْفَرَاغِ.|Aku suka menggambar dan menggambar gunung saat senggang.|مَا هِوَايَةُ فَارِسٍ؟|الرَّسْمُ|السِّبَاحَةُ|الطَّبْخُ|الْجَرْيُ
صَدِيقِي اسْمُهُ عَادِلٌ، وَنَجْلِسُ مَعًا فِي الْفَصْلِ.|Temanku bernama Adil, kami duduk bersama di kelas.|مَا اسْمُ صَدِيقِهِ؟|عَادِلٌ|سَامِي|يُوسُفُ|عَلِيٌّ
مَادَّتِيَ الْمُفَضَّلَةُ اللُّغَةُ الْعَرَبِيَّةُ، لِأَنَّنِي أُحِبُّ الْقِصَصَ.|Pelajaran kesukaanku Bahasa Arab karena aku menyukai cerita.|مَا مَادَّتُهُ الْمُفَضَّلَةُ؟|اللُّغَةُ الْعَرَبِيَّةُ|الرِّيَاضِيَّاتُ|الرِّيَاضَةُ|الْعُلُومُ
عِنْدِي أَخٌ وَاحِدٌ صَغِيرٌ، وَأَلْعَبُ مَعَهُ بَعْدَ الدَّرْسِ.|Aku punya seorang adik laki-laki dan bermain dengannya setelah pelajaran.|كَمْ أَخًا عِنْدَهُ؟|أَخٌ وَاحِدٌ|أَخَوَانِ|ثَلَاثَةٌ|أَرْبَعَةٌ
وَأُرِيدُ أَنْ أَكُونَ رَسَّامًا عِنْدَمَا أَكْبَرُ.|Aku ingin menjadi pelukis ketika dewasa.|مَاذَا يُرِيدُ أَنْ يَكُونَ؟|رَسَّامًا|طَبِيبًا|فَلَّاحًا|طَيَّارًا
''')
reading('qiraah',3,'Benda dan warna','أَشْيَاءُ وَأَلْوَانٌ','castle','Membaca deskripsi warna dan letak benda untuk mengidentifikasi barang.','Periksa ruang seni kastil dan temukan benda sesuai petunjuk.', '''
فِي غُرْفَةِ الرَّسْمِ طَاوِلَةٌ كَبِيرَةٌ لَوْنُهَا أَبْيَضُ.|Di ruang menggambar ada meja besar berwarna putih.|مَا لَوْنُ الطَّاوِلَةِ؟|أَبْيَضُ|أَسْوَدُ|أَحْمَرُ|أَزْرَقُ
عَلَى الطَّاوِلَةِ عُلْبَةٌ حَمْرَاءُ فِيهَا أَقْلَامُ التَّلْوِينِ.|Di meja ada kotak merah berisi pensil warna.|مَاذَا فِي الْعُلْبَةِ الْحَمْرَاءِ؟|أَقْلَامُ التَّلْوِينِ|الْأَحْذِيَةُ|الْفَوَاكِهُ|الْكُرَاتُ
وَبِجَانِبِ الْعُلْبَةِ كِتَابٌ أَخْضَرُ عَنِ الْحَدَائِقِ.|Di samping kotak ada buku hijau tentang taman.|مَا لَوْنُ الْكِتَابِ؟|أَخْضَرُ|بُنِّيٌّ|أَصْفَرُ|أَسْوَدُ
تَحْتَ الطَّاوِلَةِ كُرَةٌ صَفْرَاءُ صَغِيرَةٌ لِلَّعِبِ.|Di bawah meja ada bola kuning kecil untuk bermain.|أَيْنَ الْكُرَةُ الصَّفْرَاءُ؟|تَحْتَ الطَّاوِلَةِ|فَوْقَ الْبَابِ|دَاخِلَ الْعُلْبَةِ|خَلْفَ النَّافِذَةِ
وَعَلَى الْجِدَارِ سَاعَةٌ زَرْقَاءُ فَوْقَ السَّبُّورَةِ.|Di dinding ada jam biru di atas papan tulis.|مَا الشَّيْءُ الْأَزْرَقُ عَلَى الْجِدَارِ؟|سَاعَةٌ|حَقِيبَةٌ|قُبَّعَةٌ|زَهْرَةٌ
حَقِيبَةُ سَلْمَى وَرْدِيَّةٌ، وَهِيَ مَوْضُوعَةٌ قُرْبَ الْبَابِ.|Tas Salma merah muda dan diletakkan dekat pintu.|لِمَنْ الْحَقِيبَةُ الْوَرْدِيَّةُ؟|لِسَلْمَى|لِفَارِسٍ|لِلْمُعَلِّمِ|لِعَادِلٍ
أَمَّا حَقِيبَةُ عَادِلٍ فَسَوْدَاءُ، وَهِيَ تَحْتَ كُرْسِيِّهِ.|Tas Adil hitam dan berada di bawah kursinya.|مَا لَوْنُ حَقِيبَةِ عَادِلٍ؟|سَوْدَاءُ|بَيْضَاءُ|خَضْرَاءُ|حَمْرَاءُ
قُرْبَ النَّافِذَةِ إِنَاءٌ بَنَفْسَجِيٌّ فِيهِ زَهْرَةٌ بَيْضَاءُ.|Dekat jendela ada vas ungu dengan bunga putih.|مَا لَوْنُ الْإِنَاءِ؟|بَنَفْسَجِيٌّ|أَبْيَضُ|أَصْفَرُ|بُنِّيٌّ
وَضَعَ الْمُعَلِّمُ وَرَقًا بُرْتُقَالِيًّا أَمَامَ كُلِّ تِلْمِيذٍ.|Guru meletakkan kertas oranye di depan setiap siswa.|مَاذَا وَضَعَ الْمُعَلِّمُ أَمَامَ التَّلَامِيذِ؟|وَرَقًا بُرْتُقَالِيًّا|كُرَاتٍ صَفْرَاءَ|كُتُبًا زَرْقَاءَ|حَقَائِبَ سَوْدَاءَ
قَالَ: رَتِّبُوا الْأَدَوَاتِ بَعْدَ الرَّسْمِ لِنَجِدَهَا بِسُهُولَةٍ.|Ia berkata: Rapikan alat setelah menggambar agar mudah kita temukan.|لِمَاذَا نُرَتِّبُ الْأَدَوَاتِ؟|لِنَجِدَهَا بِسُهُولَةٍ|لِنُخْفِيَهَا دَائِمًا|لِنَكْسِرَهَا|لِنَرْمِيَهَا
''')
reading('qiraah',4,'Keluarga di rumah kebun','أُسْرَتِي الْجَمِيلَةُ','castle','Menemukan hubungan keluarga, pekerjaan, dan kegiatan dalam bacaan.','Baca surat keluarga penjaga perpustakaan.', '''
أَنَا إِبْرَاهِيمُ، وَتَسْكُنُ أُسْرَتِي فِي بَيْتٍ لَهُ حَدِيقَةٌ وَاسِعَةٌ.|Aku Ibrahim dan keluargaku tinggal di rumah yang memiliki taman luas.|مَا اسْمُ صَاحِبِ الْقِصَّةِ؟|إِبْرَاهِيمُ|فَارِسٌ|عُمَرُ|عَادِلٌ
أَبِي مُهَنْدِسٌ، وَيَرْسُمُ خُطَطَ الْبُيُوتِ فِي مَكْتَبِهِ كُلَّ يَوْمٍ.|Ayahku insinyur, ia menggambar rancangan rumah di kantornya setiap hari.|مَا عَمَلُ الْأَبِ؟|مُهَنْدِسٌ|طَبِيبٌ|مُعَلِّمٌ|سَائِقٌ
أُمِّي مُعَلِّمَةٌ، وَتَقْرَأُ مَعَنَا الْكُتُبَ بَعْدَ عَوْدَتِهَا مِنَ الْمَدْرَسَةِ.|Ibuku guru, ia membaca buku bersama kami setelah pulang sekolah.|مَاذَا تَفْعَلُ الْأُمُّ مَعَ الْأَوْلَادِ؟|تَقْرَأُ الْكُتُبَ|تَبْنِي الْبُيُوتَ|تَبِيعُ الْفَوَاكِهَ|تَصْنَعُ الْقَوَارِبَ
أُخْتِي الْكَبِيرَةُ زَيْنَبُ تَدْرُسُ فِي الصَّفِّ السَّادِسِ وَتُحِبُّ الْعُلُومَ.|Kakak perempuanku Zainab belajar di kelas enam dan menyukai sains.|فِي أَيِّ صَفٍّ تَدْرُسُ زَيْنَبُ؟|السَّادِسِ|الْأَوَّلِ|الثَّانِي|الثَّالِثِ
أَخِي الصَّغِيرُ بِلَالٌ يُحِبُّ اللَّعِبَ بِالسَّيَّارَاتِ الصَّغِيرَةِ فِي الْبَيْتِ.|Adik laki-lakiku Bilal suka bermain mobil-mobilan di rumah.|بِمَاذَا يَلْعَبُ بِلَالٌ؟|بِالسَّيَّارَاتِ الصَّغِيرَةِ|بِالطَّائِرَاتِ|بِالْقَوَارِبِ|بِالْكُرَاتِ
يَزُورُنَا جَدِّي يَوْمَ السَّبْتِ وَيَجْلِسُ تَحْتَ شَجَرَةِ اللَّيْمُونِ.|Kakek mengunjungi kami hari Sabtu dan duduk di bawah pohon lemon.|مَتَى يَزُورُهُمُ الْجَدُّ؟|يَوْمَ السَّبْتِ|يَوْمَ الْإِثْنَيْنِ|يَوْمَ الْأَرْبِعَاءِ|يَوْمَ الْجُمُعَةِ
وَتُحْضِرُ جَدَّتِي مَعَهَا خُبْزًا طَازَجًا صَنَعَتْهُ فِي الصَّبَاحِ.|Nenek membawa roti segar yang dibuatnya pagi hari.|مَاذَا تُحْضِرُ الْجَدَّةُ؟|خُبْزًا طَازَجًا|سَمَكًا|حَلِيبًا|أَرُزًّا
فِي الْعُطْلَةِ، نَطْبُخُ الْحَسَاءَ مَعًا وَنُوَزِّعُ الْأَعْمَالَ بَيْنَنَا.|Saat libur kami memasak sup bersama dan membagi pekerjaan.|مَاذَا تَطْبُخُ الْأُسْرَةُ فِي الْعُطْلَةِ؟|الْحَسَاءَ|الْكَعْكَ|الْأَرُزَّ|السَّمَكَ
تَغْسِلُ زَيْنَبُ الْخَضْرَوَاتِ، وَأَنَا أُرَتِّبُ الْمَائِدَةَ قَبْلَ الْغَدَاءِ.|Zainab mencuci sayur, dan aku menata meja sebelum makan siang.|مَنْ يُرَتِّبُ الْمَائِدَةَ؟|إِبْرَاهِيمُ|زَيْنَبُ|بِلَالٌ|الْجَدُّ
نَحْنُ أُسْرَةٌ مُتَعَاوِنَةٌ، وَالْعَمَلُ مَعًا يَجْعَلُنَا سُعَدَاءَ فِي بَيْتِنَا.|Kami keluarga yang bekerja sama, dan bekerja bersama membuat kami bahagia di rumah.|مَا الْفِكْرَةُ الرَّئِيسَةُ؟|التَّعَاوُنُ فِي الْأُسْرَةِ|السَّفَرُ بَعِيدًا|شِرَاءُ سَيَّارَةٍ|بِنَاءُ مَدْرَسَةٍ
''')
reading('qiraah',5,'Ensiklopedia hewan','حَيَوَانَاتٌ مُثِيرَةٌ','castle','Membandingkan ciri dan perilaku hewan dari bacaan informatif.','Temukan halaman ensiklopedia yang cocok dengan jejak misterius.', '''
قَرَأَتْ دِينَا كِتَابًا عَنِ الْحَيَوَانَاتِ فِي مَكْتَبَةِ الْقَلْعَةِ الْكَبِيرَةِ.|Dina membaca buku hewan di perpustakaan kastil besar.|أَيْنَ قَرَأَتْ دِينَا الْكِتَابَ؟|فِي مَكْتَبَةِ الْقَلْعَةِ|فِي السُّوقِ|فِي الْمَطْبَخِ|فِي الْقَارِبِ
قَرَأَتْ أَنَّ الْجَمَلَ يَعِيشُ فِي الصَّحْرَاءِ وَيَتَحَمَّلُ الْعَطَشَ مُدَّةً طَوِيلَةً.|Ia membaca bahwa unta hidup di gurun dan tahan haus cukup lama.|أَيْنَ يَعِيشُ الْجَمَلُ؟|فِي الصَّحْرَاءِ|فِي الْبَحْرِ|فِي الثَّلْجِ|فِي الْبِرْكَةِ
وَأَنَّ السَّمَكَةَ تَعِيشُ فِي الْمَاءِ، وَتَسْبَحُ بِزَعَانِفِهَا لِتَبْحَثَ عَنْ طَعَامِهَا.|Ikan hidup di air dan berenang dengan sirip untuk mencari makanan.|بِمَاذَا تَسْبَحُ السَّمَكَةُ؟|بِزَعَانِفِهَا|بِأَجْنِحَتِهَا|بِقَدَمَيْهَا|بِأُذُنَيْهَا
وَالْبَطْرِيقُ طَائِرٌ، وَلَكِنَّهُ لَا يَطِيرُ، بَلْ يَسْبَحُ بِمَهَارَةٍ فِي الْمَاءِ.|Penguin adalah burung, tetapi tidak terbang; ia berenang dengan terampil.|مَاذَا يَسْتَطِيعُ الْبَطْرِيقُ؟|السِّبَاحَةَ|الطَّيَرَانَ|تَسَلُّقَ النَّخِيلِ|الْعَيْشَ دُونَ مَاءٍ
وَيَحْمِلُ الْكَنْغَرُو صَغِيرَهُ فِي جَيْبٍ عَلَى بَطْنِهِ لِيَحْمِيَهُ مِنَ الْخَطَرِ.|Kanguru membawa anaknya dalam kantong di perut untuk melindunginya dari bahaya.|أَيْنَ يَحْمِلُ الْكَنْغَرُو صَغِيرَهُ؟|فِي جَيْبٍ عَلَى بَطْنِهِ|عَلَى رَأْسِهِ|فِي عُشٍّ|عَلَى ظَهْرِ سَمَكَةٍ
وَتَصْنَعُ النَّحْلَةُ الْعَسَلَ، وَتَطِيرُ بَيْنَ الْأَزْهَارِ لِتَجْمَعَ الرَّحِيقَ.|Lebah membuat madu dan terbang di antara bunga untuk mengumpulkan nektar.|مَاذَا تَجْمَعُ النَّحْلَةُ؟|الرَّحِيقَ|الرَّمْلَ|الْحَجَرَ|الْخَشَبَ
وَتَحْمِلُ السُّلَحْفَاةُ دِرْعًا صُلْبًا عَلَى ظَهْرِهَا يُسَاعِدُهَا عَلَى حِمَايَةِ جِسْمِهَا.|Kura-kura membawa tempurung keras di punggung untuk membantu melindungi tubuhnya.|مَا فَائِدَةُ دِرْعِ السُّلَحْفَاةِ؟|حِمَايَةُ جِسْمِهَا|مُسَاعَدَتُهَا عَلَى الطَّيَرَانِ|جَمْعُ الرَّحِيقِ|حَمْلُ الْمَاءِ
وَالْخُفَّاشُ يَخْرُجُ لَيْلًا لِيَبْحَثَ عَنْ طَعَامِهِ، وَيَسْتَرِيحُ فِي النَّهَارِ.|Kelelawar keluar malam mencari makanan dan beristirahat siang hari.|مَتَى يَخْرُجُ الْخُفَّاشُ؟|لَيْلًا|ظُهْرًا|فِي الصَّبَاحِ فَقَطْ|بَعْدَ الْفَجْرِ فَقَطْ
وَعَرَفَتْ دِينَا أَنَّ لِكُلِّ حَيَوَانٍ صِفَاتٍ تُسَاعِدُهُ عَلَى الْعَيْشِ فِي بِيئَتِهِ.|Dina memahami bahwa setiap hewan memiliki ciri yang membantu hidup di lingkungannya.|مَاذَا تُسَاعِدُ صِفَاتُ الْحَيَوَانِ؟|الْعَيْشَ فِي بِيئَتِهِ|قِرَاءَةَ الْكُتُبِ|بِنَاءَ الْمَدَارِسِ|قِيَادَةَ السَّيَّارَةِ
أَغْلَقَتْ دِينَا الْكِتَابَ وَقَرَّرَتْ أَنْ تَحْتَرِمَ الْحَيَوَانَاتِ وَتُحَافِظَ عَلَى أَمَاكِنِهَا.|Dina menutup buku dan memutuskan menghormati hewan serta menjaga habitatnya.|مَاذَا قَرَّرَتْ دِينَا؟|الْمُحَافَظَةَ عَلَى أَمَاكِنِ الْحَيَوَانَاتِ|تَخْرِيبَ الْأَعْشَاشِ|صَيْدَ كُلِّ الْحَيَوَانَاتِ|تَرْكَ الْكِتَابِ مَفْتُوحًا
''')
reading('qiraah',6,'Sehari dalam hidupku','يَوْمٌ فِي حَيَاتِي','castle','Memahami urutan kegiatan dan hubungan waktu dalam catatan harian.','Baca buku harian penjaga muda untuk mengetahui jadwal pertemuan.', '''
اِسْتَيْقَظَتْ رَانِيَا يَوْمَ الْأَحَدِ مُبَكِّرًا لِتَسْتَعِدَّ لِرِحْلَةٍ مَدْرَسِيَّةٍ إِلَى الْمَتْحَفِ.|Rania bangun pagi pada hari Minggu untuk bersiap mengikuti kunjungan sekolah ke museum.|إِلَى أَيْنَ سَتَذْهَبُ رَانِيَا؟|الْمَتْحَفِ|الْمَطَارِ|الشَّاطِئِ|الْمَزْرَعَةِ
غَسَلَتْ وَجْهَهَا، ثُمَّ تَنَاوَلَتْ فُطُورًا بَسِيطًا مِنَ الْخُبْزِ وَالْجُبْنِ مَعَ أُسْرَتِهَا.|Ia mencuci muka lalu sarapan sederhana roti dan keju bersama keluarga.|مَاذَا أَكَلَتْ فِي الْفُطُورِ؟|الْخُبْزَ وَالْجُبْنَ|السَّمَكَ|الْأَرُزَّ|الْحَسَاءَ
وَضَعَتْ فِي حَقِيبَتِهَا دَفْتَرًا وَقَلَمًا وَزُجَاجَةَ مَاءٍ قَبْلَ الْخُرُوجِ مِنَ الْبَيْتِ.|Ia memasukkan buku tulis, pena, dan botol air ke tas sebelum keluar rumah.|مَاذَا وَضَعَتْ مَعَ الدَّفْتَرِ وَالْقَلَمِ؟|زُجَاجَةَ مَاءٍ|كُرَةً|حِذَاءً|وِسَادَةً
اِنْطَلَقَتِ الْحَافِلَةُ مِنَ الْمَدْرَسَةِ فِي السَّاعَةِ الثَّامِنَةِ وَكَانَ الْجَمِيعُ سُعَدَاءَ.|Bus berangkat dari sekolah pukul delapan dan semua bergembira.|مَتَى اِنْطَلَقَتِ الْحَافِلَةُ؟|فِي الثَّامِنَةِ|فِي السَّابِعَةِ|فِي التَّاسِعَةِ|فِي الْعَاشِرَةِ
عِنْدَ الْوُصُولِ، شَاهَدَتْ رَانِيَا سَاعَةً قَدِيمَةً وَأَوَانِيَ جَمِيلَةً مِنَ الْفَخَّارِ.|Saat tiba, Rania melihat jam tua dan peralatan tembikar yang indah.|مَاذَا شَاهَدَتْ فِي الْمَتْحَفِ؟|سَاعَةً قَدِيمَةً|أَسَدًا|طَائِرَةً حَدِيثَةً|شَجَرَةَ مَوْزٍ
شَرَحَ الدَّلِيلُ لِلتَّلَامِيذِ كَيْفَ كَانَ النَّاسُ يَسْتَخْدِمُونَ الْأَوَانِيَ فِي الْمَاضِي.|Pemandu menjelaskan bagaimana orang menggunakan peralatan tersebut pada masa lalu.|مَنْ شَرَحَ لِلتَّلَامِيذِ؟|الدَّلِيلُ|السَّائِقُ|الطَّبِيبُ|الْبَائِعُ
فِي الظُّهْرِ، جَلَسَ التَّلَامِيذُ فِي الْحَدِيقَةِ وَتَنَاوَلُوا طَعَامَهُمْ تَحْتَ شَجَرَةٍ.|Siang hari para siswa duduk di taman dan makan di bawah pohon.|أَيْنَ تَنَاوَلُوا الطَّعَامَ؟|فِي الْحَدِيقَةِ|فِي الْحَافِلَةِ|فِي الْفَصْلِ|فِي الْبَيْتِ
بَعْدَ الْغَدَاءِ، رَسَمَتْ رَانِيَا إِنَاءً قَدِيمًا فِي دَفْتَرِهَا لِتَتَذَكَّرَ شَكْلَهُ.|Setelah makan, Rania menggambar bejana tua di buku agar mengingat bentuknya.|لِمَاذَا رَسَمَتِ الْإِنَاءَ؟|لِتَتَذَكَّرَ شَكْلَهُ|لِتَبِيعَهُ|لِتَكْسِرَهُ|لِتُغَيِّرَ لَوْنَهُ
عَادَتْ إِلَى بَيْتِهَا فِي الْعَصْرِ وَحَكَتْ لِأَبِيهَا عَنْ رِحْلَتِهَا الْمُمْتِعَةِ.|Ia pulang sore dan menceritakan perjalanan menyenangkan kepada ayah.|لِمَنْ حَكَتْ عَنِ الرِّحْلَةِ؟|لِأَبِيهَا|لِجَدَّتِهَا|لِلْبَائِعِ|لِلطَّبِيبِ
وَفِي اللَّيْلِ، كَتَبَتْ أَنَّ الْمَتْحَفَ يُعَلِّمُنَا كَيْفَ عَاشَ النَّاسُ قَدِيمًا.|Malam hari ia menulis bahwa museum mengajarkan bagaimana orang hidup dahulu.|مَاذَا نَتَعَلَّمُ مِنَ الْمَتْحَفِ؟|حَيَاةَ النَّاسِ قَدِيمًا|صُنْعَ الْهَوَاتِفِ فَقَطْ|السِّبَاحَةَ|قِيَادَةَ الْحَافِلَةِ
''')
reading('qiraah',7,'Pengumuman sekolah','فِي الْمَدْرَسَةِ','castle','Menemukan jadwal, syarat, dan instruksi dari pengumuman sederhana.','Baca pengumuman untuk mengikuti misi hari membaca.', '''
أَعْلَنَتْ مَدْرَسَةُ الْأَمَلِ عَنْ يَوْمِ الْقِرَاءَةِ، وَدَعَتْ تَلَامِيذَ الصُّفُوفِ الثَّالِثِ وَالرَّابِعِ وَالْخَامِسِ لِلْمُشَارَكَةِ.|Sekolah Al-Amal mengumumkan hari membaca dan mengundang siswa kelas tiga, empat, dan lima.|مَا اسْمُ الْمَدْرَسَةِ؟|الْأَمَلُ|النُّورُ|السَّلَامُ|الْفَجْرُ
سَيَكُونُ النَّشَاطُ يَوْمَ الْأَرْبِعَاءِ، وَيَبْدَأُ فِي السَّاعَةِ التَّاسِعَةِ صَبَاحًا بَعْدَ الدَّرْسِ الْأَوَّلِ.|Kegiatan berlangsung hari Rabu dan dimulai pukul sembilan pagi setelah pelajaran pertama.|فِي أَيِّ يَوْمٍ يَكُونُ النَّشَاطُ؟|الْأَرْبِعَاءِ|السَّبْتِ|الْإِثْنَيْنِ|الْجُمُعَةِ
يَجْتَمِعُ الْمُشَارِكُونَ فِي الْمَكْتَبَةِ الْجَدِيدَةِ، وَلَيْسَ فِي الْمَلْعَبِ، لِأَنَّ فِيهَا كُتُبًا كَثِيرَةً.|Peserta berkumpul di perpustakaan baru, bukan lapangan, karena ada banyak buku di sana.|أَيْنَ يَجْتَمِعُ الْمُشَارِكُونَ؟|فِي الْمَكْتَبَةِ الْجَدِيدَةِ|فِي الْمَلْعَبِ|فِي الْمَطْبَخِ|فِي الْحَافِلَةِ
عَلَى كُلِّ تِلْمِيذٍ أَنْ يُحْضِرَ قَلَمًا وَدَفْتَرًا لِيَكْتُبَ عُنْوَانَ الْقِصَّةِ وَأَسْمَاءَ شَخْصِيَّاتِهَا.|Setiap siswa membawa pena dan buku tulis untuk menulis judul cerita dan nama tokoh.|مَاذَا يَجِبُ أَنْ يُحْضِرَ التِّلْمِيذُ؟|قَلَمًا وَدَفْتَرًا|كُرَةً وَحِذَاءً|طَعَامًا لِلْبَيْعِ|قُبَّعَةً وَمِظَلَّةً
يَخْتَارُ كُلُّ مُشَارِكٍ قِصَّةً وَاحِدَةً مِنَ الرَّفِّ الْأَخْضَرِ الْمُخَصَّصِ لِقِصَصِ الْأَطْفَالِ.|Setiap peserta memilih satu cerita dari rak hijau khusus cerita anak.|مِنْ أَيِّ رَفٍّ يَخْتَارُ الْقِصَّةَ؟|الْأَخْضَرِ|الْأَحْمَرِ|الْأَزْرَقِ|الْأَسْوَدِ
يَقْرَأُ التَّلَامِيذُ بِهُدُوءٍ مُدَّةَ ثَلَاثِينَ دَقِيقَةً، ثُمَّ يَتَحَدَّثُونَ عَنِ الشَّخْصِيَّاتِ فِي مَجْمُوعَاتٍ صَغِيرَةٍ.|Siswa membaca tenang selama tiga puluh menit lalu membahas tokoh dalam kelompok kecil.|كَمْ دَقِيقَةً يَقْرَؤُونَ؟|ثَلَاثِينَ|عَشْرًا|عِشْرِينَ|سِتِّينَ
بَعْدَ الْمُنَاقَشَةِ، يَرْسُمُ كُلُّ تِلْمِيذٍ شَخْصِيَّتَهُ الْمُفَضَّلَةَ وَيَشْرَحُ لِزَمِيلِهِ سَبَبَ اِخْتِيَارِهَا.|Setelah diskusi setiap siswa menggambar tokoh favorit dan menjelaskan alasan pilihannya kepada teman.|مَاذَا يَفْعَلُونَ بَعْدَ الْمُنَاقَشَةِ؟|يَرْسُمُونَ شَخْصِيَّةً|يَلْعَبُونَ فِي الشَّارِعِ|يَنَامُونَ|يَعُودُونَ مُبَاشَرَةً
يُرْجَى عَدَمُ إِحْضَارِ الطَّعَامِ إِلَى الْمَكْتَبَةِ لِلْمُحَافَظَةِ عَلَى نَظَافَةِ الْكُتُبِ وَالطَّاوِلَاتِ.|Harap tidak membawa makanan ke perpustakaan untuk menjaga kebersihan buku dan meja.|لِمَاذَا يُمْنَعُ الطَّعَامُ؟|لِلْمُحَافَظَةِ عَلَى النَّظَافَةِ|لِأَنَّ الْكُتُبَ قَلِيلَةٌ|لِأَنَّ النَّشَاطَ لَيْلًا|لِأَنَّ الْمَلْعَبَ مُغْلَقٌ
يَنْتَهِي النَّشَاطُ فِي السَّاعَةِ الْحَادِيَةَ عَشْرَةَ، وَتُقَدِّمُ الْمُعَلِّمَةُ بِطَاقَةَ مُشَارَكَةٍ لِكُلِّ تِلْمِيذٍ.|Kegiatan berakhir pukul sebelas dan guru memberi kartu partisipasi kepada setiap siswa.|مَتَى يَنْتَهِي النَّشَاطُ؟|فِي الْحَادِيَةَ عَشْرَةَ|فِي التَّاسِعَةِ|فِي الْوَاحِدَةِ|فِي الثَّامِنَةِ
لِلتَّسْجِيلِ، يَذْهَبُ التِّلْمِيذُ إِلَى مُعَلِّمِ صَفِّهِ قَبْلَ يَوْمِ الثُّلَاثَاءِ لِيَكْتُبَ اسْمَهُ فِي الْقَائِمَةِ.|Untuk mendaftar, siswa menemui wali kelas sebelum hari Selasa agar namanya dicatat dalam daftar.|مَنْ يُسَجِّلُ أَسْمَاءَ التَّلَامِيذِ؟|مُعَلِّمُ الصَّفِّ|سَائِقُ الْحَافِلَةِ|الطَّبِيبُ|بَائِعُ الْكُتُبِ
''')
reading('qiraah',8,'Petunjuk kota','دَلِيلُ الْمَدِينَةِ','castle','Memahami letak fasilitas dan memilih rute dari petunjuk tertulis.','Temukan jalur dari stasiun menuju menara pengetahuan.', '''
أَهْلًا بِكَ فِي مَدِينَةِ الْعِلْمِ، حَيْثُ تَقَعُ مَحَطَّةُ الْحَافِلَاتِ فِي الْجَنُوبِ قُرْبَ مَدْخَلِ الْمَدِينَةِ.|Selamat datang di Kota Ilmu, stasiun bus terletak di selatan dekat pintu masuk kota.|أَيْنَ مَحَطَّةُ الْحَافِلَاتِ؟|فِي الْجَنُوبِ|فِي الشَّمَالِ|فِي الشَّرْقِ|فِي الْغَرْبِ
مِنَ الْمَحَطَّةِ، سِرْ شَمَالًا فِي شَارِعِ النُّورِ حَتَّى تَصِلَ إِلَى السَّاحَةِ الَّتِي فِيهَا نَافُورَةٌ كَبِيرَةٌ.|Dari stasiun berjalan ke utara melalui Jalan An-Nur sampai alun-alun berair mancur besar.|مَا اسْمُ الشَّارِعِ؟|النُّورُ|الْبَحْرُ|الْحَدِيقَةُ|الْجَبَلُ
تَقَعُ الْمَكْتَبَةُ الْعَامَّةُ شَرْقَ السَّاحَةِ، وَتَفْتَحُ أَبْوَابَهَا مِنَ الثَّامِنَةِ صَبَاحًا إِلَى الرَّابِعَةِ عَصْرًا.|Perpustakaan umum di timur alun-alun dan buka pukul delapan pagi sampai empat sore.|أَيْنَ الْمَكْتَبَةُ بِالنِّسْبَةِ إِلَى السَّاحَةِ؟|شَرْقَهَا|غَرْبَهَا|جَنُوبَهَا|تَحْتَهَا
أَمَّا الْمُسْتَشْفَى فَيَقَعُ غَرْبَ السَّاحَةِ، وَيُوجَدُ عَلَى بَابِهِ رَسْمُ هِلَالٍ أَحْمَرَ وَاضِحٍ.|Rumah sakit di barat alun-alun dan pintunya memiliki gambar bulan sabit merah yang jelas.|مَاذَا يَقَعُ غَرْبَ السَّاحَةِ؟|الْمُسْتَشْفَى|الْمَكْتَبَةُ|الْمَتْحَفُ|الْبُرْجُ
بِجَانِبِ الْمَكْتَبَةِ مَخْبَزٌ صَغِيرٌ يَبِيعُ الْخُبْزَ الطَّازَجَ، وَخَلْفَهُ حَدِيقَةٌ لِلْأَطْفَالِ.|Di samping perpustakaan ada toko roti segar kecil dan di belakangnya taman anak.|مَاذَا يَبِيعُ الْمَخْبَزُ؟|الْخُبْزَ الطَّازَجَ|الْأَدْوِيَةَ|الْأَحْذِيَةَ|الْكُتُبَ
لِلْوُصُولِ إِلَى الْمَتْحَفِ، اِسْتَمِرَّ شَمَالًا مِنَ السَّاحَةِ، ثُمَّ اِنْعَطِفْ يَسَارًا عِنْدَ الْمَدْرَسَةِ.|Untuk ke museum, terus ke utara dari alun-alun lalu belok kiri di sekolah.|أَيْنَ تَنْعَطِفُ لِلْوُصُولِ إِلَى الْمَتْحَفِ؟|يَسَارًا عِنْدَ الْمَدْرَسَةِ|يَمِينًا عِنْدَ الْمَحَطَّةِ|جَنُوبًا عِنْدَ الْمَخْبَزِ|غَرْبًا عِنْدَ الْحَدِيقَةِ
بُرْجُ الْمَعْرِفَةِ أَمَامَ الْمَتْحَفِ، وَمِنْ أَعْلَاهُ يَسْتَطِيعُ الزَّائِرُ رُؤْيَةَ الْمَدِينَةِ كُلِّهَا.|Menara Pengetahuan di depan museum, dari atasnya pengunjung dapat melihat seluruh kota.|أَيْنَ بُرْجُ الْمَعْرِفَةِ؟|أَمَامَ الْمَتْحَفِ|خَلْفَ الْمَحَطَّةِ|دَاخِلَ الْمُسْتَشْفَى|تَحْتَ النَّافُورَةِ
يُغْلَقُ الطَّرِيقُ بَيْنَ الْمُسْتَشْفَى وَالْمَتْحَفِ هَذَا الْأُسْبُوعَ بِسَبَبِ أَعْمَالِ تَصْلِيحِ الشَّارِعِ.|Jalan antara rumah sakit dan museum ditutup minggu ini karena perbaikan.|لِمَاذَا أُغْلِقَ الطَّرِيقُ؟|بِسَبَبِ التَّصْلِيحِ|بِسَبَبِ الثَّلْجِ|بِسَبَبِ السُّوقِ|بِسَبَبِ اللَّيْلِ
لِذَلِكَ يَسْتَخْدِمُ الزَّائِرُ طَرِيقَ الْمَدْرَسَةِ لِيَصِلَ إِلَى الْمَتْحَفِ وَالْبُرْجِ بِأَمَانٍ وَسُهُولَةٍ.|Karena itu pengunjung menggunakan rute sekolah agar sampai ke museum dan menara dengan aman dan mudah.|أَيَّ طَرِيقٍ يَسْتَخْدِمُ الزَّائِرُ؟|طَرِيقَ الْمَدْرَسَةِ|الطَّرِيقَ الْمُغْلَقَ|طَرِيقَ الْبَحْرِ|طَرِيقَ الْجَبَلِ
وَعَلَى الزَّائِرِ أَنْ يَعْبُرَ الشَّارِعَ مِنْ مَمَرِّ الْمُشَاةِ، وَيَنْتَظِرَ الْإِشَارَةَ الْخَضْرَاءَ قَبْلَ الْعُبُورِ.|Pengunjung harus menyeberang di penyeberangan pejalan kaki dan menunggu lampu hijau.|مَتَى يَعْبُرُ الزَّائِرُ؟|عِنْدَ الْإِشَارَةِ الْخَضْرَاءِ|عِنْدَ الْإِشَارَةِ الْحَمْرَاءِ|دُونَ انْتِظَارٍ|عِنْدَ إِغْلَاقِ الْمَمَرِّ
''')
reading('qiraah',9,'Dompet di pasar','قِصَّةٌ فِي السُّوقِ','castle','Memahami masalah, tindakan, dan pesan moral cerita pendek.','Bantu Rafi memecahkan kisah dompet yang ditemukan di pasar.', '''
ذَهَبَ مَازِنٌ مَعَ أُمِّهِ إِلَى السُّوقِ يَوْمَ السَّبْتِ لِشِرَاءِ الْخَضْرَوَاتِ وَبَعْضِ الْفَوَاكِهِ لِلْبَيْتِ.|Mazin pergi ke pasar bersama ibu pada Sabtu untuk membeli sayur dan buah bagi keluarga.|مَعَ مَنْ ذَهَبَ مَازِنٌ؟|أُمِّهِ|أَبِيهِ|أَخِيهِ|جَدِّهِ
عِنْدَ مَتْجَرِ الطَّمَاطِمِ، رَأَى مَحْفَظَةً بُنِّيَّةً صَغِيرَةً عَلَى الْأَرْضِ بِجَانِبِ سَلَّةٍ فَارِغَةٍ.|Di toko tomat ia melihat dompet cokelat kecil di tanah dekat keranjang kosong.|مَاذَا وَجَدَ مَازِنٌ؟|مَحْفَظَةً|سَاعَةً|قَلَمًا|حَقِيبَةً كَبِيرَةً
أَخَذَ مَازِنٌ الْمَحْفَظَةَ وَأَعْطَاهَا لِأُمِّهِ، وَلَمْ يَأْخُذْ شَيْئًا مِنَ النُّقُودِ الَّتِي فِيهَا.|Mazin mengambil dompet dan menyerahkannya kepada ibu tanpa mengambil uang di dalamnya.|لِمَنْ أَعْطَى الْمَحْفَظَةَ؟|لِأُمِّهِ|لِصَدِيقِهِ|لِأَخِيهِ|لِطِفْلٍ
قَالَتِ الْأُمُّ: يَجِبُ أَنْ نَبْحَثَ عَنْ صَاحِبِهَا، لِأَنَّ رَدَّ الْأَمَانَةِ عَمَلٌ حَسَنٌ.|Ibu berkata: Kita harus mencari pemiliknya karena mengembalikan amanah adalah perbuatan baik.|مَاذَا طَلَبَتِ الْأُمُّ؟|الْبَحْثَ عَنْ صَاحِبِهَا|إِخْفَاءَهَا|شِرَاءَ حَلْوَى بِهَا|رَمْيَهَا
ذَهَبَا إِلَى حَارِسِ السُّوقِ وَأَخْبَرَاهُ بِمَكَانِ الْعُثُورِ عَلَى الْمَحْفَظَةِ وَوَقْتِ الْعُثُورِ عَلَيْهَا.|Mereka pergi ke penjaga pasar dan memberi tahu tempat serta waktu penemuan dompet.|إِلَى مَنْ ذَهَبَا؟|حَارِسِ السُّوقِ|طَبِيبِ الْقَرْيَةِ|مُعَلِّمِ الْفَصْلِ|سَائِقِ الْحَافِلَةِ
بَعْدَ قَلِيلٍ، جَاءَ رَجُلٌ كَبِيرٌ يَبْحَثُ عَنْ مَحْفَظَتِهِ، وَبَدَا عَلَيْهِ الْقَلَقُ وَالْحُزْنُ.|Tak lama seorang pria tua datang mencari dompet, ia tampak khawatir dan sedih.|كَيْفَ بَدَا الرَّجُلُ؟|قَلِقًا وَحَزِينًا|ضَاحِكًا|غَاضِبًا مِنْ مَازِنٍ|نَائِمًا
سَأَلَهُ الْحَارِسُ عَنْ لَوْنِ الْمَحْفَظَةِ وَمَا فِيهَا، فَوَصَفَهَا الرَّجُلُ وَصْفًا صَحِيحًا وَوَاضِحًا.|Penjaga menanyakan warna dan isi dompet, dan pria itu menjelaskannya dengan benar dan jelas.|كَيْفَ تَأَكَّدَ الْحَارِسُ مِنَ الْمَالِكِ؟|بِسُؤَالِهِ عَنْ وَصْفِهَا|بِسُؤَالِهِ عَنْ طَعَامِهِ|بِرُؤْيَةِ حِذَائِهِ|بِعَدِّ أَصْدِقَائِهِ
أَعَادَ الْحَارِسُ الْمَحْفَظَةَ إِلَى الرَّجُلِ، وَأَخْبَرَهُ أَنَّ مَازِنًا هُوَ الَّذِي وَجَدَهَا.|Penjaga mengembalikan dompet kepada pria itu dan memberi tahu bahwa Mazin yang menemukannya.|مَنْ أَعَادَ الْمَحْفَظَةَ إِلَى الرَّجُلِ؟|الْحَارِسُ|الْبَائِعُ|السَّائِقُ|الْمُعَلِّمُ
شَكَرَ الرَّجُلُ مَازِنًا، وَقَالَ لَهُ: أَنْتَ طِفْلٌ أَمِينٌ، وَأَنَا سَعِيدٌ بِعَمَلِكَ الْجَمِيلِ.|Pria itu berterima kasih kepada Mazin dan berkata: Kamu anak jujur, aku senang dengan perbuatan baikmu.|بِأَيِّ صِفَةٍ وَصَفَ الرَّجُلُ مَازِنًا؟|أَمِينٌ|كَسُولٌ|مُهْمِلٌ|غَاضِبٌ
عَادَ مَازِنٌ إِلَى الْبَيْتِ فَرِحًا، وَعَرَفَ أَنَّ مُسَاعَدَةَ النَّاسِ أَثْمَنُ مِنْ أَيِّ مُكَافَأَةٍ.|Mazin pulang gembira dan memahami bahwa membantu orang lebih berharga daripada hadiah apa pun.|مَا دَرْسُ الْقِصَّةِ؟|الْأَمَانَةُ وَمُسَاعَدَةُ النَّاسِ|أَخْذُ نُقُودِ الْغَيْرِ|تَجَاهُلُ الْمُحْتَاجِ|إِخْفَاءُ الْأَشْيَاءِ
''')
reading('qiraah',10,'Rahasia harta yang hilang','سِرُّ الْكَنْزِ الْمَفْقُودِ','castle','Menggabungkan petunjuk, urutan peristiwa, dan simpulan makna harta.','Baca gulungan terakhir untuk membuka peti pengetahuan.', '''
وَصَلَتْ لَيْنَا وَصَدِيقُهَا نَادِرٌ إِلَى جَزِيرَةِ الْمَعْرِفَةِ بِقَارِبٍ صَغِيرٍ مَعَ حَارِسٍ حَكِيمٍ بَعْدَ رِحْلَةٍ طَوِيلَةٍ.|Lina dan Nadir tiba di Pulau Pengetahuan dengan perahu kecil bersama penjaga bijak setelah perjalanan panjang.|كَيْفَ وَصَلَا إِلَى الْجَزِيرَةِ؟|بِقَارِبٍ|بِطَائِرَةٍ|بِسَيَّارَةٍ|بِدَرَّاجَةٍ
كَانَ مَعَهُمَا نِصْفُ خَرِيطَةٍ قَدِيمَةٍ، فَبَحَثَا عَنِ النِّصْفِ الْآخَرِ لِيَعْرِفَا مَكَانَ الْكَنْزِ الْمَفْقُودِ بِدِقَّةٍ.|Mereka membawa separuh peta tua dan mencari separuh lainnya agar mengetahui lokasi harta dengan tepat.|مَاذَا كَانَ يَنْقُصُهُمَا؟|نِصْفُ الْخَرِيطَةِ|قَارِبٌ|حَارِسٌ|حَقِيبَةُ طَعَامٍ
قَرَآ لَافِتَةً عِنْدَ الشَّاطِئِ تَقُولُ: اِذْهَبَا إِلَى الْمَكْتَبَةِ الْحَجَرِيَّةِ، فَفِيهَا الْجَوَابُ الَّذِي تَبْحَثَانِ عَنْهُ.|Mereka membaca papan di pantai: Pergilah ke perpustakaan batu, di sana jawaban yang kalian cari.|إِلَى أَيْنَ تُرْشِدُهُمَا اللَّافِتَةُ؟|الْمَكْتَبَةِ الْحَجَرِيَّةِ|الْجَبَلِ|الْمَطَارِ|السُّوقِ
فِي الْمَكْتَبَةِ، وَجَدَ نَادِرٌ صُنْدُوقًا تَحْتَ طَاوِلَةٍ، وَفِيهِ النِّصْفُ الثَّانِي مِنَ الْخَرِيطَةِ الْقَدِيمَةِ.|Di perpustakaan Nadir menemukan kotak di bawah meja yang berisi separuh peta kedua.|مَنْ وَجَدَ النِّصْفَ الثَّانِي؟|نَادِرٌ|لَيْنَا|الْحَارِسُ|الْبَائِعُ
جَمَعَا النِّصْفَيْنِ، فَظَهَرَ طَرِيقٌ يَمْرُّ بِالْحَدِيقَةِ ثُمَّ يَصِلُ إِلَى قَلْعَةٍ صَغِيرَةٍ فِي شَمَالِ الْجَزِيرَةِ.|Mereka menyatukan peta; terlihat jalan melalui taman lalu ke kastil kecil di utara pulau.|أَيْنَ تَقَعُ الْقَلْعَةُ؟|فِي شَمَالِ الْجَزِيرَةِ|فِي جَنُوبِهَا|تَحْتَ الْبَحْرِ|فِي وَسَطِ السُّوقِ
أَمَامَ بَابِ الْقَلْعَةِ، قَرَأَتْ لَيْنَا لُغْزًا: أَنَا أُعَلِّمُكَ دُونَ أَنْ أَتَكَلَّمَ، وَصَفَحَاتِي تَحْمِلُ الْقِصَصَ.|Di pintu kastil Lina membaca teka-teki: Aku mengajar tanpa berbicara dan halaman-halamanku membawa cerita.|مَا حَلُّ اللُّغْزِ؟|الْكِتَابُ|الْحَجَرُ|الْقَارِبُ|الْحِذَاءُ
قَالَتْ لَيْنَا: الْجَوَابُ هُوَ الْكِتَابُ، فَأَعْطَاهُمَا الْحَارِسُ مِفْتَاحًا فِضِّيًّا لِفَتْحِ بَابِ الْقَلْعَةِ الثَّقِيلِ.|Lina menjawab buku, lalu penjaga memberi kunci perak untuk membuka pintu kastil berat.|مَا لَوْنُ الْمِفْتَاحِ؟|فِضِّيٌّ|ذَهَبِيٌّ|أَحْمَرُ|أَسْوَدُ
دَاخِلَ الْقَلْعَةِ، وَجَدَا رُفُوفًا مَلِيئَةً بِالْكُتُبِ، وَلَمْ يَجِدَا ذَهَبًا أَوْ فِضَّةً كَمَا تَوَقَّعَا فِي الْبِدَايَةِ.|Di dalam kastil mereka menemukan rak penuh buku, bukan emas atau perak seperti dugaan awal.|مَا الْكَنْزُ دَاخِلَ الْقَلْعَةِ؟|الْكُتُبُ|الذَّهَبُ|الْفِضَّةُ|الْمَجُوهَرَاتُ
قَالَ الْحَارِسُ: الْعِلْمُ كَنْزٌ، وَكُلَّمَا قَرَأْتُمَا وَتَعَلَّمْتُمَا زَادَتْ قُدْرَتُكُمَا عَلَى مُسَاعَدَةِ الْآخَرِينَ فِي حَيَاتِكُمَا.|Penjaga berkata: Ilmu adalah harta; semakin kalian membaca dan belajar, semakin mampu membantu orang lain dalam hidup.|لِمَاذَا الْعِلْمُ كَنْزٌ فِي الْقِصَّةِ؟|لِأَنَّهُ يُسَاعِدُ عَلَى مُسَاعَدَةِ الْآخَرِينَ|لِأَنَّهُ مِنْ ذَهَبٍ|لِأَنَّهُ يُخْفِي الْقَارِبَ|لِأَنَّهُ يُغْلِقُ الْمَكْتَبَةَ
عَادَ الصَّدِيقَانِ بِكُتُبٍ جَدِيدَةٍ وَفَرَحٍ كَبِيرٍ، وَقَرَّرَا أَنْ يَقْرَآهَا مَعَ أَطْفَالِ قَرْيَتِهِمَا لِيَنْتَفِعَ الْجَمِيعُ.|Kedua teman pulang membawa buku dan kegembiraan, serta memutuskan membacanya bersama anak desa agar semua mendapat manfaat.|مَاذَا قَرَّرَ الصَّدِيقَانِ؟|مُشَارَكَةَ الْكُتُبِ مَعَ الْأَطْفَالِ|إِخْفَاءَ الْكُتُبِ|بَيْعَ الْقَلْعَةِ|تَرْكَ الْقَرْيَةِ دَائِمًا
''')
def speaking(n,title,ar,objective,mission,dialog,rows):
    questions=[]
    for i,row in enumerate(rows.strip().splitlines()):
        q,trans,answer,alternative,meaning,criteria=row.split('|')
        questions.append(dict(id=f'kalam-{n}-q{i+1}',ar=q.strip(),translation=trans.strip(),example=answer.strip(),alternatives=[alternative.strip()],explanationAr=answer.strip(),explanationId=meaning.strip(),criteria=criteria.strip(),category='Komunikasi lisan'))
    assert len(questions)==10
    levels.append(dict(id=f'kalam-{n}',world='kalam',number=n,title=title,titleAr=ar,scene='town',objective=objective,mission=mission,character='Mimi si kucing',textAr=dialog,textId=mission,vocabulary=[],questions=questions,reward=['Kompas','Kristal','Kunci','Peta','Lentera','Permata','Daun emas','Lencana','Medali','Peti harta'][n-1]))
speaking(1,'Teman baru di desa','التَّعَارُفُ','Mengucapkan salam dan ungkapan perkenalan dengan sopan.','Mimi menyambutmu di gerbang desa. Sapa ia dan mulailah percakapan.','مَرْحَبًا! أَنَا مِيمِي. أَهْلًا بِكَ فِي قَرْيَتِنَا. هَيَّا نَتَعَارَفْ!', '''
كَيْفَ تُحَيِّي صَدِيقَكَ؟|Bagaimana menyapa temanmu?|السَّلَامُ عَلَيْكُمْ.|مَرْحَبًا.|Assalamualaikum. / Halo.|Salam yang sesuai; terima ungkapan salam lain.
مَاذَا تَقُولُ إِذَا قَالَ صَدِيقُكَ السَّلَامُ عَلَيْكُمْ؟|Apa balasan untuk assalamualaikum?|وَعَلَيْكُمُ السَّلَامُ.|وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللَّهِ.|Waalaikumussalam.|Balasan salam yang tepat.
مَا اسْمُكَ؟|Siapa namamu?|اسْمِي عَلِيٌّ.|أَنَا سَلْمَى.|Namaku Ali. Nama boleh berbeda.|Menyebut nama diri; nama apa pun diterima.
كَيْفَ حَالُكَ؟|Bagaimana kabarmu?|أَنَا بِخَيْرٍ، شُكْرًا.|بِخَيْرٍ، وَالْحَمْدُ لِلَّهِ.|Aku baik, terima kasih.|Ungkapan kabar; kondisi lain yang masuk akal juga diterima.
مَاذَا تَقُولُ فِي الصَّبَاحِ؟|Apa sapaan pada pagi hari?|صَبَاحُ الْخَيْرِ.|أَقُولُ صَبَاحَ الْخَيْرِ.|Selamat pagi.|Sapaan pagi.
كَيْفَ تَرُدُّ عَلَى صَبَاحِ الْخَيْرِ؟|Bagaimana membalas sapaan pagi?|صَبَاحُ النُّورِ.|صَبَاحُ الْخَيْرِ.|Selamat pagi juga.|Balasan sapaan pagi.
مَاذَا تَقُولُ فِي الْمَسَاءِ؟|Apa sapaan pada sore atau malam hari?|مَسَاءُ الْخَيْرِ.|أَقُولُ مَسَاءَ الْخَيْرِ.|Selamat sore/malam.|Sapaan مساء الخير.
كَيْفَ تُرَحِّبُ بِصَدِيقٍ جَدِيدٍ؟|Bagaimana menyambut teman baru?|أَهْلًا وَسَهْلًا.|مَرْحَبًا بِكَ.|Selamat datang.|Ungkapan menyambut teman.
مَاذَا تَقُولُ لِمَنْ يُسَاعِدُكَ؟|Apa ucapan untuk orang yang membantu?|شُكْرًا لَكَ.|جَزَاكَ اللَّهُ خَيْرًا.|Terima kasih.|Ungkapan terima kasih.
مَاذَا تَقُولُ عِنْدَ الْوَدَاعِ؟|Apa ucapan ketika berpisah?|مَعَ السَّلَامَةِ.|إِلَى اللِّقَاءِ.|Selamat jalan. / Sampai jumpa.|Ungkapan perpisahan.
''')
speaking(2,'Kartu identitas penjelajah','مَنْ أَنَا؟','Menyampaikan identitas sederhana, umur, dan hobi.','Mimi membuat kartu penjelajahmu. Gunakan identitas rekaan; jangan menyebut alamat lengkap.','نُرِيدُ بِطَاقَةً لِلْمُغَامِرِ. حَدِّثْنِي عَنْ نَفْسِكَ، وَلَا تَذْكُرْ عُنْوَانَكَ الْكَامِلَ.', '''
عَرِّفْ نَفْسَكَ بِجُمْلَةٍ.|Perkenalkan dirimu dalam satu kalimat.|أَنَا عَلِيٌّ وَأَنَا تِلْمِيذٌ.|أَنَا سَلْمَى وَأَنَا تِلْمِيذَةٌ.|Aku Ali dan aku siswa.|Nama dan identitas siswa; nama rekaan diterima.
كَمْ عُمْرُكَ؟|Berapa usiamu?|عُمْرِي تِسْعُ سَنَوَاتٍ.|عُمْرِي عَشْرُ سَنَوَاتٍ.|Usiaku sembilan tahun.|Ungkapan umur dengan angka masuk akal.
فِي أَيِّ صَفٍّ تَدْرُسُ؟|Kamu kelas berapa?|أَنَا فِي الصَّفِّ الثَّالِثِ.|أَدْرُسُ فِي الصَّفِّ الرَّابِعِ.|Aku kelas tiga.|Menyebut kelas; kelas lain diterima.
مَا اسْمُ مَدْرَسَتِكَ؟|Apa nama sekolahmu? Boleh rekaan.|مَدْرَسَتِي مَدْرَسَةُ النُّورِ.|أَدْرُسُ فِي مَدْرَسَةِ الْأَمَلِ.|Sekolahku An-Nur.|Menyebut nama sekolah rekaan.
هَلْ أَنْتَ تِلْمِيذٌ؟|Apakah kamu siswa?|نَعَمْ، أَنَا تِلْمِيذٌ.|نَعَمْ، أَنَا تِلْمِيذَةٌ.|Ya, aku siswa.|Respons afirmatif yang relevan.
مَا هِوَايَتُكَ؟|Apa hobimu?|هِوَايَتِي الرَّسْمُ.|أُحِبُّ السِّبَاحَةَ.|Hobiku menggambar.|Menyebut hobi; semua hobi sesuai anak diterima.
مَا لَوْنُكَ الْمُفَضَّلُ؟|Apa warna favoritmu?|لَوْنِيَ الْمُفَضَّلُ أَزْرَقُ.|أُحِبُّ اللَّوْنَ الْأَخْضَرَ.|Warna favoritku biru.|Menyebut warna apa pun.
مَا الرَّقْمُ الَّذِي تُحِبُّهُ؟|Angka apa yang kamu suka?|أُحِبُّ الرَّقْمَ سَبْعَةً.|رَقْمِيَ الْمُفَضَّلُ خَمْسَةٌ.|Aku suka angka tujuh.|Menyebut angka.
هَلْ تُحِبُّ التَّعَلُّمَ؟|Apakah kamu suka belajar?|نَعَمْ، أُحِبُّ التَّعَلُّمَ.|نَعَمْ، أُحِبُّ تَعَلُّمَ الْعَرَبِيَّةِ.|Ya, aku suka belajar.|Jawaban relevan; pendapat berbeda diterima.
مَاذَا تُرِيدُ أَنْ تَكُونَ؟|Ingin menjadi apa kelak?|أُرِيدُ أَنْ أَكُونَ طَبِيبًا.|أُرِيدُ أَنْ أَكُونَ مُعَلِّمَةً.|Aku ingin menjadi dokter.|Menyebut cita-cita dalam ungkapan sederhana.
''')
speaking(3,'Misi ruang kelas','فِي فَصْلِي','Menyebut benda kelas, warna, dan letaknya dalam percakapan.','Bantu Mimi menyiapkan kelas. Bayangkan sebuah kelas dengan benda-benda pilihanmu.','أَهْلًا فِي فَصْلِنَا! نُرَتِّبُ الْأَدَوَاتِ مَعًا. صِفْ لِي مَا تَرَاهُ.', '''
مَاذَا تَسْتَخْدِمُ لِلْكِتَابَةِ؟|Apa yang kamu gunakan untuk menulis?|أَسْتَخْدِمُ قَلَمًا.|أَكْتُبُ بِالْقَلَمِ.|Aku memakai pena.|Menyebut alat tulis sesuai fungsi.
مَاذَا تَقْرَأُ فِي الْفَصْلِ؟|Apa yang dibaca di kelas?|أَقْرَأُ كِتَابًا.|أَقْرَأُ قِصَّةً.|Aku membaca buku.|Buku atau teks yang dapat dibaca.
مَا لَوْنُ حَقِيبَتِكَ؟|Apa warna tasmu?|حَقِيبَتِي زَرْقَاءُ.|حَقِيبَتِي حَمْرَاءُ.|Tasku biru.|Tas dan warna; warna lain diterima.
أَيْنَ تَضَعُ الْقَلَمَ؟|Di mana kamu meletakkan pena?|أَضَعُهُ فِي الْمِقْلَمَةِ.|الْقَلَمُ عَلَى الْمَكْتَبِ.|Aku menaruhnya di tempat pensil.|Letak yang masuk akal.
عَلَى مَاذَا تَجْلِسُ؟|Di atas apa kamu duduk?|أَجْلِسُ عَلَى الْكُرْسِيِّ.|عَلَى كُرْسِيٍّ.|Aku duduk di kursi.|Menyebut kursi.
أَيْنَ يَكْتُبُ الْمُعَلِّمُ؟|Di mana guru menulis?|يَكْتُبُ عَلَى السَّبُّورَةِ.|الْمُعَلِّمُ يَكْتُبُ فِي الدَّفْتَرِ.|Guru menulis di papan tulis.|Permukaan tulis yang masuk akal.
صِفْ مَكْتَبَكَ.|Deskripsikan mejamu.|مَكْتَبِي بُنِّيٌّ وَصَغِيرٌ.|مَكْتَبِي كَبِيرٌ.|Mejaku cokelat dan kecil.|Sedikitnya satu sifat meja.
كَمْ كِتَابًا فِي حَقِيبَتِكَ؟|Berapa buku di tasmu?|فِي حَقِيبَتِي ثَلَاثَةُ كُتُبٍ.|عِنْدِي كِتَابَانِ.|Di tasku ada tiga buku.|Jumlah buku; angka lain diterima.
اُطْلُبْ قَلَمًا مِنْ صَدِيقِكَ.|Mintalah pena kepada temanmu.|أَعْطِنِي قَلَمًا مِنْ فَضْلِكَ.|هَلْ عِنْدَكَ قَلَمٌ؟|Berikan aku pena, tolong.|Permintaan pena yang sopan.
كَيْفَ نُحَافِظُ عَلَى نَظَافَةِ الْفَصْلِ؟|Bagaimana menjaga kelas tetap bersih?|نَضَعُ الْقُمَامَةَ فِي السَّلَّةِ.|نُنَظِّفُ الْفَصْلَ.|Kita membuang sampah di tempatnya.|Tindakan menjaga kebersihan.
''')
speaking(4,'Berkunjung ke rumah teman','أُسْرَتِي','Memperkenalkan anggota keluarga dan kegiatan mereka.','Mimi mengajakmu bercerita tentang keluarga rekaan dalam permainan.','أُسْرَتِي تُحِبُّ الضُّيُوفَ. هَلْ تَسْتَطِيعُ أَنْ تُعَرِّفَنِي بِأُسْرَتِكَ؟', '''
مَنْ فِي أُسْرَتِكَ؟|Siapa anggota keluargamu?|فِي أُسْرَتِي أَبِي وَأُمِّي وَأُخْتِي.|أَعِيشُ مَعَ أُمِّي وَجَدَّتِي.|Ada ayah, ibu, dan saudara perempuanku.|Sebut anggota keluarga; semua bentuk keluarga diterima.
كَمْ شَخْصًا فِي أُسْرَتِكَ؟|Berapa orang dalam keluargamu?|فِي أُسْرَتِي أَرْبَعَةُ أَشْخَاصٍ.|نَحْنُ خَمْسَةٌ.|Keluargaku empat orang.|Jumlah anggota keluarga.
مَا اسْمُ أَخِيكَ أَوْ أُخْتِكَ؟|Siapa nama saudaramu? Boleh rekaan.|اسْمُ أُخْتِي هِنْدٌ.|لَيْسَ عِنْدِي إِخْوَةٌ.|Nama saudariku Hind; boleh menjawab tidak memiliki saudara.|Nama saudara atau penjelasan tidak memiliki saudara.
مَاذَا يَعْمَلُ أَبُوكَ؟|Apa pekerjaan ayah tokohmu?|أَبِي فَلَّاحٌ.|أَبِي مُعَلِّمٌ.|Ayahku petani.|Pekerjaan masuk akal; tidak bekerja juga diterima.
مَاذَا تَعْمَلُ أُمُّكَ؟|Apa pekerjaan ibu tokohmu?|أُمِّي طَبِيبَةٌ.|أُمِّي تَعْمَلُ فِي الْبَيْتِ.|Ibuku dokter.|Pekerjaan atau kegiatan ibu yang relevan.
مَاذَا تُحِبُّ جَدَّتُكَ؟|Apa yang disukai nenek tokohmu?|جَدَّتِي تُحِبُّ الْقِرَاءَةَ.|تُحِبُّ زِرَاعَةَ الْأَزْهَارِ.|Nenek suka membaca.|Kesukaan nenek yang masuk akal.
صِفْ أَخَاكَ أَوْ أُخْتَكَ.|Deskripsikan saudaramu atau tokoh rekaan.|أَخِي صَغِيرٌ وَلَطِيفٌ.|أُخْتِي كَبِيرَةٌ وَذَكِيَّةٌ.|Adikku kecil dan baik.|Sifat saudara yang sesuai.
كَيْفَ تُسَاعِدُ أُسْرَتَكَ؟|Bagaimana membantu keluarga?|أُرَتِّبُ غُرْفَتِي.|أَغْسِلُ الْأَطْبَاقَ.|Aku merapikan kamar.|Tindakan membantu keluarga.
مَاذَا تَفْعَلُ مَعَ أُسْرَتِكَ فِي الْعُطْلَةِ؟|Apa kegiatan bersama keluarga saat libur?|نَذْهَبُ إِلَى الْحَدِيقَةِ.|نَقْرَأُ قِصَّةً مَعًا.|Kami pergi ke taman.|Aktivitas bersama yang relevan.
قُلْ جُمْلَةً تُعَبِّرُ بِهَا عَنْ حُبِّكَ لِأُسْرَتِكَ.|Ungkapkan kasih sayang untuk keluarga.|أُحِبُّ أُسْرَتِي كَثِيرًا.|أَنَا سَعِيدٌ مَعَ أُسْرَتِي.|Aku sangat menyayangi keluargaku.|Ungkapan kasih sayang.
''')
speaking(5,'Kedai makanan favorit','طَعَامِي الْمُفَضَّلُ','Mengungkapkan pilihan makanan, minuman, dan alasan sederhana.','Pesan bekal di kedai Mimi. Pilih makanan yang kamu suka.','أَهْلًا بِكَ فِي مَطْعَمِنَا! عِنْدَنَا أَرُزٌّ وَخُضْرَوَاتٌ وَفَوَاكِهُ. مَاذَا تُحِبُّ؟', '''
مَا طَعَامُكَ الْمُفَضَّلُ؟|Apa makanan favoritmu?|طَعَامِيَ الْمُفَضَّلُ الْأَرُزُّ.|أُحِبُّ الدَّجَاجَ.|Makanan favoritku nasi.|Nama makanan yang disukai.
مَاذَا تُحِبُّ أَنْ تَشْرَبَ؟|Apa yang ingin kamu minum?|أُحِبُّ أَنْ أَشْرَبَ الْمَاءَ.|أُرِيدُ عَصِيرَ الْبُرْتُقَالِ.|Aku suka minum air.|Nama minuman yang masuk akal.
هَلْ تُحِبُّ الْخُضْرَوَاتِ؟|Apakah suka sayuran?|نَعَمْ، أُحِبُّ الْخُضْرَوَاتِ.|لَا، لَا أُحِبُّهَا كَثِيرًا.|Ya, aku suka sayur.|Jawaban ya atau tidak yang relevan.
مَا الْفَاكِهَةُ الَّتِي تُحِبُّهَا؟|Buah apa yang disukai?|أُحِبُّ الْمَوْزَ.|فَاكِهَتِيَ الْمُفَضَّلَةُ التُّفَّاحُ.|Aku suka pisang.|Nama buah apa pun.
مَاذَا تَأْكُلُ فِي الْفُطُورِ؟|Apa yang kamu makan saat sarapan?|آكُلُ الْخُبْزَ وَالْبَيْضَ.|آكُلُ الْأَرُزَّ.|Aku makan roti dan telur.|Makanan sarapan masuk akal.
اُطْلُبْ كَأْسَ مَاءٍ بِأَدَبٍ.|Mintalah segelas air dengan sopan.|أُرِيدُ كَأْسَ مَاءٍ مِنْ فَضْلِكَ.|هَلْ يُمْكِنُ أَنْ تُعْطِيَنِي مَاءً؟|Aku ingin segelas air, tolong.|Permintaan air dengan bahasa sopan.
لِمَاذَا تُحِبُّ طَعَامَكَ الْمُفَضَّلَ؟|Mengapa kamu menyukai makanan itu?|لِأَنَّهُ لَذِيذٌ.|لِأَنَّهُ صِحِّيٌّ.|Karena lezat.|Alasan sederhana terkait makanan.
مَا الطَّعَامُ الَّذِي لَا تُحِبُّهُ؟|Makanan apa yang tidak kamu suka?|لَا أُحِبُّ السَّمَكَ.|أُحِبُّ كُلَّ الطَّعَامِ.|Aku tidak suka ikan; boleh menyukai semua makanan.|Preferensi negatif atau menyukai semua.
هَلْ تُرِيدُ طَعَامًا حَارًّا أَمْ غَيْرَ حَارٍّ؟|Mau makanan pedas atau tidak pedas?|أُرِيدُ طَعَامًا غَيْرَ حَارٍّ.|أُرِيدُ طَعَامًا حَارًّا.|Aku mau makanan tidak pedas.|Memilih salah satu pilihan.
مَاذَا تَقُولُ بَعْدَ الْأَكْلِ؟|Apa ucapan setelah makan?|الْحَمْدُ لِلَّهِ.|شُكْرًا عَلَى الطَّعَامِ.|Alhamdulillah; terima kasih atas makanannya.|Ungkapan syukur atau terima kasih.
''')
speaking(6,'Jadwal hariku','يَوْمِي','Menceritakan kegiatan harian dengan keterangan waktu.','Atur jadwal ekspedisi bersama Mimi dengan menceritakan harimu.','نَحْتَاجُ إِلَى جَدْوَلٍ لِلرِّحْلَةِ. أَخْبِرْنِي عَنْ يَوْمِكَ مِنَ الصَّبَاحِ إِلَى اللَّيْلِ.', '''
مَتَى تَسْتَيْقِظُ؟|Kapan kamu bangun?|أَسْتَيْقِظُ فِي الْخَامِسَةِ.|أَسْتَيْقِظُ صَبَاحًا.|Aku bangun pukul lima.|Waktu bangun; semua waktu masuk akal diterima.
مَاذَا تَفْعَلُ بَعْدَ الِاسْتِيقَاظِ؟|Apa kegiatan setelah bangun?|أَغْسِلُ وَجْهِي.|أُرَتِّبُ سَرِيرِي.|Aku mencuci muka.|Kegiatan setelah bangun.
مَتَى تَتَنَاوَلُ الْفُطُورَ؟|Kapan sarapan?|أَتَنَاوَلُ الْفُطُورَ فِي السَّادِسَةِ.|أَفْطُرُ قَبْلَ الْمَدْرَسَةِ.|Aku sarapan pukul enam.|Waktu atau urutan sarapan.
كَيْفَ تَذْهَبُ إِلَى الْمَدْرَسَةِ؟|Bagaimana pergi ke sekolah?|أَذْهَبُ بِالدَّرَّاجَةِ.|أَذْهَبُ مَاشِيًا.|Aku naik sepeda.|Cara pergi yang masuk akal.
مَاذَا تَفْعَلُ فِي الْفُسْحَةِ؟|Apa kegiatan saat istirahat?|أَلْعَبُ مَعَ أَصْدِقَائِي.|آكُلُ طَعَامِي.|Aku bermain bersama teman.|Aktivitas istirahat sekolah.
مَتَى تَعُودُ إِلَى الْبَيْتِ؟|Kapan pulang ke rumah?|أَعُودُ ظُهْرًا.|أَعُودُ فِي السَّاعَةِ الْوَاحِدَةِ.|Aku pulang siang.|Waktu pulang yang masuk akal.
مَاذَا تَفْعَلُ بَعْدَ الْغَدَاءِ؟|Apa kegiatan setelah makan siang?|أَسْتَرِيحُ قَلِيلًا.|أَكْتُبُ وَاجِبَاتِي.|Aku beristirahat sebentar.|Aktivitas sesudah makan siang.
كَيْفَ تُسَاعِدُ فِي الْبَيْتِ مَسَاءً؟|Bagaimana membantu di rumah pada sore hari?|أَسْقِي الْأَزْهَارَ.|أُنَظِّفُ غُرْفَتِي.|Aku menyiram bunga.|Kegiatan membantu di rumah.
مَتَى تَنَامُ؟|Kapan kamu tidur?|أَنَامُ فِي التَّاسِعَةِ لَيْلًا.|أَنَامُ مُبَكِّرًا.|Aku tidur pukul sembilan malam.|Waktu tidur.
صِفْ يَوْمَكَ فِي جُمْلَتَيْنِ مُرَتَّبَتَيْنِ.|Ceritakan harimu dengan dua kalimat berurutan.|أَذْهَبُ إِلَى الْمَدْرَسَةِ صَبَاحًا. ثُمَّ أَلْعَبُ عَصْرًا.|أَدْرُسُ صَبَاحًا وَأَقْرَأُ مَسَاءً.|Aku sekolah pagi, lalu bermain sore.|Dua aktivitas dengan urutan jelas.
''')
speaking(7,'Alamat desa petualangan','أَيْنَ تَسْكُنُ؟','Bertanya dan menjelaskan lokasi serta arah sederhana.','Jelaskan lokasi rumah rekaan di desa. Jangan menyebut alamat asli.','أَنَا زَائِرَةٌ فِي قَرْيَتِكَ. أَيْنَ الْمَكْتَبَةُ وَالْحَدِيقَةُ؟ سَاعِدْنِي لِأَجِدَ الطَّرِيقَ.', '''
أَيْنَ تَسْكُنُ فِي قَرْيَةِ اللُّعْبَةِ؟|Di mana rumahmu dalam desa permainan?|أَسْكُنُ قُرْبَ الْحَدِيقَةِ.|بَيْتِي بِجَانِبِ الْمَسْجِدِ.|Aku tinggal dekat taman.|Lokasi rekaan dengan hubungan tempat.
هَلْ بَيْتُكَ قَرِيبٌ مِنَ الْمَدْرَسَةِ؟|Apakah rumah tokohmu dekat sekolah?|نَعَمْ، بَيْتِي قَرِيبٌ.|لَا، بَيْتِي بَعِيدٌ.|Ya, rumahku dekat.|Ya atau tidak dengan dekat/jauh.
مَاذَا أَمَامَ بَيْتِكَ؟|Apa di depan rumah tokohmu?|أَمَامَ بَيْتِي شَجَرَةٌ.|أَمَامَ بَيْتِي حَدِيقَةٌ.|Di depan rumahku ada pohon.|Objek dan hubungan di depan.
مَاذَا خَلْفَ الْمَكْتَبَةِ فِي قَرْيَتِكَ؟|Apa di belakang perpustakaan desa rekaan?|خَلْفَ الْمَكْتَبَةِ مَدْرَسَةٌ.|خَلْفَهَا مَسْجِدٌ.|Di belakang perpustakaan ada sekolah.|Lokasi dengan خلف.
صِفِ الطَّرِيقَ إِلَى الْحَدِيقَةِ.|Jelaskan jalan ke taman.|اِمْشِي إِلَى الْأَمَامِ ثُمَّ اِنْعَطِفِي يَمِينًا.|اِذْهَبِي يَسَارًا.|Berjalan lurus lalu belok kanan.|Instruksi arah yang masuk akal.
اِسْأَلْنِي عَنْ مَكَانِ الْمَسْجِدِ.|Tanyakan lokasi masjid kepada Mimi.|أَيْنَ الْمَسْجِدُ؟|هَلِ الْمَسْجِدُ قَرِيبٌ؟|Di mana masjid?|Pertanyaan lokasi masjid.
هَلِ الْمَدْرَسَةُ عَلَى الْيَمِينِ أَمِ الْيَسَارِ؟|Sekolah ada di kanan atau kiri?|الْمَدْرَسَةُ عَلَى الْيَمِينِ.|هِيَ عَلَى الْيَسَارِ.|Sekolah di kanan.|Memilih kanan atau kiri.
كَيْفَ نَعْبُرُ النَّهْرَ بِأَمَانٍ؟|Bagaimana menyeberangi sungai dengan aman?|نَعْبُرُ بِالْقَارِبِ مَعَ الْحَارِسِ.|نَسْتَخْدِمُ الْجِسْرَ.|Dengan perahu bersama penjaga atau jembatan.|Cara aman menyeberang.
صِفْ بَيْتَكَ الْخَيَالِيَّ.|Deskripsikan rumah khayalanmu.|بَيْتِي صَغِيرٌ وَلَهُ بَابٌ أَزْرَقُ.|بَيْتِي كَبِيرٌ وَجَمِيلٌ.|Rumahku kecil dan berpintu biru.|Sifat rumah; warna dan ukuran bebas.
مَاذَا تَقُولُ لِمَنْ دَلَّكَ عَلَى الطَّرِيقِ؟|Apa ucapan untuk pemberi petunjuk arah?|شُكْرًا عَلَى الْمُسَاعَدَةِ.|شُكْرًا لَكَ.|Terima kasih atas bantuannya.|Ucapan terima kasih yang relevan.
''')
speaking(8,'Pemandu satwa muda','صِفْ حَيَوَانًا','Mendeskripsikan ciri, makanan, gerak, dan habitat hewan.','Pilih satu hewan dan ceritakan kepada Mimi agar ia bisa menebaknya.','أُحِبُّ الْحَيَوَانَاتِ. اِخْتَرْ حَيَوَانًا وَصِفْهُ لِي. يُمْكِنُكَ اِخْتِيَارُ أَيِّ حَيَوَانٍ.', '''
مَا الْحَيَوَانُ الَّذِي تُحِبُّهُ؟|Hewan apa yang kamu sukai?|أُحِبُّ الْأَرْنَبَ.|حَيَوَانِيَ الْمُفَضَّلُ الْقِطُّ.|Aku suka kelinci.|Nama hewan apa pun diterima.
مَا لَوْنُ هَذَا الْحَيَوَانِ؟|Apa warna hewan pilihanmu?|لَوْنُهُ أَبْيَضُ.|هُوَ بُنِّيٌّ.|Warnanya putih.|Warna sesuai hewan pilihan; variasi diterima.
هَلْ هُوَ كَبِيرٌ أَمْ صَغِيرٌ؟|Besar atau kecil?|هُوَ صَغِيرٌ.|هُوَ كَبِيرٌ.|Ia kecil.|Ukuran sesuai konteks.
أَيْنَ يَعِيشُ هَذَا الْحَيَوَانُ؟|Di mana hewan itu hidup?|يَعِيشُ فِي الْمَزْرَعَةِ.|يَعِيشُ فِي الْغَابَةِ.|Ia hidup di peternakan.|Habitat sesuai hewan pilihan.
مَاذَا يَأْكُلُ هَذَا الْحَيَوَانُ؟|Apa makanan hewan itu?|يَأْكُلُ الْجَزَرَ.|يَأْكُلُ السَّمَكَ.|Ia makan wortel.|Makanan harus dinilai sesuai hewan pilihan.
كَيْفَ يَتَحَرَّكُ؟|Bagaimana ia bergerak?|هُوَ يَقْفِزُ.|هُوَ يَسْبَحُ.|Ia melompat.|Gerakan sesuai hewan pilihan.
كَمْ رِجْلًا لَهُ؟|Berapa jumlah kakinya?|لَهُ أَرْبَعُ أَرْجُلٍ.|لَهُ رِجْلَانِ.|Ia berkaki empat.|Jumlah kaki sesuai hewan pilihan.
صِفْ أُذُنَيْهِ أَوْ ذَيْلَهُ.|Deskripsikan telinga atau ekornya.|لَهُ أُذُنَانِ طَوِيلَتَانِ.|ذَيْلُهُ قَصِيرٌ.|Telinganya panjang.|Sifat anggota tubuh sesuai hewan pilihan.
لِمَاذَا تُحِبُّهُ؟|Mengapa kamu menyukainya?|لِأَنَّهُ لَطِيفٌ.|لِأَنَّهُ جَمِيلٌ.|Karena ia lucu.|Alasan yang relevan.
كَيْفَ نَعْتَنِي بِالْحَيَوَانَاتِ؟|Bagaimana merawat hewan?|نُعْطِيهَا طَعَامًا وَمَاءً.|نُحَافِظُ عَلَى بِيئَتِهَا.|Kita memberinya makanan dan air.|Tindakan perawatan yang sesuai.
''')
speaking(9,'Berbelanja bekal','فِي السُّوقِ','Melakukan dialog jual beli: meminta barang, jumlah, harga, dan pembayaran.','Mimi menjadi penjual buah. Apel 10 riyal/kg dan pisang 5 riyal/kg. Kamu membawa 20 riyal.','أَهْلًا فِي السُّوقِ! كِيلُوغْرَامُ التُّفَّاحِ بِعَشَرَةِ رِيَالَاتٍ، وَكِيلُوغْرَامُ الْمَوْزِ بِخَمْسَةِ رِيَالَاتٍ.', '''
كَيْفَ تُحَيِّي الْبَائِعَ؟|Bagaimana menyapa penjual?|السَّلَامُ عَلَيْكُمْ.|صَبَاحُ الْخَيْرِ.|Assalamualaikum.|Sapaan sopan kepada penjual.
مَاذَا تُرِيدُ أَنْ تَشْتَرِيَ؟|Apa yang ingin kamu beli?|أُرِيدُ أَنْ أَشْتَرِيَ تُفَّاحًا.|أُرِيدُ مَوْزًا.|Aku ingin membeli apel.|Permintaan buah yang tersedia.
اِسْأَلْ عَنْ ثَمَنِ التُّفَّاحِ.|Tanyakan harga apel.|بِكَمْ كِيلُوغْرَامُ التُّفَّاحِ؟|مَا ثَمَنُ التُّفَّاحِ؟|Berapa harga satu kg apel?|Pertanyaan harga apel.
اُطْلُبْ كِيلُوغْرَامًا مِنَ التُّفَّاحِ.|Pesan satu kilogram apel.|أُرِيدُ كِيلُوغْرَامًا مِنَ التُّفَّاحِ.|أَعْطِنِي كِيلُوغْرَامَ تُفَّاحٍ مِنْ فَضْلِكَ.|Aku ingin satu kilogram apel.|Permintaan satu kg apel.
كَمْ ثَمَنُ كِيلُوغْرَامِ الْمَوْزِ؟|Berapa harga satu kg pisang di kedai ini?|ثَمَنُهُ خَمْسَةُ رِيَالَاتٍ.|بِخَمْسَةِ رِيَالَاتٍ.|Lima riyal.|Harus menyebut lima riyal.
هَلْ تُرِيدُ شَيْئًا آخَرَ؟|Ingin barang lain?|نَعَمْ، أُرِيدُ مَوْزًا.|لَا، شُكْرًا.|Ya, aku ingin pisang, atau tidak terima kasih.|Ya dengan barang atau penolakan sopan.
كَمْ ثَمَنُ كِيلُوغْرَامِ تُفَّاحٍ وَكِيلُوغْرَامِ مَوْزٍ؟|Berapa total satu kg apel dan satu kg pisang?|خَمْسَةَ عَشَرَ رِيَالًا.|الْمَجْمُوعُ خَمْسَةَ عَشَرَ.|Lima belas riyal.|Total 15 riyal.
كَمْ رِيَالًا مَعَكَ فِي هَذِهِ اللُّعْبَةِ؟|Berapa uang yang kamu bawa dalam skenario?|مَعِي عِشْرُونَ رِيَالًا.|عِنْدِي عِشْرُونَ.|Aku membawa dua puluh riyal.|20 riyal sesuai skenario.
كَمِ الْبَاقِي مِنْ عِشْرِينَ بَعْدَ دَفْعِ خَمْسَةَ عَشَرَ؟|Berapa kembalian 20 dikurangi 15?|الْبَاقِي خَمْسَةُ رِيَالَاتٍ.|خَمْسَةُ رِيَالَاتٍ.|Kembaliannya lima riyal.|5 riyal.
اِخْتِمِ الْحِوَارَ مَعَ الْبَائِعِ.|Akhiri percakapan dengan penjual.|شُكْرًا، مَعَ السَّلَامَةِ.|شُكْرًا لَكَ، إِلَى اللِّقَاءِ.|Terima kasih, sampai jumpa.|Terima kasih atau perpisahan sopan.
''')
speaking(10,'Pertemuan para penjelajah','لِقَاءُ الْمُغَامِرِينَ','Menggabungkan perkenalan, permintaan bantuan, dan rencana perjalanan lisan.','Mimi akan menemanimu ke pulau. Kalian mulai dari desa, membawa peta, lalu naik perahu bersama penjaga.','نَحْنُ فَرِيقُ الْمُغَامَرَةِ! نَنْطَلِقُ مِنَ الْقَرْيَةِ إِلَى الْجَزِيرَةِ مَعَ الْحَارِسِ. هَيَّا نُخَطِّطْ مَعًا.', '''
عَرِّفْ نَفْسَكَ لِفَرِيقِ الْمُغَامَرَةِ.|Perkenalkan dirimu kepada tim.|أَنَا عَلِيٌّ وَأُحِبُّ الْمُغَامَرَةَ.|اسْمِي سَلْمَى وَأَنَا مُسْتَعِدَّةٌ.|Aku Ali dan suka petualangan.|Nama rekaan dan keterangan diri.
مَا الَّذِي سَتَحْمِلُهُ فِي حَقِيبَتِكَ؟|Apa yang akan dibawa di tas?|سَأَحْمِلُ الْمَاءَ وَالطَّعَامَ.|سَأَحْمِلُ خَرِيطَةً وَمِصْبَاحًا.|Aku membawa air dan makanan.|Bekal perjalanan yang relevan.
لِمَاذَا نَحْتَاجُ إِلَى خَرِيطَةٍ؟|Mengapa perlu peta?|لِنَعْرِفَ الطَّرِيقَ.|لِكَيْ لَا نَضِلَّ.|Agar tahu jalan.|Fungsi peta dalam perjalanan.
اُطْلُبِ الْمُسَاعَدَةَ مِنَ الْحَارِسِ.|Mintalah bantuan penjaga.|سَاعِدْنَا مِنْ فَضْلِكَ.|هَلْ يُمْكِنُ أَنْ تُسَاعِدَنَا؟|Tolong bantu kami.|Permintaan bantuan yang sopan.
كَيْفَ سَنَصِلُ إِلَى الْجَزِيرَةِ؟|Bagaimana kita ke pulau dalam skenario ini?|سَنَذْهَبُ بِالْقَارِبِ مَعَ الْحَارِسِ.|بِالْقَارِبِ.|Dengan perahu bersama penjaga.|Perahu sesuai skenario.
مَاذَا تَقُولُ لِصَدِيقٍ مُتْعَبٍ؟|Apa ucapan untuk teman yang lelah?|اِسْتَرِحْ قَلِيلًا وَاشْرَبْ مَاءً.|هَيَّا نَسْتَرِحْ مَعًا.|Istirahat sebentar dan minum air.|Saran peduli dan aman.
صِفْ مَكَانًا تُرِيدُ زِيَارَتَهُ.|Deskripsikan tempat yang ingin dikunjungi.|أُرِيدُ زِيَارَةَ قَلْعَةٍ كَبِيرَةٍ.|أُحِبُّ حَدِيقَةً جَمِيلَةً.|Aku ingin mengunjungi kastil besar.|Tempat dengan sedikitnya satu sifat.
مَاذَا نَفْعَلُ إِذَا لَمْ نَعْرِفِ الطَّرِيقَ؟|Apa yang dilakukan jika tidak tahu jalan?|نَسْأَلُ الْحَارِسَ.|نَقْرَأُ الْخَرِيطَةَ مَعًا.|Kita bertanya kepada penjaga.|Tindakan mencari arah yang aman.
لِمَاذَا يَنْجَحُ الْفَرِيقُ الْمُتَعَاوِنُ؟|Mengapa tim yang bekerja sama berhasil?|لِأَنَّنَا نُسَاعِدُ بَعْضَنَا.|لِأَنَّنَا نَعْمَلُ مَعًا.|Karena saling membantu.|Alasan terkait kerja sama.
اُذْكُرْ خُطَّتَكَ لِلرِّحْلَةِ فِي جُمْلَتَيْنِ.|Sampaikan rencana perjalanan dalam dua kalimat.|سَنَأْخُذُ الْخَرِيطَةَ. ثُمَّ سَنَرْكَبُ الْقَارِبَ.|نَبْدَأُ مِنَ الْقَرْيَةِ ثُمَّ نَذْهَبُ إِلَى الْجَزِيرَةِ.|Kita bawa peta, lalu naik perahu.|Dua langkah rencana yang runtut dan sesuai skenario.
''')
# Concise bilingual vocabulary, rather than revealing ten story answers.
vocabs={
'istima':[
'السَّلَامُ عَلَيْكُمْ=Semoga keselamatan atasmu;صَبَاحُ الْخَيْرِ=Selamat pagi;صَدِيقٌ=Teman;بِخَيْرٍ=Baik;حَقِيبَةٌ=Tas;مَعَ السَّلَامَةِ=Selamat jalan',
'وَاحِدٌ=Satu;اِثْنَانِ=Dua;ثَلَاثَةٌ=Tiga;خَمْسَةٌ=Lima;سَبْعَةٌ=Tujuh;عَشَرَةٌ=Sepuluh',
'أَحْمَرُ=Merah;أَزْرَقُ=Biru;أَصْفَرُ=Kuning;أَخْضَرُ=Hijau;أَبْيَضُ=Putih;بَنَفْسَجِيٌّ=Ungu',
'أَبٌ=Ayah;أُمٌّ=Ibu;أَخٌ=Saudara laki-laki;أُخْتٌ=Saudara perempuan;جَدَّةٌ=Nenek;أُسْرَةٌ=Keluarga',
'فِيلٌ=Gajah;زَرَافَةٌ=Jerapah;أَسَدٌ=Singa;قِرْدٌ=Monyet;بَطَّةٌ=Bebek;أَرْنَبٌ=Kelinci',
'عَيْنٌ=Mata;أُذُنٌ=Telinga;أَنْفٌ=Hidung;فَمٌ=Mulut;يَدٌ=Tangan;قَدَمٌ=Kaki',
'أَسْتَيْقِظُ=Aku bangun;أَتَنَاوَلُ=Aku menyantap;أَذْهَبُ=Aku pergi;أَعُودُ=Aku pulang;أَسْقِي=Aku menyiram;أَنَامُ=Aku tidur',
'يَمِينٌ=Kanan;يَسَارٌ=Kiri;أَمَامَ=Di depan;خَلْفَ=Di belakang;جِسْرٌ=Jembatan;اِنْعَطِفْ=Beloklah',
'سُوقٌ=Pasar;بَائِعٌ=Penjual;ثَمَنٌ=Harga;الْمَجْمُوعُ=Total;الْبَاقِي=Kembalian;طَازَجٌ=Segar',
'مُغَامَرَةٌ=Petualangan;خَرِيطَةٌ=Peta;مِفْتَاحٌ=Kunci;صُنْدُوقٌ=Kotak;الشَّرْقُ=Timur;تَعَاوُنٌ=Kerja sama'],
'qiraah':[
'فَصْلٌ=Kelas;سَبُّورَةٌ=Papan tulis;مَكْتَبٌ=Meja;مِقْلَمَةٌ=Tempat pensil;كُرْسِيٌّ=Kursi;دَفْتَرٌ=Buku tulis',
'تِلْمِيذٌ=Siswa;عُمْرٌ=Usia;قَرْيَةٌ=Desa;دَرَّاجَةٌ=Sepeda;هِوَايَةٌ=Hobi;رَسَّامٌ=Pelukis',
'طَاوِلَةٌ=Meja;عُلْبَةٌ=Kotak;إِنَاءٌ=Vas/bejana;جِدَارٌ=Dinding;وَرْدِيٌّ=Merah muda;بُرْتُقَالِيٌّ=Oranye',
'مُهَنْدِسٌ=Insinyur;جَدٌّ=Kakek;الْعُلُومُ=Sains;خَضْرَوَاتٌ=Sayuran;مَائِدَةٌ=Meja makan;مُتَعَاوِنٌ=Suka bekerja sama',
'جَمَلٌ=Unta;صَحْرَاءُ=Gurun;زَعَانِفُ=Sirip-sirip;بَطْرِيقٌ=Penguin;نَحْلَةٌ=Lebah;خُفَّاشٌ=Kelelawar',
'مَتْحَفٌ=Museum;حَافِلَةٌ=Bus;دَلِيلٌ=Pemandu;فَخَّارٌ=Tembikar;ظُهْرًا=Pada siang hari;قَدِيمٌ=Tua/lama',
'إِعْلَانٌ=Pengumuman;مُشَارِكٌ=Peserta;رَفٌّ=Rak;مُنَاقَشَةٌ=Diskusi;نَشَاطٌ=Kegiatan;التَّسْجِيلُ=Pendaftaran',
'الشَّمَالُ=Utara;الْجَنُوبُ=Selatan;الشَّرْقُ=Timur;الْغَرْبُ=Barat;نَافُورَةٌ=Air mancur;مَمَرُّ الْمُشَاةِ=Penyeberangan pejalan kaki',
'مَحْفَظَةٌ=Dompet;نُقُودٌ=Uang;أَمِينٌ=Jujur/dapat dipercaya;حَارِسٌ=Penjaga;قَلَقٌ=Kekhawatiran;مُكَافَأَةٌ=Hadiah',
'جَزِيرَةٌ=Pulau;نِصْفٌ=Separuh;لَافِتَةٌ=Papan petunjuk;لُغْزٌ=Teka-teki;كَنْزٌ=Harta;الْعِلْمُ=Ilmu']}
vocabs['kalam']=[vocabs['istima'][0],vocabs['qiraah'][1],vocabs['qiraah'][0],vocabs['istima'][3], 'طَعَامٌ=Makanan;شَرَابٌ=Minuman;لَذِيذٌ=Lezat;حَارٌّ=Pedas;أُرِيدُ=Aku ingin;مِنْ فَضْلِكَ=Tolong',vocabs['istima'][6],vocabs['istima'][7],vocabs['istima'][4],vocabs['istima'][8],vocabs['istima'][9]]
for level in levels:
    level['vocabulary']=[dict(ar=p.split('=')[0],id=p.split('=')[1]) for p in vocabs[level['world']][level['number']-1].split(';')]
    level['difficulty']='Pemula' if level['number']<4 else 'Dasar menengah' if level['number']<7 else 'Menengah' if level['number']<10 else 'Tantangan akhir'
    level['rubric']=dict(relevance=40,vocabulary=25,structure=20,comprehensibility=15) if level['world']=='kalam' else dict(correct=10,incorrect=0)
levels.sort(key=lambda l:({'istima':0,'kalam':1,'qiraah':2}[l['world']],l['number']))
(ROOT/'data/curriculum.json').write_text(json.dumps(levels,ensure_ascii=False,indent=2))
print(f'Created {len(levels)} levels, {sum(len(x["questions"]) for x in levels)} questions')
for w in ['istima','qiraah']:
 print(w,[(l['number'],len(l['textAr'].split())) for l in levels if l['world']==w])
