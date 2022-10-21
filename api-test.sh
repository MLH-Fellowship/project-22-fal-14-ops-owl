#! /usr/bin/env bash

numOfPosts=$(curl -s http://localhost:5000/api/timeline_post | jq '.timeline_posts | length')

newPostId=$(curl -s -X POST http://localhost:5000/api/timeline_post -d "name=bosco&email=bosco.chw@gmail.com&content=random-$((numOfPosts+1))" | jq '.id')

numOfPostsAfterPOST=$(curl -s http://localhost:5000/api/timeline_post | jq '.timeline_posts | length')

if [[ $numOfPostsAfterPOST -eq $((numOfPosts+1)) ]]; then
  echo "Api test passed"
  curl -s -X DELETE "http://localhost:5000/api/timeline_post/$newPostId"
else 
  echo "Api test failed"
fi



