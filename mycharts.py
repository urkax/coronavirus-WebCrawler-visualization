import pyecharts.options as opts
from pyecharts.charts import Line, Timeline
from pyecharts.faker import Faker
import os
import csv

def get_data(base_dir):
    global_history_csv = [f for f in os.listdir(base_dir) if 'globalTotal_history.csv' in f][0]
    china_history_csv = [os.path.join('countryHistory',f) for f in os.listdir(os.path.join(base_dir, 'countryHistory')) if 'China' in f][0]

    with open(os.path.join(base_dir, china_history_csv), encoding="utf-8") as f:
        f_csv = csv.reader(f)
        china_confirmed = []
        times = []
        for line in f_csv:
            china_confirmed.append(line[0])
            times.append(line[6])

        
        china_confirmed = china_confirmed[1:]
        times = times[1:]


def timeline_bar() -> Timeline:
    xs = Faker.choose()
    ys = Faker.values()
    tl = Timeline()
    for i in range(len(xs)):
        c = (
            Line()
            .add_xaxis(xs)
            .add_yaxis("商家A", ys[:i])
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
        )

        tl.add(c, "{}x".format(i))

    return tl

if __name__ == '__main__':
    get_data('C:/Users/hasee/Desktop/pa')
    timeline_bar().render("timeline_bar.html")
