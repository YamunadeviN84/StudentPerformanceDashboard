import mysql.connector
def create_connection(host,user,password):
    conn=mysql.connector.connect(
        host="gateway01.us-west-2.prod.aws.tidbcloud.com",
        user="4VNm5hSdn9KZBiM.root",
        password="44L1IntgljTiVfG2"
    )
    return conn