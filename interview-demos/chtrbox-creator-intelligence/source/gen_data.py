"""Mock data for the Creator Intelligence Engine demo.

Every creator is a synthetic persona. Brand names are real Chtrbox clients (as publicly reported)
or labelled prospects, but every metric attached to them is simulated. Benchmarks are scaled to
public 2025-26 Indian creator data (tier ER medians, rate ranges) so the numbers look like the market.

    python3 gen_data.py data.json
"""
import json, math, random, sys

R = random.Random(20261021)


def ln(mu=0.0, sigma=0.3):
    return math.exp(R.gauss(mu, sigma))


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def pick(weights):
    """weights: dict key -> weight"""
    tot = sum(weights.values())
    r = R.random() * tot
    for k, w in weights.items():
        r -= w
        if r <= 0:
            return k
    return k


def norm(v):
    s = sum(v)
    return [x / s for x in v]


def jitter_dist(base, sigma=0.18):
    return norm([max(0.001, b * ln(0, sigma)) for b in base])


# ----------------------------------------------------------------------------- taxonomies
NICHES = {
    # key: label, female share, age dist (13-17,18-24,25-34,35-44,45+), er mult, view mult, ctr %, saves %, shares %, affluence, trust
    "beauty":    ("Beauty & Skincare",        .82, [6, 38, 38, 13, 5],  1.05, 1.00, .85, 1.6, .6, .55, 1.05),
    "fashion":   ("Fashion & Style",          .70, [7, 42, 35, 11, 5],  1.00, 1.00, .90, 1.5, .7, .58, 1.00),
    "food":      ("Food & Cooking",           .60, [4, 24, 36, 22, 14], 1.00, 1.10, .60, 2.0, 1.0, .45, 1.05),
    "fitness":   ("Fitness & Wellness",       .48, [3, 30, 42, 17, 8],  1.00, 0.95, .75, 1.4, .6, .55, 1.10),
    "finance":   ("Personal Finance",         .26, [1, 26, 48, 18, 7],  0.80, 0.85, 1.10, 2.4, 1.0, .60, 1.20),
    "tech":      ("Tech & Gadgets",           .20, [8, 40, 36, 11, 5],  0.85, 0.95, 1.00, 1.2, .6, .62, 1.10),
    "comedy":    ("Comedy & Entertainment",   .50, [12, 44, 28, 10, 6], 1.25, 1.35, .35, 0.5, 2.0, .40, 0.85),
    "parenting": ("Parenting & Family",       .78, [1, 12, 52, 28, 7],  1.10, 0.90, .80, 1.1, .8, .50, 1.20),
    "travel":    ("Travel",                   .50, [3, 30, 42, 17, 8],  0.95, 1.05, .60, 1.3, .9, .66, 0.95),
    "lifestyle": ("Lifestyle & Vlogs",        .64, [6, 38, 36, 13, 7],  1.00, 1.00, .65, 0.9, .6, .55, 1.00),
    "gaming":    ("Gaming",                   .14, [22, 50, 21, 5, 2],  1.10, 1.15, .50, 0.5, .8, .42, 0.90),
    "health":    ("Doctors & Dietitians",     .60, [2, 18, 38, 24, 18], 0.90, 0.90, .80, 1.8, .9, .50, 1.30),
    "music":     ("Music & Dance",            .56, [14, 44, 26, 10, 6], 1.15, 1.30, .40, 0.6, 1.2, .40, 0.85),
    "education": ("Education & Careers",      .44, [10, 48, 30, 8, 4],  0.90, 0.90, 1.00, 2.2, .9, .42, 1.15),
    "home":      ("Home & Decor",             .70, [2, 18, 42, 26, 12], 0.95, 0.95, .80, 1.6, .6, .55, 1.05),
    "auto":      ("Auto & Bikes",             .10, [4, 36, 40, 14, 6],  0.85, 1.00, .70, 0.9, .6, .60, 1.00),
}
NICHE_WEIGHT = {"beauty": 14, "fashion": 13, "food": 9, "fitness": 8, "finance": 7, "tech": 7, "comedy": 8,
                "parenting": 6, "travel": 5, "lifestyle": 8, "gaming": 3, "health": 5, "music": 3,
                "education": 3, "home": 3, "auto": 2}
SECONDARY = {
    "beauty": ["fashion", "lifestyle", "health"], "fashion": ["beauty", "lifestyle", "travel"],
    "food": ["lifestyle", "parenting", "travel", "health"], "fitness": ["health", "lifestyle", "food"],
    "finance": ["education", "tech", "lifestyle"], "tech": ["gaming", "education", "auto"],
    "comedy": ["lifestyle", "music", "food"], "parenting": ["food", "home", "health"],
    "travel": ["lifestyle", "food", "fashion"], "lifestyle": ["fashion", "beauty", "travel", "food"],
    "gaming": ["tech", "comedy"], "health": ["fitness", "food", "parenting"], "music": ["comedy", "lifestyle"],
    "education": ["finance", "tech"], "home": ["lifestyle", "parenting"], "auto": ["tech", "travel"],
}

# city, state, tier, content languages (weights), weight
CITIES = [
    ("Mumbai", "Maharashtra", 1, {"Hinglish": 5, "English": 3, "Hindi": 2, "Marathi": 1.2}, 15),
    ("Delhi NCR", "Delhi", 1, {"Hinglish": 5, "Hindi": 3, "English": 2.5}, 15),
    ("Bengaluru", "Karnataka", 1, {"English": 4, "Kannada": 2, "Hinglish": 1.5}, 9),
    ("Hyderabad", "Telangana", 1, {"Telugu": 3.5, "English": 2, "Hinglish": 1}, 6),
    ("Chennai", "Tamil Nadu", 1, {"Tamil": 4, "English": 2}, 6),
    ("Kolkata", "West Bengal", 1, {"Bengali": 3.5, "English": 1.5, "Hinglish": 1}, 5),
    ("Pune", "Maharashtra", 1, {"Marathi": 2, "Hinglish": 2.5, "English": 2}, 4),
    ("Ahmedabad", "Gujarat", 1, {"Gujarati": 3, "Hinglish": 1.5, "Hindi": 1}, 3),
    ("Jaipur", "Rajasthan", 2, {"Hindi": 4, "Hinglish": 2}, 3),
    ("Lucknow", "Uttar Pradesh", 2, {"Hindi": 4.5, "Hinglish": 1.5}, 3),
    ("Indore", "Madhya Pradesh", 2, {"Hindi": 4, "Hinglish": 1.5}, 2.5),
    ("Chandigarh", "Punjab", 2, {"Punjabi": 3, "Hinglish": 2, "Hindi": 1}, 2.5),
    ("Kochi", "Kerala", 2, {"Malayalam": 4, "English": 1.5}, 2.5),
    ("Coimbatore", "Tamil Nadu", 2, {"Tamil": 4.5, "English": 1}, 2),
    ("Surat", "Gujarat", 2, {"Gujarati": 4, "Hindi": 1}, 2),
    ("Nagpur", "Maharashtra", 2, {"Marathi": 3, "Hindi": 2}, 1.5),
    ("Patna", "Bihar", 2, {"Hindi": 5}, 2),
    ("Bhubaneswar", "Odisha", 2, {"Odia": 4, "Hindi": 1, "English": 0.5}, 1.5),
    ("Guwahati", "Assam", 2, {"Assamese": 3, "Hindi": 1.5, "English": 1}, 1.5),
    ("Visakhapatnam", "Andhra Pradesh", 2, {"Telugu": 5}, 1.5),
    ("Ludhiana", "Punjab", 2, {"Punjabi": 4, "Hindi": 1}, 1.2),
    ("Mysuru", "Karnataka", 2, {"Kannada": 4.5, "English": 0.8}, 1),
    ("Dehradun", "Uttarakhand", 2, {"Hindi": 4, "Hinglish": 1}, 1),
    ("Ranchi", "Jharkhand", 3, {"Hindi": 5}, 0.9),
    ("Varanasi", "Uttar Pradesh", 3, {"Hindi": 5}, 0.9),
    ("Madurai", "Tamil Nadu", 3, {"Tamil": 5}, 0.8),
    ("Nashik", "Maharashtra", 3, {"Marathi": 4, "Hindi": 1}, 0.7),
    ("Udaipur", "Rajasthan", 3, {"Hindi": 5}, 0.6),
    ("Thrissur", "Kerala", 3, {"Malayalam": 5}, 0.6),
    ("Siliguri", "West Bengal", 3, {"Bengali": 3, "Hindi": 2}, 0.5),
    ("Kota", "Rajasthan", 3, {"Hindi": 5}, 0.5),
    ("Dubai", "UAE", 0, {"English": 4, "Hinglish": 2.5, "Arabic": 1.2}, 5),
]
REGIONAL = {"Tamil", "Telugu", "Kannada", "Malayalam", "Marathi", "Bengali", "Gujarati", "Punjabi", "Odia", "Assamese"}

CODES = ["Festive & occasions", "Wedding season", "Regional pride", "Gen-Z humour", "Family-first",
         "Aspirational luxury", "Value-seeker", "Desi-modern", "Campus life", "Sustainability", "Fitness-first",
         "Cricket & IPL", "Bollywood pop", "Spiritual & Ayurveda", "Working professional", "Small-town dreams",
         "K-culture", "Science-backed"]
NICHE_CODES = {
    "beauty": {"Festive & occasions": 2, "Wedding season": 2, "K-culture": 2, "Science-backed": 2, "Desi-modern": 1.5, "Aspirational luxury": 1.5, "Value-seeker": 1},
    "fashion": {"Wedding season": 2, "Festive & occasions": 2, "Aspirational luxury": 2, "Gen-Z humour": 1, "Sustainability": 1.5, "Desi-modern": 2, "Value-seeker": 1},
    "food": {"Festive & occasions": 2, "Family-first": 2.5, "Regional pride": 2.5, "Desi-modern": 1, "Value-seeker": 1, "Spiritual & Ayurveda": 1},
    "fitness": {"Fitness-first": 4, "Science-backed": 1.5, "Working professional": 1.5, "Cricket & IPL": 1},
    "finance": {"Working professional": 3, "Value-seeker": 2, "Small-town dreams": 1.5, "Science-backed": 1},
    "tech": {"Working professional": 2, "Gen-Z humour": 1, "Campus life": 2, "Value-seeker": 2, "Cricket & IPL": 1},
    "comedy": {"Gen-Z humour": 4, "Bollywood pop": 2, "Cricket & IPL": 2, "Family-first": 1.5, "Campus life": 1.5, "Small-town dreams": 1.5},
    "parenting": {"Family-first": 4, "Festive & occasions": 1.5, "Science-backed": 1.5, "Value-seeker": 1.5, "Spiritual & Ayurveda": 1},
    "travel": {"Aspirational luxury": 2, "Regional pride": 2, "Desi-modern": 1, "Sustainability": 1},
    "lifestyle": {"Desi-modern": 2, "Aspirational luxury": 1.5, "Working professional": 1.5, "Festive & occasions": 1.5, "Gen-Z humour": 1},
    "gaming": {"Gen-Z humour": 3, "Campus life": 2, "Cricket & IPL": 1},
    "health": {"Science-backed": 4, "Spiritual & Ayurveda": 1.5, "Family-first": 1.5, "Fitness-first": 1.5},
    "music": {"Bollywood pop": 3, "Gen-Z humour": 1.5, "Regional pride": 2, "Wedding season": 1, "Festive & occasions": 1},
    "education": {"Campus life": 3, "Small-town dreams": 2.5, "Working professional": 2},
    "home": {"Festive & occasions": 2, "Family-first": 2, "Sustainability": 1.2, "Aspirational luxury": 1.2},
    "auto": {"Aspirational luxury": 1.5, "Working professional": 1.5, "Small-town dreams": 1, "Gen-Z humour": 1},
}

TIERS = [  # key, label, min, max, share, er median %, view ratio, cpf (₹ per follower per reel), story view rate
    ("nano", "Nano", 3_000, 10_000, .12, 4.9, .36, .26, .12),
    ("micro", "Micro", 10_000, 100_000, .40, 2.8, .28, .21, .09),
    ("mid", "Mid-tier", 100_000, 500_000, .28, 1.4, .22, .20, .07),
    ("macro", "Macro", 500_000, 1_000_000, .12, 0.9, .18, .19, .055),
    ("mega", "Mega", 1_000_000, 8_000_000, .08, 0.4, .13, .15, .04),
]

FIRST = {
    "north": (["Aanya", "Riya", "Simran", "Kavya", "Ishita", "Meher", "Tanvi", "Nikita", "Aditi", "Pooja", "Sakshi", "Mansi", "Shreya", "Kritika", "Avni", "Naina"],
              ["Arjun", "Kabir", "Rohan", "Aditya", "Vivaan", "Karan", "Siddharth", "Yash", "Harsh", "Rahul", "Dhruv", "Aman", "Ishaan", "Varun", "Kunal", "Manav"]),
    "south": (["Ananya", "Divya", "Keerthi", "Lakshmi", "Meera", "Nithya", "Sneha", "Varsha", "Swathi", "Pavithra", "Aparna", "Gayathri", "Anjali", "Sruthi"],
              ["Karthik", "Arun", "Vignesh", "Nikhil", "Sai", "Pranav", "Abhinav", "Harish", "Srinivas", "Akhil", "Rakesh", "Gautham", "Naveen", "Aravind"]),
    "east": (["Ishani", "Moumita", "Rimjhim", "Tanushree", "Priyanka", "Debolina", "Ankita", "Sayani", "Bornali"],
             ["Arnab", "Sourav", "Debayan", "Ritwik", "Subhankar", "Anirban", "Pritam", "Bhaskar"]),
    "west": (["Aarya", "Gauri", "Mitali", "Saloni", "Rutuja", "Krupa", "Dhwani", "Janhvi", "Hetal", "Rasika"],
             ["Omkar", "Parth", "Tejas", "Jay", "Chirag", "Neel", "Sahil", "Hrishikesh", "Devang"]),
    "gulf": (["Zara", "Aisha", "Sana", "Mariam", "Noor", "Rhea", "Alina"],
             ["Omar", "Rehan", "Zayd", "Imran", "Faisal", "Aryan"]),
}
REGION_OF = {"Maharashtra": "west", "Gujarat": "west", "Delhi": "north", "Rajasthan": "north", "Uttar Pradesh": "north",
             "Madhya Pradesh": "north", "Punjab": "north", "Bihar": "east", "Jharkhand": "east", "Uttarakhand": "north",
             "Karnataka": "south", "Telangana": "south", "Tamil Nadu": "south", "Kerala": "south", "Andhra Pradesh": "south",
             "West Bengal": "east", "Odisha": "east", "Assam": "east", "UAE": "gulf"}
INITIALS = "ABCDGJKMNPRSTVY"

COLLAB_POOL = {
    "beauty": ["L'Oréal Paris", "Maybelline", "Minimalist", "The Derma Co", "Plum", "Sugar Cosmetics", "Lakmé", "Neutrogena",
               "COSRX", "Cetaphil", "La Roche-Posay", "Pond's", "Swiss Beauty", "Mamaearth", "Dot & Key", "Innisfree", "Beauty of Joseon"],
    "fashion": ["Zara", "Nike", "Adidas", "Skechers", "Bata", "Lenskart", "Fastrack", "Only", "Vero Moda", "Max Fashion",
                "Bewakoof", "Snitch", "Uniqlo", "Myntra", "Ajio"],
    "food": ["Cadbury", "PepsiCo", "Patanjali", "Haldiram's", "Maggi", "Swiggy", "Zomato", "Blinkit", "Zepto", "Domino's", "Burger King", "KFC"],
    "fitness": ["MuscleBlaze", "OZiva", "Wellbeing Nutrition", "Nike", "Adidas", "HealthifyMe", "boAt", "Noise", "Decathlon"],
    "finance": ["Zerodha", "Upstox", "Angel One", "Paytm Money", "INDmoney", "Jupiter", "Acko", "Ditto Insurance", "Fi Money"],
    "tech": ["Dell", "Lenovo", "Asus", "Apple", "OnePlus", "boAt", "JBL", "Noise", "Xiaomi", "Realme"],
    "comedy": ["Swiggy", "Zomato", "Cadbury", "PepsiCo", "Myntra", "Dream11", "Blinkit", "Spotify", "JioSaavn"],
    "parenting": ["Himalaya", "Mamaearth", "FirstCry", "Pampers", "Johnson's Baby", "Patanjali", "Horlicks"],
    "travel": ["Air India", "Akasa Air", "MakeMyTrip", "Booking.com", "Airbnb", "Lenskart"],
    "lifestyle": ["Myntra", "Ajio", "Nykaa", "Swiggy", "Zomato", "Blinkit", "Sugar Cosmetics", "Fastrack"],
    "gaming": ["Dream11", "Asus", "Lenovo", "OnePlus", "Red Bull", "boAt"],
    "health": ["PharmEasy", "Apollo 24|7", "HealthifyMe", "OZiva", "Kapiva", "Himalaya", "Cetaphil"],
    "music": ["JioSaavn", "YouTube Music", "boAt", "JBL", "PepsiCo"],
    "education": ["Unacademy", "Physics Wallah", "upGrad", "Zerodha", "Dell"],
    "home": ["Pepperfry", "Livspace", "Asian Paints", "IKEA", "LG"],
    "auto": ["Royal Enfield", "Ola Electric", "Ather", "Tata Motors", "MRF"],
}

CRED = {
    "health": [("MBBS doctor", .40), ("Registered dietitian", .25), ("Dermatologist (MD)", .12)],
    "beauty": [("Dermatologist (MD)", .09)],
    "fitness": [("Certified trainer", .35)],
    "finance": [("SEBI-registered RIA", .20), ("SEBI-registered RA", .12), ("Chartered Accountant", .18)],
}

# ----------------------------------------------------------------------------- creators
city_w = {c[0]: c[4] for c in CITIES}
city_by = {c[0]: c for c in CITIES}
used_names = set()


def make_name(region, gender):
    fem, mal = FIRST[region]
    for _ in range(50):
        n = f"{R.choice(fem if gender == 'F' else mal)} {R.choice(INITIALS)}."
        if n not in used_names:
            used_names.add(n)
            return n
    return n


def creator(i):
    niche = pick(NICHE_WEIGHT)
    lab, fem, age, erm, vm, ctr0, saves0, shares0, aff0, trust0 = NICHES[niche]
    city = pick(city_w)
    _, state, ctier, langs, _ = city_by[city]
    region = REGION_OF[state]
    tier = pick({t[0]: t[4] for t in TIERS})
    tk = next(t for t in TIERS if t[0] == tier)
    followers = int(math.exp(R.uniform(math.log(tk[2]), math.log(tk[3]))))
    lang = pick(langs)
    langs2 = [lang]
    if lang in REGIONAL and R.random() < .5:
        langs2.append("English" if R.random() < .5 else "Hinglish")
    elif lang == "Hinglish" and R.random() < .4:
        langs2.append("Hindi")
    elif lang == "English" and R.random() < .3:
        langs2.append("Hinglish")
    cgender = "F" if R.random() < (0.35 + fem * 0.55) else "M"
    second = R.choice(SECONDARY[niche])

    # platform
    pw = {"Instagram": 72, "YouTube": 16, "Moj": 6 if lang in REGIONAL or ctier >= 2 else 1.5,
          "LinkedIn": 6 if niche in ("finance", "education") else 0.3}
    if niche in ("tech", "education", "gaming", "finance", "auto"):
        pw["YouTube"] = 34
    platform = pick(pw)
    er = clamp(tk[5] * erm * ln(0, .33), 0.15, 14)
    view_ratio = tk[6] * vm * ln(0, .32)
    if platform == "YouTube":
        view_ratio *= .55
    views = int(followers * clamp(view_ratio, .03, 1.4))

    # larger accounts carry more bought and inactive followers (consistent with 2025 audit benchmarks)
    fraud = R.random() < {"nano": .06, "micro": .07, "mid": .10, "macro": .14, "mega": .16}[tier]
    cred = clamp(R.gauss(88 - {"nano": 0, "micro": 1, "mid": 3, "macro": 6, "mega": 8}[tier], 4.2), 72, 97)
    if fraud:
        cred = R.uniform(52, 71)
        er *= .62
    growth = []
    f0 = followers / (1 + R.uniform(.04, .28))
    spike = R.randint(5, 10) if fraud else None
    cur = f0
    for m in range(12):
        g = R.uniform(.004, .028)
        if spike is not None and m == spike:
            g = R.uniform(.22, .48)
        cur = cur * (1 + g)
        growth.append(int(cur))
    scale = followers / growth[-1]
    growth = [int(x * scale) for x in growth]
    growth90 = round((growth[-1] / growth[-4] - 1) * 100, 1)

    # audience
    a_fem = clamp(fem + R.gauss(0, .07) + (.04 if cgender == "F" else -.04), .04, .97)
    a_age = jitter_dist(age, .2)
    if lang in REGIONAL:
        t3 = [.26, .40, .34]
    elif ctier == 1 and lang == "English":
        t3 = [.62, .28, .10]
    elif ctier == 1:
        t3 = [.46, .35, .19]
    elif ctier == 2:
        t3 = [.31, .42, .27]
    elif ctier == 3:
        t3 = [.19, .39, .42]
    else:
        t3 = [.58, .30, .12]
    a_tiers = jitter_dist(t3, .15)
    affl = clamp(aff0 + (.08 if lang == "English" else 0) + (.05 if ctier == 1 else -.05 if ctier == 3 else 0)
                 + R.gauss(0, .06), .15, .92)
    market = "UAE" if city == "Dubai" else "India"
    if market == "UAE":
        geo = [("UAE", R.uniform(.48, .64)), ("India", R.uniform(.2, .32)), ("Other GCC", R.uniform(.08, .16))]
    else:
        same_state = [c for c in CITIES if c[1] == state and c[0] != city]
        geo = [(city, R.uniform(.12, .26))]
        for c in R.sample([c for c in CITIES if c[0] not in (city, "Dubai")], 3):
            geo.append((c[0], R.uniform(.03, .1)))
        if same_state:
            geo.insert(1, (same_state[0][0], R.uniform(.05, .12)))
    tot = sum(g[1] for g in geo)
    k = min(1.0, .92 / tot)
    geo = [(g[0], round(g[1] * k * 100, 1)) for g in geo][:5]
    a_langs = {lang: round(R.uniform(.55, .8), 2)}
    for l2 in langs2[1:]:
        a_langs[l2] = round(R.uniform(.15, .3), 2)

    codes = set()
    cw = dict(NICHE_CODES[niche])
    if lang in REGIONAL:
        cw["Regional pride"] = cw.get("Regional pride", 0) + 3
    if ctier >= 2:
        cw["Small-town dreams"] = cw.get("Small-town dreams", 0) + 1.5
        cw["Value-seeker"] = cw.get("Value-seeker", 0) + 1
    if a_age[1] > .42:
        cw["Campus life"] = cw.get("Campus life", 0) + 1.5
        cw["Gen-Z humour"] = cw.get("Gen-Z humour", 0) + 1
    if affl > .62:
        cw["Aspirational luxury"] = cw.get("Aspirational luxury", 0) + 1.5
    for _ in range(R.choice([2, 3, 3, 4])):
        codes.add(pick(cw))

    # quality & performance
    vtr = clamp(R.gauss(44, 8) + (er - tk[5]) * 1.2, 22, 72)
    hook = clamp(R.gauss(64, 8) + (vtr - 44) * .5, 38, 88)
    sentiment = clamp(R.gauss(80, 6), 58, 95)
    cquality = clamp(R.gauss(70, 10) - (22 if fraud else 0), 25, 95)
    sponsored = clamp(R.gauss(26, 11) + (8 if tier in ("macro", "mega") else 0), 4, 72)
    safety = clamp(R.gauss(88, 6), 60, 99)
    flags = []
    if R.random() < (.16 if niche == "comedy" else .05):
        flags.append("Profanity in recent content"); safety -= R.uniform(12, 22)
    if R.random() < .035:
        flags.append("Political commentary"); safety -= R.uniform(10, 18)
    if R.random() < .025:
        flags.append("Past controversy (2025)"); safety -= R.uniform(18, 28)
    if R.random() < .03:
        flags.append("Promotes betting / real-money gaming"); safety -= R.uniform(14, 22)
    if niche in ("health", "fitness", "beauty") and R.random() < .07:
        flags.append("Unverified health claims"); safety -= R.uniform(10, 18)
    safety = round(clamp(safety, 35, 99))
    asci = clamp(R.gauss(87, 9), 48, 100)
    ontime = clamp(R.gauss(90, 6), 68, 100)
    trust = clamp(trust0 * (0.85 + sentiment / 400 + (er / tk[5] - 1) * .06) * ln(0, .1) - sponsored / 400, .6, 1.6)
    ctr = clamp(ctr0 * ln(0, .3) * (0.9 + trust / 10), .12, 2.6)
    saves = clamp(saves0 * ln(0, .3), .2, 4.5)
    shares = clamp(shares0 * ln(0, .3), .15, 4.5)
    recall = clamp(3 + (vtr - 30) / 6 + (trust - 1) * 6 + R.gauss(0, 1.6) - (2 if fraud else 0), 2, 17)

    creds = None
    for c, p in CRED.get(niche, []):
        if R.random() < p:
            creds = c
            break

    prem = {"finance": 1.35, "tech": 1.25, "beauty": 1.1, "fashion": 1.05, "health": 1.2, "comedy": 1.1, "travel": 1.1, "auto": 1.15}.get(niche, 1.0)
    reel = followers * tk[7] * (er / tk[5]) ** .35 * prem * ln(0, .15)
    if market == "UAE":
        reel *= 1.6
    reel = max(1500, round(reel / 500) * 500)
    story = max(500, round(reel * .3 / 250) * 250)
    yt = round(reel * 1.6 / 1000) * 1000 if platform == "YouTube" else None

    camps = R.choice([0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 8, 10, 13]) if tier != "nano" else R.choice([0, 0, 0, 1, 1, 2, 3])
    lifts = 0 if camps < 2 else R.choice([0, 0, 1, 1, 2, 3])
    represent = R.random() < (.12 if tier in ("mid", "macro", "mega") else .02)

    collabs = []
    pool = COLLAB_POOL[niche] + COLLAB_POOL[second][:4]
    for b in R.sample(pool, R.choice([0, 1, 1, 2, 2, 3, 4])):
        collabs.append([b, R.randint(3, 140)])
    collabs.sort(key=lambda x: x[1])

    interests = {niche: round(R.uniform(.82, .96), 2), second: round(R.uniform(.4, .62), 2)}
    for k in R.sample(list(NICHES), 2):
        interests.setdefault(k, round(R.uniform(.12, .32), 2))

    pf = {platform: followers}
    if platform != "Instagram" and R.random() < .8:
        pf["Instagram"] = int(followers * R.uniform(.08, .5))
    if platform == "Instagram" and R.random() < .35:
        pf["YouTube"] = int(followers * R.uniform(.05, .45))

    return {
        "id": f"CIE-{1001 + i}", "name": make_name(region, cgender), "g": cgender,
        "city": city, "state": state, "ctier": ctier, "market": market,
        "niche": niche, "niche2": second, "langs": langs2, "platform": platform, "pf": pf,
        "tier": tier, "followers": followers, "views": views, "er": round(er, 2),
        "vtr": round(vtr, 1), "hook": round(hook, 1), "ctr": round(ctr, 2), "saves": round(saves, 2),
        "shares": round(shares, 2), "sent": round(sentiment, 1), "cq": round(cquality), "spons": round(sponsored),
        "cred": round(cred, 1), "growth": growth, "g90": growth90, "fraud": fraud,
        "safety": safety, "flags": flags, "asci": round(asci), "ontime": round(ontime), "trust": round(trust, 2),
        "recall": round(recall, 1), "creds": creds,
        "rate": {"reel": reel, "story": story, "yt": yt},
        "camps": camps, "lifts": lifts, "represent": represent,
        "collabs": collabs, "codes": sorted(codes), "interests": interests,
        "aud": {"fem": round(a_fem, 3), "age": [round(x, 3) for x in a_age], "tiers": [round(x, 3) for x in a_tiers],
                "affl": round(affl, 2), "geo": geo, "langs": a_langs},
    }


creators = [creator(i) for i in range(420)]

# ----------------------------------------------------------------------------- brands
A = lambda *v: norm(list(v))
VERTICALS = [
    ("fmcg", "FMCG"), ("ecom", "E-commerce"), ("beauty", "Beauty & Personal Care"), ("fashion", "Fashion & Footwear"),
    ("health", "Healthcare & Wellness"), ("bfsi", "BFSI & Fintech"), ("tech", "Consumer Tech"),
    ("services", "Food, Travel & Services"), ("ent", "Entertainment & Music"),
]


def brand(id, name, parent, vertical, sub, status, src, objective, female, age, tiers, affl, langs, codes, affinity,
          competitors, compliance, budget, aov, cvr, pool, moment, brief, markets=("India",), kpis=None):
    return dict(id=id, name=name, parent=parent, vertical=vertical, sub=sub, status=status, src=src, objective=objective,
                target=dict(fem=female, age=age, tiers=tiers, affl=affl), langs=langs, codes=codes, affinity=affinity,
                competitors=competitors, compliance=compliance, budget=budget, aov=aov, cvr=cvr, pool=pool,
                moment=moment, brief=brief, markets=list(markets), kpis=kpis or [])


BR = [
    # FMCG
    brand("dabur", "Dabur", "Dabur India", "fmcg", "Ayurvedic health & food", "Reported client", "SB18", "awareness",
          .56, A(3, 14, 33, 30, 20), A(.34, .38, .28), .42, {"Hindi": 1, "Hinglish": .8, "Marathi": .6, "Bengali": .6, "Tamil": .5, "Telugu": .5, "Gujarati": .6, "English": .5, "Punjabi": .6, "Odia": .5, "Kannada": .5, "Malayalam": .5, "Assamese": .4},
          ["Family-first", "Spiritual & Ayurveda", "Festive & occasions", "Regional pride"],
          {"food": .9, "health": .95, "parenting": .9, "fitness": .6, "lifestyle": .55, "home": .55, "comedy": .35},
          ["Patanjali", "Himalaya", "Zandu", "Horlicks"], "health", 60, 320, .05, 210, "Winter immunity · Nov–Jan",
          "Make Chyawanprash a daily ritual for young families, beyond the grandparent shelf.",
          kpis=["TG reach", "Ad recall lift", "Q-commerce search lift"]),
    brand("kitkat", "KitKat", "Nestlé India", "fmcg", "Confectionery", "Reported client", "SB18", "awareness",
          .50, A(16, 46, 28, 7, 3), A(.48, .36, .16), .45, {"Hinglish": 1, "English": .9, "Hindi": .7, "Tamil": .45, "Telugu": .45, "Bengali": .45, "Marathi": .45},
          ["Gen-Z humour", "Campus life", "Cricket & IPL", "Bollywood pop"],
          {"comedy": .95, "music": .7, "gaming": .7, "lifestyle": .7, "education": .55, "food": .65},
          ["Cadbury", "Snickers", "Munch"], None, 45, 60, .04, 160, "Exam season · Feb–Mar & IPL",
          "Own the 'break' moment for students and first-jobbers.",
          kpis=["TG reach", "Ad recall lift", "Shares per view"]),
    brand("coke", "Coca-Cola", "Coca-Cola India", "fmcg", "Beverages", "Reported client", "SB18", "awareness",
          .46, A(12, 42, 30, 11, 5), A(.40, .36, .24), .42, {"Hinglish": 1, "Hindi": .9, "English": .7, "Tamil": .6, "Telugu": .6, "Bengali": .55, "Marathi": .55, "Kannada": .5, "Punjabi": .6},
          ["Festive & occasions", "Cricket & IPL", "Bollywood pop", "Gen-Z humour", "Family-first"],
          {"comedy": .9, "music": .9, "food": .8, "lifestyle": .7, "travel": .5, "gaming": .55},
          ["PepsiCo", "Campa Cola"], None, 120, 40, .04, 260, "Summer & IPL · Mar–May",
          "Be the drink of the shared meal, in every language India eats in.",
          kpis=["TG reach", "Ad recall lift", "Frequency in TG"]),
    brand("whisper", "Whisper", "P&G", "fmcg", "Feminine hygiene", "Reported client", "YS", "consideration",
          .97, A(14, 52, 28, 5, 1), A(.30, .40, .30), .40, {"Hindi": 1, "Hinglish": .9, "English": .6, "Tamil": .6, "Telugu": .6, "Bengali": .6, "Marathi": .6},
          ["Campus life", "Small-town dreams", "Science-backed"],
          {"health": .9, "lifestyle": .75, "beauty": .7, "education": .75, "fitness": .6},
          ["Stayfree", "Sofy", "Nua"], "health", 40, 180, .05, 80, "Back to college · Jun–Aug",
          "Normalise period conversations with first-year college students.",
          kpis=["Saves per view", "Sentiment", "Sampling sign-ups"]),
    brand("livon", "Livon", "Marico", "fmcg", "Hair serum", "Reported client", "CB", "consideration",
          .76, A(12, 54, 26, 6, 2), A(.42, .38, .20), .45, {"Hinglish": 1, "Hindi": .85, "English": .75, "Tamil": .55, "Telugu": .55},
          ["Campus life", "Gen-Z humour", "Desi-modern"],
          {"beauty": .95, "fashion": .8, "lifestyle": .75, "comedy": .45},
          ["L'Oréal Paris", "Streax", "Tresemmé"], None, 25, 250, .05, 70, "Monsoon frizz · Jun–Sep",
          "Swap the salon visit for a serum, for students on a budget.",
          kpis=["Saves per view", "Trial redemptions", "CTR"]),
    # E-commerce
    brand("amazon", "Amazon", "Amazon India", "ecom", "Marketplace", "Reported client", "LI", "conversion",
          .52, A(4, 32, 40, 17, 7), A(.42, .36, .22), .50, {"Hinglish": 1, "Hindi": .9, "English": .9, "Tamil": .6, "Telugu": .6, "Kannada": .6, "Bengali": .6, "Marathi": .6, "Malayalam": .55, "Gujarati": .55},
          ["Festive & occasions", "Value-seeker", "Working professional", "Family-first"],
          {"tech": .9, "fashion": .8, "beauty": .8, "home": .9, "lifestyle": .85, "parenting": .75, "food": .6, "fitness": .6, "comedy": .5},
          ["Flipkart", "Meesho", "Myntra", "Ajio"], None, 150, 1400, .028, 330, "Great Indian Festival · Sep–Oct",
          "Turn creator storefronts into the first stop for festive shopping lists.", markets=("India", "UAE"),
          kpis=["Verified orders", "iROAS", "New-to-Amazon customers"]),
    brand("flipkart", "Flipkart", "Walmart", "ecom", "Marketplace", "Reported client", "SB18", "conversion",
          .48, A(6, 40, 36, 13, 5), A(.30, .40, .30), .40, {"Hindi": 1, "Hinglish": .95, "Tamil": .75, "Telugu": .75, "Kannada": .7, "Bengali": .7, "Marathi": .7, "English": .6, "Malayalam": .65, "Gujarati": .6, "Odia": .6, "Punjabi": .6},
          ["Value-seeker", "Festive & occasions", "Small-town dreams", "Regional pride"],
          {"tech": .9, "fashion": .8, "lifestyle": .8, "home": .8, "beauty": .7, "comedy": .6, "gaming": .55, "education": .5},
          ["Amazon", "Meesho", "Shopsy"], None, 150, 1200, .026, 360, "Big Billion Days · Sep–Oct",
          "Win Bharat's first smartphone and first appliance purchase in local languages.",
          kpis=["Verified orders", "iROAS", "Tier-2/3 share of orders"]),
    brand("meesho", "Meesho", "Meesho", "ecom", "Value marketplace", "Reported client", "SB18", "conversion",
          .66, A(4, 36, 38, 16, 6), A(.18, .40, .42), .28, {"Hindi": 1, "Tamil": .85, "Telugu": .85, "Marathi": .8, "Bengali": .8, "Kannada": .8, "Gujarati": .8, "Odia": .75, "Hinglish": .7, "Malayalam": .7, "Punjabi": .7, "Assamese": .7},
          ["Value-seeker", "Small-town dreams", "Regional pride", "Family-first", "Festive & occasions"],
          {"fashion": .95, "home": .85, "lifestyle": .85, "beauty": .8, "parenting": .75, "comedy": .6, "food": .5},
          ["Flipkart", "Shopsy", "Amazon"], None, 80, 450, .03, 300, "Mega Blockbuster Sale · Sep–Oct",
          "Reach first-time online shoppers in their own language, at ₹300–₹600 price points.",
          kpis=["Verified orders", "First-order rate", "CAC"]),
    brand("nykaa", "Nykaa", "FSN E-Commerce", "ecom", "Beauty e-commerce", "Reported client", "PRN", "conversion",
          .82, A(6, 42, 38, 11, 3), A(.50, .35, .15), .58, {"Hinglish": 1, "English": .95, "Hindi": .75, "Tamil": .55, "Telugu": .55, "Bengali": .55, "Marathi": .55},
          ["Festive & occasions", "Wedding season", "K-culture", "Aspirational luxury", "Desi-modern"],
          {"beauty": 1, "fashion": .85, "lifestyle": .8, "health": .45},
          ["Purplle", "Tira", "Myntra"], None, 90, 1100, .032, 110, "Pink Friday · Nov",
          "Make Nykaa the default cart for every creator-led routine.", markets=("India", "UAE"),
          kpis=["Verified orders", "iROAS", "Basket size"]),
    # Beauty
    brand("olay", "Olay", "P&G", "beauty", "Premium skincare", "Reported client", "PRN", "consideration",
          .86, A(2, 26, 44, 21, 7), A(.62, .30, .08), .70, {"English": 1, "Hinglish": .9, "Hindi": .55},
          ["Science-backed", "Aspirational luxury", "Working professional"],
          {"beauty": 1, "lifestyle": .75, "fashion": .6, "health": .7, "fitness": .45},
          ["L'Oréal Paris", "Neutrogena", "Pond's", "Minimalist", "The Derma Co"], None, 60, 1200, .03, 48, "Festive glow · Oct–Nov",
          "Win the 25–40 working woman who is moving from basics to actives.",
          kpis=["Consideration lift", "Saves per view", "PDP clicks"]),
    brand("bioderma", "Bioderma", "NAOS", "beauty", "Dermo-cosmetics", "Reported client", "SB18", "consideration",
          .80, A(3, 36, 42, 14, 5), A(.60, .30, .10), .66, {"English": 1, "Hinglish": .85, "Hindi": .5},
          ["Science-backed", "Aspirational luxury"],
          {"beauty": 1, "health": .95, "lifestyle": .6},
          ["La Roche-Posay", "Cetaphil", "CeraVe", "Minimalist"], "health", 40, 1300, .03, 32, "Summer skin · Mar–May",
          "Earn derm credibility with sensitive-skin buyers before they search.",
          kpis=["Consideration lift", "Sentiment", "PDP clicks"]),
    brand("dalba", "d'Alba", "d'Alba (Korea)", "beauty", "K-beauty", "Reported client", "SB18", "conversion",
          .86, A(8, 52, 32, 6, 2), A(.55, .35, .10), .60, {"English": 1, "Hinglish": .95, "Hindi": .5},
          ["K-culture", "Gen-Z humour", "Aspirational luxury"],
          {"beauty": 1, "fashion": .75, "lifestyle": .8},
          ["COSRX", "Innisfree", "Laneige", "Beauty of Joseon"], None, 30, 1600, .03, 30, "Launch window · Q3",
          "Make the white-truffle mist the first K-beauty buy for Indian Gen Z.",
          kpis=["Verified orders", "Saves per view", "Search lift"]),
    brand("celimax", "Celimax", "Celimax (Korea)", "beauty", "K-beauty", "Reported client", "SB18", "conversion",
          .80, A(8, 50, 34, 6, 2), A(.52, .36, .12), .55, {"English": 1, "Hinglish": .95, "Hindi": .55},
          ["K-culture", "Science-backed", "Value-seeker"],
          {"beauty": 1, "lifestyle": .7, "fashion": .6, "health": .5},
          ["COSRX", "Axis-Y", "Beauty of Joseon"], None, 25, 1100, .03, 28, "Acne-season · Jun–Sep",
          "Turn 'Noni' into the acne-care search term for 18–28s.",
          kpis=["Verified orders", "CTR", "Repeat rate"]),
    brand("forever52", "Forever52", "Daily Life Forever52", "beauty", "Makeup", "Reported client", "SB18", "conversion",
          .92, A(6, 46, 36, 9, 3), A(.44, .38, .18), .45, {"Hinglish": 1, "Hindi": .8, "English": .8, "Tamil": .55, "Telugu": .55, "Bengali": .55, "Marathi": .55},
          ["Wedding season", "Festive & occasions", "Value-seeker", "Desi-modern"],
          {"beauty": 1, "fashion": .85, "lifestyle": .7},
          ["Swiss Beauty", "Sugar Cosmetics", "Maybelline", "Lakmé"], None, 20, 650, .035, 70, "Wedding season · Nov–Feb",
          "Be the bridesmaid kit brand in tier-1 and tier-2 weddings.",
          kpis=["Verified orders", "CTR", "Saves per view"]),
    # Fashion
    brand("hm", "H&M", "H&M India", "fashion", "Fast fashion", "Reported client", "SB18", "consideration",
          .60, A(8, 50, 32, 7, 3), A(.62, .30, .08), .62, {"English": 1, "Hinglish": .9, "Hindi": .45},
          ["Gen-Z humour", "Sustainability", "Aspirational luxury", "Desi-modern"],
          {"fashion": 1, "lifestyle": .85, "beauty": .6, "music": .55, "travel": .55},
          ["Zara", "Uniqlo", "Max Fashion", "Bewakoof"], None, 50, 1800, .025, 60, "End-of-season sale · Dec–Jan",
          "Lead the Gen-Z 'fit check' with styling that mixes desi and global.", markets=("India", "UAE"),
          kpis=["Saves per view", "PDP clicks", "Store visits"]),
    brand("puma", "Puma", "Puma India", "fashion", "Sportswear", "Reported client", "SB18", "consideration",
          .44, A(8, 44, 34, 10, 4), A(.52, .34, .14), .55, {"Hinglish": 1, "English": .9, "Hindi": .7, "Tamil": .5, "Telugu": .5, "Kannada": .5, "Punjabi": .5},
          ["Fitness-first", "Cricket & IPL", "Gen-Z humour", "Desi-modern"],
          {"fitness": 1, "fashion": .85, "lifestyle": .7, "music": .5, "travel": .45, "comedy": .4},
          ["Nike", "Adidas", "Skechers", "ASICS"], None, 70, 2800, .022, 90, "Run season · Oct–Feb",
          "Make running culture in tier-1 cities feel like a community, not a race.", markets=("India", "UAE"),
          kpis=["Engagement rate", "PDP clicks", "Event sign-ups"]),
    brand("crocs", "Crocs", "Crocs India", "fashion", "Casual footwear", "Reported client", "SB18", "conversion",
          .54, A(12, 52, 28, 6, 2), A(.55, .34, .11), .56, {"Hinglish": 1, "English": .95, "Hindi": .55},
          ["Gen-Z humour", "Campus life", "Bollywood pop"],
          {"fashion": 1, "lifestyle": .85, "comedy": .65, "music": .55, "travel": .5},
          ["Skechers", "Birkenstock", "Bata"], None, 35, 3200, .02, 55, "Monsoon · Jun–Aug",
          "Make Jibbitz the Gen-Z self-expression accessory.",
          kpis=["Verified orders", "Shares per view", "CTR"]),
    brand("zink", "Zink London", "Zink London", "fashion", "Women's western wear", "Reported client", "SB18", "conversion",
          .95, A(6, 52, 34, 6, 2), A(.48, .38, .14), .48, {"Hinglish": 1, "English": .9, "Hindi": .6},
          ["Desi-modern", "Value-seeker", "Working professional", "Gen-Z humour"],
          {"fashion": 1, "lifestyle": .8, "beauty": .65},
          ["Only", "Vero Moda", "Zara", "Max Fashion"], None, 20, 1300, .028, 40, "EOSS · Jun & Dec",
          "Become the first-job wardrobe for 21–27 year-old women.",
          kpis=["Verified orders", "CTR", "Saves per view"]),
    brand("neemans", "Neeman's", "Neeman's", "fashion", "Sustainable footwear (D2C)", "Reported client", "SB18", "conversion",
          .40, A(2, 26, 46, 19, 7), A(.62, .30, .08), .64, {"English": 1, "Hinglish": .85, "Hindi": .45},
          ["Sustainability", "Working professional", "Fitness-first"],
          {"fashion": .9, "lifestyle": .85, "fitness": .7, "travel": .75, "tech": .5},
          ["Bata", "Skechers", "Allbirds"], None, 15, 3000, .02, 35, "Office return · Jan–Mar",
          "Own the 'one shoe for office, travel and walks' position for 28–40s.",
          kpis=["Verified orders", "iROAS", "CAC"]),
    brand("rayban", "Ray-Ban", "EssilorLuxottica", "fashion", "Premium eyewear", "Reported client", "YS", "consideration",
          .48, A(4, 38, 40, 13, 5), A(.68, .26, .06), .78, {"English": 1, "Hinglish": .85, "Hindi": .35},
          ["Aspirational luxury", "Desi-modern", "Bollywood pop"],
          {"fashion": 1, "travel": .85, "lifestyle": .85, "music": .55, "auto": .5},
          ["Lenskart", "Fastrack", "Oakley"], None, 45, 7000, .012, 28, "Summer · Mar–May",
          "Keep Ray-Ban aspirational as Lenskart pushes premium downmarket.", markets=("India", "UAE"),
          kpis=["Consideration lift", "Store visits", "Saves per view"]),
    # Healthcare & wellness
    brand("hkvitals", "HK Vitals", "HealthKart", "health", "Nutraceuticals", "Reported client", "PRN", "conversion",
          .55, A(2, 32, 44, 16, 6), A(.48, .36, .16), .52, {"Hinglish": 1, "Hindi": .85, "English": .85, "Tamil": .5, "Telugu": .5},
          ["Fitness-first", "Science-backed", "Working professional"],
          {"fitness": 1, "health": .95, "beauty": .65, "food": .55, "lifestyle": .6},
          ["OZiva", "Wellbeing Nutrition", "Kapiva", "MuscleBlaze"], "health", 50, 900, .03, 90, "New-year resolutions · Jan",
          "Move biotin and collagen from impulse buy to a 90-day habit.",
          kpis=["Verified orders", "Repeat purchase", "iROAS"]),
    brand("philips", "Philips", "Philips India", "health", "Personal health & grooming", "Reported client", "SB18", "consideration",
          .42, A(4, 40, 38, 13, 5), A(.50, .36, .14), .55, {"Hinglish": 1, "English": .9, "Hindi": .7, "Tamil": .5, "Telugu": .5},
          ["Working professional", "Science-backed", "Wedding season"],
          {"lifestyle": .85, "tech": .8, "fashion": .7, "beauty": .7, "fitness": .65, "health": .6},
          ["Braun", "Havells", "Xiaomi"], None, 45, 2200, .022, 90, "Wedding season · Nov–Feb",
          "Make grooming tech part of the groom-to-be routine.",
          kpis=["Consideration lift", "PDP clicks", "Saves per view"]),
    brand("tata1mg", "Tata 1mg", "Tata Digital", "health", "E-pharmacy & diagnostics", "Prospect", None, "conversion",
          .55, A(1, 16, 40, 27, 16), A(.40, .38, .22), .45, {"Hindi": 1, "Hinglish": .95, "English": .85, "Tamil": .6, "Telugu": .6, "Bengali": .6, "Marathi": .6},
          ["Science-backed", "Family-first", "Value-seeker"],
          {"health": 1, "parenting": .8, "fitness": .65, "food": .5, "lifestyle": .5},
          ["PharmEasy", "Apollo 24|7", "Netmeds"], "health", 60, 700, .04, 150, "Monsoon health · Jul–Sep",
          "Make full-body checkups a family habit through doctors people already trust.",
          kpis=["Lab test bookings", "CAC", "Repeat orders"]),
    brand("cult", "Cult", "Curefit", "health", "Fitness memberships", "Prospect", None, "conversion",
          .48, A(2, 34, 46, 14, 4), A(.66, .28, .06), .62, {"English": 1, "Hinglish": .95, "Hindi": .55, "Kannada": .4, "Telugu": .4},
          ["Fitness-first", "Working professional", "Gen-Z humour"],
          {"fitness": 1, "health": .8, "lifestyle": .75, "food": .5},
          ["HealthifyMe", "Fittr", "Anytime Fitness"], None, 40, 4000, .015, 40, "New-year resolutions · Jan",
          "Convert January intent into memberships that survive March.",
          kpis=["Trial bookings", "Membership conversions", "CAC"]),
    # BFSI
    brand("groww", "Groww", "Groww", "bfsi", "Investing app", "Prospect", None, "conversion",
          .30, A(1, 34, 46, 14, 5), A(.42, .38, .20), .50, {"Hinglish": 1, "Hindi": .95, "English": .85, "Marathi": .55, "Gujarati": .6, "Tamil": .5, "Telugu": .5},
          ["Working professional", "Small-town dreams", "Value-seeker"],
          {"finance": 1, "education": .85, "tech": .7, "lifestyle": .45, "comedy": .35},
          ["Zerodha", "Upstox", "Angel One", "Paytm Money", "INDmoney"], "finance", 80, 2500, .05, 120, "Tax-saving season · Jan–Mar",
          "Bring first-time investors from tier-2 cities to a funded SIP.",
          kpis=["Funded accounts", "Cost per funded account", "SIP activation"]),
    brand("policybazaar", "PolicyBazaar", "PB Fintech", "bfsi", "Insurance marketplace", "Prospect", None, "conversion",
          .40, A(0, 18, 46, 26, 10), A(.44, .36, .20), .52, {"Hindi": 1, "Hinglish": .95, "English": .8, "Tamil": .5, "Telugu": .5, "Marathi": .5},
          ["Family-first", "Working professional", "Value-seeker"],
          {"finance": 1, "parenting": .8, "health": .7, "education": .55, "lifestyle": .45},
          ["Acko", "Ditto Insurance", "InsuranceDekho"], "finance", 70, 2000, .04, 110, "Tax-saving season · Jan–Mar",
          "Get young parents to buy term cover before their child's first birthday.",
          kpis=["Qualified leads", "Policies issued", "Cost per policy"]),
    brand("cred", "CRED", "Dreamplug", "bfsi", "Credit & rewards", "Prospect", None, "awareness",
          .36, A(1, 24, 50, 19, 6), A(.72, .24, .04), .80, {"English": 1, "Hinglish": .9, "Hindi": .4},
          ["Aspirational luxury", "Gen-Z humour", "Working professional"],
          {"finance": .8, "comedy": .85, "lifestyle": .8, "tech": .75, "travel": .6},
          ["Paytm", "Amazon Pay", "Jupiter"], "finance", 90, 3000, .02, 30, "IPL · Mar–May",
          "Keep CRED the 'members only' brand for the creditworthy few.",
          kpis=["Ad recall lift", "App installs", "Affluent reach"]),
    # Consumer tech
    brand("hp", "HP", "HP India", "tech", "Laptops & printers", "Reported client", "PRN", "consideration",
          .42, A(10, 50, 28, 9, 3), A(.44, .38, .18), .52, {"English": 1, "Hinglish": .95, "Hindi": .7, "Tamil": .5, "Telugu": .5, "Kannada": .5},
          ["Campus life", "Working professional", "Gen-Z humour"],
          {"tech": 1, "education": .95, "gaming": .8, "lifestyle": .55, "comedy": .45},
          ["Dell", "Lenovo", "Asus", "Apple"], None, 80, 55000, .006, 120, "Back to college · Jun–Aug",
          "Be the first laptop for students heading to college and coding bootcamps.",
          kpis=["Consideration lift", "Store and PDP visits", "Saves per view"]),
    brand("samsung", "Samsung", "Samsung India", "tech", "Phones & appliances", "Reported client", "SB18", "consideration",
          .46, A(6, 38, 38, 13, 5), A(.44, .38, .18), .52, {"Hinglish": 1, "Hindi": .9, "English": .9, "Tamil": .6, "Telugu": .6, "Kannada": .55, "Bengali": .55, "Marathi": .55},
          ["Working professional", "Festive & occasions", "Family-first"],
          {"tech": 1, "home": .8, "lifestyle": .75, "gaming": .6, "travel": .55, "parenting": .5},
          ["Apple", "OnePlus", "Xiaomi", "LG"], None, 150, 25000, .008, 260, "Festive · Sep–Nov",
          "Pair device launches with home-service moments, as in the Urban Company tie-up.", markets=("India", "UAE"),
          kpis=["Consideration lift", "PDP clicks", "Search lift"]),
    brand("sony", "Sony", "Sony India", "tech", "Audio, TV & gaming", "Reported client", "SB18", "consideration",
          .30, A(12, 46, 30, 9, 3), A(.56, .32, .12), .62, {"English": 1, "Hinglish": .9, "Hindi": .5},
          ["Gen-Z humour", "Bollywood pop", "Aspirational luxury"],
          {"tech": .95, "gaming": .95, "music": .9, "lifestyle": .5},
          ["JBL", "boAt", "Bose", "Samsung"], None, 50, 9000, .012, 70, "Festive · Oct–Nov",
          "Win the audio upgrade from boAt for 20–30 year-old music and gaming fans.",
          kpis=["Consideration lift", "PDP clicks", "Shares per view"]),
    # Food, travel & services
    brand("mcd", "McDonald's", "Westlife Foodworld", "services", "QSR", "Reported client", "SB18", "awareness",
          .50, A(14, 46, 28, 8, 4), A(.56, .34, .10), .48, {"Hinglish": 1, "Hindi": .85, "English": .85, "Marathi": .6, "Gujarati": .6, "Kannada": .55, "Tamil": .5},
          ["Gen-Z humour", "Campus life", "Value-seeker", "Family-first"],
          {"food": 1, "comedy": .9, "lifestyle": .75, "music": .6, "parenting": .5},
          ["Burger King", "KFC", "Domino's"], None, 45, 450, .04, 90, "Monsoon & festive",
          "Make the ₹99 meal the default student hangout in West & South India.",
          kpis=["TG reach", "App orders", "Code redemptions"]),
    brand("indigo", "IndiGo", "InterGlobe Aviation", "services", "Airline", "Reported client", "SB18", "consideration",
          .48, A(2, 28, 44, 18, 8), A(.58, .32, .10), .62, {"English": 1, "Hinglish": .9, "Hindi": .7, "Tamil": .5, "Malayalam": .55, "Telugu": .5},
          ["Working professional", "Festive & occasions", "Regional pride", "Aspirational luxury"],
          {"travel": 1, "lifestyle": .8, "food": .6, "fashion": .5, "comedy": .45},
          ["Air India", "Akasa Air"], None, 60, 6500, .01, 60, "Holiday travel · Oct–Dec",
          "Fill new international routes, Dubai first, with diaspora creators.", markets=("India", "UAE"),
          kpis=["Consideration lift", "Booking-page visits", "Route search lift"]),
    brand("urbanco", "Urban Company", "Urban Company", "services", "Home services", "Reported client", "SB18", "conversion",
          .66, A(1, 18, 48, 24, 9), A(.72, .24, .04), .64, {"English": 1, "Hinglish": .95, "Hindi": .6, "Kannada": .4, "Tamil": .4, "Telugu": .4},
          ["Working professional", "Family-first", "Festive & occasions"],
          {"home": 1, "lifestyle": .85, "beauty": .8, "parenting": .75},
          ["Yes Madam", "Housejoy"], None, 40, 1200, .03, 45, "Pre-Diwali cleaning · Oct",
          "Own the pre-Diwali deep-clean and salon-at-home rush.",
          kpis=["Verified bookings", "iROAS", "Repeat bookings"]),
    # Entertainment & music
    brand("spotify", "Spotify", "Spotify India", "ent", "Music streaming", "Reported client", "PRN", "awareness",
          .50, A(16, 50, 26, 6, 2), A(.54, .34, .12), .52, {"Hinglish": 1, "English": .95, "Hindi": .8, "Tamil": .7, "Telugu": .7, "Punjabi": .75, "Bengali": .6, "Malayalam": .6, "Marathi": .6},
          ["Gen-Z humour", "Bollywood pop", "Regional pride", "Campus life"],
          {"music": 1, "comedy": .85, "lifestyle": .75, "gaming": .6, "travel": .5},
          ["JioSaavn", "YouTube Music", "Gaana"], None, 50, 1400, .02, 160, "Wrapped · Dec",
          "Make Wrapped a regional-language moment, not just an English one.",
          kpis=["TG reach", "Ad recall lift", "Premium trials"]),
    brand("warner", "Warner Music India", "Warner Music Group", "ent", "Music label", "Reported client", "PRN", "awareness",
          .52, A(20, 50, 22, 6, 2), A(.42, .38, .20), .42, {"Hindi": 1, "Hinglish": .95, "Punjabi": .9, "Tamil": .6, "Telugu": .6, "English": .6},
          ["Bollywood pop", "Gen-Z humour", "Wedding season", "Regional pride"],
          {"music": 1, "comedy": .85, "lifestyle": .65, "fashion": .5},
          ["T-Series", "Saregama", "Sony Music"], None, 15, 0, 0, 220, "Release weeks",
          "Seed new tracks into 10,000 Reels in the first 72 hours.",
          kpis=["Audio uses", "Stream lift", "Shares per view"]),
]
# festive-season conversion assumptions (AOV ₹, click-to-order rate before assists)
OVR = {"amazon": (1900, .04), "flipkart": (1600, .038), "meesho": (560, .07), "nykaa": (1250, .045), "olay": (1150, .04),
       "bioderma": (1300, .035), "dalba": (1600, .04), "celimax": (1100, .045), "forever52": (650, .05), "hkvitals": (1100, .045),
       "puma": (3200, .03), "crocs": (3200, .03), "zink": (1300, .04), "neemans": (3000, .03), "urbanco": (1400, .04),
       "tata1mg": (800, .05), "cult": (4000, .02), "groww": (2500, .06), "policybazaar": (2200, .045)}
for b in BR:
    if b["id"] in OVR:
        b["aov"], b["cvr"] = OVR[b["id"]]
    b["budget"] = max(6, round(b["budget"] * .3))  # default brief budget in ₹ lakh, scaled to the 420-creator sample

SOURCES = {
    "SB18": "Storyboard18 coverage of Chtrbox campaign work",
    "PRN": "PR Newswire release (Entrepreneur India award)",
    "LI": "Chtrbox LinkedIn / agency profile",
    "YS": "YourStory profile (2018)",
    "CB": "Chtrbox blog case study (2017)",
}

# ----------------------------------------------------------------------------- simple fit (python side, for simulated campaigns)
by_id = {c["id"]: c for c in creators}


def fit_py(b, c):
    t = b["target"]
    a = c["aud"]
    g = 1 - abs(a["fem"] - t["fem"])
    ag = sum(min(x, y) for x, y in zip(a["age"], t["age"]))
    tr = sum(min(x, y) for x, y in zip(a["tiers"], t["tiers"]))
    af = 1 - abs(a["affl"] - t["affl"])
    aud = .3 * g + .3 * ag + .25 * tr + .15 * af
    cont = b["affinity"].get(c["niche"], .05) * .75 + b["affinity"].get(c["niche2"], .05) * .25
    lang = max(b["langs"].get(l, 0) for l in c["langs"])
    mk = 1 if c["market"] in b["markets"] else .2
    return (aud * .4 + cont * .4 + lang * .2) * mk * (c["cred"] / 90)


def eligible_py(b, c):
    if c["cred"] < 72 or c["safety"] < 55:
        return False
    if any(x[0] in b["competitors"] and x[1] <= 60 for x in c["collabs"]):
        return False
    if b["compliance"] == "finance" and c["niche"] == "finance" and not (c["creds"] or "").startswith("SEBI"):
        return False
    if b["compliance"] == "health" and c["niche"] == "health" and not c["creds"]:
        return False
    return c["market"] in b["markets"]


STORY = {t[0]: t[8] for t in TIERS}
ASSIST = 2.8  # promo codes + affiliate + search-assisted orders per clicked order


def predict_py(b, c, fp):
    """Same forecast as the browser engine (predict() in template.html)."""
    aff = b["affinity"].get(c["niche"], .05) * .75 + b["affinity"].get(c["niche2"], .05) * .25
    if c["platform"] == "YouTube":
        rv, sv, cost = c["views"], 0, c["rate"]["yt"]
        clicks = rv * c["ctr"] * .55 / 100
    else:
        rv, sv = c["views"], c["followers"] * STORY[c["tier"]] * 2
        cost = c["rate"]["reel"] + 2 * c["rate"]["story"]
        clicks = (rv * c["ctr"] * .3 + sv * c["ctr"] * 1.3) / 100
    clicks *= (.55 + .9 * aff)
    conv = clicks * b["cvr"] * c["trust"] * (.7 + .6 * aff) * ASSIST
    return dict(views=int(rv + sv), clicks=int(clicks), orders=int(conv), rev=int(conv * b["aov"]), cost=cost)


DAYS_LIVE = {"amazon": 14}
CAMPAIGNS = [
    ("amazon", "Great Indian Festival · creator storefronts", 21, 72, 45, True),
    ("olay", "Regenerist 28-day glow challenge", 28, 26, 16, False),
    ("dabur", "Chyawanprash · winter immunity, 9 languages", 30, 64, 32, False),
    ("meesho", "Mega Blockbuster Sale · Bharat creators", 21, 60, 30, False),
    ("hkvitals", "Biotin 90-day habit", 28, 30, 14, False),
    ("puma", "Run Your City · 10K series", 28, 28, 18, False),
]
LANGS_ALL = sorted({l for c in creators for l in c["langs"]})


def sim_campaign(cid, spec):
    bid, title, days, n, budget_l, live = spec
    b = next(x for x in BR if x["id"] == bid)
    cands = [c for c in creators if eligible_py(b, c)]

    def eff(c):
        f = predict_py(b, c, 0)
        if b["objective"] == "awareness" or not b["cvr"]:
            return f["views"] * c["cred"] / 100 / f["cost"] * 40
        return f["rev"] / f["cost"]
    cands.sort(key=lambda c: -(fit_py(b, c) ** 2 * min(eff(c), 6) ** .8))
    budget = budget_l * 1e5
    chosen, spent = [], 0
    cap = {"mega": 1, "macro": 3}
    for c in cands:
        cost = c["rate"]["yt"] or (c["rate"]["reel"] + 2 * c["rate"]["story"])
        if c["tier"] in cap and sum(1 for x in chosen if x["tier"] == c["tier"]) >= cap[c["tier"]]:
            continue
        if cost > budget * .18:
            continue
        if spent + cost <= budget * .97:
            chosen.append(c)
            spent += cost
        if len(chosen) >= n:
            break
    rows = []
    elapsed = DAYS_LIVE.get(bid, days)
    prog = elapsed / days
    tot = dict(rep=0, api=0, uniq=0, real=0, eng=0, clicks=0, orders=0, rev=0, cost=0, tg=0)
    for c in chosen:
        fp = fit_py(b, c)
        f = predict_py(b, c, fp)
        cost = f["cost"]
        posted = R.random() < (prog * 1.15 if live else 1)
        if not posted:
            act = None
        else:
            noise = ln(0, .22)
            v = f["views"] * noise
            cl = f["clicks"] * noise * ln(0, .18)
            o = f["orders"] * (cl / max(1, f["clicks"])) * ln(0, .2)
            act = dict(views=int(v), eng=int(c["followers"] * c["er"] / 100 * noise * ln(0, .15)),
                       clicks=int(cl), orders=int(o), rev=int(o * b["aov"]))
        row = dict(id=c["id"], cost=cost, fit=round(fp * 100), posted=posted,
                   f=dict(views=f["views"], clicks=f["clicks"], orders=f["orders"], rev=f["rev"]), a=act)
        rows.append(row)
        if act:
            rep = act["views"] * R.uniform(1.12, 1.32)
            tot["rep"] += rep
            tot["api"] += act["views"]
            tot["uniq"] += act["views"] * .74
            tot["real"] += act["views"] * .74 * c["cred"] / 100
            tot["tg"] += act["views"] * .74 * c["cred"] / 100 * (.5 + fp * .5)
            tot["eng"] += act["eng"]
            tot["clicks"] += act["clicks"]
            tot["orders"] += act["orders"]
            tot["rev"] += act["rev"]
            tot["cost"] += cost
    spend_plan = sum(r["cost"] for r in rows)
    # daily series
    daily = []
    weights = [math.exp(-((d - days * .45) ** 2) / (2 * (days * .28) ** 2)) * (1.25 if d % 7 in (5, 6) else 1) for d in range(days)]
    if bid == "amazon":  # sale days spike
        for d in range(7, 13):
            weights[d] *= 2.1
    sw = sum(weights[:elapsed])
    fw = sum(weights)
    fut_w = sum(weights[elapsed:]) or 1
    pend = [r for r in rows if not r["posted"]]
    pend_f = {k: sum(r["f"][k] for r in pend) for k in ("views", "clicks", "orders")}
    act_t = {"views": tot["api"], "clicks": tot["clicks"], "orders": tot["orders"]}
    for d in range(days):
        w = weights[d]
        if d < elapsed:
            k = w / sw
            daily.append(dict(d=d + 1, views=int(tot["api"] * k * ln(0, .08)), clicks=int(tot["clicks"] * k * ln(0, .1)),
                              orders=int(tot["orders"] * k * ln(0, .12)), live=True))
        else:  # posted creators keep earning at half their run-rate; scheduled creators add their forecast
            daily.append(dict(d=d + 1, live=False, **{m: int(act_t[m] / sw * w * .55 + pend_f[m] * w / fut_w) for m in act_t}))
    # attribution & incrementality
    inc_share = {"amazon": .62, "olay": .56, "dabur": .45, "meesho": .66, "hkvitals": .64, "puma": .54}[bid]
    returns = {"amazon": .09, "olay": .04, "dabur": .02, "meesho": .17, "hkvitals": .05, "puma": .11}[bid]
    attr = {"link": .46, "code": .22, "affiliate": .21, "view": .11}
    lift = {
        "amazon": [("Ad recall", 21.0, 31.5), ("Brand consideration", 48.0, 53.4), ("Purchase intent", 36.0, 41.8)],
        "olay": [("Ad recall", 14.0, 25.6), ("Awareness of Regenerist", 31.0, 39.2), ("Consideration", 18.0, 24.9), ("Purchase intent", 12.0, 16.3)],
        "dabur": [("Ad recall", 17.0, 26.1), ("Awareness: daily use", 22.0, 30.4), ("Consideration", 29.0, 33.8), ("Purchase intent", 21.0, 24.2)],
        "meesho": [("Ad recall", 19.0, 27.3), ("Consideration", 34.0, 39.1), ("Purchase intent", 28.0, 33.5)],
        "hkvitals": [("Ad recall", 12.0, 20.4), ("Consideration", 16.0, 21.8), ("Purchase intent", 11.0, 15.1)],
        "puma": [("Ad recall", 16.0, 26.8), ("Brand association: running", 22.0, 30.9), ("Consideration", 25.0, 30.2)],
    }[bid]
    alerts = {
        "amazon": [("serious", "CIE-%s CTR running 41%% below forecast on Day 3. Swap the story frame to a price-drop sticker." % rows[min(4, len(rows) - 1)]["id"][4:]),
                   ("warning", "2 posts went live without #ad in the first line. Flagged to creators and fixed within 2 hours."),
                   ("good", "Tier-2 Hindi creators are beating forecast by 28%. Moved ₹6.5L of remaining budget to them."),
                   ("warning", "Spend pacing at 92% of plan with 7 days left.")],
        "olay": [("good", "Derm-credentialed creators drove 2.1x the saves per view of lifestyle creators."),
                 ("serious", "One creator posted a competitor serum 11 days after go-live. Exclusivity clause invoked.")],
        "dabur": [("good", "Regional-language creators delivered 64% of TG reach at 41% of spend."),
                  ("warning", "Health-claim language ('cures cold') removed from 3 scripts before approval.")],
        "meesho": [("serious", "Returns on fashion orders hit 17%. Verified revenue is reported net of returns."),
                   ("good", "First-time buyer share 38% vs 22% on paid social.")],
        "hkvitals": [("warning", "Two fitness creators' scripts reworded: no 'guaranteed' hair-growth claims (ASCI)."),
                     ("good", "Repeat purchase at 60 days: 31% from creator cohorts vs 22% baseline.")],
        "puma": [("good", "Run-club event sign-ups 3,940, 2.3x forecast in Bengaluru and Pune."),
                 ("warning", "Two mega creators under-delivered on views (-34%). Re-weighting tier mix for the next flight.")],
    }[bid]
    ltv = {"amazon": 1.0, "olay": 1.5, "dabur": 1.4, "meesho": 2.2, "hkvitals": 2.1, "puma": 1.15}[bid]
    cost_live = tot["cost"]
    verified_rev = tot["rev"] * (1 - returns)
    incr_rev = verified_rev * inc_share
    holdout = dict(test_cities=6, control_cities=6, test_rate=None, control_rate=None, lift_pct=None)
    if b["cvr"]:
        cr = R.uniform(1.8, 3.2)
        holdout.update(control_rate=round(cr, 2), test_rate=round(cr / (1 - inc_share * .6), 2))
        holdout["lift_pct"] = round((holdout["test_rate"] / holdout["control_rate"] - 1) * 100, 1)
    fc_err = []
    for r in rows:
        if r["a"] and r["f"]["views"]:
            fc_err.append(abs(r["a"]["views"] - r["f"]["views"]) / r["f"]["views"])
    mape = round(sum(fc_err) / max(1, len(fc_err)) * 100, 1)
    return dict(id=f"C{cid + 1}", brand=bid, title=title, days=days, elapsed=elapsed, live=live, budget=round(spend_plan / 1e5 * 1.04, 1),
                planned=spend_plan, spent=int(cost_live), rows=rows, daily=daily, totals={k: int(v) for k, v in tot.items()},
                attr=attr, inc_share=inc_share, returns=returns, verified_rev=int(verified_rev), incr_rev=int(incr_rev),
                lift=lift, alerts=alerts, holdout=holdout, mape=mape, n_lift=1200, ltv=ltv)


campaigns = [sim_campaign(i, c) for i, c in enumerate(CAMPAIGNS)]

out = dict(
    meta=dict(generated="2026-10-20", seed=20261021, n_creators=len(creators), note="Simulated data. Creator identities are synthetic personas."),
    niches={k: v[0] for k, v in NICHES.items()},
    verticals=VERTICALS,
    tiers=[dict(key=t[0], label=t[1], min=t[2], max=t[3], er=t[5], story=t[8]) for t in TIERS],
    codes=CODES,
    langs=LANGS_ALL,
    sources=SOURCES,
    brands=BR,
    creators=creators,
    campaigns=campaigns,
)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "data.json", "w"), separators=(",", ":"), ensure_ascii=False)
print("creators", len(creators), "brands", len(BR), "campaigns", len(campaigns))
for c in campaigns:
    print(c["brand"], len(c["rows"]), "spent", c["spent"], "rev", c["totals"]["rev"], "incr", c["incr_rev"], "mape", c["mape"])
