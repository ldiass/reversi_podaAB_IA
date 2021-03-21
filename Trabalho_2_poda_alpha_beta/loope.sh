#!/bin/bash
cd /home/ubuntu/PycharmProjects/reversi_podaAB_IA/Trabalho_2_poda_alpha_beta
var=11
#count=0
until [ $var -lt 1 ]; do
  python server.py reversIA randomplayer -d 4
  let var-=1
done 
