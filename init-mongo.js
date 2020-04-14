//console.log("I just got called bitches")
print("I am a print")
db.createUser( {
    user: "test",
    pwd: "123",
    roles: [{
      role: "readWrite",
      db: "database_nir"
    }]
})
