# CONNECTION string 
Check one directory up and look in 'connection_string.py' for connection details. Currently set to my localhost, my local user and my password - those will need to be changed. And MAYBE the port will need to be changed.   

# RUN ORDER for the scripts! 
create_database.py   
create_tables.py   
populate_mechants.py   
populate_stores.py   
populate_inventory.py   
populate_featured_products.py   
popullate_users.py
CheckIfOK.py   
    
If CheckIfOK says """OK! The tables are populated properly!""" then it is all good

### The order will matter because foreign key restraints 

# side note
import psycopg2 appears to NOT be needed in the imports, but, haha, it is.