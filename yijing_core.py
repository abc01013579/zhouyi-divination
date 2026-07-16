import cs001
import cs001_en

HEXAGRAM_KEYS = [
    ((1, 1, 1, 1, 1, 1), "data01"),
    ((0, 0, 0, 0, 0, 0), "data02"),
    ((1, 0, 0, 0, 1, 0), "data03"),
    ((0, 1, 0, 0, 0, 1), "data04"),
    ((1, 1, 1, 0, 1, 0), "data05"),
    ((0, 1, 0, 1, 1, 1), "data06"),
    ((0, 1, 0, 0, 0, 0), "data07"),
    ((0, 0, 0, 0, 1, 0), "data08"),
    ((1, 1, 1, 0, 1, 1), "data09"),
    ((1, 1, 0, 1, 1, 1), "data10"),
    ((1, 1, 1, 0, 0, 0), "data11"),
    ((0, 0, 0, 1, 1, 1), "data12"),
    ((1, 0, 1, 1, 1, 1), "data13"),
    ((1, 1, 1, 1, 0, 1), "data14"),
    ((0, 0, 1, 0, 0, 0), "data15"),
    ((0, 0, 0, 1, 0, 0), "data16"),
    ((1, 0, 0, 1, 1, 0), "data17"),
    ((0, 1, 1, 0, 0, 1), "data18"),
    ((1, 1, 0, 0, 0, 0), "data19"),
    ((0, 0, 0, 0, 1, 1), "data20"),
    ((1, 0, 0, 1, 0, 1), "data21"),
    ((1, 0, 1, 0, 0, 1), "data22"),
    ((0, 0, 0, 0, 0, 1), "data23"),
    ((1, 0, 0, 0, 0, 0), "data24"),
    ((1, 0, 0, 1, 1, 1), "data25"),
    ((1, 1, 1, 0, 0, 1), "data26"),
    ((1, 0, 0, 0, 0, 1), "data27"),
    ((0, 1, 1, 1, 1, 0), "data28"),
    ((0, 1, 0, 0, 1, 0), "data29"),
    ((1, 0, 1, 1, 0, 1), "data30"),
    ((0, 0, 1, 1, 1, 0), "data31"),
    ((0, 1, 1, 1, 0, 0), "data32"),
    ((0, 0, 1, 1, 1, 1), "data33"),
    ((1, 1, 1, 1, 0, 0), "data34"),
    ((0, 0, 0, 1, 0, 1), "data35"),
    ((1, 0, 1, 0, 0, 0), "data36"),
    ((1, 0, 1, 0, 1, 1), "data37"),
    ((1, 1, 0, 1, 0, 1), "data38"),
    ((0, 0, 1, 0, 1, 0), "data39"),
    ((0, 1, 0, 1, 0, 0), "data40"),
    ((1, 1, 0, 0, 0, 1), "data41"),
    ((1, 0, 0, 0, 1, 1), "data42"),
    ((1, 1, 1, 1, 1, 0), "data43"),
    ((0, 1, 1, 1, 1, 1), "data44"),
    ((0, 0, 0, 1, 1, 0), "data45"),
    ((0, 1, 1, 0, 0, 0), "data46"),
    ((0, 1, 0, 1, 1, 0), "data47"),
    ((0, 1, 1, 0, 1, 0), "data48"),
    ((1, 0, 1, 1, 1, 0), "data49"),
    ((0, 1, 1, 1, 0, 1), "data50"),
    ((1, 0, 0, 1, 0, 0), "data51"),
    ((0, 0, 1, 0, 0, 1), "data52"),
    ((0, 0, 1, 0, 1, 1), "data53"),
    ((1, 1, 0, 1, 0, 0), "data54"),
    ((1, 0, 1, 1, 0, 0), "data55"),
    ((0, 0, 1, 1, 0, 1), "data56"),
    ((0, 1, 1, 0, 1, 1), "data57"),
    ((1, 1, 0, 1, 1, 0), "data58"),
    ((0, 1, 0, 0, 1, 1), "data59"),
    ((1, 1, 0, 0, 1, 0), "data60"),
    ((1, 1, 0, 0, 1, 1), "data61"),
    ((0, 0, 1, 1, 0, 0), "data62"),
    ((1, 0, 1, 0, 1, 0), "data63"),
    ((0, 1, 0, 1, 0, 1), "data64"),
]

HEXAGRAMS_BY_LANG = {
    "zh": {key: getattr(cs001, name) for key, name in HEXAGRAM_KEYS},
    "en": {key: getattr(cs001_en, name) for key, name in HEXAGRAM_KEYS},
}

DATA4096_BY_LANG = {
    "zh": cs001.data4096,
    "en": cs001_en.data4096,
}

YAO_LABELS_BY_LANG = {
    "zh": ["初", "二", "三", "四", "五", "上"],
    "en": ["1st", "2nd", "3rd", "4th", "5th", "6th"],
}


def calculate_changed(yao):
    if yao in (6, 9):
        return (yao + 1) % 2
    return yao % 2


def cast_reading(yao_list, lang="zh"):
    """yao_list holds six ints in {6,7,8,9}, ordered bottom line (初爻) to top line (上爻)."""
    hexagrams = HEXAGRAMS_BY_LANG[lang]
    data4096 = DATA4096_BY_LANG[lang]

    yao_tuple = tuple(yao_list)
    moving_text = data4096.get(yao_tuple)

    original_bits = tuple(yao % 2 for yao in yao_list)
    changed_bits = tuple(calculate_changed(yao) for yao in yao_list)
    has_change = changed_bits != original_bits

    return {
        "yao_list": yao_list,
        "labels": YAO_LABELS_BY_LANG[lang],
        "original_bits": list(reversed(original_bits)),
        "changed_bits": list(reversed(changed_bits)) if has_change else None,
        "moving_text": moving_text,
        "original": hexagrams.get(original_bits),
        "changed": hexagrams.get(changed_bits) if has_change else None,
        "has_change": has_change,
    }
