package db

import (
	"database/sql"
	"log"
	"os"
	"path"

	"github.com/joho/godotenv"
)

var connectionKey = GetDirs()

// GetDirs ..
func GetDirs() string {
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

	enverr := godotenv.Load(dir)
	if enverr != nil {
		log.Println("Error loading .env file: ", enverr)
	}

	log.Println("Connecting to Mariadb")
	connectionKey := os.Getenv("DB_KEY")
	log.Println("DB_CONNECTION: ", connectionKey)
	return connectionKey
}

func Connect() {
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

	_, err = db.Exec("CREATE DATABASE IF NOT EXISTS code_share")
	if err != nil {
		log.Fatal("Error creating database: ", err)
	}
	_, err = db.Exec("USE code_share")
	if err != nil {
		log.Fatal("Error selecting database: ", err)
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS messages (id int not null auto_increment primary key, text longtext, likes int)")
	if err != nil {
		log.Fatal("Error creating messages table: ", err)
	}

	log.Println("DB setup")

	return
}

// GetConnection ...
func GetConnection() *sql.DB {
	var db *sql.DB
	db, err := sql.Open("mysql", connectionKey)

	if err != nil {
		log.Fatal("Error login in mysql: ", err)
	}
	_, err = db.Exec("USE code_share")
	return db
}
