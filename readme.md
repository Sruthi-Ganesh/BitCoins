The project is used to display bit coin transaction retrieved from https://www.blockchain.com/api/api_websocket.
There are three API calls made
1. /show_transactions/ - Displays latest 100 transactions. The data will only change in every 1 minute.
2. /transactions_count_per_minute/{min_value} - Displays number of transactions per minute for the last hour. The data will change every minute.
3. /high_value_addr - Displays the bitcoin addresses which have the most aggregate value in transactions in the last 3 hours.

To run this application,
1. Install kafka & zookeeper - Follow this guide https://tecadmin.net/install-apache-kafka-ubuntu/
2. Install redis-server - sudo apt install redis-server
3. Go into the environment (venv in the git root directory) and perform "pip install -r requirements.txt"
4. Open django shell "python manage.py shell" and execute the following commands
	1. from myapp import producer
	2. producer.connect()
5. Open another django shell "python manage.py shell" and execute the following commands
	1. from myapp import consumer
	2. producer.connect()
6. Open another django shell "python manage.py shell" and execute the following commands
	1. from myapp import websocker_app
	2. websocket_app.connect()
7. In new terminal, Go to bitcoins/bitcoins (where celery.py is present) and run the command "celery -A bitcoins worker -l info"
8. In new terminal, go to bitcoins/ (where manage.py is present) and run "python manage.py runserver <port>" (Use port only if 8000 is already registered with any other server) 





