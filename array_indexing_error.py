# Program by Dyanesh S
# Program to detect and list all the array indexing errors

def check_array_indexing(data_list):
    arr_var = ''
    arr_size = 0
    indexing_err = []
    line_num = 0
    flag = 0
    for line in data_list:

        if line[2][:5] == '<line':
            line_num = line[2].split(':')[1]
        elif line[0] == 'ArraySubscriptExpr':
            flag = 1
        elif line[0] == 'DeclRefExpr' and flag == 1:
            arr_var = line[-2][1:-1]
            arr_size = int(line[-1][line[-1].find('[')+1:-2])
        elif line[0] == 'IntegerLiteral' and flag == 1:
            if int(line[-1]) >= arr_size:
                indexing_err.append([arr_var, line_num])
            flag = 0

    return indexing_err
