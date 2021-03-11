import numpy as np

from env import user, password, host
from utilities import generate_db_url, generate_df

def get_telco(cached=True):
    telco_query = """
    SELECT *
           FROM customers
               JOIN contract_types USING(contract_type_id)
               JOIN internet_service_types USING(internet_service_type_id)
               JOIN payment_types USING(payment_type_id);
    """
    
    return generate_df("telco_churn.csv", telco_query, generate_db_url(user, password, host, "telco_churn"), cached)

def clean_telco(telco_df):
    clean_df = telco_df.copy()
    
    two_year_customers = clean_df[clean_df.contract_type == "Two year"]
    two_year_customers = two_year_customers[['customer_id', 'monthly_charges', 'tenure', 'total_charges']]
    two_year_customers.total_charges = two_year_customers.total_charges.replace(" ", np.nan)
    two_year_customers = two_year_customers.dropna()
    two_year_customers.total_charges = two_year_customers.total_charges.astype(float)
    
    return two_year_customers

def wrangle_telco():
    return clean_telco(acquire_telco())
    