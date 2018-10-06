import csv 

stats = [[-0.6, 3, 1, 2, 5, 4.0, 27.3, 5.08, 1000, 9, 1], [0.0, 2, 0, 1, 2, 5.0, 28.0, 4.532, 819, 4, 2], [-0.2, 5, 0, 0, 2, 4.0, 30.0, 5.184, 1158, 7, 3], [-0.2, 5, 0, 0, 1, -2.0, 31.6, 5.092, 859, 4, 4], [-1.4, 4,
 1, 2, 3, 6.0, 28.4, 5.046, 1170, 9, 5], [-1.6, 4, 1, 2, 3, 8.0, 24.2, 5.152, 1137, 9, 6]]

for i, s in enumerate(stats):
    for k, t in enumerate(stats):
        try: 
            a_position = s[-1]
            b_position = t[-1]
            if a_position != b_position:
                row = s[:-1] + t[:-1]
                if a_position < b_position:
                    row.append(0)
                else: 
                    row.append(1)
                print(row, a_position, b_position)
        except Exception as a:
            pass