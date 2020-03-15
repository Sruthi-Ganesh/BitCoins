<h1> <b> Bit Coin Transactions </b> </h1>
The project is used to display bit coin transaction retrieved from https://www.blockchain.com/api/api_websocket.
There are three API calls made
1. <b> /show_transactions/ </b> - Displays latest 100 transactions. The data will only change in every 1 minute.
2. <b> /transactions_count_per_minute/{min_value} </b> - Displays number of transactions per minute for the last hour. The data will change every minute.
3. <b> /high_value_addr </b> - Displays the bitcoin addresses which have the most aggregate value in transactions in the last 3 hours.

To run this application,
1. Install <b> kafka & zookeeper </b> - Follow this guide https://tecadmin.net/install-apache-kafka-ubuntu/
2. Install <b> redis-server </b> - sudo apt install redis-server
3. Go into the environment (venv in the git root directory) by executing <b> "source venv/bin/activate" </b> and perform <b> "pip install -r requirements.txt" </b>.
4. Open django shell <b> "python manage.py shell" </b> and execute the following commands
	1. <b> from myapp import producer </b>
	2. <b> producer.connect() </b>
5. Open another django shell <b> "python manage.py shell" </b> and execute the following commands
	1. <b> from myapp import consumer </b>
	2. <b> producer.connect() </b>
6. Open another django shell <b> "python manage.py shell" </b> and execute the following commands
	1. <b> from myapp import websocker_app </b>
	2. <b> websocket_app.connect() </b>
7. In new terminal, Go to <b> bitcoins/bitcoins </b> (where celery.py is present) and run the command <b> "celery -A bitcoins worker -l info" </b>
8. In new terminal, go to <b> bitcoins/ </b> (where manage.py is present) and run <b> "python manage.py runserver <port>" </b>  (Use port only if 8000 is already registered with any other server) 





