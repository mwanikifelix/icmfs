"""
Management command: seed_subcounties

Usage:
    python manage.py seed_subcounties

Seeds all Kenya sub-counties and wards.
Safe to run multiple times (uses get_or_create).
Requires counties to already exist (run seed_counties first).
"""
from django.core.management.base import BaseCommand
from apps.projects.models import County, SubCounty, Ward

# Structure: county_name → [(subcounty_name, [ward1, ward2, ...])]
DATA = {
    "Mombasa": [
        ("Changamwe",    ["Airport", "Changamwe", "Chaani", "Miritini", "Port Reitz"]),
        ("Jomvu",        ["Jomvu Kuu", "Magongo", "Mikindani"]),
        ("Kisauni",      ["Bamburi", "Kisauni", "Mwakirunge", "Mjambere", "Shanzu", "Mtopanga"]),
        ("Likoni",       ["Bofu", "Likoni", "Mtongwe", "Shika Adabu", "Timbwani"]),
        ("Mvita",        ["Ganjoni", "Kuze", "Mji Wa Kale/Makadara", "Old Town", "Tudor", "Tononoka"]),
        ("Nyali",        ["Frere Town", "Kadzandani", "Kongowea", "Mkomani", "Nyali"]),
    ],
    "Kwale": [
        ("Kinango",      ["Chengoni/Samburu", "Engangani", "Gandini", "Kayafungo", "Kinango", "Mackinon Road", "Puma"]),
        ("Lungalunga",   ["Jasho", "Lungalunga", "Mwavumbo", "Shimba Hills"]),
        ("Matuga",       ["Bongwe", "Chikole", "Kubo South", "Matuga", "Tsimba Golini"]),
        ("Msambweni",    ["Diani", "Gombato Bongwe", "Msambweni", "Ukunda"]),
    ],
    "Kilifi": [
        ("Ganze",        ["Bamba", "Ganze", "Jaribuni", "Ngerenya"]),
        ("Kaloleni",     ["Kaloleni", "Mariakani", "Mwanamwinga", "Ndavaya"]),
        ("Kilifi North", ["Chasimba", "Junju", "Kibarani", "Mkunumbi", "Tezo", "Sokoni"]),
        ("Kilifi South", ["Chasimba", "Mavueni", "Shimo La Tewa", "Vipingo"]),
        ("Magarini",     ["Adu", "Gongoni", "Magarini", "Marafa", "Mjanaheri"]),
        ("Malindi",      ["Jilore", "Kakuyuni", "Malindi Town", "Mtangani", "Shella"]),
        ("Rabai",        ["Kisurutini", "Mwawesa", "Rabai/Chamari", "Ruruma"]),
    ],
    "Tana River": [
        ("Bura",         ["Chewani", "Bura", "Wayu"]),
        ("Galole",       ["Galole", "Hirimani", "Mikinduni", "Mungatana"]),
        ("Garsen",       ["Garsen Central", "Garsen North", "Garsen South", "Garsen West", "Kipini East", "Kipini West"]),
    ],
    "Lamu": [
        ("Lamu East",    ["Faza", "Kiunga", "Basuba"]),
        ("Lamu West",    ["Hindi", "Lamu Town", "Mkomani", "Mokowe", "Shella", "Witu", "Bahari"]),
    ],
    "Taita-Taveta": [
        ("Mwatate",      ["Chawia", "Mwanda", "Mwatate", "Wundanyi/Mbolia"]),
        ("Taveta",       ["Bomani", "Chala", "Mahoo", "Mata", "Taveta Town"]),
        ("Voi",          ["Kaloleni", "Marungu", "Mwakingali", "Sagala", "Voi"]),
        ("Wundanyi",     ["Mbatoni", "Mwanda", "Ngolia", "Wundanyi/Mbolia"]),
    ],
    "Garissa": [
        ("Daadab",       ["Danyere", "Daadab", "Labisigale", "Lagodera", "Dertu", "Ifo"]),
        ("Fafi",         ["Bura", "Dekaharia", "Fafi", "Jarajila", "Nanighi"]),
        ("Garissa Township", ["Galbet", "Garissa Township", "Highway", "Iftin", "Waberi"]),
        ("Hulugho",      ["Hulugho", "Ijara", "Masalani"]),
        ("Ijara",        ["Ijara", "Sangailu"]),
        ("Lagdera",      ["Balambala", "Benane", "Goreale", "Modogashe", "Maalimin", "Sabena"]),
    ],
    "Wajir": [
        ("Eldas",        ["Eldas", "Griftu", "Hadado/Athibohol", "Warbona"]),
        ("Tarbaj",       ["Ademasajida", "Buna", "Gurar", "Tarbaj"]),
        ("Wajir East",   ["Khorof/Harar", "Wagberi", "Wajir East", "Wajir Township"]),
        ("Wajir North",  ["Bute", "Dambas", "Gamba", "Majiyarey", "Wajir North"]),
        ("Wajir South",  ["Habaswein", "Lagdima", "Sarman", "Wajir South"]),
        ("Wajir West",   ["Ademasajida", "Diif", "Furaha", "Malkagufu", "Wajir West"]),
    ],
    "Mandera": [
        ("Banissa",      ["Banissa", "Derkhale", "Guba", "Kiliwehiri"]),
        ("Lafey",        ["Fino", "Lafey", "Libehia", "Sala"]),
        ("Mandera East", ["Burale", "Khalalio", "Neboi", "Township"]),
        ("Mandera North",["Ashabito", "Guticha", "Morothile", "Rhamu", "Rhamu Dimtu"]),
        ("Mandera South",["Arabia", "Gaddaley", "Kiungo", "Lagsure"]),
        ("Mandera West", ["Banissa", "Elwak North", "Elwak South", "Gither", "Shimbir Fatuma"]),
    ],
    "Marsabit": [
        ("Laisamis",     ["Laisamis", "Logologo", "Loiyangalani", "Moyale"]),
        ("Marsabit",     ["Karare", "Marsabit Central", "Marsabit North", "Sagante/Jaldesa", "Saku"]),
        ("Moyale",       ["Butiye", "Golbo", "Moyale Town", "Obbu", "Sololo"]),
        ("North Horr",   ["Dukana", "Gadamoji", "Maikona", "North Horr", "Turbi"]),
    ],
    "Isiolo": [
        ("Garbatulla",   ["Chari", "Garbatulla", "Kinna", "Meru North"]),
        ("Isiolo",       ["Bulla Pesa", "Cherab", "Ciokariga", "Garbatulla", "Isiolo Town", "Wabera", "Waso"]),
        ("Merti",        ["Merti", "Oldonyiro"]),
    ],
    "Meru": [
        ("Buuri",        ["Buuri", "Kiirua/Naari", "Kisima", "Ruiri/Rwarera", "Timau"]),
        ("Igembe Central", ["Akirang'ondu", "Athiru Gaiti", "Igembe", "Kangeta", "Njia"]),
        ("Igembe North", ["Antuambui", "Antubetwe Kiongo", "Ntunene", "Igembe North"]),
        ("Igembe South", ["Akachiu", "Kanuni", "Kiegoi/Antubochiu", "Maua"]),
        ("Imenti Central",["Abothuguchi Central", "Abothuguchi West", "Kibirichia", "Mitunguu"]),
        ("Imenti North", ["Buuri", "Municipality", "Ntima East", "Ntima West"]),
        ("Imenti South", ["Igoji East", "Igoji West", "South Imenti", "Abogeta East", "Abogeta West"]),
        ("Tigania East", ["Athwana", "Akithi", "Karama", "Kiguchwa", "Mikinduri", "Mutuati"]),
        ("Tigania West", ["Athiru Ruujine", "Mbeu", "Thangatha", "Tigania West"]),
    ],
    "Tharaka-Nithi": [
        ("Chuka/Igambang'ombe", ["Aguthi/Gaaki", "Karingani", "Magumoni", "Mugwe", "Igambang'ombe"]),
        ("Maara",        ["Chiakariga", "Ganga", "Maara", "Mwimbi", "Nkuene"]),
        ("Tharaka North",["Gatunga", "Mukothima", "Nkuene", "Tharaka"]),
        ("Tharaka South",["Marimanti", "Tharaka South"]),
    ],
    "Embu": [
        ("Manyatta",     ["Baranga", "Bindi", "Kirimari", "Manyatta A", "Manyatta B"]),
        ("Mbeere North", ["Gachoka", "Kiambere", "Makima", "Mbeti North"]),
        ("Mbeere South", ["Mbeti South", "Mwea", "Ndagani", "Nthawa"]),
        ("Runyenjes",    ["Gaturi South", "Kyeni North", "Kyeni South", "Runyenjes Central"]),
    ],
    "Kitui": [
        ("Kitui Central",["Kyangwithya East", "Kyangwithya West", "Mulango", "Nzambani"]),
        ("Kitui East",   ["Kwa Mutonga/Kithumula", "Mumoni", "Nuu", "Tseikuru"]),
        ("Kitui Rural",  ["Kalungu", "Kanyangi", "Kisasi", "Muumandu"]),
        ("Kitui South",  ["Ikanga/Kyatune", "Mutomo", "Nguni", "Zombe/Mwitika"]),
        ("Kitui West",   ["Kauwi", "Matiny'ani", "Muvuti/Kiambani", "Nguumo"]),
        ("Mwingi Central",["Kyuso", "Mwingi Central", "Mwingi East", "Ngomeni", "Nuu"]),
        ("Mwingi North", ["Kyuso", "Mwingi North", "Tharaka"]),
        ("Mwingi West",  ["Migwani", "Nguutani", "Tia"]),
    ],
    "Machakos": [
        ("Kathiani",     ["Kathiani Central", "Lower Kaewa/Kaewa", "Mitaboni", "Upper Kaewa"]),
        ("Machakos Town",["Mua", "Mutituni", "Syokimau/Mulolongo", "Township"]),
        ("Masinga",      ["Ekalakala", "Masinga Central", "Muthesya", "Ndithini", "Kivaa"]),
        ("Matungulu",    ["Kibauni", "Matungulu East", "Matungulu North", "Matungulu West", "Tala"]),
        ("Mavoko",       ["Athi River", "Kinanie", "Muthwani", "Syokimau/Mulolongo"]),
        ("Mwala",        ["Mbiuni", "Mwala", "Machakos/Kalama", "Yatta"]),
        ("Yatta",        ["Katangi", "Ndalani", "Ngomeni", "Yatta"]),
    ],
    "Makueni": [
        ("Kaiti",        ["Ilima", "Kaiti", "Kalawa", "Mukaa", "Nzaui"]),
        ("Kibwezi East", ["Emali/Mulala", "Kibwezi East", "Masongaleni", "Mtito Andei", "Thange"]),
        ("Kibwezi West", ["Kibwezi West", "Makindu", "Nguumo", "Kikumbulyu North", "Kikumbulyu South"]),
        ("Kilome",       ["Kasikeu", "Kilome", "Mukaa", "Nzaui"]),
        ("Makueni",      ["Kathonzweni", "Muvau/Kikumini", "Nzaui", "Ukia"]),
        ("Mbooni",       ["Kiima Kiu/Kalanzoni", "Mbooni", "Nzawi", "Tulimani"]),
    ],
    "Nyandarua": [
        ("Kinangop",     ["Gathara", "Githabai", "Geta", "Kanjuiri Ridge", "Magumu", "Murungaru"]),
        ("Kipipiri",     ["Geta", "Kipipiri", "Mirangine", "Wanjohi"]),
        ("Ndaragwa",     ["Leshau/Pondo", "Ndaragwa", "North Kinangop", "Shamata"]),
        ("Ol Kalou",     ["Gathanji", "Gatimu", "Karau", "Kiru", "Ol Kalou", "Rurii"]),
        ("Oljoro Orok",  ["Engineer", "Oljoro Orok", "Murungaru", "Weru"]),
    ],
    "Nyeri": [
        ("Kieni East",   ["Gatarakwa", "Mweiga", "Naromoru/Kiamathaga", "Thegu River"]),
        ("Kieni West",   ["Chinga", "Gakawa", "Kabaru", "Mweiga"]),
        ("Mathira East", ["Karatina Town", "Mahiga", "Iria-ini", "Tetu"]),
        ("Mathira West", ["Iriani", "Mukurweini", "Ruguru", "Kirimukuyu"]),
        ("Mukurweini",   ["Gikondi", "Mukurweini South", "Rugi", "Aguthi"]),
        ("Nyeri Town",   ["Gatitu/Muruguru", "Kiganjo/Mathari", "Rware", "Ruring'u"]),
        ("Tetu",         ["Dedan Kimathi", "Wamagana", "Aguthi-Gaaki", "Chinga"]),
    ],
    "Kirinyaga": [
        ("Kirinyaga Central",["Baragwi", "Kabare", "Kerugoya", "Mutira"]),
        ("Kirinyaga East",   ["Gichugu", "Ndia", "Ngariama", "Karumandi"]),
        ("Kirinyaga West",   ["Mukure", "Mutithi", "Kangai"]),
        ("Mwea East",        ["Thiba", "Tebere", "Nyangati", "Murinduko"]),
        ("Mwea West",        ["Gathigiriri", "Wamumu", "Tebere", "Kangai"]),
    ],
    "Murang'a": [
        ("Gatanga",      ["Ithanga", "Kakuzi/Mitubiri", "Mugumo-ini", "Ng'ang'a", "Ngoliba"]),
        ("Kahuro",       ["Gaichanjiru", "Kahuro", "Mugoiri", "Wangu"]),
        ("Kandara",      ["Gaturi North", "Gaturi South", "Kandara", "Muruka", "Ng'araria"]),
        ("Kangema",      ["Kanyenyaini", "Muguru", "Rwathia"]),
        ("Kigumo",       ["Kahumbu", "Kigumo", "Muthithi", "Township"]),
        ("Kiharu",       ["Gaturi South", "Ithiru", "Mukangu", "Wiumiririe"]),
        ("Mathioya",     ["Gitugi", "Kiru", "Kamacharia"]),
        ("Murang'a South",["Kimorori/Mwangi", "Makuyu", "Mbiri", "Township"]),
    ],
    "Kiambu": [
        ("Githunguri",   ["Githunguri", "Githiga", "Ikinu", "Ngewa", "Komothai"]),
        ("Kabete",       ["Gitaru", "Kabete", "Muguga", "Nyadhuna", "Uthiru"]),
        ("Kiambaa",      ["Cianda", "Karuri", "Kihara", "Ndenderu", "Township"]),
        ("Kiambu",       ["Kiambu Town", "Ndumberi", "Riabai", "Township"]),
        ("Kikuyu",       ["Karai", "Kikuyu", "Kinoo", "Ndeiya", "Sigona"]),
        ("Lari",         ["Bibirioni", "Lari/Kirenga", "Nyanduma", "Kinale", "Kijabe"]),
        ("Limuru",       ["Bibirioni", "Limuru Central", "Limuru East", "Limuru West", "Ndeiya", "Ngecha/Tigoni"]),
        ("Ruiru",        ["Gitothua", "Kahawa Wendani", "Mwiki", "Ruiru", "Theta"]),
        ("Thika Town",   ["Kamenu", "Gatuanyaga", "Ngoliba", "Township"]),
    ],
    "Turkana": [
        ("Kibish",       ["Kibish", "Nauyapong", "Lapur"]),
        ("Loima",        ["Loima", "Nakwamoru", "Nadapal", "Turkwel"]),
        ("Turkana Central",["Kerio Delta", "Lodwar Township", "Nawoitorong", "Kanamkemer"]),
        ("Turkana East", ["Katilu", "Lokiriama/Lorengippi", "Turkana East"]),
        ("Turkana North",["Kaeris", "Lakezone", "Lapur", "Turkana North"]),
        ("Turkana South",["Kalokol", "Kerio Delta", "Lokichar", "Turkana South"]),
        ("Turkana West", ["Kalobeyei", "Kakuma", "Lokichoggio", "Turkana West"]),
    ],
    "West Pokot": [
        ("Central Pokot",["Batei", "Lelan", "Sook", "Central Pokot"]),
        ("Kacheliba",    ["Alale", "Kacheliba", "Kasei", "Kodich"]),
        ("Kapenguria",   ["Kapenguria", "Masool", "Mnagei", "Riwo", "Siyoi"]),
        ("Pokot South",  ["Chepareria", "Kodich", "Pokot South", "Tapach"]),
    ],
    "Samburu": [
        ("Samburu East", ["Archer's Post", "El Barta", "Wamba East", "Wamba North", "Wamba West"]),
        ("Samburu North",["Angata Nanyokie", "Loosuk", "Nyiro", "Samburu North"]),
        ("Samburu West", ["Kirisia", "Lodokejek", "Maralal", "Poro", "Suguta Marmar"]),
    ],
    "Trans-Nzoia": [
        ("Cherangany",   ["Cherangany", "Kaplamai", "Motosiet", "Sigor", "Sinyereri"]),
        ("Endebess",     ["Endebess", "Matumbei", "Chepchoina"]),
        ("Kiminini",     ["Kiminini", "Sikhendu", "North Kiminini", "Township"]),
        ("Kwanza",       ["Kwanza", "Keiyo", "South Kwanza", "Bidii"]),
        ("Saboti",       ["Kinyoro", "Matisi", "Saboti", "Tuwani"]),
    ],
    "Uasin Gishu": [
        ("Ainabkoi",     ["Ainabkoi/Olare", "Kapsoya", "Kimumu"]),
        ("Kapseret",     ["County Council", "Kapseret", "Langas", "Ngeria"]),
        ("Kesses",       ["Kesses", "Megun", "Ziwa"]),
        ("Moiben",       ["Moiben", "Ondiek/Ngenyilel", "Soy", "Sergoit"]),
        ("Soy",          ["Kuinet/Kapsengere", "Moi's Bridge", "Soy", "Ziwa"]),
        ("Turbo",        ["Huruma", "Ngeria", "Tapsagoi", "Turbo"]),
    ],
    "Elgeyo-Marakwet": [
        ("Keiyo North",  ["Emsoo", "Kamariny", "Keiyo North", "Lelan"]),
        ("Keiyo South",  ["Arror", "Chepkorio", "Keiyo South", "Tambach"]),
        ("Marakwet East",["Embobut/Embulot", "Endo", "Marakwet East", "Soy North"]),
        ("Marakwet West",["Lelan", "Marakwet West", "Ng'elecha", "Kapyego"]),
    ],
    "Nandi": [
        ("Aldai",        ["Kemeloi-Maraba", "Kobujoi", "Kaptumo-Kaboi", "Nandi Hills", "Ol'lessos"]),
        ("Chesumei",     ["Chepterwai", "Koyo-Ndurio", "Ngechek", "Ng'etunyi", "Songhor/Soba"]),
        ("Emgwen",       ["Chemundu/Kapng'etuny", "Chepkumia", "Kapsimotwa", "Kilibwoni", "Nandi Hills"]),
        ("Mosop",        ["Kabisaga", "Kabiyet", "Ndalat", "Ngechek", "Ngenyilel"]),
        ("Tinderet",     ["Tinderet", "Songhor/Soba", "Chombek", "Kipsaos"]),
        ("Nandi Hills",  ["Kaptinga", "Kobujoi", "Nandi Hills", "Ol'lessos"]),
    ],
    "Baringo": [
        ("Baringo Central",["Kabarnet", "Kapropita", "Marigat", "Sacho", "Tenges"]),
        ("Baringo North",  ["Bartabwa", "Baringo North", "Saimo/Soi", "Saimo/Kipsaraman"]),
        ("Baringo South",  ["Baringo South", "Eldama Ravine", "Koibatek", "Mogotio"]),
        ("East Pokot",     ["Churo/Amaya", "East Pokot", "Mochongoi", "Ribkwo", "Silale"]),
        ("Mogotio",        ["Mogotio", "Emining", "Kisanana"]),
        ("Tiaty",          ["Churo/Amaya", "Silale", "Tangulbei/Korossi", "Tiaty East", "Tiaty West"]),
    ],
    "Laikipia": [
        ("Laikipia East",  ["Engage", "Laikipia East", "Ngobit", "Tigithi"]),
        ("Laikipia North", ["Laikipia North", "Mukogodo East", "Mukogodo West"]),
        ("Laikipia West",  ["Githiga", "Kinamba", "Laikipia West", "Marmanet", "Umande"]),
        ("Nanyuki",        ["Nanyuki", "Naibor", "Thingithu"]),
    ],
    "Nakuru": [
        ("Bahati",         ["Bahati", "Dundori", "Kabatini", "Kiamaina", "Lanet/Umoja"]),
        ("Gilgil",         ["Eburru/Mau Narok", "Elementaita", "Gilgil", "Malewa West", "Mbaruk/Eburu"]),
        ("Kuresoi North",  ["Kuresoi North", "Nyota", "Olenguruone"]),
        ("Kuresoi South",  ["Kiptororo", "Kuresoi South", "Maela", "Sirikwa"]),
        ("Molo",           ["Elburgon", "Mariashoni", "Molo", "Turi"]),
        ("Naivasha",       ["Biashara", "Hells Gate", "Lake View", "Mai Mahiu", "Mai-Ella", "Naivasha East", "Viwandani"]),
        ("Nakuru Town East",["Biashara", "Kivumbini", "Menengai", "Nakuru East"]),
        ("Nakuru Town West",["Barut", "London", "Nakuru West", "Shauri Yako"]),
        ("Njoro",          ["Lare", "Mau Narok", "Mauche", "Nakuru East", "Njoro"]),
        ("Rongai",         ["Menengai West", "Mosop", "Rongai", "Soin"]),
        ("Subukia",        ["Kabazi", "Subukia", "Waseges"]),
    ],
    "Narok": [
        ("Kilgoris",       ["Keyian", "Kilgoris Central", "Kimintet", "Lolgorian", "Shankoe"]),
        ("Narok East",     ["Keekonyokie", "Mosiro", "Olpusimoru", "Suswa"]),
        ("Narok North",    ["Melili", "Narok Town", "Nkareta", "Olokurto"]),
        ("Narok South",    ["Majimoto/Naroosura", "Mara", "Narok South", "Ntulele", "Ololulung'a"]),
        ("Narok West",     ["Ilkisonko", "Mara", "Narok West", "Ololulung'a", "Ol Purkel"]),
        ("Transmara East", ["Kimintet", "Lolgorian", "Mara", "Transmara East"]),
        ("Transmara West", ["Isuria", "Kilgoris", "Lolgorian", "Transmara West"]),
    ],
    "Kajiado": [
        ("Kajiado Central",["Dalalekutuk", "Kajiado Central", "Matapato North", "Matapato South", "Purko"]),
        ("Kajiado East",   ["Imaroro", "Kajiado East", "Keekonyokie", "Oloosirkon/Sholinke"]),
        ("Kajiado North",  ["Ildamat", "Kajiado North", "Keekonyokie", "Ngong"]),
        ("Kajiado South",  ["Iloodokilani", "Kajiado South", "Loitokitok", "Mbirikani/Eselenkei"]),
        ("Kajiado West",   ["Keekonyokie", "Magadi", "Mosiro", "Kajiado West"]),
    ],
    "Kericho": [
        ("Ainamoi",        ["Ainamoi", "Kericho East", "Kericho West", "Kipchebor", "Kipkenyo"]),
        ("Belgut",         ["Belgut", "Chaik", "Kabianga", "Kapsoit", "Waldai"]),
        ("Bureti",         ["Cheplanget", "Kapkatet", "Litein", "Roret", "Tebesonik"]),
        ("Kipkelion East", ["Chepseon", "Kipkelion", "Londiani", "Tendeno/Sorget"]),
        ("Kipkelion West", ["Chilchila", "Kipkelion West", "Kunyak", "Sigor"]),
        ("Sigowet/Soin",   ["Soin", "Sigowet", "Kamasian", "Beru"]),
    ],
    "Bomet": [
        ("Bomet Central",  ["Bomet Central", "Kembu", "Mutarakwa", "Ndaraweta", "Sigor"]),
        ("Bomet East",     ["Bomet East", "Chesoen", "Kipreres", "Singorwet"]),
        ("Chepalungu",     ["Chepalungu", "Kaplong", "Kongasis", "Merigi"]),
        ("Konoin",         ["Chesubet", "Embomos", "Kipreres", "Konoin", "Merigi"]),
        ("Sotik",          ["Ndanai/Abosi", "Sotik", "Tabaka"]),
    ],
    "Kakamega": [
        ("Butere",         ["Butere", "Esumeyia", "Khumusalaba", "Marama Central", "Marama North", "Marama South", "Marama West"]),
        ("Ikolomani",      ["Ingotse-Matungu", "Isukha Central", "Isukha East", "Isukha North", "Isukha South"]),
        ("Khwisero",       ["East Kabras", "Khwisero", "Murhanda", "West Kabras"]),
        ("Lugari",         ["Chekalini", "East Kabras", "Lugari", "Mautuma", "Moi's Bridge"]),
        ("Lurambi",        ["Butsotso Central", "Butsotso East", "Butsotso South", "Mahiakalo", "Sheywe"]),
        ("Malava",         ["Chemuche", "East Kabras", "Malava", "Manda-Shivanga", "Shirugu-Mugai", "South Kabras"]),
        ("Matungu",        ["Koyonzo", "Matungu", "Musanda", "Namamali"]),
        ("Mumias East",    ["Mumias East", "Musanda", "Mumias Central", "East Wanga"]),
        ("Mumias West",    ["Etenje", "Mumias West", "Musanda", "Mumias Central"]),
        ("Navakholo",      ["Bunyala Central", "Bunyala East", "Bunyala West", "Navakholo"]),
        ("Shinyalu",       ["Ileho", "Murhanda", "Shieywe", "Shinyalu", "Butsotso North"]),
    ],
    "Vihiga": [
        ("Emuhaya",        ["Emuhaya", "Emukangu", "North Maragoli", "Wemilabi"]),
        ("Hamisi",         ["Banja", "Gisambai", "Hamisi", "Shiru", "Tambua"]),
        ("Luanda",         ["Bunyore Central", "Bunyore East", "Bunyore West", "Luanda", "Wemilabi"]),
        ("Sabatia",        ["Chavakali", "North Maragoli", "Sabatia", "Vihiga", "West Maragoli", "Wodanga"]),
        ("Vihiga",         ["Emmaville", "Luanda", "Vihiga", "Wodanga"]),
    ],
    "Bungoma": [
        ("Bumula",         ["Bumula", "Bunyala East", "Khasoko", "Kabuyefwe", "Kalama", "Kimaeti", "Namwela"]),
        ("Kabuchai",       ["Kabuchai/Chwele", "Bokoli", "Ndivisi", "West Nalondo"]),
        ("Kanduyi",        ["Bukembe East", "Bukembe West", "Hospital", "Khalaba", "Musikoma", "Township"]),
        ("Kimilili",       ["Kibingei", "Kimilili", "Maeni", "Kamukuywa"]),
        ("Mt. Elgon",      ["Cheptais", "Chesikaki", "Chepyuk", "Kopsiro", "Kaptama"]),
        ("Sirisia",        ["Lwandanyi", "Malakisi/South Kulisiru", "Namwela", "Sirisia"]),
        ("Tongaren",       ["Tongaren", "Milima", "Naitiri/Kabuyefwe", "Ndalu/Tabani"]),
        ("Webuye East",    ["Maraka", "Mihuu", "Ndivisi", "Webuye East"]),
        ("Webuye West",    ["Chwele", "Misikhu", "Sitikho", "Webuye West"]),
    ],
    "Busia": [
        ("Butula",         ["Butula", "Elugulu", "Namboboto Nambuku", "Nangubo", "West Bunyala"]),
        ("Funyula",        ["Funyula", "Mukhweya", "North Bunyala", "Namboboto Nambuku"]),
        ("Nambale",        ["Nambale Central", "Nambale Magosi", "Bukhayo North", "Bukhayo Central"]),
        ("Samia",          ["Ageng'a Nanguba", "Bunyala Central", "Bunyala East", "Bunyala West"]),
        ("Teso North",     ["Chakol North", "Chakol South", "Malaba Central", "Teso North"]),
        ("Teso South",     ["Ang'urai North", "Ang'urai South", "Busia Central", "Malaba North", "Township"]),
    ],
    "Siaya": [
        ("Alego Usonga",   ["Alego West", "Central Alego", "North Alego", "Siaya Township", "South East Alego", "Usonga"]),
        ("Bondo",          ["Bondo Central", "Got Regea", "Kabonyo/Kanyagwal", "Nyamila", "Usigu"]),
        ("Gem",            ["Central Gem", "East Gem", "North Gem", "Sirembe", "Yala Township"]),
        ("Rarieda",        ["East Asembo", "North Uyoma", "Uyoma", "West Asembo"]),
        ("Ugenya",         ["East Ugenya", "Ugenya Central", "Ukwala", "West Ugenya"]),
        ("Ugunja",         ["Sidindi", "Sigomre", "Ugunja"]),
    ],
    "Kisumu": [
        ("Kisumu Central", ["Kisumu Central", "Kisumu North", "Kisumu South", "Market Milimani", "Shaurimoyo Kaloleni"]),
        ("Kisumu East",    ["Kajulu", "Kolwa Central", "Kolwa East", "Manyatta B", "Nyalenda A", "Nyalenda B"]),
        ("Kisumu West",    ["Central Kisumu", "Kisumu North", "North West Kisumu", "South West Kisumu"]),
        ("Muhoroni",       ["Chemelil/Songhor", "Miwani", "Muhoroni/Koru", "Ombeyi", "West Kano"]),
        ("Nyakach",        ["Central Nyakach", "East Nyakach", "North Nyakach", "South Nyakach", "West Nyakach"]),
        ("Nyando",         ["Awasi/Ohumba", "Kochogo", "Kobura", "Lower Nyakach"]),
        ("Seme",           ["Central Seme", "East Seme", "North Seme", "West Seme"]),
    ],
    "Homa Bay": [
        ("Gwasi",          ["Gwasi North", "Gwasi South", "Kaksingri West", "Magunga"]),
        ("Homa Bay Town",  ["Homa Bay Central", "Homa Bay Arujo", "Homa Bay East", "Homa Bay West", "Kanyadhiang"]),
        ("Kabondo Kasipul",["East Kamagak", "Kabondo East", "Kabondo West", "West Kamagak"]),
        ("Karachuonyo",    ["Central Karachuonyo", "Kabwoch", "Kanyaluo", "Kibiri", "North Karachuonyo"]),
        ("Kasipul",        ["Central Kasipul", "East Kasipul", "Kasipul", "Kochia", "West Kasipul"]),
        ("Mbita",          ["Mfangano Island", "Mbita", "Rusinga Island", "Sindo"]),
        ("Ndhiwa",         ["Kanyikela", "Kabuoch North", "Kabuoch South/Pala", "Ndhiwa", "Oyugis"]),
        ("Rangwe",         ["Central Karachuonyo", "East Gem", "North Rangwe", "West Gem"]),
        ("Suba",           ["Gembe", "Gwassi", "Mfangano Island", "Rusinga Island", "Suba"]),
    ],
    "Migori": [
        ("Awendo",         ["Central Sakwa", "Kadibo", "North Sakwa", "South Sakwa", "West Sakwa"]),
        ("Kuria East",     ["Kuria East", "Nyabasi East", "Nyabasi West"]),
        ("Kuria West",     ["Isibania", "Kuria West", "Masaba", "Tagare", "Wiga"]),
        ("Mabera",         ["Mabera", "Ntimaru East", "Ntimaru West", "Nyabasi East"]),
        ("Nyatike",        ["Kachieng", "Karungu", "Kanyasa", "North Kadem", "Nyatike", "Sori"]),
        ("Rongo",          ["North Kamagambo", "Central Kamagambo", "East Kamagambo", "Rongo Central", "South Kamagambo"]),
        ("Suna East",      ["Kakrao", "Kwa", "Manyatta", "Migori Town", "Suna East"]),
        ("Suna West",      ["God Jope", "Suna West", "Waregi"]),
        ("Uriri",          ["Central Kamagambo", "North Uriri", "South Uriri", "West Kanyamkago"]),
    ],
    "Kisii": [
        ("Bobasi",         ["Bobasi Central", "Bobasi Chache", "Bogiakumu", "Masige East", "Masige West", "Nyacheki"]),
        ("Bomachoge Borabu",["Boochi/Tendere", "Boochi/Borabu", "Bomachoge Borabu", "Moticho", "Riana"]),
        ("Bomachoge Chache",["Iranda", "Getenga", "Masige West", "Magenche"]),
        ("Bonchari",       ["Bomariba", "Bogiakumu", "Bomorenda", "Rigoma"]),
        ("Kitutu Chache North",["Keumbu", "Kegati", "Monyerero", "Sensi", "Nyaribari Masaba"]),
        ("Kitutu Chache South",["Boikang'a", "Kitutu Chache", "Masimba"]),
        ("Nyaribari Chache",["Ichuni", "Mwembe", "Rioma", "Suneka"]),
        ("Nyaribari Masaba",["Bobaracho", "Kiamokama", "Masaba", "Nyanchwa", "Riana"]),
        ("South Mugirango",["Bokeira", "Magwagwa", "Mumbere", "Nyakoe"]),
    ],
    "Nyamira": [
        ("Borabu",         ["Borabu", "Getenga", "Magwagwa", "Metembe", "Nyansiongo"]),
        ("Manga",          ["Gesima", "Manga", "Nyansiongo", "Tombe"]),
        ("Masaba North",   ["Esise", "Masaba North", "Rigona"]),
        ("Nyamira North",  ["Itibo", "Kemera", "Nyansiongo", "Nyamira Town"]),
        ("Nyamira South",  ["Bosamaro", "Gesieka", "Magwagwa", "Nyamira South"]),
    ],
    "Nairobi": [
        ("Dagoretti North",["Gatina", "Kawangware", "Kilimani", "Kinoo", "Mutu-ini"]),
        ("Dagoretti South",["Uthiru/Ruthimitu", "Waithaka", "Riruta", "Woodley/Kenyatta Golf Course"]),
        ("Embakasi Central",["Embakasi", "Kariobangi South", "Kayole Central", "Kayole North", "Kayole South"]),
        ("Embakasi East",  ["Cemetary", "Harambee", "Lower Savannah", "Mwangaza", "Sevani/Embakasi"]),
        ("Embakasi North", ["Dandora Area I", "Dandora Area II", "Dandora Area III", "Dandora Area IV", "Komarock"]),
        ("Embakasi South", ["Kwa Njenga", "Kwa Reuben", "Pipeline", "Shams/Mwangaza"]),
        ("Embakasi West",  ["Kariobangi North", "Kangundo", "Mihang'o", "Utawala"]),
        ("Kamukunji",      ["Eastleighville", "Kamukunji", "Pumwani", "Ngara East"]),
        ("Kasarani",       ["Clay City", "Kasarani", "Mwiki", "Njiru", "Roysambu"]),
        ("Kibra",          ["Laini Saba", "Lindi", "Makina", "Soweto East", "Woodley"]),
        ("Lang'ata",       ["Karen", "Lang'ata", "Mugumoini", "Nairobi West", "South C"]),
        ("Makadara",       ["Harambee", "Hamza/Maringo", "Makadara", "Viwandani"]),
        ("Mathare",        ["Hospital", "Huruma", "Kiamaiko", "Mabatini", "Mathare North", "Ngei"]),
        ("Roysambu",       ["Githurai", "Kahawa West", "Mwihoko", "Roysambu", "Zimmerman"]),
        ("Ruaraka",        ["Baba Dogo", "Githurai", "Korogocho", "Lucky Summer", "Mathare North", "Utalii"]),
        ("Starehe",        ["Eastleighville", "Nairobi Central", "Ngara", "Pangani", "Ziwani/Kariokor"]),
        ("Westlands",      ["Kangemi", "Mountain View", "Parklands/Highridge", "Sarang'ombe", "Westlands"]),
    ],
}


class Command(BaseCommand):
    help = "Seed all Kenya sub-counties and wards (requires seed_counties to be run first)"

    def handle(self, *args, **options):
        total_sc = 0
        total_w  = 0

        for county_name, subcounties in DATA.items():
            try:
                county = County.objects.get(name=county_name)
            except County.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  SKIP: County '{county_name}' not found"))
                continue

            self.stdout.write(f"\n{county_name}")

            for sc_name, wards in subcounties:
                sc, sc_created = SubCounty.objects.get_or_create(
                    name=sc_name, county=county,
                    defaults={"is_active": True},
                )
                if sc_created:
                    total_sc += 1
                    self.stdout.write(f"  + SubCounty: {sc_name}")

                for ward_name in wards:
                    w, w_created = Ward.objects.get_or_create(
                        name=ward_name, sub_county=sc,
                        defaults={"is_active": True},
                    )
                    if w_created:
                        total_w += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Done. {total_sc} sub-counties, {total_w} wards seeded."
        ))