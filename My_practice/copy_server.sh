#!/bin/bash

echo "改程序可以把母服服务器版本内容复制到对象服务器中，对象服务器会自动清档"
echo "程序不可逆，小心操作！"

read -p " - 输入母服服务器目录名,例如“fytx2_test_p017a” - >>" read_server
read -p " -- 输入目标服服务器目录名 -- >>" target_server
read -p " --- 输入目标服务器ID --- >>" target_server_id 
read_server_path=/data/$read_server/server
target_server_path=/data/$target_server/server
cd $target_server_path
pwd
./close.sh
echo "删除当前服务器..."
rm -rf ./cw ./dbs ./gg ./gt  ./kd ./instance ./svr_source
echo "拷贝母服服务器..."
ln -sf $read_server_path/cw cw
ln -sf $read_server_path/dbs dbs
ln -sf $read_server_path/gg gg
ln -sf $read_server_path/gt gt
ln -sf $read_server_path/kd kd
ln -sf $read_server_path/instance instance
echo "拷贝完成"

echo "服务器清档..."
DB='mongo --port 37017'
$DB<<EOF
use sid$target_server_id
db.dropDatabase()
exit;
EOF
echo "清档完成"

./start.sh
echo "母服$read_server" > copy_$read_server.txt
