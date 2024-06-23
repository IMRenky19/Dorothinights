from random import randint




def randomizePutNode(total: int, column_amount: int, column_min_and_max_node: list) -> list:
    before_first_try = [randint(column_min_and_max_node[x][0], column_min_and_max_node[x][1]) \
        for x in range(column_amount - 1)]
    last_column = total - sum(before_first_try)
    if (last_column <= column_min_and_max_node[column_amount - 1][1]) and \
        (last_column >= column_min_and_max_node[column_amount - 1][0]):
        #print(before_first_try, last_column, "0")
        before_first_try.append(last_column)
        return before_first_try
    
    if (last_column > column_min_and_max_node[column_amount - 1][1]):
        #print(">")
        index = 0
        modify_3 = []
        for i in column_min_and_max_node[0:-1]:
            i[0] = 0
            i[1] = column_min_and_max_node[index][1] - before_first_try[index]
            index += 1
            #print(i)
            modify_3.append(i)
        #print(last_column - column_min_and_max_node[column_amount - 1][1], column_amount - 1)
        modified = randomizePutNode(last_column - column_min_and_max_node[column_amount - 1][1],
                         column_amount - 1, modify_3)
        #print(modified, ">")
        #print(len(before_first_try), len(modified) , ">")
        #print(list(range(len(before_first_try))), list(range(len(modified))))
        for a, b in zip(list(range(len(before_first_try))), list(range(len(modified)))):
            before_first_try[a] += modified[b]
        before_first_try.append(column_min_and_max_node[column_amount - 1][1])
        return before_first_try
    if (last_column < column_min_and_max_node[column_amount - 1][0]):
        #print("<")
        index = 0
        modify_3 = []
        for i in column_min_and_max_node[0:-1]:
            i[0] = 0
            i[1] = before_first_try[index] - column_min_and_max_node[index][0]
            index += 1
            modify_3.append(i)
        maximal_index = modify_3.index(max(modify_3))
        before_first_try[maximal_index] -= (column_min_and_max_node[column_amount - 1][0] - last_column)
        last_column = column_min_and_max_node[column_amount - 1][0]
        before_first_try.append(column_min_and_max_node[column_amount - 1][1])
        return before_first_try
    
    
if __name__ == "__main__":
    for i in range(10):
        print(randomizePutNode(20,5,[[1,4], [2,4], [2,4],[2,4],[3,4]]))