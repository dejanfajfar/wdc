wdc start 0730 -t SAH00322 -m "Some adaptations"
[ $? -eq 0 ]  || exit 1
wdc start 1015 -t bespr -m "Daily standup"
[ $? -eq 0 ]  || exit 1
wdc start 1030 -t SAH00322 -m "Some adaptations"
[ $? -eq 0 ]  || exit 1
wdc start 1130 -t break
[ $? -eq 0 ]  || exit 1
wdc start 1200 -t SAH00501 -m "General analysis"
[ $? -eq 0 ]  || exit 1
wdc start 1500 -t bespr -m "Team coordination"
[ $? -eq 0 ]  || exit 1
wdc start 1515 -t SAH00501 -m "General analysis"
[ $? -eq 0 ]  || exit 1
wdc end -e 1700
[ $? -eq 0 ]  || exit 1
