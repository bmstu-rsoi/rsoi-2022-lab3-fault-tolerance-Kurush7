sleep 5
docker ps -a
docker exec -i postgres psql -U program libraries < test/libraries.dump
docker exec -i postgres psql -U program ratings < test/ratings.dump
docker exec -i postgres psql -U program reservations < test/reservations.dump