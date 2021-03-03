"""
Script for generating fake customers and sales CSV files
"""
import os
import csv
import random
from pathlib import Path
from typing import Iterator

from faker import Faker

CUR_DIR = os.path.dirname(os.path.dirname(__file__))
RES_FOLDER = os.path.join(CUR_DIR, "data")
USERS_NUM = 10_000
CUSTOMERS_FILENAME = "customers.csv"
SALES_FILENAME = "sales.csv"


class FakeDataGenerator:

    PRODUCT_PRICE_RANGE = {
        # product name, min price, max price:
        "TV": (500, 2500),
        "Laptop": (500, 3500),
        "Phone": (150, 1500),
        "Vacuum cleaner": (80, 800),
        "Microwave oven": (100, 600),
        "coffee machine": (100, 5000),
    }
    PRODUCTS = tuple(PRODUCT_PRICE_RANGE.keys())
    MAX_PRODUCTS_PER_CUSTOMER: int = 3

    def __init__(self, users_num: int,
                 res_folder: str = RES_FOLDER,
                 ):
        self._users_num = users_num
        self._res_folder = res_folder
        self._random_seed = 0

        Path(res_folder).mkdir(parents=True, exist_ok=True)

    def generate_customer_data(self, filename: str):
        path = os.path.join(self._res_folder, filename)
        print(f"Going to generate customer data into {path}")
        fieldnames = [
            'first_name',
            'last_name',
            'age',
            'email',
        ]
        random.seed(self._random_seed)

        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for name in self._generate_names():
                first_name, last_name = name.split()
                age = random.randint(20, 55)
                email = f"{first_name.lower()}_{last_name.lower()}@example.com"

                writer.writerow({
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'email': email
                })
        print(f"{self._users_num} rows of customer data generated")

    def generate_sales_data(self, filename: str):
        path = os.path.join(self._res_folder, filename)
        print(f"Going to generate sales data into {path}")
        fieldnames = [
            'client',
            'purchase_date',
            'product',
            'price',
        ]
        random.seed(self._random_seed)

        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            row_count = 0
            for name in self._generate_names():
                purchase_num = random.randint(0,
                                              self.MAX_PRODUCTS_PER_CUSTOMER)

                for _ in range(purchase_num):
                    product = random.choice(self.PRODUCTS)
                    price = self._generate_product_price(product)
                    purchase_date = f"2021-03-{random.randint(1, 30)}"

                    writer.writerow({
                        'client': name,
                        'purchase_date': purchase_date,
                        'product': product,
                        'price': price,
                    })
                    row_count += 1
        print(f"{row_count} rows of sales data generated")

    def _generate_product_price(self, product: str):
        if product in self.PRODUCTS:
            return random.randint(
                *self.PRODUCT_PRICE_RANGE[product],
            )
        else:
            raise ValueError(f"Unknown product {product}")

    def _generate_names(self) -> Iterator[str]:
        """
        Generate fake names.
        :return: next fake name
        """
        # self._fake.seed_instance(self._random_seed)
        # Faker.seed(self._random_seed)
        fake = Faker()
        fake.seed_instance(self._random_seed)

        for _ in range(self._users_num):
            name = fake.unique.name()
            # filter out names with prefixes and suffixes like Mr, Ms, MD etc:
            if len(name.split()) == 2:
                yield name


if __name__ == '__main__':
    fake_data_generator = FakeDataGenerator(
        users_num=USERS_NUM,
    )

    fake_data_generator.generate_customer_data(CUSTOMERS_FILENAME)
    fake_data_generator.generate_sales_data(SALES_FILENAME)
