import csv
import sqlite3
DATAFILE = "AppleStore.csv"
lista = []



with open(DATAFILE, encoding="utf8") as csv_file:
    #csv_reader = csv.reader(csv_file)
    csv_reader = csv.DictReader(csv_file)
    
    cabecalho = True
    for row in csv_reader:
        if cabecalho:
            #print(f'Nomes das colunas: {", ".join(row)}')
            cabecalho = False
        else:
          #print(type(row))
            #print(row['prime_genre'])
            linha = {'id': row['id'],'track_name':row['track_name'], 'size_bytes':row['size_bytes'],'currency':row['currency'],'price':row['price'],'rating_count_tot':row['rating_count_tot'],'rating_count_ver':row['rating_count_ver'],'user_rating':row['user_rating'],'user_rating_ver':row['user_rating_ver'],'cont_rating':row['cont_rating'],'prime_genre':row['prime_genre']}
            #print(linha['prime_genre'])
            lista.append(linha)

def criar_tabela():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS tb_news")
    cursor.execute("DROP TABLE IF EXISTS tb_music_book")
    cursor.execute('CREATE TABLE if not exists tb_news(id integer,track_name text,rating_count_tot text, size_bytes integer, price text, prime_genre text)')

    cursor.execute('CREATE TABLE if not exists tb_music_book(id integer,track_name text,rating_count_tot text, size_bytes integer, price text, prime_genre text)')


criar_tabela()

def save_maior_news(lista):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    for l in lista:
        cursor.execute("INSERT INTO tb_news VALUES('"+l['id']+"','"+l['track_name']+"','"+l['rating_count_tot']+"','"+l['size_bytes']+"','"+l['price']+"','"+l['prime_genre']+"')")
        connection.commit()


###### Salvar os 10 maiores music e book no csv ######
def save_10_maior_music_book_csv(lista):
    with open('10_maior_music_book.csv', mode='w', encoding="utf8") as file:
        fieldnames = ['id', 'track_name','rating_count_tot','size_bytes','price','prime_genre']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for l in lista:
            writer.writerow({'id': l['id'], 'track_name': l['track_name'],'rating_count_tot':l['rating_count_tot'],'size_bytes':l['size_bytes'],'price':l['price'],'prime_genre':l['prime_genre']})


###### Salvar os 10 maiores music e book no banco local ######
def save_10_maior_music_book_db(lista):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    for l in lista:
        cursor.execute("INSERT INTO tb_music_book VALUES('"+l['id']+"','"+l['track_name']+"','"+l['rating_count_tot']+"','"+l['size_bytes']+"','"+l['price']+"','"+l['prime_genre']+"')")
        connection.commit()


def exibir_dados_tabela(tabela):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()


    sql = "SELECT * FROM '"+tabela+"'"
    cursor.execute(sql)
    #print(cursor.fetchall())
    if tabela == "tb_news":
        print("\nMaior avaliação news:\n")
        for row in cursor.execute("SELECT  * FROM '"+tabela+"'"):
            print(row)
    else:
        print("\nLista das 10 maiores avaliações Music e Book:\n")
        for row in cursor.execute("SELECT  * FROM '"+tabela+"'"):
            print(row)


def maior_news_rating_count_tot(lista):
    nova_lista = []
    for l in lista:
        if(l['prime_genre'] == "News"):
            nova_lista.append({"id":l['id'],'track_name':l['track_name'],'rating_count_tot':l['rating_count_tot'],'size_bytes':l['size_bytes'],'price': l['price'],'prime_genre':l['prime_genre']})
    lista_retorno = sorted(nova_lista, key=lambda x: int(x['rating_count_tot']), reverse=True)[:1]
    save_maior_news(lista_retorno)
    exibir_dados_tabela("tb_news")
    return lista_retorno


def maior_music_book_rating_count_tot(lista):
    lista_music = []
    lista_book = []
    for l in lista:
        if(l['prime_genre'] == "Music"):
            lista_music.append({"id":l['id'],'track_name':l['track_name'],'rating_count_tot':l['rating_count_tot'],'size_bytes':l['size_bytes'],'price': l['price'],'prime_genre':l['prime_genre']})
        if(l['prime_genre'] == "Book"):
            lista_book.append({"id":l['id'],'track_name':l['track_name'],'rating_count_tot':l['rating_count_tot'],'size_bytes':l['size_bytes'],'price': l['price'],'prime_genre':l['prime_genre']})
    lista_retorno_music = sorted(lista_music, key=lambda x: int(x['rating_count_tot']), reverse=True)[:10]

    lista_retorno_book = sorted(lista_book, key=lambda x: int(x['rating_count_tot']), reverse=True)[:10]
    lista_retorno_music.extend(lista_retorno_book)
    save_10_maior_music_book_db(lista_retorno_music)
    save_10_maior_music_book_csv(lista_retorno_music)
    exibir_dados_tabela("tb_music_book")
    return lista_retorno_music



#Exibir a maior aplicação News
maior_news_rating_count_tot(lista)
maior_music_book_rating_count_tot(lista)





