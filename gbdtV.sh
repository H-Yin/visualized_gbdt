
python -c 'import graphviz' > /dev/null 2>&1
if [[ $? -gt 0 ]]; then
    pip install graphviz --user > /dev/null 2>&1
fi;
