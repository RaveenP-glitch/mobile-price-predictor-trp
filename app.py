import streamlit as st
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

# import the model
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

add_selectbox = st.sidebar.selectbox(
    "Get Started!",
    ("Price Predictor", "Price Tracker")
)

if add_selectbox == 'Price Predictor':
    st.title("Mobile Phone Price Predictor 	📱")

    # brand
    brand = st.selectbox('Brand',df['Brand'].unique())

    # Model of the mobile phone
    model = st.selectbox('Model',df['Model'].sort_values().unique())

    # Rom
    rom = st.selectbox('ROM (in GB)',[2,4,6,8,12,16,24,32,64,128,256,512,1024])

    # Ram
    ram = st.selectbox('RAM (in MB)',df['RAM'].unique())

    #OS
    os = st.selectbox('OS',df['OS'].unique())

    # screen size
    screen_size = st.number_input('Screen Size')

    # Dual Sim
    dual_sim = st.selectbox('Dual SIM',['No','Yes'])

    # Expandable Memory
    expandable_memory = st.selectbox('Expandable Memory',['No','Yes'])

    # 5G
    connectivity = st.selectbox('5G',['No','Yes'])

    # Fingerprint Sensor
    fingerprint = st.selectbox('Fingerprint Sensor',['No','Yes'])


    if st.button('Predict Price'):
        # query
        if dual_sim == 'Yes':
            dual_sim = 1
        else:
            dual_sim = 0

        if expandable_memory == 'Yes':
            expandable_memory = 1
        else:
            expandable_memory = 0

        if connectivity == 'Yes':
            connectivity = 1
        else:
            connectivity = 0

        if fingerprint == 'Yes':
            fingerprint = 1
        else:
            fingerprint = 0

        # X_res = int(resolution.split('x')[0])
        # Y_res = int(resolution.split('x')[1])
        # ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
        query = np.array([brand,model,rom,ram,os,screen_size,dual_sim,expandable_memory,connectivity,fingerprint])

        query = query.reshape(1,10)
        pred_price = round(pipe.predict(query)[0],2)
        st.header("The predicted price for this configuration is: Rs. " + str(pred_price))


        depreciation_rate = 25
        if(brand == 'Apple'):
            depreciation_rate = 20

        curr_cpi = 254
        old_cpi = 130
        new_price = pred_price * curr_cpi / old_cpi
        newd_price = new_price*(100-depreciation_rate)/100
        #st.header("The Price after inflation adjustment is: Rs. " + str(round(newd_price,2)))
        st.text("*All prices are in LKR")

    ROM = str(rom)

    if st.button('Scrape the Web'):
        weblink = 'https://ikman.lk/en/ads/sri-lanka?sort=relevance&buy_now=0&urgent=0&query=' + brand + '%20' + model + '%20' + ROM + 'gb&page=1'
        print(weblink)
        baseurl = "https://ikman.lk"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
                    }

        k = requests.get(weblink).text
        soup = BeautifulSoup(k, 'html.parser')
        productlist = soup.find_all("div", {"class": "price--3SnqI color--t0tGX"})
        print(productlist)
        # <div class="price--3SnqI color--t0tGX"><span>Rs 209,000</span><span class="spacer--904y9"></span></div>
        priceList = []
        try:
            for i in range(len(productlist)):
                #             list_item_names_tmain = item_list_names[i].text
                #             print(list_item_names_tmain)

                price_list_index = productlist[i]
                price_list_tmain = price_list_index.find("span").text
                priceList.append(price_list_index.find("span").text)
                print(price_list_index.find("span").text)

            #             links_to_sites_index = list_links_to_itms[i]
            #             sites_links_tmain = "https://ikman.lk/" + links_to_sites_index.get('href')
            #             print("https://ikman.lk/" + links_to_sites_index.get('href'))
            print(price_list_tmain)
            st.success("Scraped successfully !")

        except Exception as e:
            print("error: ", e)
            st.error("Error! Couldn't find enough data for the given configuration.")

        df = pd.DataFrame(priceList)
        df[0] = df[0].str.replace("Rs ", "")
        df[0] = df[0].str.replace(",", "")
        df2 = df[0].astype(float)
        q_low = df2.quantile(0.20)
        q_hi = df2.quantile(0.75)

        df_filtered = df2[(df2 < q_hi) & (df2 > q_low)]

        st.header("The mean price from ikman.lk is: Rs. " + str(round(df_filtered.mean(), 2)))
        st.text("*Prices are in LKR")

if add_selectbox == 'Price Tracker':
    st.write('Welcome to the Price Tracker');
    st.title("Mobile Phone Price Tracker 📊")

    # brand
    brand = st.selectbox('Select the brand', df['Brand'].unique())

    # Model of the mobile phone
    model = st.selectbox('Select the model', df['Model'].sort_values().unique())

    #Tracking interval
    time_interval = st.slider('Select tracking interval(mins)', min_value=0, max_value=120, value=5, step=1, format=None, key=None, help=None,
              on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    st.write('Fetching price data every ',time_interval, ' minutes.')

    data = {
        "Price (LKR)": [42000, 38000, 19000,28000,49200]
    }

    # load data into a DataFrame object:
    dataset = pd.DataFrame(data)
    #Graph showing the price data
    st.markdown("***")
    st.write('Realtime price tracking')
    st.line_chart(data=dataset, x=None, y=None, width=0, height=0, use_container_width=True)