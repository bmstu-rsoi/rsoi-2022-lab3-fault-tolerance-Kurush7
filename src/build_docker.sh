cd library
docker build -t rsoi_lab2_library .

cd ../rating
docker build -t rsoi_lab2_rating .

cd ../reservation
docker build -t rsoi_lab2_reservation .

cd ..
docker build -f ApiDockerfile -t rsoi_lab2_api .
