# RUN ORDER for the scripts! 
create_database.py
create_tables.py
populate_mechants.py
populate_stores.py
populate_inventory.py
populate_featured_products.py
CheckIfOK.py

If CheckIfOK says """OK! The tables are populated properly!""" then it is all good

### The order will matter because foreign key restraints 

# side note
import psycopg2 appears to NOT be needed in the imports, but, haha, it is.