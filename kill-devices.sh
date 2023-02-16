docker container ls -a | grep android | awk '{print $1}' | xargs docker container kill | xargs docker container rm
exit 0
