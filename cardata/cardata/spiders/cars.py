import scrapy
import pandas as pd


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['www.cars.com']

    start_urls = [
        'https://www.cars.com/shopping/results/?page=1&page_size=100&list_price_max=&makes%5B%5D=toyota&maximum_distance=all&models%5B%5D=&stock_type=all&zip='
    ]

    def parse(self, response):
        cols = ['year', 'make', 'model', 'cond', 'mileage', 'price']

        names = response.xpath("//div[@class='vehicle-details']//a//h2/text()").getall()
        cond = response.xpath("//div[@class='vehicle-details']//p/text()").getall()
        mileage = response.xpath("//div[@class='vehicle-details']//div[@class='mileage']/text()").getall()
        price = response.xpath("//span[@class='primary-price']/text()").getall()

        name_str = [s.split(maxsplit=2) for s in names]

        year = [s[0] for s in name_str]
        make = [s[1] for s in name_str]
        model = [s[2] for s in name_str]

        price = [p.replace('$', '').replace(',', '') for p in price]

        mileage = [m.strip().replace(' mi.', '').replace(',', '') for m in mileage]

        zipped_list = list(zip(year, make, model, cond, mileage, price))

        df1 = pd.DataFrame(
            data=zipped_list,
            columns=cols
        )

        # df1.to_csv('df1.csv', index=False)
        df2 = pd.read_csv(r'../../Used_Car_Price_Data.csv')
        df2[['year', 'make', 'model']] = df2['Name'].str.split(n=2, expand=True)

        del df2['Name']

        df2.rename(
            {
                'Price($)': 'price',
                'Milage': 'mileage',
                'Review': 'review',
                'Review_count': 'review_count',
                'Badge': 'badge'
            },
            axis='columns',
            inplace=True
        )

        df2['mileage'] = df2['mileage'].str.replace(',', '')
        df2['price'] = df2['price'].str.replace(',', '')

        df_concat = pd.concat(
            [df1, df2],
            ignore_index=True,
            sort=True
        )

        df_concat = df_concat[cols]

        df_concat.to_csv('../../concat_toyota_values.csv', index=False)

        return
