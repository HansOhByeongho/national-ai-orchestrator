def development_cost(area_m2,unit_cost_per_m2,contingency_pct=10):
    base=float(area_m2)*float(unit_cost_per_m2); contingency=base*float(contingency_pct)/100
    return {"area_m2":area_m2,"unit_cost_per_m2":unit_cost_per_m2,"base_cost":round(base),"contingency":round(contingency),"total":round(base+contingency)}
def funding_mix(total,shares):
    total=float(total); s=sum(float(v) for v in shares.values())
    if abs(s-100)>0.001:return {"status":"error","reason":"shares must total 100%","sum":s}
    return {"status":"ok","total":total,"amounts":{k:round(total*float(v)/100) for k,v in shares.items()}}
