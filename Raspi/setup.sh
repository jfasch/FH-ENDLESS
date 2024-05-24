if [ -n "$1" ]; then
    root=$1
else
    root=$(pwd)
fi

export PYTHONPATH=$root/src:$PYTHONPATH
