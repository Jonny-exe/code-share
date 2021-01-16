package main

import (
	_ "encoding/json"

	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/Jonny-exe/code-share/back-end/httpd/db"
	"github.com/Jonny-exe/code-share/back-end/httpd/handlers"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	"github.com/rs/cors"
)

func handleRequest() error {
	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/test", handlers.Test).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/insertMessage", handlers.InsertMessage).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/getMessages", handlers.GetMessages).Methods("GET", "OPTIONS")
	c := cors.New(cors.Options{
		// AllowedOrigins: []string{"http://localhost:5000"},
		AllowedOrigins: []string{"http://127.0.0.1:5000"},
		// AllowedOrigins:   []string{"*"},
		AllowCredentials: false,
		AllowedMethods:   []string{"POST", "GET", "OPTIONS"},
		AllowedHeaders:   []string{"*"},

		// Enable Debugging for testing, consider disabling in production
		// To debug turn this to true
		Debug: false,
	})

	dir := os.Getenv("CODE_SHARE_ENV")
	log.Println("Env variable CODE_SHARE_ENV is: ", dir)
	if dir == "" {
		log.Println("Error: GO_MESSAGES_DIR is not set.")
		log.Println("Error: Set it like: export GO_MESSAGES_DIR=\"/home/user/Documents/GitHub/go-server/httpd\"")
	}

	enverr := godotenv.Load(dir)
	if enverr != nil {
		log.Println("Error loading .env file: ", enverr)
	}

	var port string = os.Getenv("SERVER_PORT")

	PORT, err := strconv.Atoi(port)
	if err != nil {
		log.Fatal("Error converting string to number: ", err)
	}
	corsHandler := c.Handler(myRouter)
	log.Println("Listening on port: ", PORT)
	log.Fatal(http.ListenAndServe(":"+strconv.Itoa(PORT), corsHandler))
	return nil
}

func main() {

	connect()
	log.Println("Db connection sucessfull")
	err := handleRequest()
	if err != nil {
		log.Fatal(err)
	}
}

func connect() {
	db.GetDirs()
	db.Connect()
}
