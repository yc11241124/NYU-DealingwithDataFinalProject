import os
import csv
import json


#计算平均数
def averagenum(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)


#计算中位数
def mediannum(num):
    listnum = [num[i] for i in range(len(num))]
    listnum.sort()
    lnum = len(num)
    if lnum % 2 == 1:
        i = int((lnum + 1) / 2)-1
        return listnum[i]
    else:
        i = int(lnum / 2)-1
        return (listnum[i] + listnum[i + 1]) / 2


#计算众数
def publicnum(num, d = 0):
    dictnum = {}
    for i in range(len(num)):
        if num[i] in dictnum.keys():
            dictnum[num[i]] += 1
        else:
            dictnum.setdefault(num[i], 1)
    maxnum = 0
    maxkey = 0
    for k, v in dictnum.items():
        if v > maxnum:
            maxnum = v
            maxkey = k
    return maxkey


def get_statistic_json_data():
    country_name_list = ['London', 'SanFrancisco', 'Sydney']
    cate_name_list = ['plus', 'listing']
    root_path = "data"

    for country_name in country_name_list:
        for cate_name in cate_name_list:
            output_dir_name = 'json_data/' + country_name + '/' + cate_name
            if not os.path.exists(output_dir_name):
                os.makedirs(output_dir_name)
            subdir_name = root_path + "/" + country_name + '/' + cate_name
            subdir = os.listdir(subdir_name)

            if cate_name == 'listing':
                for file in subdir:
                    data = csv.reader(open(subdir_name + '/' + file, encoding='utf-8'))
                    data = list(data)
                    roomtype_index = data[0].index('room_type')
                    price_index = data[0].index('price')
                    listings_per_host_index = data[0].index('calculated_host_listings_count')
                    host_id_index = data[0].index('host_id')

                    del data[0]

                    roomtype_list = []
                    price_list = []
                    host_id_list = []
                    listings_per_host_list = []

                    for item in data:
                        roomtype_list.append(item[roomtype_index])
                        price_list.append(int(item[price_index].replace('$', '').replace('.00', '').replace(',', '')))
                        if item[host_id_index] not in host_id_list:
                            listings_per_host_list.append(int(item[listings_per_host_index]))
                            host_id_list.append(item[host_id_index])

                    entire_count = roomtype_list.count('Entire home/apt')
                    private_count = roomtype_list.count('Private room')
                    shared_count = roomtype_list.count('Shared room')

                    result = {}
                    result['Total Listings'] = len(data)
                    result['Entire Room #'] = entire_count
                    result['Entire Room %'] = round((entire_count / len(data)),2)
                    result['Private Room #'] = private_count
                    result['Private Room %'] = round((private_count / len(data)),2)
                    result['Shared Room #'] = shared_count
                    result['Shared Room %'] = round((shared_count / len(data)),2)
                    result['Min Price'] = min(price_list)
                    result['Max Price'] = max(price_list)
                    result['Average Price'] = round(averagenum(price_list),2)
                    result['Median Price'] = mediannum(price_list)
                    result['Public Price'] = publicnum(price_list)
                    result['Total Host #'] = len(listings_per_host_list)
                    result['Single Host #'] = listings_per_host_list.count(1)
                    result['Single Host %'] = round(listings_per_host_list.count(1) / len(listings_per_host_list),2)
                    result['Multiple Host #'] = len(listings_per_host_list) - listings_per_host_list.count(1)
                    result['Multiple Host %'] = round((len(listings_per_host_list) - listings_per_host_list.count(1)) / len(
                        listings_per_host_list),2)

                    file = file[:file.index('.')] + '.json'
                    with open(output_dir_name + '/' + file, 'w') as f:
                        f.write(json.dumps(result))

                if cate_name == 'plus':
                    for file in subdir:
                        with open(subdir_name + '/' + file, 'r') as load_f:
                            load_dict = json.load(load_f)

                        with open(output_dir_name + '/' + file, 'w') as f:
                            result = {}
                            result['plus_number'] = len(load_dict)
                            f.write(json.dumps(result))

def get_location_json_data():
    country_name_list = ['London', 'SanFrancisco', 'Sydney']
    root_path = "data"

    for country_name in country_name_list:
        output_dir_name = 'json_data/' + country_name + '/location'
        if not os.path.exists(output_dir_name):
            os.makedirs(output_dir_name)
        subdir_name = root_path + "/" + country_name + '/listing'
        subdir = os.listdir(subdir_name)

        for file in subdir:
            data = csv.reader(open(subdir_name + '/' + file, encoding='utf-8'))
            data = list(data)
            longitude_index = data[0].index('longitude')  # 经度，x axis
            latitude_index = data[0].index('latitude')  # 维度, y axis
            name_index = data[0].index('name')
            id_index = data[0].index('id')
            roomtype_index = data[0].index('room_type')

            del data[0]

            country_location_list = []

            for index in range(len(data)):
                temp_dict = {}
                temp_dict['lnglat'] = [float(data[index][latitude_index]),float(data[index][longitude_index])]
                temp_dict['name'] = data[index][name_index]
                temp_dict['id'] = int(data[index][id_index])

                if data[index][roomtype_index] == 'Entire home/apt':
                    temp_dict['roomtype'] = 0
                    temp_dict['style'] = 0
                elif data[index][roomtype_index] == 'Private room':
                    temp_dict['roomtype'] = 1
                    temp_dict['style'] = 1
                else:
                    temp_dict['roomtype'] = 2
                    temp_dict['style'] = 2

                temp_dict['plus'] = 0

                country_location_list.append(temp_dict)

            if file.__contains__('2018-10'):
                with open(root_path + "/" + country_name + '/plus/2018-10.json', 'r') as load_f:
                    plus_data = json.load(load_f)
                    for item in plus_data:
                        temp_dict = {}
                        location_str = item['location'].split(',')
                        temp_dict['lnglat'] = [float(location_str[0]), float(location_str[1])]
                        temp_dict['name'] = 'plus' + item['id']
                        temp_dict['id'] = item['id']
                        temp_dict['roomtype'] = 0
                        temp_dict['style'] = 3
                        temp_dict['plus'] = 1
                        country_location_list.append(temp_dict)


            file = file[:file.index('.')] + '.json'
            with open(output_dir_name + '/' + file, 'w') as f:
                f.write(json.dumps(country_location_list))



def get_time_axis():
    country_dir = os.listdir('json_data/London/comparison')
    all_time_list = []
    for subdir in country_dir:
        all_time_list.append(subdir.replace('.json',''))

    return all_time_list