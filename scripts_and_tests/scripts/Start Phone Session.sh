## Start Phone Session
curl -X "POST" "http://localhost:22000/api/MySession/start-session-phone" \
     -H 'Authorization: Bearer $2b$10$Q4R2NmWSs0u6XDIqu2Ywa.RYVuxmT0IQtWotfvOGxqqS.liGGJGX.' \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "phone": "491605740074",
  "webhook": "false"
}'
