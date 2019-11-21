import requests
from Crawler_test import price_url,coin_list_url
import pandas as pd
from Crawler_test import headers as crawler_headers
import os
coin_list_cookies={
    '__cfduid': 'd68054b144b436dcd6f99ee3966182ffe1574195426',
    '_ga': 'GA1.2.229848946.1574195428',
    '_gid': 'GA1.2.1930892196.1574195428',
    '_fbp': 'fb.1.1574195428447.2064039032',
    '__gads': 'ID=c7728118c0cfe30d:T=1574195428:S=ALNI_MYnlBxphTjtl-BZ1EHt2qiRagZoTg',
    'rtk_gdpr_a': '0',
    'rtk_gdpr_c': 'US',
}
coin_list_headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'If-Modified-Since': 'Tue, 19 Nov 2019 20:45:04 GMT',
    'Cache-Control': 'max-age=0',
}
class Crawler:
    def __init__(self):
        self._session=requests.Session()
        self._headers=crawler_headers
        self._session.headers=self._headers
        self._df_list=[]
        self._coin_info_nodes=[]
    def Initial(self):
        api_response=requests.get(url=coin_list_url,headers=coin_list_headers,cookies=coin_list_cookies)
        data=api_response.json()
        for i in range(20):
            self._coin_info_nodes.append(CoinInfo(data[i]['name'],data[i]['symbol'],data[i]['id'],data[i]['slug']))
    def GetData(self):
        for node in self._coin_info_nodes:
            params=(
                ('convert','USD,{}'.format(node._symbol)),
                ('format','chart_crypto_details'),
                ('id',str(node._id)),
                ('interval', '5m'),
                ('time_end', '1574236800'),
                ('time_start', '2019-11-01')
            )
            api_response=self._session.get('https://web-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical',params=params,timeout=100)
            data=api_response.json()['data']
            for item in data:
                templist=[str(item)]
                for itm in data[item]['USD']:
                    templist.append(itm)
                self._df_list.append(templist)
            column_list=['time','price','24h_vol','capital_vol']
            df=pd.DataFrame(self._df_list,columns=column_list)
            df.to_csv('{}_data.csv'.format(node._symbol),index=False)
            self._df_list=[]
            print('{} Done'.format(node._symbol))
class CoinInfo:
    def __init__(self,name,symbol,id,slug):
        self._name=name
        self._symbol=symbol
        self._id=id
        self._slug=slug
class CsvDeal:
    def __init__(self):
        self._csv_name_list=[]
        self._df_list=[]
        self._name_list=[]
    def GetCorr(self):
        file_path="C:\\Users\\Alec-J\\OneDrive - Dezhkeda\\Coding\\tradingSystem1\\paxful\\csgoPaxful\\wxm's proj"
        file_list=os.listdir(file_path)
        for item in file_list:
            if item.find('csv')!=-1:
                self._csv_name_list.append(item)
            else:continue
        csv_list=[]
        for csvfile in self._csv_name_list:
            csv_df= pd.read_csv(csvfile,names=['time','price','24h_vol','capital_vol'])
            self._name_list.append(csvfile.replace('.csv',''))
            temp_list=csv_df['price'].tolist()[1:]
            for i in range(len(temp_list)):
                temp_list[i]=float(temp_list[i])
            csv_list.append(temp_list)
        for i in range(153) :
            temp_list=[]
            for list_node in csv_list:
                temp_list.append(list_node[i])
            self._df_list.append(temp_list)
        ''' for i in range(len(csv_list)):
        for j in range(i+1,len(csv_list)):
        a=stats.pearsonr(np.array(csv_list[i]),np.array(csv_list[j]))
        print(self._name_list[i]+', '+self._name_list[j]+': '+str(a))'''
        df=pd.DataFrame(self._df_list,columns=self._name_list)
        print(df)
        corr_df=df.corr()
        corr_df.to_csv('correlation_matrix.csv')
'''def main():
    csv_dealer=CsvDeal()
    csv_dealer.GetCorr()


if __name__ == '__main__':
    main()
'''


def main():
    crawler=Crawler()
    crawler.Initial()
    crawler.GetData()


if __name__ == '__main__':
    main()
