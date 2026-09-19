def scenario_demand(base_population,trip_rate,capture_rate,rail_share,scenarios=None):
    scenarios=scenarios or {"low":0.8,"base":1.0,"high":1.2}
    base=float(base_population)*float(trip_rate)*float(capture_rate)*float(rail_share)
    return {"assumptions":{"base_population":base_population,"trip_rate":trip_rate,"capture_rate":capture_rate,"rail_share":rail_share},"daily_demand":{k:round(base*float(v)) for k,v in scenarios.items()},"warning":"Planning scenario, not an official transport-demand forecast."}
