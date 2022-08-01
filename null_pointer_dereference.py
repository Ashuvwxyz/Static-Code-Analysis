# Program by Dyanesh S
# Program to detect null pointer dereference

def check_nullpointer_dereference(data_list, filename):
    vars = []
    null_pointers = []
    line_num = 0
    index = 0
    for i in range(len(data_list)):
        if data_list[i][2][:5] == '<line' or data_list[i][2][:len(filename)+1] == '<'+filename:
            line_num = data_list[i][2][1:-1]

        if data_list[i][0] == 'BinaryOperator' and data_list[i][-1] == "'='" and data_list[i][-2][-2] == '*':
            if data_list[i+2][0] == 'ImplicitCastExpr' and data_list[i+2][-1] == '<NullToPointer>':
                vars.append([data_list[i+1][-3][1:-1],
                            data_list[i+1][-3], line_num])
            elif data_list[i+1][0] == 'DeclRefExpr' and data_list[i+1][-3] in [i[1] for i in vars] and data_list[i+2][-1] != '<NullToPointer>':
                for idx in range(len(vars)):
                    if vars[idx][2] == data_list[i+1][-3]:
                        index = idx
                        break
                vars.pop(index)

        elif data_list[i][0] == 'UnaryOperator' and data_list[i][-3] == "'*'":
            if data_list[i+2][0] == 'DeclRefExpr' and data_list[i+2][-3] in [i[1] for i in vars]:
                for idx in range(len(vars)):
                    if vars[idx][2] == data_list[i+2][-3]:
                        index = idx
                        break
                null_pointers.append(
                    [vars[index][0], line_num, vars[index][2]])

    return null_pointers
    # output: [[var, error line, line where var = NULL], ... ]
