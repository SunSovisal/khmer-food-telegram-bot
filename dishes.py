"""Curated Khmer dish and ingredient data used by the bot.

The ingredient tags are intentionally practical rather than prescriptive:
family recipes vary, so a dish can have several common household variants.
"""

from dataclasses import dataclass


VEGETABLES = {
    "water_spinach": "ត្រកួន",
    "mustard_green": "ស្ពៃជ្រក់/ស្ពៃខៀវ",
    "cabbage": "ស្ពៃក្តោប",
    "cauliflower": "ផ្កាខាត់ណា",
    "eggplant": "ត្រប់",
    "pumpkin": "ល្ពៅ",
    "winter_melon": "ត្រឡាច",
    "luffa": "ននោង",
    "long_bean": "សណ្តែកគួរ",
    "green_papaya": "ល្ហុងខ្ចី",
    "pineapple": "ម្នាស់",
    "tomato": "ប៉េងប៉ោះ",
    "cucumber": "ត្រសក់",
    "lettuce": "សាឡាត់",
    "mushroom": "ផ្សិត",
    "potato": "ដំឡូងបារាំង",
    "carrot": "ការ៉ុត",
    "bitter_melon": "ម្រះ",
    "bamboo_shoot": "ទំពាំង",
}

MEATS = {
    "fish": "ត្រី",
    "chicken": "សាច់មាន់",
    "pork": "សាច់ជ្រូក",
    "beef": "សាច់គោ",
    "shrimp": "បង្គា",
    "duck": "សាច់ទា",
    "egg": "ស៊ុត",
    "none": "មិនដាក់សាច់",
}


@dataclass(frozen=True, slots=True)
class Dish:
    id: str
    name_km: str
    name_en: str
    proteins: tuple[str, ...]
    vegetables: tuple[str, ...]
    category_km: str
    note_km: str


DISHES = (
    # Fish dishes
    Dish("fish_amok", "អាម៉ុកត្រី", "Fish amok", ("fish",), (), "ចំហុយ", "ត្រីចំហុយជាមួយគ្រឿងអាម៉ុក និងខ្ទិះដូង។"),
    Dish("korko_fish", "សម្លកកូរត្រី", "Samlor korko with fish", ("fish",), ("eggplant", "pumpkin", "green_papaya", "long_bean", "luffa"), "សម្ល", "សម្លបន្លែច្រើនមុខជាមួយគ្រឿងកកូរ ប្រហុក និងអង្ករលីង។"),
    Dish("machu_water_spinach_fish", "សម្លម្ជូរត្រកួនត្រី", "Sour fish and water-spinach soup", ("fish",), ("water_spinach",), "សម្ល", "សម្លជូរស្រាលៗ មានត្រកួន និងត្រី។"),
    Dish("machu_youn_fish", "សម្លម្ជូរយួនត្រី", "Khmer sour fish soup", ("fish",), ("pineapple", "tomato"), "សម្ល", "សម្លជូរផ្អែមមានត្រី ម្នាស់ និងប៉េងប៉ោះ។"),
    Dish("prahal_fish", "សម្លប្រហើរត្រី", "Samlor prahal", ("fish",), ("winter_melon", "pumpkin", "luffa"), "សម្ល", "សម្លត្រីជាមួយគ្រឿងប្រហើរ និងបន្លែទន់ៗ។"),
    Dish("sweet_sour_fish", "ត្រីឆាជូរអែម", "Sweet-and-sour fish", ("fish",), ("pineapple", "cucumber", "tomato"), "ឆា", "ត្រីបំពងឬឆាជាមួយម្នាស់ ត្រសក់ និងទឹកជូរអែម។"),
    Dish("fish_mustard_soup", "ស្ងោរស្ពៃជ្រក់ត្រី", "Fish and pickled-mustard soup", ("fish",), ("mustard_green",), "ស្ងោរ", "ត្រីស្ងោរជាមួយស្ពៃជ្រក់ រសជាតិជូរប្រៃ។"),
    Dish("steamed_fish_mushroom", "ត្រីចំហុយផ្សិត", "Steamed fish with mushrooms", ("fish",), ("mushroom",), "ចំហុយ", "ត្រីចំហុយជាមួយផ្សិត ខ្ញី និងខ្ទឹម។"),
    Dish("fish_winter_melon", "ស្ងោរត្រីត្រឡាច", "Fish and winter-melon soup", ("fish",), ("winter_melon",), "ស្ងោរ", "ស្ងោរត្រីជាមួយត្រឡាច ងាយធ្វើ និងស្រាលពោះ។"),
    Dish("grilled_fish", "ត្រីអាំងជ្រលក់ទឹកត្រី", "Grilled fish", ("fish",), ("cucumber",), "អាំង", "ត្រីអាំង ញ៉ាំជាមួយត្រសក់ និងទឹកត្រីជូរហឹរ។"),
    # Chicken dishes
    Dish("chicken_curry", "សម្លការីសាច់មាន់", "Khmer chicken curry", ("chicken",), ("potato", "carrot"), "សម្ល", "ការីខ្មែរជាមួយខ្ទិះដូង ដំឡូង និងការ៉ុត។"),
    Dish("chicken_kroeung", "សាច់មាន់ឆាគ្រឿង", "Chicken cha kroeung", ("chicken",), ("eggplant", "long_bean"), "ឆា", "មាន់ឆាជាមួយគ្រឿងលឿង ស្លឹកក្រូច និងបន្លែ។"),
    Dish("ginger_chicken_mushroom", "មាន់ឆាខ្ញីផ្សិត", "Ginger chicken with mushrooms", ("chicken",), ("mushroom",), "ឆា", "សាច់មាន់ឆាជាមួយខ្ញី និងផ្សិត។"),
    Dish("chicken_cauliflower", "មាន់ឆាផ្កាខាត់ណា", "Chicken and cauliflower stir-fry", ("chicken",), ("cauliflower", "carrot"), "ឆា", "ឆាសាច់មាន់ ផ្កាខាត់ណា និងការ៉ុត។"),
    Dish("chicken_cabbage", "មាន់ឆាស្ពៃក្តោប", "Chicken and cabbage stir-fry", ("chicken",), ("cabbage",), "ឆា", "សាច់មាន់ឆាស្ពៃក្តោបបែបម្ហូបផ្ទះ។"),
    Dish("chicken_winter_melon", "ស្ងោរមាន់ត្រឡាច", "Chicken and winter-melon soup", ("chicken",), ("winter_melon",), "ស្ងោរ", "ស្ងោរសាច់មាន់ជាមួយត្រឡាច និងម្រេច។"),
    Dish("chicken_papaya_soup", "ស្ងោរមាន់ល្ហុងខ្ចី", "Chicken and green-papaya soup", ("chicken",), ("green_papaya",), "ស្ងោរ", "មាន់ស្ងោរជាមួយល្ហុងខ្ចី រសជាតិផ្អែមធម្មជាតិ។"),
    Dish("chicken_lime_mushroom", "ស្ងោរជូរមាន់ផ្សិត", "Lime chicken and mushroom soup", ("chicken",), ("mushroom", "tomato"), "ស្ងោរ", "ស្ងោរមាន់រសជាតិជូរស្រាល ជាមួយផ្សិត និងប៉េងប៉ោះ។"),
    Dish("braised_chicken_potato", "មាន់ខដំឡូង", "Braised chicken and potatoes", ("chicken",), ("potato", "carrot"), "ខ", "សាច់មាន់ខជាមួយដំឡូង និងការ៉ុត។"),
    # Pork dishes
    Dish("braised_pork_egg", "ខសាច់ជ្រូកពងទា", "Braised pork and eggs", ("pork",), (), "ខ", "សាច់ជ្រូកខទឹកដូងជាមួយពងទា ឬពងមាន់។"),
    Dish("pork_mustard_soup", "ស្ងោរស្ពៃជ្រក់សាច់ជ្រូក", "Pork and pickled-mustard soup", ("pork",), ("mustard_green",), "ស្ងោរ", "សាច់ជ្រូកស្ងោរជាមួយស្ពៃជ្រក់។"),
    Dish("pork_cabbage", "សាច់ជ្រូកឆាស្ពៃក្តោប", "Pork and cabbage stir-fry", ("pork",), ("cabbage",), "ឆា", "សាច់ជ្រូកឆាជាមួយស្ពៃក្តោប។"),
    Dish("pork_eggplant", "សាច់ជ្រូកឆាត្រប់", "Pork and eggplant stir-fry", ("pork",), ("eggplant",), "ឆា", "សាច់ជ្រូកឆាត្រប់ជាមួយខ្ទឹម និងជី។"),
    Dish("pork_long_bean", "សាច់ជ្រូកឆាសណ្តែកគួរ", "Pork and long-bean stir-fry", ("pork",), ("long_bean",), "ឆា", "សាច់ជ្រូកឆាសណ្តែកគួរ ងាយធ្វើប្រចាំថ្ងៃ។"),
    Dish("pork_papaya_soup", "ស្ងោរសាច់ជ្រូកល្ហុងខ្ចី", "Pork and green-papaya soup", ("pork",), ("green_papaya",), "ស្ងោរ", "ឆ្អឹងឬសាច់ជ្រូកស្ងោរជាមួយល្ហុងខ្ចី។"),
    Dish("pork_pumpkin_soup", "សម្លល្ពៅសាច់ជ្រូក", "Pork and pumpkin soup", ("pork",), ("pumpkin",), "សម្ល", "សម្លល្ពៅផ្អែមធម្មជាតិជាមួយសាច់ជ្រូក។"),
    Dish("prahok_ktiss", "ប្រហុកខ្ទិះ", "Prahok ktiss", ("pork",), ("eggplant", "cucumber", "long_bean"), "ជ្រលក់", "ប្រហុកខ្ទិះសាច់ជ្រូកចិញ្ច្រាំ ញ៉ាំផ្ទាប់បន្លែ។"),
    Dish("pork_mushroom", "សាច់ជ្រូកឆាផ្សិត", "Pork and mushroom stir-fry", ("pork",), ("mushroom",), "ឆា", "សាច់ជ្រូកឆាជាមួយផ្សិត និងខ្ទឹម។"),
    Dish("pork_cauliflower", "សាច់ជ្រូកឆាផ្កាខាត់ណា", "Pork and cauliflower stir-fry", ("pork",), ("cauliflower", "carrot"), "ឆា", "សាច់ជ្រូកឆាផ្កាខាត់ណា និងការ៉ុត។"),
    Dish(
    "pork_minced_winter_melon",
    "ឆាត្រឡាចសាច់ជ្រូកចិញ្ច្រាំ",
    "Stir-fried winter melon with minced pork",
    ("pork",),
    ("winter_melon",),
    "ឆា",
    "ត្រឡាចឆាជាមួយសាច់ជ្រូកចិញ្ច្រាំ និងខ្ទឹមស។",
),
    # Beef dishes
    Dish("beef_lok_lak", "ឡុកឡាក់សាច់គោ", "Beef lok lak", ("beef",), ("lettuce", "tomato", "cucumber"), "ឆា", "សាច់គោឡុកឡាក់ ញ៉ាំជាមួយប៉េងប៉ោះ ត្រសក់ និងទឹកម្រេច។"),
    Dish("machu_kroeung_beef", "សម្លម្ជូរគ្រឿងសាច់គោ", "Sour kroeung beef soup", ("beef",), ("water_spinach", "eggplant", "long_bean"), "សម្ល", "សម្លជូរគ្រឿងខ្មែរជាមួយសាច់គោ និងបន្លែ។"),
    Dish("beef_kroeung", "សាច់គោឆាគ្រឿង", "Beef cha kroeung", ("beef",), ("eggplant", "long_bean"), "ឆា", "សាច់គោឆាគ្រឿងជាមួយត្រប់ ឬសណ្តែកគួរ។"),
    Dish("beef_cauliflower", "សាច់គោឆាផ្កាខាត់ណា", "Beef and cauliflower stir-fry", ("beef",), ("cauliflower", "carrot"), "ឆា", "សាច់គោឆាជាមួយផ្កាខាត់ណា។"),
    Dish("beef_cabbage", "សាច់គោឆាស្ពៃក្តោប", "Beef and cabbage stir-fry", ("beef",), ("cabbage",), "ឆា", "សាច់គោឆាស្ពៃក្តោប និងខ្ទឹម។"),
    Dish("beef_sweet_sour", "សាច់គោឆាជូរអែម", "Sweet-and-sour beef", ("beef",), ("pineapple", "tomato", "cucumber"), "ឆា", "សាច់គោឆាជូរអែមជាមួយម្នាស់ និងបន្លែ។"),
    Dish("beef_stew", "គោខដំឡូងការ៉ុត", "Khmer beef stew", ("beef",), ("potato", "carrot", "tomato"), "ខ", "សាច់គោខទន់ជាមួយដំឡូង ការ៉ុត និងប៉េងប៉ោះ។"),
    Dish("beef_cucumber_salad", "ញាំសាច់គោត្រសក់", "Beef and cucumber salad", ("beef",), ("cucumber", "tomato"), "ញាំ", "ញាំសាច់គោជាមួយត្រសក់ ជី និងទឹកត្រីជូរអែម។"),
    # Shrimp dishes
    Dish("machu_youn_shrimp", "សម្លម្ជូរយួនបង្គា", "Khmer sour shrimp soup", ("shrimp",), ("pineapple", "tomato"), "សម្ល", "សម្លជូរអែមមានបង្គា ម្នាស់ និងប៉េងប៉ោះ។"),
    Dish("shrimp_cabbage", "បង្គាឆាស្ពៃក្តោប", "Shrimp and cabbage stir-fry", ("shrimp",), ("cabbage",), "ឆា", "បង្គាឆាជាមួយស្ពៃក្តោប។"),
    Dish("shrimp_cauliflower", "បង្គាឆាផ្កាខាត់ណា", "Shrimp and cauliflower stir-fry", ("shrimp",), ("cauliflower", "carrot"), "ឆា", "បង្គាឆាជាមួយផ្កាខាត់ណា និងការ៉ុត។"),
    Dish("shrimp_mushroom", "បង្គាឆាផ្សិត", "Shrimp and mushroom stir-fry", ("shrimp",), ("mushroom",), "ឆា", "បង្គាឆាជាមួយផ្សិត និងខ្ទឹម។"),
    Dish("shrimp_long_bean", "បង្គាឆាសណ្តែកគួរ", "Shrimp and long-bean stir-fry", ("shrimp",), ("long_bean",), "ឆា", "បង្គាឆាជាមួយសណ្តែកគួរ។"),
    Dish("shrimp_pumpkin", "សម្លល្ពៅបង្គា", "Pumpkin and shrimp soup", ("shrimp",), ("pumpkin",), "សម្ល", "សម្លល្ពៅជាមួយបង្គា រសជាតិផ្អែមស្រាល។"),
    Dish("shrimp_amok", "អាម៉ុកបង្គា", "Shrimp amok", ("shrimp",), (), "ចំហុយ", "បង្គាចំហុយជាមួយគ្រឿងអាម៉ុក និងខ្ទិះដូង។"),
    # Duck dishes
    Dish("duck_ginger_mushroom", "សាច់ទាឆាខ្ញីផ្សិត", "Ginger duck with mushrooms", ("duck",), ("mushroom",), "ឆា", "សាច់ទាឆាជាមួយខ្ញី និងផ្សិត។"),
    Dish("duck_bamboo", "សម្លទាទំពាំង", "Duck and bamboo-shoot soup", ("duck",), ("bamboo_shoot",), "សម្ល", "សម្លសាច់ទាជាមួយទំពាំង និងគ្រឿងខ្មែរ។"),
    Dish("duck_curry", "សម្លការីសាច់ទា", "Khmer duck curry", ("duck",), ("potato", "carrot"), "សម្ល", "ការីសាច់ទាជាមួយខ្ទិះដូង ដំឡូង និងការ៉ុត។"),
    Dish("duck_cabbage", "សាច់ទាខស្ពៃក្តោប", "Braised duck and cabbage", ("duck",), ("cabbage",), "ខ", "សាច់ទាខជាមួយស្ពៃក្តោបឲ្យទន់។"),
    Dish("duck_kroeung", "សាច់ទាឆាគ្រឿង", "Duck cha kroeung", ("duck",), ("eggplant", "long_bean"), "ឆា", "សាច់ទាឆាគ្រឿងលឿងជាមួយបន្លែ។"),
    # Egg dishes
    Dish("bitter_melon_egg", "ម្រះឆាស៊ុត", "Bitter melon with egg", ("egg",), ("bitter_melon",), "ឆា", "ម្រះហាន់ស្តើងឆាជាមួយស៊ុត។"),
    Dish("mushroom_omelette", "ពងមាន់ចៀនផ្សិត", "Mushroom omelette", ("egg",), ("mushroom",), "ចៀន", "ពងមាន់ចៀនជាមួយផ្សិត និងស្លឹកខ្ទឹម។"),
    Dish("long_bean_omelette", "ពងមាន់ចៀនសណ្តែកគួរ", "Long-bean omelette", ("egg",), ("long_bean",), "ចៀន", "សណ្តែកគួរហាន់ខ្លីចៀនជាមួយពងមាន់។"),
    Dish("tomato_egg", "ប៉េងប៉ោះឆាស៊ុត", "Tomato and egg stir-fry", ("egg",), ("tomato",), "ឆា", "ប៉េងប៉ោះឆាជាមួយស៊ុត រសជាតិជូរផ្អែម។"),
    Dish("cabbage_egg", "ស្ពៃក្តោបឆាស៊ុត", "Cabbage and egg stir-fry", ("egg",), ("cabbage",), "ឆា", "ស្ពៃក្តោបឆាជាមួយស៊ុត។"),
    # Meat-free dishes
    Dish("veg_korko", "សម្លកកូរបួស", "Vegetarian samlor korko", ("none",), ("eggplant", "pumpkin", "green_papaya", "long_bean", "luffa"), "សម្ល", "សម្លកកូរបន្លែច្រើនមុខ មិនដាក់សាច់។"),
    Dish("mixed_vegetables", "ឆាបន្លែចម្រុះ", "Mixed vegetable stir-fry", ("none",), ("cauliflower", "carrot", "cabbage", "mushroom"), "ឆា", "បន្លែចម្រុះឆាជាមួយខ្ទឹម និងទឹកស៊ីអ៊ីវ។"),
    Dish("veg_curry", "សម្លការីបន្លែ", "Khmer vegetable curry", ("none",), ("potato", "carrot", "pumpkin", "eggplant"), "សម្ល", "ការីខ្មែរខ្ទិះដូងជាមួយបន្លែ មិនដាក់សាច់។"),
    Dish("mushroom_amok", "អាម៉ុកផ្សិត", "Mushroom amok", ("none",), ("mushroom",), "ចំហុយ", "ផ្សិតចំហុយជាមួយគ្រឿងអាម៉ុក និងខ្ទិះដូង។"),
    Dish("pumpkin_coconut", "សម្លល្ពៅខ្ទិះដូង", "Pumpkin coconut soup", ("none",), ("pumpkin",), "សម្ល", "ល្ពៅស្ងោរជាមួយខ្ទិះដូង រសជាតិផ្អែមប្រៃ។"),
    Dish("veg_sour_soup", "សម្លម្ជូរបន្លែ", "Vegetarian sour soup", ("none",), ("water_spinach", "pineapple", "tomato", "mushroom"), "សម្ល", "សម្លជូរបន្លែ និងផ្សិត មិនដាក់សាច់។"),
    Dish("cabbage_mushroom", "ស្ពៃក្តោបឆាផ្សិត", "Cabbage and mushroom stir-fry", ("none",), ("cabbage", "mushroom"), "ឆា", "ស្ពៃក្តោបឆាជាមួយផ្សិត និងខ្ទឹម។"),
    Dish("bitter_melon_soup", "ស្ងោរម្រះបួស", "Vegetarian bitter-melon soup", ("none",), ("bitter_melon", "mushroom"), "ស្ងោរ", "ម្រះស្ងោរជាមួយផ្សិត មិនដាក់សាច់។"),
)
