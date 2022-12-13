docker build -f LibraryDockerfile     -t rsoi_lab3_library .
docker build -f RatingDockerfile      -t rsoi_lab3_rating .
docker build -f ReservationDockerfile -t rsoi_lab3_reservation .
docker build -f ApiDockerfile         -t rsoi_lab3_api .
