import cs001

HEXAGRAMS = {
    (1, 1, 1, 1, 1, 1): cs001.data01,
    (0, 0, 0, 0, 0, 0): cs001.data02,
    (1, 0, 0, 0, 1, 0): cs001.data03,
    (0, 1, 0, 0, 0, 1): cs001.data04,
    (1, 1, 1, 0, 1, 0): cs001.data05,
    (0, 1, 0, 1, 1, 1): cs001.data06,
    (0, 1, 0, 0, 0, 0): cs001.data07,
    (0, 0, 0, 0, 1, 0): cs001.data08,
    (1, 1, 1, 0, 1, 1): cs001.data09,
    (1, 1, 0, 1, 1, 1): cs001.data10,
    (1, 1, 1, 0, 0, 0): cs001.data11,
    (0, 0, 0, 1, 1, 1): cs001.data12,
    (1, 0, 1, 1, 1, 1): cs001.data13,
    (1, 1, 1, 1, 0, 1): cs001.data14,
    (0, 0, 1, 0, 0, 0): cs001.data15,
    (0, 0, 0, 1, 0, 0): cs001.data16,
    (1, 0, 0, 1, 1, 0): cs001.data17,
    (0, 1, 1, 0, 0, 1): cs001.data18,
    (1, 1, 0, 0, 0, 0): cs001.data19,
    (0, 0, 0, 0, 1, 1): cs001.data20,
    (1, 0, 0, 1, 0, 1): cs001.data21,
    (1, 0, 1, 0, 0, 1): cs001.data22,
    (0, 0, 0, 0, 0, 1): cs001.data23,
    (1, 0, 0, 0, 0, 0): cs001.data24,
    (1, 0, 0, 1, 1, 1): cs001.data25,
    (1, 1, 1, 0, 0, 1): cs001.data26,
    (1, 0, 0, 0, 0, 1): cs001.data27,
    (0, 1, 1, 1, 1, 0): cs001.data28,
    (0, 1, 0, 0, 1, 0): cs001.data29,
    (1, 0, 1, 1, 0, 1): cs001.data30,
    (0, 0, 1, 1, 1, 0): cs001.data31,
    (0, 1, 1, 1, 0, 0): cs001.data32,
    (0, 0, 1, 1, 1, 1): cs001.data33,
    (1, 1, 1, 1, 0, 0): cs001.data34,
    (0, 0, 0, 1, 0, 1): cs001.data35,
    (1, 0, 1, 0, 0, 0): cs001.data36,
    (1, 0, 1, 0, 1, 1): cs001.data37,
    (1, 1, 0, 1, 0, 1): cs001.data38,
    (0, 0, 1, 0, 1, 0): cs001.data39,
    (0, 1, 0, 1, 0, 0): cs001.data40,
    (1, 1, 0, 0, 0, 1): cs001.data41,
    (1, 0, 0, 0, 1, 1): cs001.data42,
    (1, 1, 1, 1, 1, 0): cs001.data43,
    (0, 1, 1, 1, 1, 1): cs001.data44,
    (0, 0, 0, 1, 1, 0): cs001.data45,
    (0, 1, 1, 0, 0, 0): cs001.data46,
    (0, 1, 0, 1, 1, 0): cs001.data47,
    (0, 1, 1, 0, 1, 0): cs001.data48,
    (1, 0, 1, 1, 1, 0): cs001.data49,
    (0, 1, 1, 1, 0, 1): cs001.data50,
    (1, 0, 0, 1, 0, 0): cs001.data51,
    (0, 0, 1, 0, 0, 1): cs001.data52,
    (0, 0, 1, 0, 1, 1): cs001.data53,
    (1, 1, 0, 1, 0, 0): cs001.data54,
    (1, 0, 1, 1, 0, 0): cs001.data55,
    (0, 0, 1, 1, 0, 1): cs001.data56,
    (0, 1, 1, 0, 1, 1): cs001.data57,
    (1, 1, 0, 1, 1, 0): cs001.data58,
    (0, 1, 0, 0, 1, 1): cs001.data59,
    (1, 1, 0, 0, 1, 0): cs001.data60,
    (1, 1, 0, 0, 1, 1): cs001.data61,
    (0, 0, 1, 1, 0, 0): cs001.data62,
    (1, 0, 1, 0, 1, 0): cs001.data63,
    (0, 1, 0, 1, 0, 1): cs001.data64,
}

YAO_LABELS = ["初", "二", "三", "四", "五", "上"]


def calculate_changed(yao):
    if yao in (6, 9):
        return (yao + 1) % 2
    return yao % 2


def cast_reading(yao_list):
    """yao_list holds six ints in {6,7,8,9}, ordered bottom line (初爻) to top line (上爻)."""
    yao_tuple = tuple(yao_list)
    moving_text = cs001.data4096.get(yao_tuple)

    original_bits = tuple(yao % 2 for yao in yao_list)
    changed_bits = tuple(calculate_changed(yao) for yao in yao_list)
    has_change = changed_bits != original_bits

    return {
        "yao_list": yao_list,
        "labels": YAO_LABELS,
        "original_bits": list(reversed(original_bits)),
        "changed_bits": list(reversed(changed_bits)) if has_change else None,
        "moving_text": moving_text,
        "original": HEXAGRAMS.get(original_bits),
        "changed": HEXAGRAMS.get(changed_bits) if has_change else None,
        "has_change": has_change,
    }
