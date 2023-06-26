
import requests
import csv

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
}


def get_detail(year, sid):
    lst = []
    try:
        for i in range(1, 11):

            
            url = f"https://static-data.gaokao.cn/www/2.0/schoolspecialscore/{sid}/{year}/37.json"
            print(url)
            data = requests.request(
                "GET", url, headers=headers, timeout=5).json()['data']
            num = int(data['3_1570_0']['numFound'])
            lst += data['3_1570_0']['item']
            if num <= i * 10:
                break
    except Exception as e:
        print(f'Error: {e}, url: {url}')
    return lst


def get_school_list(province_id="", is_985="", is_211="", is_dual_class=""):
    page_size = 30
    lst_sch = []
    for i in range(1, 2000):
        url = f"https://api.eol.cn/web/api/?&keyword=&page={i}&uri=apidata/api/gk/school/lists&size={page_size}&province_id={province_id}"
        print(url)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        num = int(data['data']['numFound'])
        for item in data['data']['item']:
            lst_sch.append([item['school_id'], str(item['code_enroll']), item['name'],
                           item['province_name'], item['city_name']])

        if i * 30 >= num:
            break
    return lst_sch


def main():
    save_file = open('result.csv', 'w')
    output = csv.writer(save_file)
    output.writerow(['年份', '省份', '院校代码', '学校', '学科门类', '专业类',
                    '专业名称', '最低分', '最低位次', '选科要求', '城市', '地址' '录取批次', '网址'])
    lst_sch = get_school_list(province_id="37")
    for sid, scode, sname, province, city in lst_sch:
        print(sid, scode[:-2], sname, province, city)
        for year in range(2022, 2016, -1):
            data = get_detail(year=year, sid=sid)
            for item in data:
                tmp = [year, province, scode[:-2], sname, item['level2_name'], item['level3_name'], item['spname'],
                       item['min'], item['min_section'],
                       item['sp_info'], city, item['local_batch_name'],
                       f'https://www.gaokao.cn/school/{sid}/provinceline']
                output.writerow(tmp)


    save_file.close()


if __name__ == '__main__':
    main()

