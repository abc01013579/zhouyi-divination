import math
from datetime import datetime

import ichingpy as icp
from ichingpy.enum.five_phase import FivePhase

# ichingpy exposes .phase on EarthlyBranch but not on HeavenlyStem, so map stems by hand.
STEM_PHASE = {
    icp.HeavenlyStem.Jia: FivePhase.WOOD,
    icp.HeavenlyStem.Yi: FivePhase.WOOD,
    icp.HeavenlyStem.Bing: FivePhase.FIRE,
    icp.HeavenlyStem.Ding: FivePhase.FIRE,
    icp.HeavenlyStem.Wu: FivePhase.EARTH,
    icp.HeavenlyStem.Ji: FivePhase.EARTH,
    icp.HeavenlyStem.Geng: FivePhase.METAL,
    icp.HeavenlyStem.Xin: FivePhase.METAL,
    icp.HeavenlyStem.Ren: FivePhase.WATER,
    icp.HeavenlyStem.Gui: FivePhase.WATER,
}

# ichingpy.FourPillars derives the month branch from a hardcoded per-year table of
# jieqi (solar term) start dates, which can drift a day in years where the real
# jieqi falls earlier/later than the table assumes. We instead derive it from the
# sun's actual ecliptic longitude, so the month boundary always lands on the real
# jieqi regardless of year.
MONTH_BRANCH_ORDER = [
    icp.EarthlyBranch.Yin,
    icp.EarthlyBranch.Mao,
    icp.EarthlyBranch.Chen,
    icp.EarthlyBranch.Si,
    icp.EarthlyBranch.Wu,
    icp.EarthlyBranch.Wei,
    icp.EarthlyBranch.Shen,
    icp.EarthlyBranch.You,
    icp.EarthlyBranch.Xu,
    icp.EarthlyBranch.Hai,
    icp.EarthlyBranch.Zi,
    icp.EarthlyBranch.Chou,
]

# 五虎遁: year stem -> stem of the first (Yin) month.
MONTH_FIRST_STEM = {
    icp.HeavenlyStem.Jia: icp.HeavenlyStem.Bing,
    icp.HeavenlyStem.Ji: icp.HeavenlyStem.Bing,
    icp.HeavenlyStem.Yi: icp.HeavenlyStem.Wu,
    icp.HeavenlyStem.Geng: icp.HeavenlyStem.Wu,
    icp.HeavenlyStem.Bing: icp.HeavenlyStem.Geng,
    icp.HeavenlyStem.Xin: icp.HeavenlyStem.Geng,
    icp.HeavenlyStem.Ding: icp.HeavenlyStem.Ren,
    icp.HeavenlyStem.Ren: icp.HeavenlyStem.Ren,
    icp.HeavenlyStem.Wu: icp.HeavenlyStem.Jia,
    icp.HeavenlyStem.Gui: icp.HeavenlyStem.Jia,
}


def _to_julian_date(year: int, month: int, day: int, ut_hour: float) -> float:
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5 + ut_hour / 24


def _sun_longitude(jd: float) -> float:
    t = (jd - 2451545.0) / 36525.0
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    m = math.radians(357.52911 + 35999.05029 * t - 0.0001537 * t * t)
    c = (
        (1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(m)
        + (0.019993 - 0.000101 * t) * math.sin(2 * m)
        + 0.000289 * math.sin(3 * m)
    )
    return (l0 + c) % 360


def _solar_month_index(year: int, month: int, day: int, hour: int) -> int:
    """Index (0=Yin ... 11=Chou) of the jieqi month containing the birth instant."""
    ut_hour = hour - 8  # Beijing (UTC+8) civil hour -> UT
    jd = _to_julian_date(year, month, day, ut_hour)
    longitude = _sun_longitude(jd)
    return int(((longitude - 315) % 360) // 30)


def _month_pillar(year: int, month: int, day: int, hour: int, year_stem: icp.HeavenlyStem):
    zhi_index = _solar_month_index(year, month, day, hour)
    branch = MONTH_BRANCH_ORDER[zhi_index]
    stem = MONTH_FIRST_STEM[year_stem] + zhi_index
    return stem, branch


def _year_pillar(year: int, month: int, day: int, hour: int):
    # ichingpy.FourPillars.get_year_pillar cuts the year over at a hardcoded Feb 4,
    # but the real Lichun moment varies year to year (e.g. it fell on Feb 3 in 2021
    # and 2025) and even shifts within the day itself. Find which solar month the
    # birth instant actually falls in and only step the year back when that's still
    # Chou (idx 11, i.e. before this year's Lichun) or the tail of the previous
    # year's Zi month spilling into January (idx 10 and month == 1).
    zhi_index = _solar_month_index(year, month, day, hour)
    effective_year = year - 1 if (zhi_index == 11 or (zhi_index == 10 and month == 1)) else year
    # A mid-year date is always safely past that year's Lichun, so this just reuses
    # ichingpy's validated stem/branch cycle math for the year we already determined.
    return icp.FourPillars.get_year_pillar(datetime(effective_year, 6, 1))

PILLAR_LABELS_BY_LANG = {
    "zh": ["年柱", "月柱", "日柱", "时柱"],
    "en": ["Year", "Month", "Day", "Hour"],
}

PHASE_LABELS_BY_LANG = {
    "zh": {phase: phase.label for phase in FivePhase},
    "en": {phase: phase.name.title() for phase in FivePhase},
}


def _stem_branch_label(stem: icp.HeavenlyStem, branch: icp.EarthlyBranch, lang: str) -> str:
    if lang == "en":
        return f"{stem.name} {branch.name}"
    return f"{stem.label}{branch.label}"


def calculate_bazi(year: int, month: int, day: int, hour: int, lang: str = "zh") -> dict:
    """Birthday -> BaZi (Four Pillars) -> Five Element breakdown, ready for template rendering."""
    phase_labels = PHASE_LABELS_BY_LANG[lang]
    dt = datetime(year, month, day, hour)
    year_pillar = _year_pillar(year, month, day, hour)
    month_stem, month_branch = _month_pillar(year, month, day, hour, year_pillar.stem)
    day_pillar = icp.FourPillars.get_day_pillar(dt)
    hour_pillar = icp.FourPillars.get_hour_pillar(dt, day_pillar.stem)

    pillars = []
    counts: dict[FivePhase, int] = {phase: 0 for phase in FivePhase}
    stem_branch_pairs = [
        (year_pillar.stem, year_pillar.branch),
        (month_stem, month_branch),
        (day_pillar.stem, day_pillar.branch),
        (hour_pillar.stem, hour_pillar.branch),
    ]
    for label, (stem, branch) in zip(PILLAR_LABELS_BY_LANG[lang], stem_branch_pairs):
        stem_phase = STEM_PHASE[stem]
        branch_phase = branch.phase
        pillars.append(
            {
                "label": label,
                "text": _stem_branch_label(stem, branch, lang),
                "stem_phase": phase_labels[stem_phase],
                "branch_phase": phase_labels[branch_phase],
            }
        )
        counts[stem_phase] += 1
        counts[branch_phase] += 1

    return {
        "pillars_text": " ".join(pillar["text"] for pillar in pillars),
        "pillars": pillars,
        "counts": [{"label": phase_labels[phase], "count": counts[phase]} for phase in FivePhase],
    }
