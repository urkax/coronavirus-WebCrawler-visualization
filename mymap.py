import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie
import os
import re
import csv

"""
Gallery 使用 pyecharts 1.0.0
参考地址: https://gallery.echartsjs.com/editor.html?c=xSkGI6zLmb

目前无法实现的功能:

1、
"""


def get_flist(base_dir):
    # 返回省份简写和文件路径名

    #[csv名称,路径\\csv名称]
    f_list = [[f, os.path.join('chinaProvinceHistory',f)] for f in os.listdir(os.path.join(base_dir, 'chinaProvinceHistory')) if f.endswith('.csv')]

    for i, f_info in enumerate(f_list):
        #https://blog.csdn.net/m0_37360684/article/details/84140403
        #扫描字符串，返回第一个匹配的数字序列
        char1= re.search('\d+', f_info[0]).group()
        char2=char1[0]
        pos=f_info[0].index(char2)

        #第一个数字下标之前为省的名称
        prov_name = f_info[0][:pos]

        #只留省份简写，简化地图表示
        if '省' in prov_name:
            prov_name = prov_name[: prov_name.index('省')]
        elif '市' in prov_name:
            prov_name = prov_name[: prov_name.index('市')]
        elif '回族' in prov_name:
            prov_name = prov_name[: prov_name.index('回族')]
        elif '壮' in prov_name:
            prov_name = prov_name[: prov_name.index('壮')]
        elif '维' in prov_name:
            prov_name = prov_name[: prov_name.index('维')]
        elif '自治区' in prov_name:
            prov_name = prov_name[: prov_name.index('自治区')]

        f_list[i][0] = prov_name

    return f_list

def get_csvdata(path):
    #返回某个省份的确诊人数

    with open(path, encoding="utf-8") as f:
        f_csv = csv.reader(f)

        #现存确诊人数和时间
        current_confirmed = []
        times = []
        for line in f_csv:
            current_confirmed.append(line[4]) #现存确诊人数
            time_i = line[6]
            time_i = '-'.join([time_i[:4], time_i[4:6], time_i[6:]])  # 例：2020-01-20
            times.append(time_i)  # 日期

        #去掉标题
        current_confirmed = current_confirmed[1:]
        times = times[1:]

    return current_confirmed, times

def get_data(base_dir, f_list):

    #由于湖北的时间最早，故以湖北的时间轴作为全时间轴
    hubei_f = [f for f in f_list if f[0]=="湖北"][0]
    _, times = get_csvdata(os.path.join(base_dir, hubei_f[1]))
    data = [{"time": t, "data":[]} for t in times]

    #[{"time": 1980, "data": [  {xx},{xx}  ] }]

    for f_info in f_list:
        current_confirmed, times_f = get_csvdata(os.path.join(base_dir, f_info[1]))
        f_i = 0
        for i, time_i in enumerate(times):
            if time_i != times_f[f_i]:
                curr_data = 0
            else:
                curr_data = current_confirmed[f_i]
                f_i += 1

            #0位置处的数据在源代码中表示比例
            insert_data = {"name": f_info[0], "value": [int(curr_data), 0, f_info[0]]}
            data[i]["data"].append(insert_data)  #data的每一行代表一天内全国确诊人数情况

    for i_time, data_timei in enumerate(data):
        #统计每一天全国确诊人数
        #每一行是某一天全国各省份的确诊情况
        data_all = [prov_data['value'][0] for prov_data in data_timei['data']]

        sum_data = sum(data_all)
        for i_prov, prov_data in enumerate(data_timei['data']):
            percent = prov_data['value'][0]/sum_data*100  #某天该省份确诊人数占全国的百分比，用来画饼状图
            data[i_time]['data'][i_prov]['value'][1] = percent
    return times, data

# data = [
#     {
#         "time": 1980,
#         "data": [
#             {"name": "台湾", "value": [633.76, 12.28, "台湾"]},
#             # {"name": "香港", "value": [432.47, 8.38, "香港"]},
#             # {"name": "江苏", "value": [319.8, 6.2, "江苏"]},
#             # {"name": "上海", "value": [311.89, 6.05, "上海"]},
#             # {"name": "山东", "value": [292.13, 5.66, "山东"]},
#             # {"name": "辽宁", "value": [281, 5.45, "辽宁"]},
#             # {"name": "广东", "value": [249.65, 4.84, "广东"]},
#             # {"name": "四川", "value": [229.31, 4.44, "四川"]},
#             # {"name": "河南", "value": [229.16, 4.44, "河南"]},
#             # {"name": "黑龙江", "value": [221, 4.28, "黑龙江"]},
#         ],
#     },
#     {
#         "time": 2000,
#         "data": [
#             {"name": "台湾", "value": [27435.15, 19.47, "台湾"]},
#             {"name": "香港", "value": [14201.59, 10.08, "香港"]},
#             # {"name": "广东", "value": [10741.25, 7.62, "广东"]},
#             # {"name": "江苏", "value": [8553.69, 6.07, "江苏"]},
#             # {"name": "山东", "value": [8337.47, 5.92, "山东"]},
#             # {"name": "浙江", "value": [6141.03, 4.36, "浙江"]},
#             # {"name": "河南", "value": [5052.99, 3.59, "河南"]},
#             # {"name": "河北", "value": [5043.96, 3.58, "河北"]},
#             # {"name": "上海", "value": [4771.17, 3.39, "上海"]},
#             {"name": "辽宁", "value": [4669.1, 3.31, "辽宁"]},
#         ],
#     },
#     {
#         "time": 2005,
#         "data": [
#             {"name": "台湾", "value": [30792.89, 12.52, "台湾"]},
#             {"name": "广东", "value": [22527.37, 9.16, "广东"]},
#             {"name": "江苏", "value": [18598.69, 7.56, "江苏"]},
#             {"name": "山东", "value": [18366.87, 7.47, "山东"]},
#             {"name": "香港", "value": [14869.68, 6.05, "香港"]},
#             {"name": "浙江", "value": [13417.68, 5.46, "浙江"]},
#             {"name": "河南", "value": [10587.42, 4.3, "河南"]},
#             {"name": "河北", "value": [10043.42, 4.08, "河北"]},
#             {"name": "上海", "value": [9247.66, 3.76, "上海"]},
#             {"name": "辽宁", "value": [8047.3, 3.27, "辽宁"]},
#         ],
#     },
#     {
#         "time": 2010,
#         "data": [
#             {"name": "广东", "value": [46036.25, 9.49, "广东"]},
#             {"name": "江苏", "value": [41425.48, 8.54, "江苏"]},
#             {"name": "山东", "value": [39169.92, 8.08, "山东"]},
#             {"name": "台湾", "value": [30205.64, 6.23, "台湾"]},
#             {"name": "浙江", "value": [27747.65, 5.72, "浙江"]},
#             {"name": "河南", "value": [23092.36, 4.76, "河南"]},
#             {"name": "河北", "value": [20394.26, 4.21, "河北"]},
#             {"name": "辽宁", "value": [18457.3, 3.81, "辽宁"]},
#             {"name": "四川", "value": [17185.48, 3.54, "四川"]},
#             {"name": "上海", "value": [17165.98, 3.54, "上海"]},
#         ],
#     },
#     {
#         "time": 2015,
#         "data": [
#             {"name": "广东", "value": [72812.55, 9.35, "广东"]},
#             {"name": "江苏", "value": [70116.38, 9, "江苏"]},
#             {"name": "山东", "value": [63002.3, 8.09, "山东"]},
#             {"name": "浙江", "value": [42886, 5.51, "浙江"]},
#             {"name": "河南", "value": [37010.25, 4.75, "河南"]},
#             {"name": "台湾", "value": [32604.52, 4.19, "台湾"]},
#             {"name": "四川", "value": [30103.1, 3.87, "四川"]},
#             {"name": "河北", "value": [29806.1, 3.83, "河北"]},
#             {"name": "湖北", "value": [29550.19, 3.8, "湖北"]},
#             {"name": "湖南", "value": [29047.2, 3.73, "湖南"]},
#         ],
#     },
# ]


def part_data(all_data, first_k = 12):
    #返回确诊人数最多的前12个省份

    data = []
    for d in all_data:
        time_i = d['time']
        data.append({"time": time_i, "data":[]})

    for i_time, data_timei in enumerate(all_data):
        data_i_d = data_timei['data']
        data_i_d_sort = sorted(data_i_d, key = lambda x: x['value'][0], reverse=True)
        data_i_d_k = data_i_d_sort[:first_k]
        data[i_time]['data'] = data_i_d_k

    return data

def get_year_chart(data, all_data, year):
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == year
    ][0]
    map_temp_data = [
        [[x["name"], x["value"][0]] for x in d["data"]] for d in all_data if d["time"] == year
    ][0]
    
    min_data, max_data = (
        min([d[1][0] for d in map_data]),
        max([d[1][0] for d in map_data]),
    )
    map_chart = (
        Map()
        .add(
            series_name="",
            data_pair=map_temp_data,
            label_opts=opts.LabelOpts(is_show=False),
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="中国各省现存确诊人数变化",
                subtitle="确诊人数单位:例",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    bar_x_data = [x[0] for x in map_data]

    # 这里注释的部分会导致 label 和 value 与 饼图不一致
    # 使用下面的 List[Dict] 就可以解决这个问题了。
    # bar_y_data = [x[1][0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
        .add_xaxis(xaxis_data=bar_x_data)
        .add_yaxis(
            series_name="",
            yaxis_index=1,
            y_axis=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b}: {c}"
            ),
        )
        .reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        rotation=JsCode("Math.PI / 4"),
                        bounding="raw",
                        right=110,
                        bottom=110,
                        z=100,
                    ),
                    children=[
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                            graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="rgba(0,0,0,0.3)"
                            ),
                        ),
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                text=f"{str(year)}",
                                font="bold 26px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="#fff"),
                            ),
                        ),
                    ],
                )
            ],
        )
    )

    pie_data = [[x[0], x[1][0]] for x in map_data]
    percent_sum = sum([x[1][1] for x in map_data])
    rest_value = 0
    for d in map_data:
        rest_percent = 100.0
        rest_percent = rest_percent - percent_sum
        if d[1][1] != 0:
            rest_value = d[1][0] * (rest_percent / d[1][1])
            break
    pie_data.append(["其他省份", rest_value])
    pie = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["12%", "20%"],
            center=["75%", "85%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    grid_chart = (
        Grid()
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="70%", pos_bottom="5"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts())
        .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart

if __name__ == '__main__':
    # base_dir = 'D:/大三下/简历/深研院夏令营报名/入营附件/DXY'
    base_dir = 'C:/Users/hasee/Desktop/pa'
    f_list = get_flist(base_dir)
    time_list, all_data = get_data(base_dir, f_list)
    data = part_data(all_data)

    # Draw Timeline
    # time_list = [1980, 2000, 2005, 2010, 2015]
    timeline = Timeline(
        init_opts=opts.InitOpts(width="1200px", height="800px", theme=ThemeType.DARK)
    )
    for y in time_list:
        g = get_year_chart(data, all_data, year=y)
        timeline.add(g, time_point=str(y))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=500,
        is_loop_play = False,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="50",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    # timeline.render("D:/大三下/简历/深研院夏令营报名/入营附件/china_current.html")
    timeline.render("china_current.html")
