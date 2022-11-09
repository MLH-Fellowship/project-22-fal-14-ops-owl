#!/bin/bash
curl --request POST http://localhost:5000/api/timeline_post -d 'name=Sarah&email=smgraywood@gmail.com&content=Just Added Database to Portfolio Site!' {"content":"Just Added Database to Portfolio Site!","created_at":"Mon, 10 Oct 2022 08:50:30 GMT","email":"smgraywood@gmail.com", "id":1,"name":"Sarah"}

curl -X POST http://localhost:5000/api/timeline_post -d 'name=Sarah&email=smgraywood@gmail.com&content=Testing endpoints with postman and curl' {"content":"Testing endpoints with postman and curl","created_at":"Mon, 10 Oct 2022 08:50:30 GMT","email":"smgraywood@gmail.com", "id":1,"name":"Sarah"}


curl --request GET http://localhost:5000/api/timeline_post {"timeline_posts": []}

curl http://localhost:5000/api/timeline_post {"timeline_posts": []}