from math import pi as pi

P = 0.9
YIELD = 370
E = 200000
N = 1.34
member_list = []
steel_list = []
line_counter = 3

with open('Internal.csv', 'r') as file:
    file.readline()
    for line in file:
        line = line.strip().split(',')
        line = line[0:5]
        if line[0] in ('Top Members', 'Bottom Members', 'Diagonal Members', 'Vertical Members', 'Member'):
            continue
        #print(line)
        member = {'Member': line[0],
                  'Force': float(line[1]),
                  'Type': line[2],
                  'Length': float(line[3]),
                  'Min Area': line[4]
                  }
        #print(member)
        member_list.append(member)
        line_counter += 1
        if line_counter == 56:
            break
    file.readline()
    file.readline()
    for line in file:
        line = line.strip().split(',')
        line = line[0:4]
        #print(line)
        steel = {'Designation': line[0],
                 'Area': float(line[2]),
                 'r': float(line[3])
                 }
        steel_list.append(steel)

#print(member_list, '\n', steel_list)

for member in member_list:
    
    if member['Type'] == 'C':
        comp_des_list = []
        pass_comp = []
        for steel in steel_list:
            sigma_e = (pi ** 2 * E) / (member['Length'] / steel['r']) ** 2
            #print(sigma_e)
            lam = (YIELD / sigma_e) ** 0.5
            #print(lam)
            f = 1 / (1 + lam ** (2 * N)) ** (1 / N)
            #print(f)
            c = round((P * f * YIELD * steel['Area']) / 1000, 2)
            #print(c)
            comp_des_list.append([c, steel['Designation'], steel['Area']])
        for comp_des in comp_des_list:
            #print(comp_des)
            if comp_des[0] > member['Force']:
                pass_comp.append(comp_des)
            # print(comp_des_list[0])
        pass_comp.sort()

        #print(comp_des_list)
        #print(member['Member'], pass_comp[0:2])
        #print(pass_comp[1][0])
        
    if member['Type'] == 'T':
        pass_ten = []
        for steel in steel_list:
            if steel['Area'] > float(member['Min Area']):
                ten_res = round((P * YIELD * steel['Area']) / 1000, 2)
                pass_ten.append(
                    [steel['Area'], steel['Designation'], ten_res])
        pass_ten.sort()
        #print(member['Member'],member['Min Area'], pass_ten[0:2])
        print(pass_ten[1][2])
        

#print(min(comp_des_list), max(comp_des_list))
