import streamlit as st
import pandas as pd

# from streamlit_option_menu import option_menu

# title
st.title("데이터 시각화 연구소")

# widgets
if st.button("Show Data"):
    # make dataframe
    df = pd.DataFrame(
        {"first_columns": [1, 2, 3, 4], "second_columns": [10, 20, 30, 40]}
    )

    # write dataframe
    st.write(df)

    # write line chart
    st.line_chart(data=df, x="first_columns", y="second_columns")

else:
    st.write("push the button")

# make sidebar
option = st.sidebar.selectbox("Menu", ("시세조사", "거래량"))
# with st.sidebar:
#     choice = option_menu(
#         "Menu",
#         ["페이지1", "페이지2", "페이지3"],
#         icons=["house", "kanban", "bi bi-robot"],
#         menu_icon="app-indicator",
#         default_index=0,
#         styles={
#             "container": {"padding": "4!important", "background-color": "#fafafa"},
#             "icon": {"color": "black", "font-size": "25px"},
#             "nav-link": {
#                 "font-size": "16px",
#                 "text-align": "left",
#                 "margin": "0px",
#                 "--hover-color": "#fafafa",
#             },
#             "nav-link-selected": {"background-color": "#08c7b4"},
#         },
#     )


# # make dataframe
# df = pd.DataFrame({"first_columns": [1, 2, 3, 4], "second_columns": [10, 20, 30, 40]})

# # write dataframe
# st.write(df)

# # write line chart
# st.line_chart(data=df, x="first_columns", y="second_columns")
