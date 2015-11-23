import sqlite3

'''
inserts newline if attack name is too long
'''

conn = sqlite3.connect("data1.db")
conn.text_factory = str
c = conn.cursor()

c.execute("SELECT attack FROM attacks")
attacks = c.fetchall()

new_attack = ""

for attack in attacks:
    attack = attack[0]
    change = False
    l = len(attack)
    print l
    print attack
    for letter in attack:
    	if l > 14:	
        	last = 0
        	while last < l:
        	    i = attack.find(" ", last + 1)
        	    if i > 14:
        	    	change = True
        	    	new_attack = attack[0:last] + "\\n" + attack[last+1:l]
        	        break
        	    last+=1
    if change:
    	print new_attack
    	sql = "UPDATE attacks SET attack='%s' WHERE attack='%s'" % (new_attack, attack)
    	c.execute(sql)

