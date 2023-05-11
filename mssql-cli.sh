#! /bin/bash
cat <<EOF 
  __  __    _____    _____    ____    _           _____   _        _____ 
 |  \/  |  / ____|  / ____|  / __ \  | |         / ____| | |      |_   _|
 | \  / | | (___   | (___   | |  | | | |        | |      | |        | |  
 | |\/| |  \___ \   \___ \  | |  | | | |        | |      | |        | |  
 | |  | |  ____) |  ____) | | |__| | | |____    | |____  | |____   _| |_ 
 |_|  |_| |_____/  |_____/   \___\_\ |______|    \_____| |______| |_____|
                                                                         
EXP : 
""" 
1>  select name from sys.databases
2>  go
""" 
EOF

sleep 2
export $(cat .env | xargs)
docker exec -it mssql  /opt/mssql-tools/bin/sqlcmd -S mssql -U sa -P $MSSQL_SA_PASSWORD