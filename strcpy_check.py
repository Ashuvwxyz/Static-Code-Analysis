import subprocess

def parse(filename):
    raw = subprocess.run(["clang", "-Xclang", "-ast-dump", filename],capture_output = True, text = True)
    lst = raw.stdout.split("\n")
    parsed_code = []
  
    for line in lst[:-1]:
        words = [word for word in line.split() if word != "|"]
        words[0] = words[0][2:]
        parsed_code.append(words)
    return parsed_code

def check_strcpy_overflow(parsed_code):
    length = len(parsed_code)
    overflows = []
    for i in range(length):
        for j in parsed_code[i]:
            if j == "'__builtin___strcpy_chk'":
                s = parsed_code[i+1][2].index(":")+1
                e = parsed_code[i+1][2][s+1:].index(":")+s+1
                line = parsed_code[i+1][2][s:e]
                destination_size = int(parsed_code[i+2][4][1:-2])
                source_size = int(parsed_code[i+5][4][1:-2])
                if destination_size <= source_size:
                    overflows.append((line,source_size,destination_size))
    return overflows
    
def main():
    parsed_code = parse("lol.c")
    result = check_strcpy_overflow(parsed_code)
    if len(result) != 0:
        for i in range(len(result)):
            print("Buffer Overflow due to strcpy() on line",result[i][0],"source size:",result[i][1],"bytes",", destination size:",result[i][2],"bytes")

if __name__ == "__main__":
    main()