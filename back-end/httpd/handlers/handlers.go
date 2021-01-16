package handlers

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/Jonny-exe/code-share/back-end/httpd/db"
	"github.com/Jonny-exe/code-share/back-end/httpd/models"
)

// Test ...
func Test(w http.ResponseWriter, r *http.Request) {
	var req interface{}

	json.NewDecoder(r.Body).Decode(&req)

	log.Println(req)

	json.NewEncoder(w).Encode(req)
}

// InsertMessage ..
func InsertMessage(w http.ResponseWriter, r *http.Request) {
	var req models.InsertMessage
	json.NewDecoder(r.Body).Decode(&req)
	db := db.GetConnection()
	defer db.Close()
	// Before doing this you have to check if the token alredy exists
	json.NewDecoder(r.Body).Decode(&req)

	insert, err := db.Prepare("INSERT INTO messages(text, likes) VALUES(?, ?)")
	if err != nil {
		log.Fatal(err)
	}

	insert.Exec(req.Text, 0)
	defer insert.Close()
	json.NewEncoder(w).Encode(http.StatusOK)
	return
}
