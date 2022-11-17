

in cmd prompot 

***
 python3 -m pip install -r requirements.txt
***


Start docker 

check docker is runninng using this command 
***
  docker ps 
***
using this command you can start the rabbit mq server 
***
  docker run --rm -it -d --hostname my-rabbit --name my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3.10-management
***
