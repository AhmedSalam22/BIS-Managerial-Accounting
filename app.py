import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import base64



st.title("Mangerial Accounting")


def high_low_method():
    st.markdown("""
                ##### Note: High-Low method used to seperate semi-variable into (Fixed Cost and variable cost)
                """)
    volume_high = st.number_input("Maximum Volume (activity level)-High" , 45000.0)
    volume_low  = st.number_input("Minumum Volume (activity level)-Low" , 32000.0)
    cost_high = st.number_input("Maximum cost -High" , 217500.0)
    cost_low  = st.number_input("Minumum cost -Low" , 159000.0)

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
        volume_range[0] = 0
        # st.write(volume_range)
        cost_range =  total_fixed_cost + vc_unit * volume_range        
        # st.write(cost_range)
        predication_data = {
            "volume":volume_range , 
            "semi-variable cost" : cost_range
        }

        df_predication = pd.DataFrame(predication_data)
        df_predication["FC"] = total_fixed_cost
        df_predication["VC"] = vc_unit * volume_range 

        st.markdown("### Sample for predective model")
        st.write(df_predication)

       
        # df_predication.plot(x= "volume" , y ="cost", kind="line")
        # df_predication.plot(x= "volume" , y ="FC", kind="line")
        df_predication.set_index("volume").plot.line()
        plt.title("Predection Model")
        plt.ylabel("cost")
        st.pyplot()


def cost_statement():
    production_volume = st.number_input("Production Volume" , 12000.0)
    sales_volume = st.number_input("sales Volume" , 9000.0)
    sales_price = st.number_input("Sales price" , 20.0)
    beg_fg = st.number_input("beginning finished goods inventory" , 0.0)
    dm = st.number_input("Direct Material per unit" , 1.0)
    dl = st.number_input("Direct Labor per unit" , 2.0)
    v_mfg_oh = st.number_input("variable manufacturing overhead per unit", 4.0)
    f_mfg_oh= st.number_input("Total Fixed manufacturing overhead " , 50000.0)
    f_selling = st.number_input("Total Fixed selling cost" , 20000.0)
    v_selling = st.number_input("variable  selling cost per unit" , 1.0)
    f_administrative = st.number_input("Total Fixed administrative" , 0.0)

    cost_type = st.selectbox("Cost Type" , ["" ,"Direct" , "Absorption"] )

    Units_Of_Goods_Available_For_Sale = beg_fg + production_volume
    cost_of_goods_manufactured = ((((dm + dl + v_mfg_oh) * production_volume) + f_mfg_oh)/production_volume) * production_volume
    cost_of_beg_fg_inventory = beg_fg * (((dm + dl + v_mfg_oh) * production_volume) + f_mfg_oh)/production_volume
    cost_of_ending_fg_inventory = (Units_Of_Goods_Available_For_Sale - sales_volume) *  (((dm + dl + v_mfg_oh) * production_volume) + f_mfg_oh)/production_volume
    mainpulated_Data = {
        "Units Of Goods Available For Sale":  Units_Of_Goods_Available_For_Sale,
        "Ending F.G Inventory" : Units_Of_Goods_Available_For_Sale - sales_volume ,
        "Prime Cost":  dm + dl ,
        "Sales Revenue":  sales_volume * sales_price , 
        "V. MFG": dm + dl + v_mfg_oh , 
        "Total MFG": ((dm + dl + v_mfg_oh) * production_volume) + f_mfg_oh , 
        "MFG/Unit": (((dm + dl + v_mfg_oh) * production_volume) + f_mfg_oh)/production_volume ,
        "F.MFG OH /unit": f_mfg_oh // production_volume ,
        "Cost Of Beg F.G Inventory": cost_of_beg_fg_inventory  ,
        "Cost Of Ending F.G Inventory": cost_of_ending_fg_inventory, 
        "FC In Beg F.G inventory":  beg_fg * f_mfg_oh, 
        "FC In Ending F.G inventory": (Units_Of_Goods_Available_For_Sale - sales_volume) * f_mfg_oh /production_volume, 
        "Cost of Goods Maunfatcured": cost_of_goods_manufactured,
        "V.Cost of Goods Manufactured" : (dm + dl + v_mfg_oh) * production_volume, 
        "Cost of Goods Sold": cost_of_goods_manufactured
                                + cost_of_beg_fg_inventory
                                - cost_of_ending_fg_inventory , 
        "V.Cost Of Goods Sold": sales_volume  * (dm + dl + v_mfg_oh),
        "Gross Profit": (sales_volume * sales_price) - (cost_of_goods_manufactured +cost_of_beg_fg_inventory -cost_of_ending_fg_inventory), 
        "V.selling Cost": sales_volume * v_selling , 
        "Contribution Margin": (sales_volume * sales_price) -(sales_volume  * (dm + dl + v_mfg_oh)) - (sales_volume * v_selling)
                    
    }

    st.markdown("### mainpulated_Data")
    if st.checkbox("Show mainpulated_Data" , False):
        st.write(mainpulated_Data)

    if cost_type == "Absorption":
        st.markdown("#### Cost Statement under Absorption")
        st.markdown("""
        ```
        Production Volume		 {production_volume}
        Product Cost			
            DM			 {dm} 
            DL			 {dl}
            V.MFG OH			 {total_v_mgf_oh}
            F.MFG OH			 {total_f_mfg_oh}
                    Cost of Goods Manufactured			 {cost_of_goods_manufactured} 
        + Cost of Beg F.G Inventory			      {BgFG}  
        - Cost of Ending F.G Inventory			  ({EnfingFG}) 
                    Cost Of Good Sold			   {COGS}
                
        """.format(production_volume=production_volume , 
                    dm = dm * production_volume , 
                    dl = dl * production_volume , 
                    total_v_mgf_oh = v_mfg_oh * production_volume  , 
                    total_f_mfg_oh = f_mfg_oh , 
                    cost_of_goods_manufactured = mainpulated_Data["Cost of Goods Maunfatcured"] , 
                    BgFG = mainpulated_Data["Cost Of Beg F.G Inventory"] , 
                    EnfingFG = mainpulated_Data["Cost Of Ending F.G Inventory"] , 
                    COGS = mainpulated_Data["Cost of Goods Sold"]

        
                )
        
        )

        st.markdown("### Income Statement under Absorption	")
        st.markdown("""
        ||
        |-----------|---------------|
        |Sales Volume|			{sv}|
        |Sales Rvenue|			{sr}|
        |-Cost of Good sold|	({cogs})    |
        |Gross Profit|			{gp}|
        |-v.Selling Cost|		({vsc})|
        |-F.Selling|			({fsc})|
        |-f.administrative|			({fa})|
        |Net Operating Income|			{noi}|

        
        """.format(
                    sv = sales_volume ,
                    sr = mainpulated_Data["Sales Revenue"] ,
                    cogs = mainpulated_Data["Cost of Goods Sold"] ,
                    gp = mainpulated_Data["Gross Profit"] ,
                    vsc = mainpulated_Data["V.selling Cost"] ,
                    fsc = f_selling , 
                    fa = f_administrative , 
                    noi = mainpulated_Data["Gross Profit"] - mainpulated_Data["V.selling Cost"] - f_selling - f_administrative

        )
        
        
        )
    elif cost_type == "Direct":
        st.markdown("### Cost Statement under Direct")
        st.markdown("""
        ```
                Production Volume		   {pv}
                Product Cost			
                    DM			            {dm}
                    DL			            {dl} 
                    V.MFG OH			    {v_mfg_oh} 
                            
                        V.Cost of Goods Manufactured  {v_cgmfg}
                + V.Cost of Beg F.G Inventory			 {v_cbfg}   
                -V. Cost of Ending F.G Inventory		({v_cefg}) 
                    V. Cost Of Good Sold			 {cogs}
        ```
                    """.format(
                        pv = production_volume ,
                        dm = dm * production_volume  ,
                        dl = dl * production_volume, 
                        v_mfg_oh = v_mfg_oh *  production_volume, 
                        v_cgmfg =  mainpulated_Data["V.Cost of Goods Manufactured"] , 
                        v_cbfg =  mainpulated_Data["Cost Of Beg F.G Inventory"] - mainpulated_Data["FC In Beg F.G inventory"] , 
                        v_cefg = mainpulated_Data["Cost Of Ending F.G Inventory"] - mainpulated_Data["FC In Ending F.G inventory"],
                        cogs = mainpulated_Data["V.Cost Of Goods Sold"]
                    )
                    )
        st.markdown("### Income Statement under Direct")
        st.markdown("""
        ```
        Sales Volume			{sv}
        Sales Rvenue			{sr}
        -V.Cost of Good sold		({vcogs})
        -V.selling_Cost			({vsc})
        Contribution Margin		{cm}
        - F.MFG OH			({f_mfg_oh})
        -F.Selling			({fs})
        -f.administrative		({fa})
            Net Operating Income	{noi}

        ```
        """.format(
                    sv = sales_volume ,
                    sr = mainpulated_Data["Sales Revenue"] , 
                    vcogs =  mainpulated_Data["V.Cost Of Goods Sold"] ,
                    vsc = mainpulated_Data["V.selling Cost"] , 
                    cm = mainpulated_Data["Contribution Margin"] ,
                    f_mfg_oh = f_mfg_oh , 
                    fs = f_selling,
                    fa = f_administrative ,
                    noi = mainpulated_Data["Contribution Margin"] - f_selling - f_administrative - f_mfg_oh



        )
        
               )
    else:
        st.markdown("# Please select cost type")

    if production_volume > sales_volume:
        st.markdown("##### Note: Net income under absorption is greater than net income under direct")
    elif production_volume < sales_volume:
        st.markdown("##### Note: Net income under absorption is less than net income under direct")
    
    if st.checkbox("Do you want to see Reconciliation " , False):
        st.markdown("""
        ```
                Reconciliation			
        Net Income Under Absorption			{ab}
        +Fc IN Beg F.G Inventory			{fcb}
        -Fc IN Ending F.G Inventory			({fce})
        Net Income Under Direct			        {d}
        """.format(
            ab = mainpulated_Data["Gross Profit"] - mainpulated_Data["V.selling Cost"] - f_selling - f_administrative , 
            fcb = mainpulated_Data["FC In Beg F.G inventory"] ,
            fce = mainpulated_Data["FC In Ending F.G inventory"]  , 
            d = mainpulated_Data["Contribution Margin"] - f_selling - f_administrative - f_mfg_oh

        ) 
                 )





# ----------------------sidebar-------------------------
# High Low Method
if st.sidebar.checkbox("High-Low Method Function" , False):
    high_low_method()

# Cost Statement
if st.sidebar.checkbox("Prepare Cost Statements" , False):
    cost_statement()


st.sidebar.markdown('<a href="mailto:ahmedsalam22@gmail.com">Contact us!</a>', unsafe_allow_html=True)

st.markdown("#### Copyright@Ahmed Maher Fouy Mohamed Salam 2020")