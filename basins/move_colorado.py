import os


print('Moving streamflow from one model to the next...')

orig_df = {}
region_list = [14]
for region in region_list:
    region_name = '20210730_v11_gm_r' + str(region).zfill(2)
    orig_file = open(os.path.join(region_name, 'statvar.out'), 'r')
    for line in orig_file:
        line_split = line.split()
        if len(line_split) > 5:
            orig_date = ('_').join(line_split[1:4])
            if orig_date in orig_df:
                orig_df[orig_date] = orig_df[orig_date] + float(line_split[7]) + float(line_split[8])
            else:
                orig_df[orig_date] = float(line_split[7]) + float(line_split[8])
    
dest_file = open(os.path.join('20210730_v11_gm_r15', 'sf_data'), 'r')
new_sf_data = open(os.path.join('20210730_v11_gm_r15', 'new_sf_data'), 'w')
comment_lines = 0 
for line in dest_file:
    line_split = line.split()
    if len(line_split) > 100:
        date_str = ('_').join(line_split[0:3])
        if date_str in orig_df:
            line_split.append('{:.1f}'.format(orig_df[orig_date]))
        else:
            line_split.append('0.0')
        new_sf_data.write(' '.join(line_split) + '\n')
    elif line_split[0] == 'runoff':
        line_split[1] = str(int(line_split[1]) + 1)
        new_sf_data.write(' '.join(line_split) + '\n')
    elif line_split[0] == '/////////////////////////////////////////////////////////////////////////' and comment_lines != 1:
        comment_lines += 1
    elif line_split[0] == '/////////////////////////////////////////////////////////////////////////' and comment_lines == 1:
        new_sf_data.write('// 99999999\n')
        new_sf_data.write(line)
        comment_lines += 1
    else:
        new_sf_data.write(line)

