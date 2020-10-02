from app import add, call_external_api

add.delay(5,2)
add.delay(4,9)
add.delay(5,87)
add.delay(6,1)

call_external_api.delay()
call_external_api.delay()
call_external_api.delay()
call_external_api.delay()

print("Tasks have been called! ")
print("Run `docker-compose logs -f celery-logger` to see the logger in action.")