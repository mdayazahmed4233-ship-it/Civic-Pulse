// ─── Complete Telangana Location Data ───────────────────────────────
// All 33 districts with mandals (blocks) and major streets/colonies
const TELANGANA_DATA = {
  "Adilabad": {
    mandals: ["Adilabad Rural", "Adilabad Urban", "Bazarhatnoor", "Bela", "Bhainsa", "Boath", "Dilawarpur", "Gudihatnoor", "Ichoda", "Indervelli", "Jainath", "Kaddam", "Laxmanchanda", "Manjrath", "Mavala", "Narnoor", "Neradigonda", "Tamsi", "Utnoor"],
    streets: {
      "Adilabad Urban": ["Main Road", "Collector Office Road", "Gandhi Chowk", "Railway Station Road", "Bus Stand Area", "Ashok Nagar", "Ambedkar Colony", "Revenue Colony"],
      "Bhainsa": ["Bhainsa Main Road", "Market Road", "Old Town", "New Colony"],
      "default": ["Main Road", "Colony Road", "Market Area", "Government Quarters"]
    }
  },
  "Bhadradri Kothagudem": {
    mandals: ["Aswapuram", "Bayyaram", "Bhadrachalam", "Burgampahad", "Cherla", "Dammapeta", "Gundala", "Julurpad", "Kothagudem", "Laxmidevipally", "Manuguru", "Mulkalapally", "Palvancha", "Pinapaka", "Sujathanagar", "Tekulapally", "Thirumalayapalem", "Yellandu"],
    streets: {
      "Bhadrachalam": ["Temple Road", "Godavari Ghat Road", "RTC Bus Stand Road", "Old Town", "New Colony", "Sitarampuram"],
      "Kothagudem": ["Main Road", "Singareni Colony", "Power House Road", "Civil Lines"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Hanamkonda": {
    mandals: ["Elkathurthy", "Geesugonda", "Hanamkonda", "Hasanparthy", "Kamalapur", "Parkal", "Rayaparthy", "Sangem", "Shayampet", "Velair", "Wardhannapet"],
    streets: {
      "Hanamkonda": ["Hanamkonda Main Road", "Mulugu Road", "Nakkalagutta", "Subedari", "Chaitanyapuri", "Vidyanagar", "Ramagundam Road", "Station Road", "Warangal Road"],
      "Hasanparthy": ["Hasanparthy Main Road", "NH163", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Hyderabad": {
    mandals: ["Amberpet", "Asifnagar", "Bandlaguda Jagir", "Charminar", "Golconda", "Khairatabad", "Musheerabad", "Nampally", "Secunderabad", "Shaikpet", "Tirumalgiri", "Yakutpura"],
    streets: {
      "Khairatabad": ["Banjara Hills Road No.1", "Banjara Hills Road No.12", "Jubilee Hills Road No.36", "Panjagutta", "Raj Bhavan Road", "Somajiguda", "Ameerpet", "SR Nagar"],
      "Secunderabad": ["MG Road", "SD Road", "Paradise Circle", "SP Road", "James Street", "Bowenpally", "Maredpally", "Trimulgherry"],
      "Charminar": ["Charminar Road", "Laad Bazaar", "Pathar Gatti", "Sultan Shahi", "Shalibanda", "Purana Haveli", "Mir Alam Mandi"],
      "Golconda": ["Golconda Fort Road", "Toli Chowki", "Karwan", "Rethibowli", "Falaknuma"],
      "Musheerabad": ["Musheerabad Main Road", "Kavadiguda", "Narayanguda", "Himayatnagar", "Basheerbagh"],
      "default": ["Main Road", "Colony Road", "Nagar", "Hills Road"]
    }
  },
  "Jagtial": {
    mandals: ["Buggaram", "Dharmapuri", "Gollapelly", "Jagtial", "Kathalapur", "Kodimial", "Koratla", "Mallapur", "Metpally", "Pegadapally", "Raikal", "Sarangapur", "Velgatoor"],
    streets: {
      "Jagtial": ["Main Road", "Collector Office Road", "Bus Stand Road", "Civil Lines", "Ambedkar Colony"],
      "Koratla": ["Koratla Main Road", "Market Road", "NH163"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Jangaon": {
    mandals: ["Bachannapet", "Devaruppula", "Ghanpur Station", "Jangaon", "Kodakandla", "Lingalaghanpur", "Narmetta", "Palakurthi", "Raghunathpally", "Rayavaram", "Regonda", "Tarigoppula", "Zaffergadh"],
    streets: {
      "Jangaon": ["Main Road", "Bus Stand Area", "RTC Colony", "Bhuvanagiri Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Jayashankar Bhupalpally": {
    mandals: ["Bhupalpally", "Chityal", "Eturunagaram", "Ghanpur", "Kataram", "Mahadevpur", "Malharrao", "Mogullapally", "Mulugu", "Palimela", "Regunta", "Tadvai", "Tekumatla", "Venkatapur"],
    streets: {
      "Bhupalpally": ["Main Road", "Bus Stand Road", "Revenue Colony", "Ambedkar Colony"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Jogulamba Gadwal": {
    mandals: ["Alampur", "Attoor", "Dharur", "Gadwal", "Gattu", "Goliyadoddi", "Ieeja", "Itikyal", "Krishna", "Lingal", "Maldakal", "Manopad", "Nagarkurnool", "Waddepally"],
    streets: {
      "Gadwal": ["Gadwal Main Road", "Market Road", "Bus Stand Road", "Old Town"],
      "Alampur": ["Alampur Main Road", "Temple Road", "Colony Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Kamareddy": {
    mandals: ["Banswada", "Bheemgal", "Bhiknoor", "Domakonda", "Ellareddy", "Gandhari", "Jakranpally", "Kamareddy", "Lingampet", "Machareddy", "Madnoor", "Naspur", "Pitlam", "Ramareddy", "Sadashivnagar", "Sarangapur", "Yellareddy"],
    streets: {
      "Kamareddy": ["Main Road", "Bus Stand Road", "Collector Office Road", "Ambedkar Colony"],
      "Banswada": ["Banswada Main Road", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Karimnagar": {
    mandals: ["Choppadandi", "Chigurumamidi", "Elkathurthy", "Gangadhara", "Huzurabad", "Jammikunta", "Karimnagar Rural", "Karimnagar Urban", "Koheda", "Manakondur", "Manthani", "Ramagundam", "Saidapur", "Shankarapatnam", "Thimmapur", "Veenavanka"],
    streets: {
      "Karimnagar Urban": ["Main Road", "Collectorate Road", "Jyothinagar", "Godavarikhani Road", "Ramagundam Road", "SP Road", "Civil Lines", "Kakatiya Circle"],
      "Ramagundam": ["Ramagundam Main Road", "Power House Road", "NTPC Colony", "Old Town"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Khammam": {
    mandals: ["Aswaraopeta", "Balapanur", "Bonakal", "Enkoor", "Kamepalli", "Khammam Rural", "Khammam Urban", "Konijerla", "Kusumanchi", "Madhira", "Mudigonda", "Nelakondapally", "Sattupally", "Singareni", "Thallada", "Wyra"],
    streets: {
      "Khammam Urban": ["Main Road", "Wyra Road", "Kothagudem Road", "Balaji Nagar", "Nehru Nagar", "Bus Stand Area", "Collectorate Road"],
      "Madhira": ["Madhira Main Road", "Market Road", "NH163"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Komaram Bheem Asifabad": {
    mandals: ["Asifabad", "Bejjur", "Dahegaon", "Jainath", "Kaghaznagar", "Kerameri", "Koutala", "Rebbena", "Sirpur (T)", "Sirpur (U)", "Tiryani", "Wankidi"],
    streets: {
      "Asifabad": ["Main Road", "Bus Stand Road", "Revenue Colony"],
      "Kaghaznagar": ["Kaghaznagar Main Road", "Paper Mill Road", "Colony Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Mahabubabad": {
    mandals: ["Bayyaram", "Chintakani", "Curruppagallu", "Dornakal", "Gudur", "Kesamudram", "Khanapur", "Mahabubabad", "Maripeda", "Nellipaka", "Nellikuduru", "Narsimhulapet", "Thorrur"],
    streets: {
      "Mahabubabad": ["Main Road", "Bus Stand Road", "Collector Office Road", "Revenue Colony"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Mahabubnagar": {
    mandals: ["Addakal", "Balanagar", "Bhoothpur", "Chinnachintakunta", "Devarkadra", "Farooqnagar", "Jadcherla", "Koilkonda", "Kosgi", "Mahabubnagar Rural", "Mahabubnagar Urban", "Makthal", "Midjil", "Narayanpet", "Peddamandadi", "Shadadnagar"],
    streets: {
      "Mahabubnagar Urban": ["Main Road", "Collectorate Road", "Bus Stand Road", "Civil Lines", "New Town", "Jadcherla Road"],
      "Jadcherla": ["Jadcherla Main Road", "NH44", "Industrial Area"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Mancherial": {
    mandals: ["Bellampalli", "Bheemini", "Chandrapur", "Chennur", "Dandepally", "Hajipur", "Jaipur", "Luxettipet", "Mancherial", "Mandamarri", "Naspur", "Ramakrishnapur", "Vemulawada"],
    streets: {
      "Mancherial": ["Main Road", "Bus Stand Road", "Bellarpur Road", "Civil Lines"],
      "Bellampalli": ["Bellampalli Main Road", "Coal Mine Road", "Revenue Colony"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Medak": {
    mandals: ["Alladurg", "Andole", "Chegunta", "Dubbak", "Gajwel", "Havelighanpur", "Jogipet", "Kondapur", "Medak", "Narayankhed", "Narsapur", "Papannapet", "Ramayampet", "Shankarampet (A)", "Shankarampet (R)", "Siddipet", "Tekmal", "Toopran", "Yeldurthy"],
    streets: {
      "Medak": ["Main Road", "Cathedral Road", "Bus Stand Area", "Old Town", "Revenue Colony"],
      "Gajwel": ["Gajwel Main Road", "NH161", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Medchal-Malkajgiri": {
    mandals: ["Alwal", "Balanagar", "Bachupally", "Bollaram", "Dundigal-Gandimaisamma", "Ghatkesar", "Keesara", "Kompally", "Malkajgiri", "Medchal", "Quthbullapur", "Suraram", "Uppal"],
    streets: {
      "Malkajgiri": ["Malkajgiri Main Road", "ECIL Road", "Neredmet", "Safilguda", "Kushaiguda", "Lothkunta"],
      "Kompally": ["Kompally Main Road", "Suchitra Circle", "Pragati Nagar", "JNTU Road"],
      "Uppal": ["Uppal Main Road", "Nagole Road", "Habsiguda", "Tarnaka", "Mallapur"],
      "Ghatkesar": ["Ghatkesar Main Road", "LB Nagar Road", "Boduppal", "Pocharam"],
      "default": ["Main Road", "Colony Road", "Nagar", "Circle"]
    }
  },
  "Mulugu": {
    mandals: ["Eturnagaram", "Govindaraopet", "Kannaigudem", "Mangapet", "Mulugu", "Tadvai", "Venkatapur", "Wazeedu"],
    streets: {
      "Mulugu": ["Main Road", "Bus Stand Road", "Revenue Colony"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Nagarkurnool": {
    mandals: ["Achampet", "Amrabad", "Bijnapally", "Bijinapalle", "Bhoothpur", "Charakonda", "Dhanwada", "Kollapur", "Kodair", "Lingal", "Maddur", "Nagarkurnool", "Peddakothapally", "Tadoor", "Telkapally", "Uppununthala", "Veldanda", "Waddepally"],
    streets: {
      "Nagarkurnool": ["Main Road", "Bus Stand Road", "Collectorate Road", "Revenue Colony"],
      "Achampet": ["Achampet Main Road", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Nalgonda": {
    mandals: ["Alair", "Aler", "Bhuvanagiri", "Chandampet", "Choutuppal", "Devarakonda", "Gattu", "Huzurnagar", "Khammam", "Miryalaguda", "Munugodu", "Nalgonda", "Narayanapur", "Nidamanur", "Nereducharla", "Pedda Adisarlpeta", "Ramannapet", "Thipparthi", "Tirumalagiri", "Tungaturthy"],
    streets: {
      "Nalgonda": ["Main Road", "Collectorate Road", "Bus Stand Road", "Civil Lines", "Miryalaguda Road", "Hyderabad Road"],
      "Miryalaguda": ["Miryalaguda Main Road", "Market Road", "Station Road"],
      "Huzurnagar": ["Huzurnagar Main Road", "Suryapet Road", "Market Area"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Narayanpet": {
    mandals: ["Kosgi", "Maddur", "Maganoor", "Marikal", "Narayanpet", "Narva"],
    streets: {
      "Narayanpet": ["Main Road", "Bus Stand Road", "Revenue Colony"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Nirmal": {
    mandals: ["Bhainsa", "Dilawarpur", "Gudihatnoor", "Khanapur", "Kubeer", "Laxmanchanda", "Lokeswaram", "Mamada", "Mudhole", "Narsapur", "Nirmal", "Sarangapur", "Tanoor", "Utnoor"],
    streets: {
      "Nirmal": ["Main Road", "Collectorate Road", "Bus Stand Area", "Revenue Colony"],
      "Bhainsa": ["Bhainsa Main Road", "Market Road", "Old Town"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Nizamabad": {
    mandals: ["Armoor", "Balkonda", "Banswada", "Bheemgal", "Bodhan", "Dichpally", "Domakonda", "Edapally", "Enkoor", "Jakranpally", "Kotgiri", "Lingampet", "Madnoor", "Mortad", "Navipet", "Nizamabad Rural", "Nizamabad Urban", "Pitlam", "Yedpally", "Yellareddy"],
    streets: {
      "Nizamabad Urban": ["Main Road", "Collectorate Road", "Station Road", "Bodhan Road", "Armoor Road", "Civil Lines", "Kumarpally"],
      "Bodhan": ["Bodhan Main Road", "Market Road", "Sugar Factory Road"],
      "Armoor": ["Armoor Main Road", "Market Road", "NH44"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Peddapalli": {
    mandals: ["Anthargaon", "Dharmaram", "Gorrepadu", "Julapally", "Kalwacherthyal", "Karimnagar", "Kathlapur", "Korutla", "Manthani", "Odela", "Peddapalli", "Ramagundam", "Srirampur", "Sultanabad"],
    streets: {
      "Peddapalli": ["Main Road", "Bus Stand Road", "Revenue Colony"],
      "Ramagundam": ["Ramagundam Main Road", "NTPC Colony", "Power House Road", "Station Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Rajanna Sircilla": {
    mandals: ["Boinpally", "Chandurthi", "Chinnakodur", "Eddula", "Elkathurthy", "Gambhiraopet", "Illanthakunta", "Koheda", "Konaraopet", "Mustabad", "Rudrangi", "Sircilla", "Thangallapally", "Vemulawada"],
    streets: {
      "Sircilla": ["Main Road", "Bus Stand Road", "Textile Mill Road", "Revenue Colony", "Market Road"],
      "Vemulawada": ["Vemulawada Main Road", "Temple Road", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Rangareddy": {
    mandals: ["Bandlaguda Jagir", "Chevella", "Farooqnagar", "Ghatkesar", "Hayathnagar", "Ibrahimpatnam", "Kandukur", "Kothur", "Kulkacharla", "Marpally", "Maheswaram", "Manchal", "Meankanur", "Nandigama", "Narsingi", "Rajendranagar", "Saroornagar", "Shamshabad", "Shabad", "Srisailam", "Tandur", "Yacharam"],
    streets: {
      "Rajendranagar": ["Rajendranagar Main Road", "Srinagar Colony", "Attapur", "Kishanbagh", "Mehdipatnam"],
      "Shamshabad": ["Shamshabad Main Road", "Airport Road", "Rajapur", "Kothur Road"],
      "Saroornagar": ["Saroornagar Main Road", "LB Nagar", "Vanasthalipuram", "Dilsukhnagar Road"],
      "Hayathnagar": ["Hayathnagar Main Road", "Nagole Road", "Boduppal Road"],
      "Ibrahimpatnam": ["Ibrahimpatnam Main Road", "Pochampally Road", "Market Road"],
      "default": ["Main Road", "Colony Road", "Nagar", "Road"]
    }
  },
  "Sangareddy": {
    mandals: ["Andole", "Chegunta", "Hasnabad", "Isnapur", "Jogipet", "Kohir", "Kondapur", "Manoor", "Mulugu", "Narayankhed", "Narsapur", "Nyalkal", "Papannapet", "Patancheru", "Pulkal", "Ramachandrapuram", "Sangaredddy", "Sadasivpet", "Ameenpur"],
    streets: {
      "Sangaredddy": ["Main Road", "Bus Stand Road", "Collectorate Road", "Civil Lines", "Patancheru Road"],
      "Patancheru": ["Patancheru Main Road", "APIIC Road", "Industrial Area", "Bollarum Road"],
      "Sadasivpet": ["Sadasivpet Main Road", "Market Road", "NH65"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Siddipet": {
    mandals: ["Cheriyal", "Chinnapotharam", "Doultabad", "Doulthabad", "Dubbak", "Gajwel", "Husnabad", "Komuravelly", "Maddur", "Markook", "Nangnoor", "Raipole", "Siddipet", "Thoguta", "Wargal"],
    streets: {
      "Siddipet": ["Main Road", "Bus Stand Road", "Collectorate Road", "Revenue Colony", "Gajwel Road"],
      "Gajwel": ["Gajwel Main Road", "Market Road", "Hyderabad Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Suryapet": {
    mandals: ["Atmakur", "Chivvemla", "Deverkonda", "Garidepally", "Huzurnagar", "Kodad", "Munagala", "Neredcherla", "Ramannapet", "Suryapet", "Thipparthi", "Tirumalapur"],
    streets: {
      "Suryapet": ["Main Road", "Collectorate Road", "Bus Stand Road", "Market Road", "Hyderabad Road"],
      "Kodad": ["Kodad Main Road", "Market Road", "NH65"],
      "Huzurnagar": ["Huzurnagar Main Road", "Market Area"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Vikarabad": {
    mandals: ["Bantwaram", "Basheerabad", "Bomraspet", "Dharur", "Doulatabad", "Kulkacherla", "Marpally", "Nawabpet", "Pargi", "Pudur", "Tandur", "Vikarabad", "Yalal"],
    streets: {
      "Vikarabad": ["Main Road", "Bus Stand Road", "Market Road", "Revenue Colony"],
      "Tandur": ["Tandur Main Road", "Industrial Area", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Wanaparthy": {
    mandals: ["Amarchinta", "Atmakur", "Bhoothpur", "Ghanpur", "Gopalpet", "Kothakota", "Madanapur", "Peddamandadi", "Pebbair", "Rever", "Srirangapur", "Wanaparthy", "Weepangandla"],
    streets: {
      "Wanaparthy": ["Main Road", "Bus Stand Road", "Market Road", "Revenue Colony"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Warangal": {
    mandals: ["Atmakur", "Chennaraopet", "Dharmasagar", "Duggondi", "Geesugonda", "Hasanparthy", "Khanapur", "Nallabelly", "Parvathagiri", "Shayampet", "Warangal"],
    streets: {
      "Warangal": ["Hanamkonda Road", "Kazipet Road", "Mulugu Road", "Station Road", "Subedari", "Nakkalagutta", "Ramji Junction", "Hanmakonda Main Road"],
      "Hasanparthy": ["Hasanparthy Main Road", "Market Road"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  },
  "Yadadri Bhuvanagiri": {
    mandals: ["Alair", "Bhuvanagiri", "Bibinagar", "Choutuppal", "Damarcherla", "Dameracherla", "Gundlapochampally", "Motakondur", "Mothkur", "Munagala", "Narketpally", "Nereducharla", "Ramannapeta", "Rajapet", "Turkapally", "Yadagirigutta"],
    streets: {
      "Yadagirigutta": ["Temple Road", "Yadadri Main Road", "Pilgrim Road", "Market Road", "Bus Stand Road"],
      "Bhuvanagiri": ["Bhuvanagiri Main Road", "Market Road", "Station Road"],
      "Bibinagar": ["Bibinagar Main Road", "AIIMS Road", "Market Area"],
      "default": ["Main Road", "Colony Road", "Market Area"]
    }
  }
};

// Get all 33 districts
const TELANGANA_DISTRICTS = Object.keys(TELANGANA_DATA);

// Get mandals for a district
function getMandals(district) {
  return TELANGANA_DATA[district]?.mandals || [];
}

// Get streets/localities for a mandal within a district
function getStreets(district, mandal) {
  const streets = TELANGANA_DATA[district]?.streets;
  if (!streets) return ["Main Road", "Colony Road", "Market Area"];
  return streets[mandal] || streets["default"] || ["Main Road", "Colony Road", "Market Area"];
}

// Export for use in HTML (window object)
window.TELANGANA_DATA = TELANGANA_DATA;
window.TELANGANA_DISTRICTS = TELANGANA_DISTRICTS;
window.getMandals = getMandals;
window.getStreets = getStreets;
