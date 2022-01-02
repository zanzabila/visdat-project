import pandas as pd
import numpy as np
from bokeh.io import output_notebook, output_file, curdoc
from bokeh.plotting import figure, show, reset_output
from bokeh.models import ColumnDataSource, CDSView, HoverTool, Panel
from bokeh.models.widgets import TableColumn, DataTable, Tabs
import math


df_province = pd.read_csv('./data/province.csv', index_col=0)
df_cases = pd.read_csv('./data/cases.csv')

df_province['province_name'] = df_province['province_name'].str[1:]
df_province = df_province[:-1]


# Tab table

stats = df_province.groupby('island')['population'].describe()
stats = stats.reset_index()

src = ColumnDataSource(stats)

table_columns = [TableColumn(field='island', title='Island'),
                TableColumn(field='min', title='Minimum Population'),
                TableColumn(field='50%', title='Median Population'),
                TableColumn(field='max', title='Maximum Population')]

table = DataTable(source=src, columns=table_columns, width=1000)
tab1 = Panel(child=table, title='Population Summary')


# Tab line & bar plot

reset_output()
output_notebook()
cases_cds = ColumnDataSource(df_cases)

fig_line = figure(plot_height=600, plot_width=800,
                  title='Jumlah Terkonfirmasi Positif Maret 2020',
                  x_axis_label='Tanggal', y_axis_label='Jumlah kasus',
                  x_range=df_cases.get('date'),
                  toolbar_location='right')

fig_line.line(x='date', y='acc_confirmed',
              line_color='black',
              legend_label='Kasus akumulasi',
              source=cases_cds)

fig_line.vbar(x='date', top='new_confirmed',
              width=0.8,
              alpha=0.3,
              fill_color='#47A1BF',
              legend_label='Terkonfirmasi positif harian',
              source=cases_cds)

fig_line.vbar(x='date', top='new_released',
              width=0.8,
              alpha=0.3,
              fill_color='#E332B4',
              legend_label='Sembuh harian',
              source=cases_cds)

fig_line.vbar(x='date', top='new_deceased',
              width=0.8,
              alpha=0.3,
              fill_color='#99E332',
              legend_label='Meninggal harian',
              source=cases_cds)

fig_line.vbar(x='date', top='new_tested',
              width=0.8,
              alpha=0.3,
              fill_color='#FFD036',
              legend_label='Tes harian',
              source=cases_cds)

fig_line.vbar(x='date', top='being_checked',
              width=0.8,
              alpha=0.3,
              fill_color='#36FFBC',
              legend_label='Tes dalam proses',
              source=cases_cds)

fig_line.legend.location = 'top_left'

fig_line.xaxis.major_label_orientation = math.pi/3

tooltips = [('Total Kasus', '@acc_confirmed'),
            ('Kasus baru', '@new_confirmed'),
            ('Sembuh', '@new_released'),
            ('Meninggal', '@new_deceased'),
            ('Jumlah tes baru', '@new_tested'),
            ('Dalam proses tes', '@being_checked')]

acc_hover_glyph = fig_line.circle(x='date', y='acc_confirmed', source=cases_cds,
                                  size=15, alpha=0,
                                  hover_fill_color='black', hover_alpha=0.5)

new_confirmed_hover_glyph = fig_line.circle(x='date', y='new_confirmed', source=cases_cds,
                                            size=15, alpha=0,
                                            hover_fill_color='black', hover_alpha=0.1)

new_released_hover_glyph = fig_line.circle(x='date', y='new_released', source=cases_cds,
                                           size=15, alpha=0,
                                           hover_fill_color='black', hover_alpha=0.1)

new_deceased_hover_glyph = fig_line.circle(x='date', y='new_deceased', source=cases_cds,
                                          size=15, alpha=0,
                                          hover_fill_color='black', hover_alpha=0.1)

new_tested_hover_glyph = fig_line.circle(x='date', y='new_tested', source=cases_cds,
                                         size=15, alpha=0,
                                         hover_fill_color='black', hover_alpha=0.1)

being_checked_hover_glyph = fig_line.circle(x='date', y='being_checked', source=cases_cds,
                                            size=15, alpha=0,
                                            hover_fill_color='black', hover_alpha=0.1)

fig_line.add_tools(HoverTool(tooltips=tooltips, renderers=[new_confirmed_hover_glyph,
                                                           new_released_hover_glyph,
                                                           new_deceased_hover_glyph,
                                                           new_tested_hover_glyph,
                                                           being_checked_hover_glyph,
                                                           acc_hover_glyph]))

fig_line.legend.click_policy = 'hide'

tab2 = Panel(child=fig_line, title='Plot Jumlah Kasus')


# Tab scatter

province_cds = ColumnDataSource(df_province)
select_tools = ['box_select',
                'lasso_select',
                'poly_select',
                'tap',
                'reset']

fig_scatter = figure(plot_height=600, plot_width=800,
                     x_axis_label='Populasi per KM persegi',
                     y_axis_label='Kasus terkonfirmasi',
                     title='Perbandingan Kasus Positif terhadap Kepadatan Penduduk',
                     toolbar_location='right',
                     tools=select_tools)

fig_scatter.square(x='population_kmsquare',
                   y='confirmed',
                   source=province_cds,
                   color='#34EB6E',
                   selection_color='#17CF7F',
                   nonselection_color='lightgray',
                   nonselection_alpha='0.3')

tooltips = [('Provinsi', '@province_name'),
           ('Pulau', '@island'),
           ('Ibukota', '@capital_city'),
           ('Kasus positif', '@confirmed'),
           ('Meninggal', '@deceased'),
           ('Sembuh', '@released')]

fig_scatter.add_tools(HoverTool(tooltips=tooltips))

tab3 = Panel(child=fig_scatter, title='Populasi Per KM Persegi & Kasus Terkonfirmasi')


tabs = Tabs(tabs=[tab1, tab2, tab3])

curdoc().add_root(tabs)
