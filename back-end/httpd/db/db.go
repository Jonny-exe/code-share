package db

import (
	"database/sql"
	"log"
	"os"
	"path"
	"reflect"

	"github.com/joho/godotenv"
)

var connectionKey = getDirs()

// GetDirs ..
func getDirs() string {
	var err error
	ex, err := os.Executable()
	if err != nil {
		log.Fatal(err)
	}
	log.Print("Executable is ", ex)
	dir := path.Dir(ex)
	log.Println("Dir of executable is ", dir)

	if err != nil {
		log.Fatal("Error connecting to db: ", err)
	}
	dir = os.Getenv("CODE_SHARE_ENV")
	log.Println("Env variable GO_MESSAGES_DIR is: ", dir)
	if dir == "" {
		log.Println("Error: GO_MESSAGES_DIR is not set.")
		log.Println("Error: Set it like: export GO_MESSAGES_DIR=\"/home/user/Documents/GitHub/go-server/httpd\"")
	}

	enverr := godotenv.Load(dir + "/.env")
	if enverr != nil {
		log.Println("Error loading .env file: ", enverr)
	}

	// e.g.: export GO_MESSAGES_DIR="/home/a/Documents/GitHub/go-server/httpd"
	dir = os.Getenv("WEB_MAKER_ROOT")
	// dir = "/home/a/Documents/GitHub/web-maker/web-maker-server/httpd"
	log.Println("Env variable WEB_MAKER_ROOT is: ", dir)
	if dir == "" {
		log.Println("Error: WEB_MAKER_ROOT is not set.")
		log.Println("Error: Set it like: export WEB_MAKER_ROOT=\"/home/user/Documents/GitHub/web-maker\"")
	}

	log.Println("Connecting to Mariadb")
	connectionKey := os.Getenv("DB_CONNECTION")
	log.Println("DB_CONNECTION: ", connectionKey)
	return connectionKey
}

func Connect() {
	// sql.Register("mysql", &MySQLDriver{})

	// db, err = sql.Register("mysql")
	db, err := sql.Open("mysql", connectionKey)

	if err != nil {
		log.Fatal("Error login in mysql: ", err)
	}
	defer db.Close()
	err = db.Ping()
	log.Println("Ping: ", db.Ping())
	if err != nil {
		log.Fatal("Ping failed: ", err)
	}

	_, err = db.Exec("CREATE DATABASE IF NOT EXISTS web_maker")
	if err != nil {
		log.Fatal("Error creating database: ", err)
	}
	_, err = db.Exec("USE web_maker")
	if err != nil {
		log.Fatal("Error selecting database: ", err)
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS token_object ( token varchar(30), object longtext)")
	if err != nil {
		log.Fatal("Error creating token_object table: ", err)
	}

	_, err = db.Exec("CREATE TABLE IF NOT EXISTS token_recovery ( token varchar(30), recovery varchar(30))")
	if err != nil {
		log.Fatal("Error creating token_recovery table: ", err)
	}

	log.Println(reflect.TypeOf(db))
	// hanlder.Insert()
	return
}

func getConnection() *sql.DB {
	var db *sql.DB
	db, err := sql.Open("mysql", connectionKey)

	if err != nil {
		log.Fatal("Error login in mysql: ", err)
	}
	_, err = db.Exec("USE web_maker")
	return db
}
