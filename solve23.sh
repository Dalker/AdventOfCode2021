cat solve23c.txt | egrep -o "[0-9]+" | tr "\n" "+" | sed -e "s/+$//" -e "s/+/ + /g"
