import pandas as pd
from sqlalchemy import create_engine
import os

def setup_database():
    """
    Loads data from CSV files into a SQLite database.
    """
    db_path = os.path.join(os.path.dirname(__file__), 'ecommerce_data.db')
    engine = create_engine(f'sqlite:///{db_path}')

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    try:
        ad_sales_df = pd.read_csv(os.path.join(data_dir, 'Product-Level Ad Sales and Metrics.csv'))
        total_sales_df = pd.read_csv(os.path.join(data_dir, 'Product-Level Total Sales and Metrics.csv'))
        eligibility_df = pd.read_csv(os.path.join(data_dir, 'Product-Level Eligibility.csv'))
    except FileNotFoundError as e:
        print(f"Error loading CSV file: {e}")
        return

    ad_sales_df.to_sql('ad_sales', engine, if_exists='replace', index=False)
    total_sales_df.to_sql('total_sales', engine, if_exists='replace', index=False)
    eligibility_df.to_sql('eligibility', engine, if_exists='replace', index=False)

    print("Database and tables created successfully.")

if __name__ == '__main__':
    setup_database()