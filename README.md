# Natual Language Query Machine powered by ChatGPT

Natural Language Query Machine takes natural language queries as input, uses ChatGPT to generate SQL statements, and then sends these SQL statements to a real database to retrieve data.

Typically, data analysis teams spend a lot of effort processing data extraction requests from business teams, marketing teams, and others. By using Natural Language Query Machine, business and marketing teams can directly input natural language queries and receive the resulting extracted data themselves.

In cases where it is difficult to hire data analysts, such as in startups, it can be useful.

-----------
## You can improve your data analysis process

As-is

Data extraction requests from other team -> Data analysts make queries -> Extracted data

To-be

Directly ask the requests to Natural Language Query Machine -> Query Machine make queries with ChatGPT and get data from real DB -> Extracted data 

------------


## Install and Run
1. git clone
   
   Clone this repository where you want to operate this software.
   Please check file write permission of the directory that this repository would be cloned.
2. pip install 
   ```
   pip install -r requirements.txt
   ```
3. setting environment parameters

   You should get APIkey and OrganizationID for ChatGPT before using this software. 
   See this page https://platform.openai.com/account/api-keys, https://platform.openai.com/account/org-settings
   
   apikey.sh 
   ```
   export API_KEY=YOUR_API_KEY
   export ORGANIZATION=YOUR_ORGANIZATION
   ```

   at shell
   ```
   source apikey.sh
   ```
4. DB configuration

   You can set your own DB configuration with yaml files. This file is composed of four parts. 
   1. name : name of DB. should be unique
   2. type : type of DB. Now we only have MariaDB, SqliteDB, FireBirdDB. You can add new type DB connector in `db.py`
   3. connection : connection information of DB. If you want to know what you need for this part, then check the init method of classes in `db.py` 
   4. tables : You should specify two parameters here. `table_schema_type` is for specifying how we provide table information to the ChatGPT, and you can choose either `ddl` or `yaml`. `table_schema_path` is the path of the file that specifies table schema. I will skip the detailed explanation. Please refer to the example file. `./configs/finance/tables.yaml`, `./configs/music/ddl`

    `./configs/dbconfigs.yaml`
   ```
   - name: music
     type: SqliteDB
     connection:
        database: ./configs/music/chinook.db
     tables:
        table_schema_type: ddl
        table_schema_path: ./configs/music/ddl

   - name: finance
     type: FireBirdDB
     connection:
       host: 172.26.80.1
       port: 3050
       user: sysdba
       password: masterkey
       database: FIREBIRD_DB_FILE_PATH
     tables:
       table_schema_type: yaml
       table_schema_path: ./configs/finance/tables.yaml

   ```
5. run API

   check your network configuration and run API server
   ```
   python -m uvicorn main:app --host=0.0.0.0 --port=8000
   ```
   If you have been following all processes well, then you can open the address `127.0.0.1:8000` in your web browser.
   Choose the DB you want ask, and input your question in natural language.
   You can see the sql sentence is generated, and you can click the download button below. (csv file would be downloaded)

   - If you want to use query machine core without API server, then check `example.py`.
   - If you want to read the documents for API, then check `127.0.0.1:8000/docs`.

6. example natural language query
   ```
   query : daily revenue
   
   output sql : SELECT strftime('%Y-%m-%d', i.InvoiceDate) AS Date, SUM(ii.UnitPrice * ii.Quantity) AS Revenue FROM invoices i JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId GROUP BY Date ORDER BY Date DESC;
   ```
   
   ```
   query : top 10 customers
   
   output sql : SELECT c.FirstName, c.LastName, SUM(i.Total) as TotalSpent FROM customers c JOIN invoices i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId ORDER BY TotalSpent DESC LIMIT 10;
   ```
   
   ```
   query : Customers who spent the most money on a daily basis.
   
   output sql : SELECT c.CustomerId, c.FirstName || ' ' || c.LastName AS CustomerName, strftime('%Y-%m-%d', i.InvoiceDate) AS InvoiceDate, SUM(ii.UnitPrice * ii.Quantity) AS TotalSpent FROM customers c INNER JOIN invoices i ON c.CustomerId = i.CustomerId INNER JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId GROUP BY c.CustomerId, InvoiceDate ORDER BY TotalSpent DESC;
----------

## Important note
- We do not take responsibility for the results obtained using this software.
- This software was created as a hobby project, and although we will pay some attention to its maintenance, we will not invest a significant amount of effort into it.
- Especially, the quality of webpage is very bad. We have no plans to improve it.
- This software sends your query and your database table schema to ChatGPT.
