MILESTONE_YEARS = (5, 10, 20, 30, 40, 50, 60)


def calculate_dca(yearly_amount, annual_rate_pct):
    """Future value of a fixed yearly investment compounding at annual_rate_pct,
    at each of the milestone year counts. Assumes each year's contribution is
    made at the start of that year, so it compounds through the full year
    (annuity-due convention) -- the standard assumption for "invest early each
    year" DCA illustrations.
    """
    r = annual_rate_pct / 100
    rows = []
    for years in MILESTONE_YEARS:
        contributed = yearly_amount * years
        if r == 0:
            total_value = contributed
        else:
            total_value = yearly_amount * (((1 + r) ** years - 1) / r) * (1 + r)
        rows.append({
            "years": years,
            "contributed": contributed,
            "total_value": total_value,
            "growth": total_value - contributed,
        })
    return rows
