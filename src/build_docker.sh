docker build -f LibraryDockerfile     -t rsoi_lab2_library .
docker build -f RatingDockerfile      -t rsoi_lab2_rating .
docker build -f ReservationDockerfile -t rsoi_lab2_reservation .
docker build -f ApiDockerfile         -t rsoi_lab2_api .
