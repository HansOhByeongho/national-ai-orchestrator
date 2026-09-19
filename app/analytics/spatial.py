from math import radians,sin,cos,asin,sqrt
def haversine_km(lat1,lon1,lat2,lon2):
    r=6371.0088; p1,p2=radians(lat1),radians(lat2); dp=radians(lat2-lat1); dl=radians(lon2-lon1)
    a=sin(dp/2)**2+cos(p1)*cos(p2)*sin(dl/2)**2
    return 2*r*asin(sqrt(a))
def influence_zone(lat,lon,points,radius_km=2.0):
    rows=[]
    for p in points:
        d=haversine_km(lat,lon,float(p["lat"]),float(p["lon"]))
        rows.append({**p,"distance_km":round(d,3),"inside":d<=radius_km})
    return {"center":{"lat":lat,"lon":lon},"radius_km":radius_km,"points":sorted(rows,key=lambda x:x["distance_km"])}
