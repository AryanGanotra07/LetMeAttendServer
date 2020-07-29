def digitsumlist(n):
    bests = [0]
    for i in range(1, n+1):
        bests.append(min(int(str(d) + str(bests[i - d**2]).strip('0'))
                        for d in range(1, 10)
                        if i >= d**2))
    n = len(bests)
    for i in range(1,n):
        bests.append(bests[i]*10)
    print(sorted(bests))
digitsumlist(5)