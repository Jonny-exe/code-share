package main

import (
	_ "encoding/json"

	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/Jonny-exe/web-maker/web-maker-server/httpd/filecreator"
	"github.com/Jonny-exe/web-maker/web-maker-server/httpd/handler"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	"github.com/rs/cors"
)

func handleRequest() error {
	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/insertTokenRecovery", handler.InsertTokenRecovery).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/updateTokenObject", handler.UpdateTokenObject).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/insertTokenObject", handler.InsertTokenObject).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/getTokenFromRecovery", handler.GetTokenFromRecovery).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/getObjectFromToken", handler.GetObjectFromToken).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/exportIntoHTML", handler.ExportIntoHTML).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/removeFile", handler.RemoveFile).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/doesRecoveryKeyExist", handler.DoesRecoveryKeyExist).Methods("POST", "OPTIONS")
	myRouter.HandleFunc("/test", handler.Test).Methods("POST", "OPTIONS")

	c := cors.New(cors.Options{
		AllowedOrigins: []string{"https://localhost:5000"},
		// AllowedOrigins:   []string{"*"},
		AllowCredentials: false,
		AllowedMethods:   []string{"POST", "GET", "OPTIONS"},
		AllowedHeaders:   []string{"*"},

		// Enable Debugging for testing, consider disabling in production
		// To debug turn this to true
		Debug: false,
	})

	var port string = os.Getenv("SERVE_PORT")
	dir := os.Getenv("CODE_SHARE_ENV")
	log.Println("Env variable CODE_SHARE_ENV is: ", dir)
	if dir == "" {
		log.Println("Error: GO_MESSAGES_DIR is not set.")
		log.Println("Error: Set it like: export GO_MESSAGES_DIR=\"/home/user/Documents/GitHub/go-server/httpd\"")
	}

	enverr := godotenv.Load(dir + "/.env")
	if enverr != nil {
		log.Println("Error loading .env file: ", enverr)
	}
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
	filecreator.GetTempFilesDir()
	handler.GetDirs()
	handler.Connect()
}

// tempFilesWipe is used to remove all the files that arent used and have not been removed because the user closed the browser
