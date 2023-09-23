def risk_reward_ratio(entry: float, stop: float, target: float) -> float:
    risk_per_share = round(entry - stop, 2)
    reward_per_share = round(target - entry, 2)

    rrr = round(reward_per_share / risk_per_share, 2)

    return rrr