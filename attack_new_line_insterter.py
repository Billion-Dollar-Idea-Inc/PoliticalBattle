attacks = ["asds dfgd f dg gfd gfd asd", "asda sad", "asd as d d", "asdasd asd", "dasdasd asd asd asd ads d", "asdsa", "asdasd sad", "asd sad", "sdad asdas da sd asd asd"] # get dat saucy sql attacks in here, random strings in here to test and so you can run to see it work

for a in range(len(attacks)):
    s = attacks[a]
    l = len(s)
    if l > 14:
        last = 0
        while last < l:
            i = s.find(" ", last + 1)
            if i > 14:
                out = s[0:last] + "\n" + s[last+1:l]
                break
            last = i
        attacks[a] = out
i = 1
for s in attacks:
    print "string ", i, " ", s
    i  = i + 1

# Slam dat swaggin array back in dat sql DB here brah, maybe remove dem prints too
