

def write_datafile(timedict_):
    outfile = open('pet.cbh', 'w')
    outfile.write('OpenET passed to NHM-PRMS as PET\n')
    outfile.write('potet '+str(nhru)+'\n')
    for time in timedict_.keys():
        hru_data = timedict_[time]
        date_strings = str(year) + ' ' + str(month) + ' ' + str(day) + ' ' + str(hour) + ' ' + str(minute) + ' ' + \
                       str(second) + ' '
        outfile.write(date_string)
        for hru in hru_data:
            outfile.write(str(hru) + ' ')
        outfile.write('\n')
    outfile.close()