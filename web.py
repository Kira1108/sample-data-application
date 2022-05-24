import streamlit as st
from extract import MysqlLoader
from datetime import datetime, date

# an app has a title
st.title('原油价格预测系统')


st.sidebar.title("预测选项")
label = ['Price', 'Open', 'High', 'Low', 'Vol.', 'Change %','prediction']
plot_col = ['Price', 'Open', 'High', 'Low', 'prediction']
select_col = st.sidebar.multiselect("筛选所需要的列", label, default = label)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "选择预测模型",
        ("Moving Averge days = 5", "Moving Averge days = 10")
    )
    
start = st.sidebar.date_input(
    "开始时间",
    date(2018,1,1)
)

end = st.sidebar.date_input(
    "结束时间",
    date(2022,5,4)
)

@st.cache
def load_data(table):
    return MysqlLoader(f"select * from {table}_predict").load()

for table in ['brent', 'wti']:
    data_load_state = st.text(f'Loading data {table}...')
    data = load_data(table)
    data_load_state.text(f'Loading data {table}...done!')
    st.subheader(f'{table} data')
    st.write(data[["Date"] + select_col][
        (data['Date'] >= datetime.combine(start, datetime.min.time())) & 
        (data['Date'] <= datetime.combine(end, datetime.min.time()))
        ])
    names = {'brent':"布伦特",'wti':"WTI"}
    st.text("历史" + names.get(table) + "油价")
    columns = set(plot_col).intersection(set(select_col))
    st.line_chart(
        data[
        (data['Date'] >= datetime.combine(start, datetime.min.time())) & 
        (data['Date'] <= datetime.combine(end, datetime.min.time()))
        ].set_index("Date")[list(columns)]
    )
