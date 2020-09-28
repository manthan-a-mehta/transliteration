#!/usr/bin/env bash

touch READ.ME
echo "##################################" > READ.ME
echo "" >> READ.ME
echo "Submitted by: Parth Patel" >> READ.ME
echo "M.Tech. CSE, IIT Bombay, 173050032" >> READ.ME
echo "" >> READ.ME
echo "##################################" >> READ.ME
echo "" >> READ.ME
echo "" >> READ.ME
echo "==================================" >> READ.ME
echo "Contents of the folder:" >> READ.ME
echo "==================================" >> READ.ME
echo "" >> READ.ME
echo "" >> READ.ME
echo "##################################" >> READ.ME
echo "" >> READ.ME
echo "" >> READ.ME
echo "==================================" >> READ.ME
echo "parthpatel643@gmail.com" >> READ.ME
echo "==================================" >> READ.ME
find . -maxdepth 3 -type d  -exec cp READ.ME {} \;
