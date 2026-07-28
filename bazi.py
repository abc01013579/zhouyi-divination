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
    ba_zi = icp.FourPillars.from_datetime(datetime(year, month, day, hour))

    pillars = []
    counts: dict[FivePhase, int] = {phase: 0 for phase in FivePhase}
    for label, pillar in zip(PILLAR_LABELS_BY_LANG[lang], [ba_zi.year, ba_zi.month, ba_zi.day, ba_zi.hour]):
        stem_phase = STEM_PHASE[pillar.stem]
        branch_phase = pillar.branch.phase
        pillars.append(
            {
                "label": label,
                "text": _stem_branch_label(pillar.stem, pillar.branch, lang),
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
