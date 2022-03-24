

def fortranformat(n):  # thank you stack exchange
    a = '{:.3E}'.format(float(n))
    e = a.find('E')
    return '0.{}{}{}{:02d}'.format(a[0],a[2:e],a[e:e+2],abs(int(a[e+1:])*1+1))


def write_actet():
    infile = open('potet.day', 'r')
    outfile = open('actet.day', 'w')
    outfile.write('AET calculated as 0.9 * PET\n')
    outfile.write('actet    3851\n')
    for row, line in enumerate(infile):
        if row == 2:
            outfile.write(line)
        if row > 2:
            split_lines = line.split()
            outfile.write(line[0:18])
            for col, item in enumerate(split_lines):
                if col > 5:
                    fl = float(item)*0.9
                    fl_fort = fortranformat(fl)
                    outfile.write(fl_fort+'  ')
            outfile.write('\n')
    outfile.close()


write_actet()
