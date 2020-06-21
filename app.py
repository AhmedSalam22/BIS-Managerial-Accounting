import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


st.title("Mangerial Accounting")

# High Low Method
if st.sidebar.checkbox("High-Low Method Function" , False):
    st.markdown("""
                ##### Note: High-Low method used to seperate semi-variable into (Fixed Cost and variable cost)
                """)
    volume_high = st.number_input("Maximum Volume (activity level)-High")
    volume_low  = st.number_input("Minumum Volume (activity level)-Low")
    cost_high = st.number_input("Maximum cost -High")
    cost_low  = st.number_input("Minumum cost -Low")

    vc_unit = (cost_high - cost_low) / (volume_high - volume_low)
    total_fixed_cost = cost_high - (volume_high * vc_unit)
    st.markdown("""
    ## Result :
    ```
             VC/unit = {a}
             Total fixed cost = {b}
    ```
                

    ```math
                    Y = a + b * x
                    Y = {a} + {b} * x
    Where: 
            Y is Semi-variable
            a is Total fixed cost 
            b is variable cost / unit
            x is volume (activity level)
     ```
    """.format(a=vc_unit , b = total_fixed_cost))
    if vc_unit == 0:
        st.title("Note: it is not a semi variable ")

    # for predication vizualization
    if vc_unit != 0 and volume_high !=0 and volume_low !=0 and cost_high != 0  and cost_low != 0 :
        # Create list from low to high volume  and cost
        volume_range = np.linspace(volume_low , volume_high , 10)
        volume_range = np.array(list(map(lambda x: int(x) , volume_range)))
        # st.write(volume_range)
        cost_range =  total_fixed_cost + vc_unit * volume_range        
        # st.write(cost_range)
        predication_data = {
            "volume":volume_range , 
            "cost" : cost_range
        }

        df_predication = pd.DataFrame(predication_data)
        # st.write(df_predication)

       
        df_predication.plot(x= "volume" , y ="cost", kind="line")
        plt.title("Predection Model")
        plt.ylabel("cost")
        st.pyplot()

st.markdown("#### Copyright@Ahmed Maher Fouy Mohamed Salam 2020")