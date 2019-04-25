if geometry:
    data = geometry.GetUserStrings()
    d = {}
    k = []
    v = []
    for u in data:
        k.append(u)
        d[u] = data[u]
        v.append(d[u])
    U = d
    Attributes = k
    Values = v