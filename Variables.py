import datetime

current_year = datetime.datetime.now().year

nationality_contry_code = [
    ("Afghan", "+93"),
    ("Albanian", "+355"),
    ("Algerian", "+213"),
    ("American", "+1"),
    ("Andorran", "+376"),
    ("Angolan", "+244"),
    ("Antiguan", "+1-268"),
    ("Argentine", "+54"),
    ("Armenian", "+374"),
    ("Australian", "+61"),
    ("Austrian", "+43"),
    ("Azerbaijani", "+994"),
    ("Bahamian", "+1-242"),
    ("Bahraini", "+973"),
    ("Bangladeshi", "+880"),
    ("Barbadian", "+1-246"),
    ("Barbudan", "+1-268"),
    ("Batswana", "+267"),
    ("Belarusian", "+375"),
    ("Belgian", "+32"),
    ("Belizean", "+501"),
    ("Beninese", "+229"),
    ("Bhutanese", "+975"),
    ("Bolivian", "+591"),
    ("Bosnian", "+387"),
    ("Brazilian", "+55"),
    ("Bruneian", "+673"),
    ("Bulgarian", "+359"),
    ("Burkinabe", "+226"),
    ("Burmese", "+95"),
    ("Burundian", "+257"),
    ("Cambodian", "+855"),
    ("Cameroonian", "+237"),
    ("Canadian", "+1"),
    ("Cape Verdean", "+238"),
    ("Central African", "+236"),
    ("Chadian", "+235"),
    ("Chilean", "+56"),
    ("Chinese", "+86"),
    ("Colombian", "+57"),
    ("Comoran", "+269"),
    ("Congolese", "+242"),
    ("Costa Rican", "+506"),
    ("Croatian", "+385"),
    ("Cuban", "+53"),
    ("Cypriot", "+357"),
    ("Czech", "+420"),
    ("Danish", "+45"),
    ("Djiboutian", "+253"),
    ("Dominican", "+1-767"),
    ("Dutch", "+31"),
    ("East Timorese", "+670"),
    ("Ecuadorean", "+593"),
    ("Egyptian", "+20"),
    ("Emirati", "+971"),
    ("Equatorial Guinean", "+240"),
    ("Eritrean", "+291"),
    ("Estonian", "+372"),
    ("Ethiopian", "+251"),
    ("Fijian", "+679"),
    ("Filipino", "+63"),
    ("Finnish", "+358"),
    ("French", "+33"),
    ("Gabonese", "+241"),
    ("Gambian", "+220"),
    ("Georgian", "+995"),
    ("German", "+49"),
    ("Ghanaian", "+233"),
    ("Greek", "+30"),
    ("Grenadian", "+1-473"),
    ("Guatemalan", "+502"),
    ("Guinea-Bissauan", "+245"),
    ("Guinean", "+224"),
    ("Guyanese", "+592"),
    ("Haitian", "+509"),
    ("Herzegovinian", "+387"),
    ("Honduran", "+504"),
    ("Hungarian", "+36"),
    ("Icelander", "+354"),
    ("Indian", "+91"),
    ("Indonesian", "+62"),
    ("Iranian", "+98"),
    ("Iraqi", "+964"),
    ("Irish", "+353"),
    ("Israeli", "+972"),
    ("Italian", "+39"),
    ("Ivorian", "+225"),
    ("Jamaican", "+1-876"),
    ("Japanese", "+81"),
    ("Jordanian", "+962"),
    ("Kazakhstani", "+7"),
    ("Kenyan", "+254"),
    ("Kiribati", "+686"),
    ("Kuwaiti", "+965"),
    ("Kyrgyz", "+996"),
    ("Laotian", "+856"),
    ("Latvian", "+371"),
    ("Lebanese", "+961"),
    ("Liberian", "+231"),
    ("Libyan", "+218"),
    ("Liechtensteiner", "+423"),
    ("Lithuanian", "+370"),
    ("Luxembourger", "+352"),
    ("Macedonian", "+389"),
    ("Malagasy", "+261"),
    ("Malawian", "+265"),
    ("Malaysian", "+60"),
    ("Maldivian", "+960"),
    ("Malian", "+223"),
    ("Maltese", "+356"),
    ("Marshallese", "+692"),
    ("Mauritanian", "+222"),
    ("Mauritian", "+230"),
    ("Mexican", "+52"),
    ("Micronesian", "+691"),
    ("Moldovan", "+373"),
    ("Monacan", "+377"),
    ("Mongolian", "+976"),
    ("Montenegrin", "+382"),
    ("Moroccan", "+212"),
    ("Mozambican", "+258"),
    ("Namibian", "+264"),
    ("Nauruan", "+674"),
    ("Nepalese", "+977"),
    ("New Zealander", "+64"),
    ("Nicaraguan", "+505"),
    ("Nigerien", "+227"),
    ("Nigerian", "+234"),
    ("Norwegian", "+47"),
    ("Omani", "+968"),
    ("Pakistani", "+92"),
    ("Palauan", "+680"),
    ("Panamanian", "+507"),
    ("Papua New Guinean", "+675"),
    ("Paraguayan", "+595"),
    ("Peruvian", "+51"),
    ("Polish", "+48"),
    ("Portuguese", "+351"),
    ("Qatari", "+974"),
    ("Romanian", "+40"),
    ("Russian", "+7"),
    ("Rwandan", "+250"),
    ("Saint Lucian", "+1-758"),
    ("Saint Vincentian", "+1-784"),
    ("Samoan", "+685"),
    ("San Marinese", "+378"),
    ("Sao Tomean", "+239"),
    ("Saudi", "+966"),
    ("Senegalese", "+221"),
    ("Serbian", "+381"),
    ("Seychellois", "+248"),
    ("Sierra Leonean", "+232"),
    ("Singaporean", "+65"),
    ("Slovak", "+421"),
    ("Slovenian", "+386"),
    ("Solomon Islander", "+677"),
    ("Somali", "+252"),
    ("South African", "+27"),
    ("South Korean", "+82"),
    ("South Sudanese", "+211"),
    ("Spanish", "+34"),
    ("Sri Lankan", "+94"),
    ("Sudanese", "+249"),
    ("Surinamer", "+597"),
    ("Swazi", "+268"),
    ("Swedish", "+46"),
    ("Swiss", "+41"),
    ("Syrian", "+963"),
    ("Taiwanese", "+886"),
    ("Tajik", "+992"),
    ("Tanzanian", "+255"),
    ("Thai", "+66"),
    ("Togolese", "+228"),
    ("Tongan", "+676"),
    ("Trinidadian", "+1-868"),
    ("Tunisian", "+216"),
    ("Turkish", "+90"),
    ("Tuvaluan", "+688"),
    ("Ugandan", "+256"),
    ("Ukrainian", "+380"),
    ("Uruguayan", "+598"),
    ("Uzbekistani", "+998"),
    ("Vanuatuan", "+678"),
    ("Venezuelan", "+58"),
    ("Vietnamese", "+84"),
    ("Yemeni", "+967"),
    ("Zambian", "+260"),
    ("Zimbabwean", "+263")
]
countries = [country[0] for country in nationality_contry_code]

#combobox values for days, month, year
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(day) for day in range(10, 32)]
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

emp_years = [str(year) for year in range(current_year - 60, current_year - 17)]
client_years = [str(year) for year in range(2000, current_year)]
